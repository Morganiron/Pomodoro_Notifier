import time
import logging
from plyer import notification
import pygame
import threading


class PomodoroTimer:
    def __init__(self, work_interval, break_interval, update_callback, notify_callback, sound_path=None):
        self.work_interval = work_interval * 60  # Convert to seconds
        self.break_interval = break_interval * 60
        self.update_callback = update_callback
        self.notify_callback = notify_callback
        self.sound_path = sound_path  # Store the sound path
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.current_mode = 'work'  # 'work' or 'break'
        self.timer_thread = None

        # Initialize pygame mixer for sound playback
        pygame.mixer.init()

        logging.debug("PomodoroTimer initialized with work_interval=%s minutes, break_interval=%s minutes",
                      work_interval, break_interval)

    def start(self):
        if not self.is_running:
            logging.debug("Starting timer.")
            self.is_running = True
            self.is_paused = False
            self.remaining_time = self.work_interval if self.current_mode == 'work' else self.break_interval
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()

    def pause(self):
        if self.is_running and not self.is_paused:
            logging.debug("Pausing timer.")
            self.is_paused = True
        elif self.is_running and self.is_paused:
            logging.debug("Resuming timer.")
            self.is_paused = False
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()

    def stop(self):
        logging.debug("Stopping timer.")
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0

    def run(self):
        logging.debug("Timer running: mode=%s, remaining_time=%s seconds", self.current_mode, self.remaining_time)
        while self.is_running and self.remaining_time > 0:
            if not self.is_paused:
                self.update_callback(self.remaining_time)
                time.sleep(1)
                self.remaining_time -= 1
            else:
                logging.debug("Timer paused.")
                break

        if self.remaining_time == 0:
            logging.debug("Timer reached 0 seconds.")
            self.notify()

    def notify(self):
        logging.debug("Notify called: mode=%s", self.current_mode)

        # Stop the timer
        self.is_running = False

        # Play sound if one is selected
        if self.sound_path:
            logging.debug("Playing sound: %s", self.sound_path)
            try:
                pygame.mixer.music.load(self.sound_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)  # Wait for the sound to finish playing
            except Exception as e:
                logging.error("Error playing sound: %s", e)

        # Send notification
        if self.current_mode == 'work':
            title = "Break Time!"
            message = "It's time to take a break!"
            self.current_mode = 'break'
            self.remaining_time = self.break_interval
        else:
            title = "Work Time!"
            message = "Break is over! Back to work."
            self.current_mode = 'work'
            self.remaining_time = self.work_interval

        logging.debug("Sending notification: title=%s, message=%s", title, message)
        notification.notify(
            title=title,
            message=message,
            timeout=10  # Notification duration in seconds
        )
        logging.debug("Notification sent.")

        # Restart the timer after notification is sent
        if not self.is_paused:
            logging.debug("Restarting timer thread for the next interval.")
            self.is_running = True
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()
