from plyer import notification
from playsound import playsound


def send_notification_with_sound(title, message, sound_path=None):
    # Play the selected alarm sound if provided
    if sound_path:
        playsound(sound_path)

    # Send the desktop notification
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification duration in seconds
    )
