import sys

import pygame
import logging
import tkinter as tk
import winsound  # Import the winsound module for Windows default sound
import time  # Import time for time.sleep
import threading  # Import threading for handling sound playback in the background

# Check if running as a frozen executable or logging is already disabled
if getattr(sys, 'frozen', False) or logging.getLogger().disabled:
    logging.disable(logging.CRITICAL)

# Initialize pygame mixer
pygame.mixer.init()

# Global flag to stop sound
stop_sound_flag = False


def send_notification_with_sound(title, message, sound_path=None, resume_event=None):
    global stop_sound_flag
    logging.debug("send_notification_with_sound called: title=%s, message=%s, sound_path=%s", title, message,
                  sound_path)

    # Reset the stop sound flag
    stop_sound_flag = False

    # Create and display the popup notification in the main thread
    popup_thread = threading.Thread(target=show_popup_notification, args=(title, message, sound_path, resume_event))
    popup_thread.start()
    logging.debug("Popup notification thread started.")


def play_sound(sound_path):
    logging.debug("play_sound called with sound_path=%s", sound_path)
    if sound_path:
        logging.debug("Attempting to play selected sound: %s", sound_path)
        try:
            if not pygame.mixer.music.get_busy():  # Check if the sound is still playing
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            else:
                logging.debug("Sound is already playing.")
        except Exception as e:
            logging.error("Error playing sound: %s", e)
    else:
        logging.debug("Playing default Windows notification sound.")
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            logging.error("Error playing default Windows sound: %s", e)


def show_popup_notification(title, message, sound_path, resume_event):
    logging.debug("Creating popup window: title=%s, message=%s", title, message)
    root = tk.Tk()
    root.title(title)
    root.geometry("300x150")

    tk.Label(root, text=message, padx=20, pady=20).pack()

    # Dismiss button to close the popup
    def dismiss_popup():
        global stop_sound_flag
        logging.debug("Dismiss button clicked.")

        # Stop the sound immediately if it's playing
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            logging.debug("Sound playback stopped due to dismiss button.")

        stop_sound_flag = True  # Stop repeating sound
        if resume_event:
            logging.debug("Setting resume_event to allow timer to continue.")
            resume_event.set()  # Signal the timer to resume
        root.destroy()
        logging.debug("Popup window destroyed.")

    tk.Button(root, text="Dismiss", command=dismiss_popup).pack(pady=10)

    def repeat_sound():
        logging.debug("Starting sound repetition thread.")
        # Repeat sound every 10 seconds until the popup is dismissed
        while not stop_sound_flag:
            play_sound(sound_path)
            logging.debug("Waiting for 10 seconds before repeating sound.")
            time.sleep(10)

    logging.debug("Running Tkinter mainloop for popup.")
    sound_thread = threading.Thread(target=repeat_sound)
    sound_thread.start()

    root.mainloop()
    logging.debug("Exited Tkinter mainloop.")
