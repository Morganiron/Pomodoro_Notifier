# Pomodoro Timer

A simple Pomodoro Timer application built with Python and Tkinter. This application allows users to manage their work and break intervals using the Pomodoro Technique. It features a graphical user interface (GUI) where users can start, pause, and stop the timer, as well as customize the length of work and break intervals.

## Features

- **Work and Break Intervals**: Default intervals set to 25 minutes for work and 5 minutes for break.
- **Customizable Intervals**: Users can manually adjust the length of the work and break intervals.
- **Start, Pause, and Stop Controls**: Full control over the timer with dedicated buttons.
- **Real-Time Countdown Display**: A visible countdown timer shows the remaining time for the current session.
- **Popup Notifications**: Custom popup windows alert users when it's time to take a break and when the break is over.
- **Sound Alerts**: Users can select a sound file to play when a work or break interval ends.
- **Continuous Loop**: The timer alternates between work and break intervals until the user pauses or stops it.
- **Graceful Shutdown**: The application stops the timer and closes cleanly when the window is closed.

## Installation

### Prerequisites

- Python 3.x installed on your machine.

### Clone the Repository

```bash
git clone https://github.com/yourusername/pomodoro-timer.git
cd pomodoro-timer
```

### Install Dependencies

After cloning the repository, you need to install the required libraries for sound playback and notifications:

```bash
pip install pygame
```

### Running the Application

1. **Run the application** using the main script:

```bash
python pomodoro_timer.py
```

2. The GUI will appear, and you can start using the timer.

## Usage

- **Work Interval**: Set your desired work interval (in minutes) using the input field and the up/down buttons.
- **Break Interval**: Set your desired break interval (in minutes) using the input field and the up/down buttons.
- **Start Timer**: Click the "Start" button to begin the countdown. The timer will alternate between work and break intervals.
- **Pause Timer**: Click the "Pause" button to pause the timer. You can resume it by clicking "Pause" again (which will be labeled "Resume").
- **Stop Timer**: Click the "Stop" button to stop the timer and reset it to the initial work interval.
- **Close the Application**: The application will automatically stop the timer and close when you close the window.
- **Select Sound**: Use the "Select Sound" button to choose a sound file for notifications.

## Project Structure

```plaintext
pomodoro-timer/
│
├── pomodoro_timer.py          # Main script to run the application
├── timer.py                   # Timer logic and threading
├── notifications.py           # Notification handling
└── gui.py                     # GUI components and logic
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push your branch and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- [Tkinter](https://docs.python.org/3/library/tkinter.html) - The built-in Python GUI library.
- [Pygame](https://www.pygame.org/news) - Used for playing sound notifications.
