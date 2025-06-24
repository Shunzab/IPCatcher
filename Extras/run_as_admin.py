import win32con
import win32event
from win32com.shell import shell, shellcon

def run_cmd_script_as_admin(script_path):
    while True:
        try:
            print(f"Attempting to run script with admin privileges: {script_path}")
            
            proc_info = shell.ShellExecuteEx(
                fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                lpVerb='runas',  # Request elevation
                lpFile='cmd.exe',
                lpParameters=f'/c "{script_path}"',
                nShow=win32con.SW_SHOWNORMAL
            )

            # Wait for the process to finish
            handle = proc_info['hProcess']
            win32event.WaitForSingleObject(handle, win32event.INFINITE)

            print("✅ Script executed successfully with admin rights.")
            break  # Exit loop if successful

        except Exception as e:
            print(f"❌ Failed to execute script as admin: {e}")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                print("Exiting without completing the task.")
                break


#  if __name__ == "__main__":
#  script_path = r"C:\Path\To\Your\Script.bat"
#   run_cmd_script_as_admin(script_path)

