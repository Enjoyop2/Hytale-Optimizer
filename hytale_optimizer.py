import io
import json
import os
import shutil
import zipfile
from pathlib import Path

CLR_RED="\033[91m"
CLR_GREEN="\033[92m"
CLR_YELLOW="\033[93m"
CLR_CYAN="\033[96m"
CLR_RST="\033[0m"

TARGET_ZIP="Assets.zip"
BACKUP_SUFFIX=".bak"
TEMP_SUFFIX=".tmp.zip"
EMPTY_OGG="Empty.ogg"
JSON_LOG="json_errors.log"

PNG_MAX_WIDTH=256
PNG_MAX_HEIGHT=256

def info(msg):
	print(f"{CLR_CYAN}[*] {msg}{CLR_RST}")

def success(msg):
	print(f"{CLR_GREEN}[+] {msg}{CLR_RST}")

def warning(msg):
	print(f"{CLR_YELLOW}[!] {msg}{CLR_RST}")

def error(msg):
	print(f"{CLR_RED}[-] {msg}{CLR_RST}")

def format_size(size):
	value=float(size)
	for unit in ("B","KB","MB","GB","TB"):
		if value<1024 or unit=="TB":
			return f"{value:.2f} {unit}"
		value/=1024
	return f"{size} B"

class ZipManager:
	def find_assets(self):
		root=Path(__file__).resolve().parent
		direct=root/TARGET_ZIP
		if direct.is_file():
			return direct
		for path in root.rglob(TARGET_ZIP):
			if path.is_file():
				return path
		return None

	def backup_path(self,path):
		return path.with_name(path.name+BACKUP_SUFFIX)

	def temp_path(self,path):
		return path.with_name(path.name+TEMP_SUFFIX)

	def backup(self,path):
		backup=self.backup_path(path)
		if backup.exists():
			warning(f"Backup already exists: {backup.name}")
			return backup
		shutil.copy2(path,backup)
		success(f"Backup created: {backup.name}")
		return backup

	def validate(self,path):
		try:
			with zipfile.ZipFile(path,"r",allowZip64=True) as archive:
				bad=archive.testzip()
				if bad:
					error(f"Corrupted file: {bad}")
					return False
			return True
		except zipfile.BadZipFile:
			error("Invalid ZIP archive.")
			return False
		except Exception as exc:
			error(f"ZIP validation error: {exc}")
			return False

class JsonOptimizer:
	EXTENSIONS=(".json",".particlesystem",".particlespawner")

	def __init__(self):
		self.errors=0

	def process(self,filename,data):
		name=filename.replace("\\","/")
		if not name.startswith("Server/"):
			return data,False
		if not name.lower().endswith(self.EXTENSIONS):
			return data,False
		try:
			parsed=json.loads(data.decode("utf-8"))
			result=json.dumps(parsed,separators=(",",":"),ensure_ascii=False).encode("utf-8")
			if len(result)>=len(data):
				return data,False
			return result,True
		except Exception as exc:
			self.errors+=1
			try:
				with open(Path(__file__).resolve().parent/JSON_LOG,"a",encoding="utf-8") as log:
					log.write(f"{filename}\nReason: {exc}\n{'-'*70}\n")
			except Exception:
				pass
			return data,False

class ClientJsonOptimizer:
	EXTENSIONS=(".blockymodel",".blockyanim")

	def __init__(self):
		self.errors=0

	def process(self,filename,data):
		name=filename.replace("\\","/")
		if not name.startswith("Common/"):
			return data,False
		if not name.lower().endswith(self.EXTENSIONS):
			return data,False
		try:
			parsed=json.loads(data.decode("utf-8"))
			result=json.dumps(parsed,separators=(",",":"),ensure_ascii=False).encode("utf-8")
			if len(result)>=len(data):
				return data,False
			return result,True
		except Exception as exc:
			self.errors+=1
			try:
				with open(Path(__file__).resolve().parent/JSON_LOG,"a",encoding="utf-8") as log:
					log.write(f"{filename}\nReason: {exc}\n{'-'*70}\n")
			except Exception:
				pass
			return data,False

