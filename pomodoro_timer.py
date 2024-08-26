import logging
from gui import PomodoroApp

# Disable all logging messages
logging.disable(logging.CRITICAL)

if __name__ == "__main__":
    app = PomodoroApp()
    app.run()
