import time
import threading
import logging

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

        logging.debug("PomodoroTimer initialized with work_interval=%s minutes, break_interval=%s minutes", work_interval, break_interval)

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

        # Ensure transition occurs when timer reaches 0
        if self.is_running and self.remaining_time <= 0:
            logging.debug("Timer reached 0 seconds.")
            self.notify()

    def notify(self):
        logging.debug("Notify called: mode=%s", self.current_mode)
        if self.current_mode == 'work':
            logging.debug("Switching to break mode.")
            self.notify_callback("Break Time!", "It's time to take a break!", self.sound_path)
            self.current_mode = 'break'
            self.remaining_time = self.break_interval
        else:
            logging.debug("Switching to work mode.")
            self.notify_callback("Work Time!", "Break is over! Back to work.", self.sound_path)
            self.current_mode = 'work'
            self.remaining_time = self.work_interval

        if self.is_running:
            logging.debug("Restarting timer thread for the next interval.")
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()
