import subprocess
import os
from file_manager import get_settings

def check_device_connected():
    """Returns True if an Android device is connected with USB Debugging enabled."""
    try:
        # Runs 'adb devices' which returns a list of connected devices
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        
        # Skip the first line ("List of devices attached") and check the rest
        for line in lines[1:]:
            if 'device' in line and 'offline' not in line and 'unauthorized' not in line:
                return True
        return False
    except FileNotFoundError:
        print("[ERROR] ADB is not installed or not in system PATH.")
        return False

def push_files_to_android( ):
    """Pushes all individual files from the local folder to the Android folder."""

    settings = get_settings()

    local_folder = settings["downloadFolder"]
    android_dest = settings["android_downloadFolder"]

    
    if not check_device_connected():
        print("[ERROR] Device not found. Ensure USB debugging is on and phone is unlocked.")
        return False
        
    if not os.path.exists(local_folder):
        print(f"[ERROR] Local download folder not found: {local_folder}")
        return False

    # 1. Create the destination folder on the phone if it doesn't exist
    subprocess.run(["adb", "shell", "mkdir", "-p", android_dest], capture_output=True)
    
    # 2. Grab only the files (ignore sub-folders)
    files = [f for f in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, f))]
    
    if not files:
        print("[USB SYNC] No files found in the local directory to transfer.")
        return True
        
    success_count = 0
    print(f"[USB SYNC] Starting transfer of {len(files)} files...")
    
    # 3. Loop through and push each file individually to append to the phone's folder
    for file_name in files:
        local_path = os.path.join(local_folder, file_name)
        print(f"Pushing: {file_name}")
        
        try:
            subprocess.run(["adb", "push", local_path, android_dest], capture_output=True, check=True)
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to push {file_name}. Error: {e.stderr}")
            
    print(f"[USB SYNC] Complete! Successfully transferred {success_count}/{len(files)} files.")
    return success_count == len(files)