class MusicOptimizer:
	def __init__(self):
		self.empty_audio=None

	def load(self):
		path=Path(__file__).resolve().parent/EMPTY_OGG
		if not path.exists():
			raise FileNotFoundError(f"{EMPTY_OGG} not found.")
		self.empty_audio=path.read_bytes()
		if not self.empty_audio:
			raise ValueError(f"{EMPTY_OGG} is empty.")

	def process(self,filename,data):
		name=filename.replace("\\","/")
		if not name.startswith("Common/Music/") or not name.lower().endswith(".ogg"):
			return data,False
		if data==self.empty_audio:
			return data,False
		return self.empty_audio,True

class PngOptimizer:
	def __init__(self):
		self.Image=None
		self.available=None

	def load_pillow(self):
		if self.available is not None:
			return self.available
		try:
			from PIL import Image
			self.Image=Image
			self.available=True
		except ImportError:
			self.available=False
		return self.available

	@staticmethod
	def has_transparency(image):
		if image.mode in ("RGBA","LA"):
			alpha=image.getchannel("A")
			try:
				return alpha.getextrema()[0]<255
			finally:
				alpha.close()
		if "transparency" in image.info:
			try:
				rgba=image.convert("RGBA")
				alpha=rgba.getchannel("A")
				try:
					return alpha.getextrema()[0]<255
				finally:
					alpha.close()
			except Exception:
				return True
		return False

	def process(self,filename,data):
		if not filename.lower().endswith(".png"):
			return data,False
		if not self.load_pillow():
			return data,False
		buffer=io.BytesIO(data)
		try:
			with self.Image.open(buffer) as image:
				width,height=image.size
				if width>PNG_MAX_WIDTH or height>PNG_MAX_HEIGHT:
					return data,False
				transparency=self.has_transparency(image)
				if image.mode=="RGB":
					converted=image.convert("RGB")
				elif image.mode=="RGBA":
					converted=image.convert("RGBA")
				elif transparency:
					converted=image.convert("RGBA")
				else:
					converted=image.convert("RGB")
				output=io.BytesIO()
				try:
					converted.save(output,format="PNG",compress_level=0,optimize=False)
					new_data=output.getvalue()
				finally:
					converted.close()
					output.close()
				return new_data,True
		except Exception as exc:
			warning(f"PNG skipped: {filename} -> {exc}")
			return data,False
		finally:
			buffer.close()

class ArchiveOptimizer:
	def __init__(self):
		self.json=JsonOptimizer()
		self.music=MusicOptimizer()
		self.png=PngOptimizer()
		self.client_json=ClientJsonOptimizer()

	def make_zip_info(self,item,compress_type):
		info_obj=zipfile.ZipInfo(item.filename,date_time=item.date_time)
		info_obj.compress_type=compress_type
		info_obj.comment=item.comment
		info_obj.create_system=item.create_system
		info_obj.create_version=item.create_version
		info_obj.extract_version=item.extract_version
		info_obj.flag_bits=item.flag_bits
		info_obj.volume=item.volume
		info_obj.internal_attr=item.internal_attr
		info_obj.external_attr=item.external_attr
		info_obj.extra=b""
		return info_obj

	def optimize(self,source,destination,mode):
		changed=0
		passed=0
		errors=0
		if mode=="music":
			self.music.load()
		with zipfile.ZipFile(source,"r",allowZip64=True) as src:
			with zipfile.ZipFile(destination,"w",allowZip64=True,compression=zipfile.ZIP_DEFLATED) as dst:
				for item in src.infolist():
					data=None
					try:
						if item.is_dir():
							info_obj=self.make_zip_info(item,zipfile.ZIP_STORED)
							dst.writestr(info_obj,b"")
							continue
						data=src.read(item.filename)
						new_data=data
						is_changed=False
						if mode=="json":
							new_data,is_changed=self.json.process(item.filename,data)
						elif mode=="music":
							new_data,is_changed=self.music.process(item.filename,data)
						elif mode=="png":
							new_data,is_changed=self.png.process(item.filename,data)
						elif mode=="client_json":
							new_data,is_changed=self.client_json.process(item.filename,data)
						if is_changed and mode=="png":
							compress_type=zipfile.ZIP_STORED
						else:
							compress_type=item.compress_type
						info_obj=self.make_zip_info(item,compress_type)
						dst.writestr(info_obj,new_data)
						if is_changed:
							changed+=1
						else:
							passed+=1
					except Exception as exc:
						errors+=1
						warning(f"Could not process: {item.filename}")
						warning(f"Reason: {exc}")
						if data is None:
							data=src.read(item.filename)
						info_obj=self.make_zip_info(item,item.compress_type)
						dst.writestr(info_obj,data)
						passed+=1
		return changed,passed,errors

