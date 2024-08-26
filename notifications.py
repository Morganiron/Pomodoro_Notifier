import time
import pygame
import logging
import tkinter as tk

# Initialize pygame mixer
pygame.mixer.init()

def send_notification_with_sound(title, message, sound_path=None):
    logging.debug("Sending notification: title=%s, message=%s", title, message)

    # Play the selected alarm sound if provided
    if sound_path:
        logging.debug("Playing sound: %s", sound_path)
        try:
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # Wait for the sound to finish playing
        except Exception as e:
            logging.error("Error playing sound: %s", e)

    # Create a simple Tkinter popup for the notification
    show_popup_notification(title, message)

def show_popup_notification(title, message):
    # Initialize a new Tkinter window
    root = tk.Tk()
    root.title(title)
    root.geometry("300x150")  # Adjust size as needed

    # Label to display the message
    tk.Label(root, text=message, padx=20, pady=20).pack()

    # Button to close the popup
    tk.Button(root, text="Dismiss", command=root.destroy).pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()
