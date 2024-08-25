import tkinter as tk
from tkinter import messagebox, filedialog
from timer import PomodoroTimer
from notifications import send_notification_with_sound
import logging

class PomodoroApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.timer = None

        self.work_interval = 25
        self.break_interval = 5
        self.alarm_sound_path = None  # To store the selected sound file path

        # Bind the close window event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Call method to create GUI widgets
        self.create_widgets()

        logging.debug("PomodoroApp initialized with default work_interval=%s minutes and break_interval=%s minutes.", self.work_interval, self.break_interval)

    def create_widgets(self):
        # [Widget creation code here, omitted for brevity]
        logging.debug("Widgets created.")

    def select_sound_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Alarm Sound",
            initialdir="C:\\Windows\\Media",
            filetypes=(("Sound files", "*.wav *.mp3"), ("All files", "*.*"))
        )
        if file_path:
            logging.debug("Sound file selected: %s", file_path)
            self.alarm_sound_path = file_path

    def start_timer(self):
        logging.debug("Start button pressed.")
        if self.timer is None or not self.timer.is_running:
            try:
                work_interval = int(self.work_entry.get())
                break_interval = int(self.break_entry.get())
                logging.debug("Starting timer with work_interval=%s minutes and break_interval=%s minutes.", work_interval, break_interval)
            except ValueError:
                logging.error("Invalid input for intervals.")
                tk.messagebox.showerror("Invalid input", "Please enter valid integers for the intervals.")
                return

            self.timer = PomodoroTimer(work_interval, break_interval, self.update_timer_display,
                                       send_notification_with_sound, self.alarm_sound_path)
            self.timer.start()
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            self.update_timer_display(self.timer.remaining_time)

            # Disable interval changes while running
            self.work_entry.config(state=tk.DISABLED)
            self.break_entry.config(state=tk.DISABLED)
            self.work_up_button.config(state=tk.DISABLED)
            self.work_down_button.config(state=tk.DISABLED)
            self.break_up_button.config(state=tk.DISABLED)
            self.break_down_button.config(state=tk.DISABLED)

    def pause_timer(self):
        logging.debug("Pause/Resume button pressed.")
        if self.timer:
            self.timer.pause()
            self.pause_button.config(text="Resume" if self.timer.is_paused else "Pause")

    def stop_timer(self):
        logging.debug("Stop button pressed.")
        if self.timer:
            self.timer.stop()
            self.timer = None
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(text="Pause")

            # Re-enable interval changes after stopping
            self.work_entry.config(state=tk.NORMAL)
            self.break_entry.config(state=tk.NORMAL)
            self.work_up_button.config(state=tk.NORMAL)
            self.work_down_button.config(state=tk.NORMAL)
            self.break_up_button.config(state=tk.NORMAL)
            self.break_down_button.config(state=tk.NORMAL)

    def on_closing(self):
        logging.debug("Application closing.")
        if self.timer:
            self.timer.stop()  # Stop the timer if it's running
        self.root.destroy()  # Close the application

    def run(self):
        logging.debug("Application started.")
        self.root.mainloop()
