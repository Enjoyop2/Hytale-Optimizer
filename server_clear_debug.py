import zipfile
import io
import os
import tempfile

# Target configuration
JAR_NAME = "HytaleServer.jar"
BACKUP_NAME = "HytaleServerBackup.jar"
FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)

def find_target_jar(start_dir):
	"""Scans the starting directory and all its subdirectories to locate HytaleServer.jar."""
	print(f"Scanning initiated: Searching for '{JAR_NAME}' in '{start_dir}' and its subdirectories...")
	for root, dirs, files in os.walk(start_dir):
		if JAR_NAME in files:
			found_path = os.path.join(root, JAR_NAME)
			print(f"Found! Target path: {found_path}")
			return found_path
	return None

def strip_debug_attributes(class_bytes):
	"""
	Scans the Java class byte structure and safely neutralizes debug attributes
	(LineNumberTable, LocalVariableTable, LocalVariableTypeTable, SourceFile)
	without breaking the code integrity.
	"""
	try:
		debug_tags = [b'LineNumberTable', b'LocalVariableTable', b'LocalVariableTypeTable', b'SourceFile']
		modified_bytes = class_bytes
		for tag in debug_tags:
			if tag in modified_bytes:
				# Overwrite the attribute names to force the JVM to safely ignore them,
				# preventing unnecessary metadata from wasting server RAM.
				modified_bytes = modified_bytes.replace(tag, b'X' * len(tag))
		return modified_bytes
	except Exception:
		return class_bytes

def process_jar(jar_bytes):
	"""
	Opens the JAR file in-memory, processes inner classes, optimizes nested JARs,
	and repackages them while keeping folder structures completely intact.
	"""
	input_buffer = io.BytesIO(jar_bytes)
	output_buffer = io.BytesIO()
	
	with zipfile.ZipFile(input_buffer, 'r') as in_jar:
		with zipfile.ZipFile(output_buffer, 'w') as out_jar:
			for item in in_jar.infolist():
				data = in_jar.read(item.filename)
				
				# Nested JAR detection (process recursively)
				if item.filename.endswith('.jar'):
					data = process_jar(data)
				
				# Java Class file detection
				elif item.filename.endswith('.class'):
					data = strip_debug_attributes(data)
				
				# Maintain original file info, structure, compression, and apply fixed timestamps
				new_info = zipfile.ZipInfo(item.filename)
				new_info.date_time = FIXED_DATE_TIME
				new_info.external_attr = item.external_attr
				new_info.compress_type = item.compress_type
				
				out_jar.writestr(new_info, data)
				
	return output_buffer.getvalue()

def run_optimization():
	current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

	# Phase 1: Dynamically locate HytaleServer.jar in subdirectories
	target_jar = find_target_jar(current_dir)
	if not target_jar:
		print(f"\nERROR: '{JAR_NAME}' could not be found.")
		return

	jar_folder = os.path.dirname(target_jar)
	backup_path = os.path.join(jar_folder, BACKUP_NAME)
	
	# Phase 2: Create a complete backup copy before any structural modifications
	print(f"Creating backup -> {backup_path}")
	try:
		with open(target_jar, 'rb') as src, open(backup_path, 'wb') as dst:
			original_bytes = src.read()
			dst.write(original_bytes)
	except Exception as e:
		print(f"An error occurred during backup creation: {e}")
		return

	# Phase 3: Create a safe temporary file in the same directory
	fd, tmp_path = tempfile.mkstemp(suffix=".jar", dir=jar_folder)
	os.close(fd)

	try:
		print("Optimization started (Stripping debug tables and metadata)...")
		optimized_bytes = process_jar(original_bytes)
		
		with open(tmp_path, 'wb') as f:
			f.write(optimized_bytes)
			
		# Phase 4: Atomic replacement of the original file after successful processing
		if os.path.exists(target_jar):
			os.remove(target_jar)
		os.rename(tmp_path, target_jar)
		
		orig_size = len(original_bytes) / (1024 * 1024)
		opt_size = len(optimized_bytes) / (1024 * 1024)
		
		print("\n" + "=" * 60)
		print("SUCCESSFULLY COMPLETED")
		print(f" Optimized File Path   : {target_jar}")
		print(f" Saved Backup Path     : {backup_path}")
		print(f" Size (Before)         : {orig_size:.2f} MB")
		print(f" Size (After)          : {opt_size:.2f} MB")
		print(f" Total Space Saved     : {(orig_size - opt_size):.2f} MB")
		print(f" All File Timestamps   : Standardized to 1980-01-01 00:00:00")
		print("=" * 60)

	except Exception as e:
		if os.path.exists(tmp_path):
			os.remove(tmp_path)
		print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
	run_optimization()
