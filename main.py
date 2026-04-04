"""
main.py
-------
Entry point for the OpenModelica Simulation Launcher.

Usage:
    python main.py
"""

import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MainWindow


def main():
    """Initialize and launch the PyQt6 application."""
    app = QApplication(sys.argv)
    app.setApplicationName("OpenModelica Simulation Launcher")
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()