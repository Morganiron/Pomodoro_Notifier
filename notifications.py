from plyer import notification
from playsound import playsound
import logging


def send_notification_with_sound(title, message, sound_path=None):
    logging.debug("Sending notification: title=%s, message=%s", title, message)

    # Play the selected alarm sound if provided
    if sound_path:
        logging.debug("Playing sound: %s", sound_path)
        playsound(sound_path)

    # Send the desktop notification
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification duration in seconds
    )
    logging.debug("Notification sent.")
