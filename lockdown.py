import psutil
import threading
import time
import getpass
import sys



def monitor_and_kill (banned_names, stop_event, interval = 1):
    """
    Continuously scans for banned process names (all lowercase)
    and terminates them, until stop_event is set.

    """
    while not stop_event.is_set():

        for proc in psutil.process_iter():
            try:
                name = proc.name().lower()
                # If on banned list, kill it!
                if name in banned_names:
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        time.sleep(interval)

def start_lockdown(banned, password):
    stop_event = threading.Event()

    t = threading.Thread(
        target=monitor_and_kill,
        args=(banned,stop_event),
        daemon=True
    )
    t.start()

    while True:
        entry = getpass.getpass("Enter password to unlock: ")
        if entry == password:
            stop_event.set()
            t.join()
            print("Unlocked!")
            return True
        print("Wrong Password! Try again..")




if __name__ == "__main__":
    print("🛠️  Script is running…")


    # Collecting banned apps.
    banned = []

    while True:
        app = input("Enter a banned app (Enter to finish): ").strip().lower()

        if not app:
            break
        banned.append(app)
        print(f"Banned apps: {banned}")


    while True:
        pw1 = getpass.getpass("Set your unlock password ")
        pw2 = getpass.getpass("Confirm your password")
        if pw1 == pw2:
            password = pw1
            break
        print("❌ Passwords did not match. Try again.\n")
    
    unlocked = start_lockdown(banned, password)

    if not unlocked:
        sys.exit(1)
