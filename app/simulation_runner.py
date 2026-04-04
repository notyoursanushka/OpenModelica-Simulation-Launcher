"""
simulation_runner.py
--------------------
Handles launching the OpenModelica compiled executable
as a subprocess with the correct simulation flags.
"""

import subprocess
import os
from PyQt6.QtCore import QThread, pyqtSignal


class SimulationRunner(QThread):
    """
    Runs the OpenModelica executable in a background QThread
    so the GUI does not freeze during execution.

    Signals:
        finished_signal (str): Emitted with output on success.
        error_signal   (str): Emitted with error message on failure.
        progress_signal (int): Emitted to update progress bar.
    """

    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, executable_path: str, start_time: int, stop_time: int):
        super().__init__()
        self.executable_path = executable_path
        self.start_time = start_time
        self.stop_time = stop_time

    def run(self):
        """Executes the simulation with OpenModelica override flags."""
        command = [
            self.executable_path,
            f"-override=startTime={self.start_time},stopTime={self.stop_time}",
        ]
        working_dir = os.path.dirname(self.executable_path)

        try:
            self.progress_signal.emit(20)

            result = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )

            self.progress_signal.emit(80)

            output = ""
            if result.stdout:
                output += result.stdout
            if result.stderr:
                output += result.stderr

            self.progress_signal.emit(100)
            self.finished_signal.emit(
                output or "Simulation completed successfully."
            )

        except FileNotFoundError:
            self.error_signal.emit(
                f"Executable not found:\n{self.executable_path}"
            )
        except subprocess.TimeoutExpired:
            self.error_signal.emit(
                "Simulation timed out after 60 seconds."
            )
        except Exception as exc:
            self.error_signal.emit(f"Unexpected error:\n{str(exc)}")