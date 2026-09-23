import zipfile
import os
import tempfile

# Target configuration
TARGET_PREFIX = "Common/Music/"
ZIP_NAME = "Assets.zip"
SOURCE_SILENT_FILE = "Empty.ogg"

FIXED_DATE_TIME = (1980, 1, 1, 0, 0, 0)

def find_target_zip(start_dir):
	"""Scans the starting directory and all its subdirectories to locate Assets.zip."""
	print(f"Scanning initiated: Searching for '{ZIP_NAME}' in '{start_dir}' and its subdirectories...")
	for root, dirs, files in os.walk(start_dir):
		if ZIP_NAME in files:
			found_path = os.path.join(root, ZIP_NAME)
			print(f"Found! Target path: {found_path}")
			return found_path
	return None

def process_assets():
	current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
	source_file_path = os.path.join(current_dir, SOURCE_SILENT_FILE)

	# Phase 1: Dynamically locate Assets.zip in subdirectories
	target_zip = find_target_zip(current_dir)
	
	if not target_zip:
		print(f"\nERROR: '{ZIP_NAME}' could not be found.")
		print(f"Scanned root directory: {current_dir}")
		print("Please ensure the zip file exists within this folder or its subdirectories.")
		return

	# Phase 2: Check if the external source silent file exists
	if not os.path.exists(source_file_path):
		print(f"\nERROR: Source silent file '{SOURCE_SILENT_FILE}' could not be found.")
		print(f"Expected path: {source_file_path}")
		print(f"Please place a valid '{SOURCE_SILENT_FILE}' file next to this script.")
		return

	# Read the local silent file data
	try:
		with open(source_file_path, "rb") as f:
			silent_ogg_bytes = f.read()
	except Exception as e:
		print(f"Error reading '{SOURCE_SILENT_FILE}': {e}")
		return

	total_before = 0
	total_after = 0
	changed = 0

	# Create a temporary file in the same directory as the target zip
	zip_folder = os.path.dirname(target_zip)
	fd, tmp_path = tempfile.mkstemp(suffix=".zip", dir=zip_folder)
	os.close(fd)

	try:
		with zipfile.ZipFile(target_zip, "r") as zin:
			with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_STORED) as zout:
				for item in zin.infolist():
					data = zin.read(item.filename)
					orig_len = len(data)
					
					normalized_name = item.filename.replace("\\", "/")
					is_target = (
						normalized_name.startswith(TARGET_PREFIX)
						and normalized_name.lower().endswith(".ogg")
					)

					if is_target:
						new_data = silent_ogg_bytes
						changed += 1
						print(f"Silenced: {item.filename} ({orig_len:,} -> {len(new_data):,} bytes)")
					else:
						new_data = data

					total_before += orig_len
					total_after += len(new_data)

					# Strictly override date_time to 1980-01-01 00:00:00
					new_info = zipfile.ZipInfo(item.filename)
					new_info.date_time = FIXED_DATE_TIME
					new_info.external_attr = item.external_attr
					new_info.compress_type = zipfile.ZIP_STORED
					zout.writestr(new_info, new_data)

		# Remove original file and rename the temporary one
		if os.path.exists(target_zip):
			os.remove(target_zip)
		os.rename(tmp_path, target_zip)

		print("\n" + "=" * 60)
		print("SUCCESSFULLY COMPLETED")
		print(f" Target File Path      : {target_zip}")
		print(f" Source Silent File    : {SOURCE_SILENT_FILE}")
		print(f" Silenced .ogg Files   : {changed} files")
		print(f" All File Timestamps   : Set to 1980-01-01 00:00:00")
		print(f" Size (Before)         : {total_before / (1024**2):.2f} MB")
		print(f" Size (After)          : {total_after / (1024**2):.2f} MB")
		print(f" Total Space Saved     : {(total_before - total_after) / (1024**2):.2f} MB")
		print("=" * 60)

	except Exception as e:
		if os.path.exists(tmp_path):
			os.remove(tmp_path)
		print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
	process_assets()