class HytaleOptimizer:
	def __init__(self):
		self.zip=ZipManager()
		self.archive=ArchiveOptimizer()

	def run(self,mode):
		source=self.zip.find_assets()
		if not source:
			error("Assets.zip not found!")
			return
		info(f"Assets: {source}")
		if not self.zip.validate(source):
			error("Original ZIP is invalid.")
			return
		try:
			self.zip.backup(source)
		except Exception as exc:
			error(f"Backup failed: {exc}")
			return
		temp=self.zip.temp_path(source)
		if temp.exists():
			try:
				temp.unlink()
			except Exception as exc:
				error(f"Cannot remove temporary ZIP: {exc}")
				return
		old_size=source.stat().st_size
		try:
			if mode=="json":
				info("Server JSON optimization started...")
			elif mode=="music":
				info("Music optimization started...")
			elif mode=="png":
				info("PNG optimization started...")
				info("Only PNGs <= 256x256 are processed.")
			elif mode=="client_json":
				info("Model and Anim JSON optimization started...")
			changed,passed,errors=self.archive.optimize(source,temp,mode)
			info("Validating new ZIP...")
			if not self.zip.validate(temp):
				raise ValueError("New ZIP validation failed.")
			os.replace(temp,source)
			new_size=source.stat().st_size
			difference=new_size-old_size
			print()
			print("===================================")
			print(f"{CLR_GREEN}HYTALE OPTIMIZER 2.1.1{CLR_RST}")
			print("===================================")
			print(f"Old ZIP : {format_size(old_size)}")
			print(f"New ZIP : {format_size(new_size)}")
			if difference<0:
				saved=abs(difference)
				percent=saved/old_size*100 if old_size else 0
				print(f"{CLR_GREEN}Saved : {format_size(saved)} ({percent:.2f}%){CLR_RST}")
			elif difference>0:
				percent=difference/old_size*100 if old_size else 0
				print(f"{CLR_YELLOW}Increase : {format_size(difference)} ({percent:.2f}%){CLR_RST}")
			else:
				print("Size change : None")
			print(f"Changed : {changed}")
			print(f"Skipped : {passed}")
			print(f"Errors : {errors}")
			if mode=="json":
				print(f"JSON errors : {self.archive.json.errors}")
			if mode=="png" and not self.archive.png.available:
				warning("Pillow is not installed.")
				print("Install with: pip install Pillow")
			print("===================================")
			print()
			success(f"Backup: {self.zip.backup_path(source).name}")
			print()
		except KeyboardInterrupt:
			if temp.exists():
				temp.unlink()
			warning("Process stopped. Original ZIP preserved.")
		except Exception as exc:
			error(f"Critical error: {exc}")
			if temp.exists():
				try:
					temp.unlink()
				except Exception:
					pass
			warning("Original Assets.zip preserved.")

	def check(self):
		source=self.zip.find_assets()
		if not source:
			error("Assets.zip not found!")
			return
		info(f"Checking: {source}")
		if self.zip.validate(source):
			success("ZIP looks healthy.")
			print(f"Size: {format_size(source.stat().st_size)}")
		else:
			error("ZIP verification failed.")

def menu():
	optimizer=HytaleOptimizer()
	while True:
		print()
		print("---------------------------------------------")
		print("🐊 HYTALE OPTIMIZER 2.1.1")
		print("---------------------------------------------")
		print("1) 🧹 Server JSON Minify")
		print("2) 🎵 Mute Music")
		print("3) 🎯 Uncompress PNGs <= 256x256")
		print("4) 🧹 Client JSON Minify (model and anim)")
		print("5) 🔍 Check ZIP")
		print("6) ❌ Exit")
		print("---------------------------------------------")
		try:
			choice=input("Please make a choice (1-5): ").strip()
		except KeyboardInterrupt:
			print()
			success("Exited. Have a good game!")
			return
		if choice=="1": optimizer.run("json")
		elif choice=="2": optimizer.run("music")
		elif choice=="3": optimizer.run("png")
		elif choice=="4": optimizer.run("client_json")
		elif choice=="5": optimizer.check()
		elif choice=="6":
			print()
			success("Exited. Have a good game!")
			return
		else:
			error("Invalid choice! Choose between 1-5.")

if __name__=="__main__":
	menu()
