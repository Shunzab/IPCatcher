import subprocess

def run_script_as_root(script_path):
    while True:
        try:
            print(f"Attempting to run script with root privileges: {script_path}")
            
            # Use sudo to run the script
            result = subprocess.run(
                ['sudo', 'bash', script_path],
                check=True  # Raises CalledProcessError if it fails
            )
            
            print("✅ Script executed successfully with root privileges.")
            break  # Exit loop if successful

        except subprocess.CalledProcessError as e:
            print(f"❌ Script failed to run as root: {e}")
            retry = input("Would you like to try again? (y/n): ").strip().lower()
            if retry != 'y':
                print("Exiting without completing the task.")
                break

        except KeyboardInterrupt:
            print("\nCancelled by user.")
            break

#if __name__ == "__main__":
#   script_path = "/path/to/your/script.sh"
#    run_script_as_root(script_path)

##########################################################################################################################
# You can also run directly a scricpt by importing subprocess, and running "subprocess.run(['sudo', script_path])" if it is executable, or by running subprocess.run(['sudo', 'bash', 'your_script.sh'])
# if it is not executeable.
