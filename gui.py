import tkinter as tk
from tkinter import messagebox, filedialog
from timer import PomodoroTimer
from notifications import send_notification_with_sound
import logging

# Configure logging
logging.basicConfig(filename='pomodoro.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class PomodoroApp:
    def __init__(self):
        logging.debug("Initializing PomodoroApp...")
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
        logging.debug("PomodoroApp initialized with default work_interval=%s minutes and break_interval=%s minutes.",
                      self.work_interval, self.break_interval)

    def create_widgets(self):
        # Work interval
        tk.Label(self.root, text="Work Interval (minutes):").grid(row=0, column=0, padx=10, pady=5)
        self.work_entry = tk.Entry(self.root, width=5)
        self.work_entry.grid(row=0, column=1, pady=5)
        self.work_entry.insert(0, str(self.work_interval))
        self.work_up_button = tk.Button(self.root, text="▲", command=self.increase_work_interval)
        self.work_up_button.grid(row=0, column=2, pady=5)
        self.work_down_button = tk.Button(self.root, text="▼", command=self.decrease_work_interval)
        self.work_down_button.grid(row=0, column=3, pady=5, padx=(0, 10))

        # Break interval
        tk.Label(self.root, text="Break Interval (minutes):").grid(row=1, column=0, padx=10, pady=5)
        self.break_entry = tk.Entry(self.root, width=5)
        self.break_entry.grid(row=1, column=1, pady=5)
        self.break_entry.insert(0, str(self.break_interval))
        self.break_up_button = tk.Button(self.root, text="▲", command=self.increase_break_interval)
        self.break_up_button.grid(row=1, column=2, pady=5)
        self.break_down_button = tk.Button(self.root, text="▼", command=self.decrease_break_interval)
        self.break_down_button.grid(row=1, column=3, pady=5, padx=(0, 10))

        # Timer display
        self.timer_label = tk.Label(self.root, text="25:00", font=("Helvetica", 24))
        self.timer_label.grid(row=2, column=0, columnspan=4, pady=10)

        # Sound selection button and optional label
        self.sound_button = tk.Button(self.root, text="Select Sound", command=self.select_sound_file)
        self.sound_button.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        self.optional_label = tk.Label(self.root, text="(optional)")
        self.optional_label.grid(row=3, column=1, padx=5, pady=10, sticky='w')

        # Start, Pause, Stop buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.grid(row=4, column=0, padx=10, pady=10)
        self.pause_button = tk.Button(self.root, text="Pause", state=tk.DISABLED, command=self.pause_timer)
        self.pause_button.grid(row=4, column=1, padx=10, pady=10)
        self.stop_button = tk.Button(self.root, text="Stop", state=tk.DISABLED, command=self.stop_timer)
        self.stop_button.grid(row=4, column=2, padx=(10, 20), pady=10)

        logging.debug("Widgets created successfully.")

    def select_sound_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Alarm Sound",
            initialdir="C:\\Windows\\Media",
            filetypes=(("Sound files", "*.wav *.mp3"), ("All files", "*.*"))
        )
        if file_path:
            logging.debug("Sound file selected: %s", file_path)
            self.alarm_sound_path = file_path

    def increase_work_interval(self):
        self.work_interval = int(self.work_entry.get()) + 1
        self.work_entry.delete(0, tk.END)
        self.work_entry.insert(0, str(self.work_interval))
        self.update_timer_display(self.work_interval * 60)

    def decrease_work_interval(self):
        if self.work_interval > 1:
            self.work_interval = int(self.work_entry.get()) - 1
            self.work_entry.delete(0, tk.END)
            self.work_entry.insert(0, str(self.work_interval))
            self.update_timer_display(self.work_interval * 60)

    def increase_break_interval(self):
        self.break_interval = int(self.break_entry.get()) + 1
        self.break_entry.delete(0, tk.END)
        self.break_entry.insert(0, str(self.break_interval))

    def decrease_break_interval(self):
        if self.break_interval > 1:
            self.break_interval = int(self.break_entry.get()) - 1
            self.break_entry.delete(0, tk.END)
            self.break_entry.insert(0, str(self.break_interval))

    def update_timer_display(self, remaining_time):
        mins, secs = divmod(remaining_time, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def start_timer(self):
        logging.debug("Start button pressed.")
        if self.timer is None or not self.timer.is_running:
            try:
                work_interval = int(self.work_entry.get())
                break_interval = int(self.break_entry.get())
                logging.debug("Starting timer with work_interval=%s minutes and break_interval=%s minutes.",
                              work_interval, break_interval)
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
