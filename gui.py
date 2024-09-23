import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from timer import PomodoroTimer
from notifications import send_notification_with_sound
import logging

# Check if running as a frozen executable
if getattr(sys, 'frozen', False):
    # Disable all logging to prevent log file creation
    logging.disable(logging.CRITICAL)
else:
    # Configure logging only if not already disabled
    if not logging.getLogger().disabled:
        logging.basicConfig(filename='pomodoro.log', level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class PomodoroApp:
    def __init__(self):
        logging.debug("Initializing PomodoroApp...")
        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")
        self.root.configure(bg='white')
        self.root.minsize(525, 450)
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
        # Configure grid layout
        self.root.grid_rowconfigure(0, weight=2)  # For TimerTextBlock
        self.root.grid_rowconfigure(1, weight=0)  # For Progress Bar
        self.root.grid_rowconfigure(2, weight=0)  # For Custom Sound Button
        self.root.grid_rowconfigure(3, weight=0)  # For Custom Input
        self.root.grid_rowconfigure(4, weight=1)  # For Buttons
        self.root.grid_columnconfigure(0, weight=1)

        # Timer display
        self.timer_label = tk.Label(self.root, text="25:00", font=("Helvetica", 48), bg='white')
        self.timer_label.grid(row=0, column=0, columnspan=4, pady=10, sticky='n')

        # Progress bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.grid(row=1, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.progress["value"] = 0  # Ensure progress bar starts at 0
        self.progress["maximum"] = 100  # Set an arbitrary non-zero maximum to avoid issues

        # Custom Sound Selection
        self.sound_button = tk.Button(self.root, text="Select Sound", command=self.select_sound_file, width=12)
        self.sound_button.grid(row=2, column=0, padx=10, pady=5, sticky='e')

        self.optional_label = tk.Label(self.root, text="(optional)", bg='white')
        self.optional_label.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Custom Time Input
        time_input_frame = tk.Frame(self.root, bg='white')
        time_input_frame.grid(row=3, column=0, columnspan=4, pady=10)

        tk.Label(time_input_frame, text="Work (min):", bg='white').grid(row=0, column=0, padx=10, pady=5)
        self.work_entry = tk.Entry(time_input_frame, width=5)
        self.work_entry.grid(row=0, column=1, pady=5)
        self.work_entry.insert(0, str(self.work_interval))
        self.work_entry.bind("<KeyRelease>", self.update_work_interval)

        # Break input in minutes
        tk.Label(time_input_frame, text="Break (min):", bg='white').grid(row=0, column=2, padx=10, pady=5)
        self.break_entry = tk.Entry(time_input_frame, width=5)
        self.break_entry.grid(row=0, column=3, pady=5)
        self.break_entry.insert(0, str(self.break_interval))
        self.break_entry.bind("<KeyRelease>", self.update_break_interval)

        # Break input in seconds
        tk.Label(time_input_frame, text="sec:", bg='white').grid(row=0, column=4, padx=10, pady=5)
        self.break_entry_sec = tk.Entry(time_input_frame, width=5)
        self.break_entry_sec.grid(row=0, column=5, pady=5)
        self.break_entry_sec.insert(0, "0")  # Default seconds to 0

        # Buttons (Start, Pause, Stop)
        button_frame = tk.Frame(self.root, bg='white')
        button_frame.grid(row=4, column=0, columnspan=4, pady=20)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer, width=10)
        self.start_button.pack(side='left', padx=10)

        self.pause_button = tk.Button(button_frame, text="Pause", state=tk.DISABLED, command=self.pause_timer, width=10)
        self.pause_button.pack(side='left', padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop", state=tk.DISABLED, command=self.stop_timer, width=10)
        self.stop_button.pack(side='left', padx=10)

        logging.debug("Widgets created successfully.")

    def update_timer_display(self, remaining_time, update_progress=True):
        mins, secs = divmod(remaining_time, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        # Update progress bar only if the timer is running
        if update_progress and self.timer and self.timer.is_running:
            # Check if we need to update the maximum for the progress bar
            if self.timer.current_mode == 'work':
                self.progress["maximum"] = self.work_interval * 60
            else:
                self.progress["maximum"] = (int(self.break_entry.get()) * 60) + int(self.break_entry_sec.get())

            self.update_progress_bar(remaining_time)  # Update the progress bar

    def update_progress_bar(self, remaining_time):
        total_time = self.progress["maximum"]  # Use the maximum set in the progress bar
        elapsed_time = total_time - remaining_time
        self.progress["value"] = max(0, elapsed_time)  # Update the current value

    def update_work_interval(self, event=None):
        try:
            work_interval = int(self.work_entry.get())
        except ValueError:
            work_interval = self.work_interval  # Use the default if parsing fails

        self.work_interval = work_interval
        self.update_timer_display(self.work_interval * 60, update_progress=False)  # Update display without progress bar

    def update_break_interval(self, event=None):
        try:
            break_interval = int(self.break_entry.get())
        except ValueError:
            break_interval = self.break_interval  # Use the default if parsing fails

        self.break_interval = break_interval

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
        if self.timer is None or not self.timer.is_running:
            try:
                work_interval = int(self.work_entry.get())
                break_interval_minutes = int(self.break_entry.get())  # Get break interval in minutes
                break_interval_seconds = int(self.break_entry_sec.get())  # Get break interval in seconds
            except ValueError:
                tk.messagebox.showerror("Invalid input", "Please enter valid integers for the intervals.")
                return

            total_break_interval = (break_interval_minutes * 60) + break_interval_seconds  # Convert to total seconds

            if total_break_interval <= 0:
                tk.messagebox.showerror("Invalid input", "Break interval cannot be zero or negative.")
                return

            logging.debug(f"Starting timer with work_interval={work_interval} minutes, "
                          f"total_break_interval={total_break_interval} seconds.")

            self.timer = PomodoroTimer(work_interval, total_break_interval, self.update_timer_display,
                                       send_notification_with_sound, self.alarm_sound_path)
            self.timer.start()
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            self.sound_button.config(state=tk.DISABLED)  # Disable Select Sound button
            self.update_timer_display(self.timer.remaining_time)

            # Set the maximum for the progress bar based on the initial mode
            if self.timer.current_mode == 'work':
                self.progress["maximum"] = work_interval * 60  # Set maximum based on work interval in seconds
            else:
                self.progress["maximum"] = total_break_interval  # Set maximum based on total break interval in seconds

            # Reset progress bar to start from 0
            self.progress["value"] = 0

            # Disable interval changes while running
            self.work_entry.config(state=tk.DISABLED)
            self.break_entry.config(state=tk.DISABLED)
            self.break_entry_sec.config(state=tk.DISABLED)

    def pause_timer(self):
        if self.timer:
            self.timer.pause()
            self.pause_button.config(text="Resume" if self.timer.is_paused else "Pause")
            # Optionally enable the sound button if paused
            if self.timer.is_paused:
                self.sound_button.config(state=tk.NORMAL)
            else:
                self.sound_button.config(state=tk.DISABLED)

    def stop_timer(self):
        if self.timer:
            self.timer.stop()
            self.timer = None
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
            self.sound_button.config(state=tk.NORMAL)  # Re-enable Select Sound button
            self.pause_button.config(text="Pause")

            # Re-enable interval changes after stopping
            self.work_entry.config(state=tk.NORMAL)
            self.break_entry.config(state=tk.NORMAL)
            self.break_entry_sec.config(state=tk.NORMAL)

            # Reset timer display to work interval
            self.update_timer_display(self.work_interval * 60, update_progress=False)  # No progress bar update
            self.progress["value"] = 0  # Reset progress bar

    def on_closing(self):
        logging.debug("Application closing.")
        if self.timer:
            self.timer.stop()  # Stop the timer if it's running
        self.root.destroy()  # Close the application

    def run(self):
        logging.debug("Application started.")
        self.root.mainloop()
