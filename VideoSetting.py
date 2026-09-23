import os
import json
import tempfile

# Target Configuration
TARGET_DIR_NAME = "userdata"
TARGET_FILE_NAME = "settings.json"

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

def find_config_path(start_dir: str) -> str:
	"""Recursively scans subdirectories to find target Settings.json inside UserData folder."""
	print(f"Scanning initiated: Searching for '{TARGET_FILE_NAME}' inside '{TARGET_DIR_NAME}' layout...")
	for root, dirs, files in os.walk(start_dir):
		# Case-insensitive comparison for Android environment compatibility
		if os.path.basename(root).lower() == TARGET_DIR_NAME:
			for file in files:
				if file.lower() == TARGET_FILE_NAME:
					found_path = os.path.join(root, file)
					print(f"{GREEN}Found target path:{RESET} {found_path}")
					return found_path
	return None

def main():
	enable_windows_ansi()
	
	# Determine current execution context path
	current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
	
	# Phase 1: Scan and find the file location dynamically
	config_path = find_config_path(current_dir)

	if not config_path:
		print(f"{RED}ERROR: Could not find '{TARGET_FILE_NAME}' inside any '{TARGET_DIR_NAME}' folder under: {current_dir}{RESET}")
		return

	tmp_path = None
	try:
		# Load the JSON structure securely
		with open(config_path, "r", encoding="utf-8-sig") as f:
			data = json.load(f)

		# Traverse directly into your RenderingSettings block
		if "RenderingSettings" in data and isinstance(data["RenderingSettings"], dict):
			render_block = data["RenderingSettings"]
			
			# Edit existing entries directly
			if "RenderScale" in render_block:
				render_block["RenderScale"] = 50
			if "ViewDistance" in render_block:
				render_block["ViewDistance"] = 128
		else:
			print(f"{RED}ERROR: 'RenderingSettings' key structure missing inside the found file.{RESET}")
			return

		# Safe atomic replacement using temp files
		config_dir = os.path.dirname(config_path)
		fd, tmp_path = tempfile.mkstemp(suffix=".json", dir=config_dir)
		os.close(fd)

		with open(tmp_path, "w", encoding="UTF-8") as f:
			json.dump(data, f, indent=4, ensure_ascii=False)

		# Swapping operations
		os.remove(config_path)
		os.rename(tmp_path, config_path)

		# Standardize local device modification metadata timestamps
		try:
			os.utime(config_path, (315532800, 315532800))
		except Exception:
			pass

		print("\n" + "=" * 60)
		print(f"{GREEN}SUCCESSFULLY COMPLETED{RESET}")
		print(f" File Patched   : {config_path}")
		print(f" RenderScale    : 50")
		print(f" ViewDistance   : 128")
		print("=" * 60)

	except Exception as e:
		if tmp_path and os.path.exists(tmp_path):
			os.remove(tmp_path)
		print(f"{RED}CRITICAL ERROR: Failed to parse or modify target JSON -> {e}{RESET}")

if __name__ == "__main__":
	main()
