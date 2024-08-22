import time
import threading

class PomodoroTimer:
    def __init__(self, work_interval, break_interval, update_callback, notify_callback):
        self.work_interval = work_interval * 60  # Convert to seconds
        self.break_interval = break_interval * 60
        self.update_callback = update_callback
        self.notify_callback = notify_callback
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0
        self.current_mode = 'work'  # 'work' or 'break'
        self.timer_thread = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.remaining_time = self.work_interval if self.current_mode == 'work' else self.break_interval
            self.timer_thread = threading.Thread(target=self.run)
            self.timer_thread.start()

    def pause(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
        elif self.is_running and self.is_paused:
            self.is_paused = False
            self.run()

    def stop(self):
        self.is_running = False
        self.is_paused = False
        self.remaining_time = 0

    def run(self):
        while self.is_running and self.remaining_time > 0:
            if not self.is_paused:
                self.update_callback(self.remaining_time)
                time.sleep(1)
                self.remaining_time -= 1
            if self.remaining_time == 0:
                self.notify()

    def notify(self):
        if self.current_mode == 'work':
            self.notify_callback("Break Time!", "It's time to take a break!")
            self.current_mode = 'break'
            self.remaining_time = self.break_interval
        else:
            self.notify_callback("Work Time!", "Break is over! Back to work.")
            self.current_mode = 'work'
            self.remaining_time = self.work_interval

        if self.is_running:
            self.run()
