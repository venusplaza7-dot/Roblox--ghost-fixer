
import subprocess
import sys

PACKAGE_NAME = "com.roblox.client"

def run_adb_command(cmd):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def main():
    print("==================================================")
    print("      Roblox Ghost App Killer & Blacklist Tool    ")
    print("==================================================")
    print("Make sure USB Debugging is enabled on your Android phone.\n")

    # 1. Check connection
    devices = run_adb_command(["adb", "devices"])
    if not devices or len(devices.splitlines()) <= 1:
        print("[X] Error: No Android device detected via ADB.")
        print("    -> Enable Developer Options & USB Debugging on your phone.")
        sys.exit(1)
    print("[✓] Android device connected.")

    # 2. Force stop
    print("[*] Force stopping Roblox...")
    run_adb_command(["adb", "shell", f"am force-stop {PACKAGE_NAME}"])

    # 3. Wipe package from user profile
    print("[*] Purging APK and user data instances...")
    uninstall_res = run_adb_command(["adb", "shell", f"pm uninstall --user 0 {PACKAGE_NAME}"])
    
    # 4. Clear Play Store and Download Manager cache queues
    print("[*] Flushing Google Play Store and Download queues...")
    run_adb_command(["adb", "shell", "pm clear com.android.providers.downloads"])
    run_adb_command(["adb", "shell", "pm clear com.android.vending"])

    # 5. Freeze / Suspend package
    print("[*] Freezing package ID to block automated re-downloads...")
    suspend_res = run_adb_command(["adb", "shell", f"pm suspend {PACKAGE_NAME}"])

    print("\n--------------------------------------------------")
    if uninstall_res is not None or suspend_res is not None:
        print("[SUCCESS] Roblox has been nuked and frozen from your profile!")
        print("[!] Recommended: Restart your phone now to flush system cache.")
    else:
        print("[!] Process finished with warnings. Make sure your phone trusted this PC.")
    print("==================================================")

if __name__ == "__main__":
    main()
