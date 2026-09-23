import zipfile
import io
import os
import json
import tempfile
from pathlib import Path

# Target configuration
ZIP_NAME = "Assets.zip"
TARGET_SUBDIR = "Server/"  # Only process files inside this subdirectory
FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def enable_windows_ansi() -> None:
	"""Enables ANSI escape color codes in legacy Windows cmd.exe (Win10+)."""
	if os.name == "nt":
		try:
			import ctypes
			kernel32 = ctypes.windll.kernel32
			handle = kernel32.GetStdHandle(-11)
			mode = ctypes.c_uint32()
			kernel32.GetConsoleMode(handle, ctypes.byref(mode))
			kernel32.SetConsoleMode(handle, mode.value | 0x0004)
		except Exception:
			pass

def find_target_zip(start_dir: str) -> str:
	"""Scans the starting directory and all subdirectories to locate Assets.zip."""
	print(f"Scanning initiated: Searching for '{ZIP_NAME}' in '{start_dir}' and its subdirectories...")
	for root, dirs, files in os.walk(start_dir):
		if ZIP_NAME in files:
			found_path = os.path.join(root, ZIP_NAME)
			print(f"{GREEN}Found!{RESET} Target path: {found_path}")
			return found_path
	return None

def process_data(raw_bytes: bytes, filename: str):
	"""Validates and minifies data WITHOUT sorting structural keys alphabetically."""
	try:
		# Decode using UTF-8 and safely parse data
		data = json.loads(raw_bytes.decode("UTF-8"))
		minified = json.dumps(
			data, sort_keys=False, separators=(",", ":"), ensure_ascii=False
		)
		return minified.encode("UTF-8"), True, None
	except Exception as e:
		return raw_bytes, False, str(e)

def run_zip_optimization():
	enable_windows_ansi()
	current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

	# Phase 1: Dynamically locate Assets.zip
	target_zip = find_target_zip(current_dir)
	if not target_zip:
		print(f"{RED}ERROR: '{ZIP_NAME}' could not be found.{RESET}")
		return

	zip_folder = os.path.dirname(target_zip)
	
	# Phase 2: Create a secure temporary file in the target directory
	fd, tmp_path = tempfile.mkstemp(suffix=".zip", dir=zip_folder)
	os.close(fd)

	ok_count = 0
	error_count = 0
	total_processed_count = 0

	try:
		print(f"\nOpening '{ZIP_NAME}' and optimizing target files inside '{TARGET_SUBDIR}'...")
		
		with zipfile.ZipFile(target_zip, 'r') as zin:
			with zipfile.ZipFile(tmp_path, 'w') as zout:
				for item in zin.infolist():
					data = zin.read(item.filename)
					
					# Normalize paths for Windows/Linux consistency
					normalized_name = item.filename.replace("\\", "/")
					lower_name = normalized_name.lower()
					
					is_target_file = (
						normalized_name.startswith(TARGET_SUBDIR) 
						and (
							lower_name.endswith(".json")
							or lower_name.endswith(".particlesystem")
							or lower_name.endswith(".particlespawner")
						)
					)

					if is_target_file:
						total_processed_count += 1
						new_data, success, error_msg = process_data(data, item.filename)
						
						if success:
							ok_count += 1
							data = new_data
						else:
							error_count += 1
							# Real-time red error logging for invalid files
							print(f"{RED}ERROR processing: {item.filename} -> {error_msg}{RESET}")
					
					# Create new zip info entry, keeping original file flags, attributes, and compress mode
					new_info = zipfile.ZipInfo(item.filename)
					new_info.date_time = FIXED_DATE_TIME
					new_info.external_attr = item.external_attr
					new_info.compress_type = item.compress_type
					
					zout.writestr(new_info, data)

		# Phase 3: Replace old file with the newly minified package
		if os.path.exists(target_zip):
			os.remove(target_zip)
		os.rename(tmp_path, target_zip)

		# Execution Summary Report Output
		print("\n" + "=" * 60)
		print(f"{GREEN}SUCCESSFULLY COMPLETED{RESET}")
		print(f" Modified Archive Path : {target_zip}")
		print(f" Target Subdirectory   : {TARGET_SUBDIR}")
		print(f" Total Identified Files: {total_processed_count}")
		print(f" Successfully Minified : {ok_count}")
		print(f" Failed / Bypassed     : {error_count}")
		print(f" All Entry Timestamps  : Standardized to 1980-01-01 00:00:00")
		print("=" * 60)

	except Exception as e:
		if os.path.exists(tmp_path):
			os.remove(tmp_path)
		print(f"{RED}Critical failure during archive optimization: {e}{RESET}")

if __name__ == "__main__":
	run_zip_optimization()
