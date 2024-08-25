from plyer import notification
import pygame
import logging

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
        except Exception as e:
            logging.error("Error playing sound: %s", e)

    # Send the desktop notification
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification duration in seconds
    )
    logging.debug("Notification sent.")
