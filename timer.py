import sys
import time
import logging
import pygame
import threading

# Check if running as a frozen executable or logging is already disabled
if getattr(sys, 'frozen', False) or logging.getLogger().disabled:
    logging.disable(logging.CRITICAL)


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
        self.resume_event = threading.Event()  # Event to control timer execution

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
        self.resume_event.set()  # Ensure the timer can proceed if waiting

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

        # Determine the next interval
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

        logging.debug("Sending popup notification: title=%s, message=%s", title, message)

        # Clear the resume event before showing the popup
        self.resume_event.clear()
        logging.debug("Cleared resume_event, waiting for popup to be dismissed.")

        # Update the maximum progress bar value based on the new interval
        self.update_callback(self.remaining_time)  # This ensures the maximum is updated in the GUI

        # Send popup notification and pass the event
        self.notify_callback(title, message, self.sound_path, self.resume_event)

        # Wait for user to dismiss the popup before continuing
        logging.debug("Waiting for popup to be dismissed. is_running=%s, is_paused=%s", self.is_running, self.is_paused)
        self.resume_event.wait()
        logging.debug("Popup dismissed, resume_event set. is_running=%s, is_paused=%s", self.is_running, self.is_paused)

        # Restart the timer after notification is sent and event is set
        self.is_running = True
        logging.debug("Restarting timer thread for the next interval.")
        self.timer_thread = threading.Thread(target=self.run)
        self.timer_thread.start()
        logging.debug("Timer thread started: mode=%s, remaining_time=%s seconds", self.current_mode,
                      self.remaining_time)
