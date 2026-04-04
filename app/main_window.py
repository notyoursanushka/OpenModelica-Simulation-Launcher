"""
main_window.py
--------------
Defines the MainWindow class — the primary GUI for the
OpenModelica Simulation Launcher application.
"""

import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog,
    QTextEdit, QMessageBox, QGroupBox, QStatusBar,
    QProgressBar,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor

from app.validators import validate_times
from app.simulation_runner import SimulationRunner
from app.result_plotter import plot_results


class MainWindow(QMainWindow):
    """Main application window for the OpenModelica Simulation Launcher."""

    def __init__(self):
        super().__init__()
        self._runner = None
        self._last_exe_path = None
        self._init_ui()

    def _init_ui(self):
        """Build and arrange all widgets."""
        self.setWindowTitle("OpenModelica Simulation Launcher")
        self.setMinimumSize(700, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        root_layout = QVBoxLayout(central_widget)
        root_layout.setSpacing(16)
        root_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("OpenModelica Simulation Launcher")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.addWidget(title)

        # Input Group
        input_group = QGroupBox("Simulation Parameters")
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)

        # 1. Executable path
        exe_layout = QHBoxLayout()
        exe_label = QLabel("Executable:")
        exe_label.setFixedWidth(100)
        self.exe_input = QLineEdit()
        self.exe_input.setPlaceholderText(
            "Path to compiled OpenModelica executable..."
        )
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.clicked.connect(self._browse_executable)
        exe_layout.addWidget(exe_label)
        exe_layout.addWidget(self.exe_input)
        exe_layout.addWidget(self.browse_btn)
        input_layout.addLayout(exe_layout)

        # 2. Start time
        start_layout = QHBoxLayout()
        start_label = QLabel("Start Time:")
        start_label.setFixedWidth(100)
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("Integer (0 <= start < stop < 5)")
        self.start_input.textChanged.connect(self._validate_live)
        start_layout.addWidget(start_label)
        start_layout.addWidget(self.start_input)
        input_layout.addLayout(start_layout)

        # 3. Stop time
        stop_layout = QHBoxLayout()
        stop_label = QLabel("Stop Time:")
        stop_label.setFixedWidth(100)
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("Integer (start < stop < 5)")
        self.stop_input.textChanged.connect(self._validate_live)
        stop_layout.addWidget(stop_label)
        stop_layout.addWidget(self.stop_input)
        input_layout.addLayout(stop_layout)

        root_layout.addWidget(input_group)

        # Output Log (created before buttons that reference it)
        output_group = QGroupBox("Output Log")
        output_layout = QVBoxLayout(output_group)
        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setFont(QFont("Courier New", 9))
        self.output_log.setPlaceholderText(
            "Simulation output will appear here..."
        )
        output_layout.addWidget(self.output_log)

        # Buttons Row
        btn_layout = QHBoxLayout()

        self.run_btn = QPushButton("▶  Run Simulation")
        self.run_btn.setFixedHeight(40)
        self.run_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.run_btn.clicked.connect(self._run_simulation)

        self.plot_btn = QPushButton("📊  Show Results Graph")
        self.plot_btn.setFixedHeight(40)
        self.plot_btn.setFont(QFont("Arial", 11))
        self.plot_btn.setEnabled(False)
        self.plot_btn.clicked.connect(self._show_graph)

        self.clear_btn = QPushButton("🗑  Clear Log")
        self.clear_btn.setFixedHeight(40)
        self.clear_btn.clicked.connect(self.output_log.clear)

        self.save_btn = QPushButton("💾  Save Log")
        self.save_btn.setFixedHeight(40)
        self.save_btn.clicked.connect(self._save_log)

        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.plot_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.save_btn)
        root_layout.addLayout(btn_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        root_layout.addWidget(self.progress_bar)

        # Add output group after buttons
        root_layout.addWidget(output_group)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def _validate_live(self):
        """Highlight input fields red/green as user types."""
        start = self.start_input.text().strip()
        stop = self.stop_input.text().strip()
        is_valid, _ = validate_times(start, stop)

        if start and stop:
            color = "#c8f7c5" if is_valid else "#f7c5c5"
            self.start_input.setStyleSheet(f"background-color: {color};")
            self.stop_input.setStyleSheet(f"background-color: {color};")
        else:
            self.start_input.setStyleSheet("")
            self.stop_input.setStyleSheet("")

    def _browse_executable(self):
        """Open file dialog to select the executable."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            caption="Select OpenModelica Executable",
            directory=os.getcwd(),
            filter="Executable Files (*.exe);;All Files (*)",
        )
        if path:
            self.exe_input.setText(path)
            self.status_bar.showMessage("Selected: " + path)

    def _run_simulation(self):
        """Validate inputs then launch simulation."""
        exe_path = self.exe_input.text().strip()
        start_str = self.start_input.text().strip()
        stop_str = self.stop_input.text().strip()

        if not exe_path:
            self._show_error("Please select an executable file.")
            return
        if not os.path.isfile(exe_path):
            self._show_error("Executable not found: " + exe_path)
            return

        is_valid, error_msg = validate_times(start_str, stop_str)
        if not is_valid:
            self._show_error(error_msg)
            return

        start_time = int(start_str)
        stop_time = int(stop_str)
        self._last_exe_path = exe_path

        self.output_log.clear()
        self._append_colored("Starting simulation...\n", "#2196F3")
        self._append_colored(f"  Executable : {exe_path}\n", "#555555")
        self._append_colored(f"  Start Time : {start_time}\n", "#555555")
        self._append_colored(f"  Stop Time  : {stop_time}\n", "#555555")
        self._append_colored("-" * 50 + "\n", "#555555")

        self.run_btn.setEnabled(False)
        self.plot_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_bar.showMessage("Running simulation...")

        self._runner = SimulationRunner(exe_path, start_time, stop_time)
        self._runner.finished_signal.connect(self._on_simulation_done)
        self._runner.error_signal.connect(self._on_simulation_error)
        self._runner.progress_signal.connect(self.progress_bar.setValue)
        self._runner.start()

    def _on_simulation_done(self, output: str):
        """Called when simulation completes."""
        for line in output.splitlines():
            if "error" in line.lower():
                self._append_colored(line + "\n", "#F44336")
            elif "warning" in line.lower():
                self._append_colored(line + "\n", "#FF9800")
            else:
                self._append_colored(line + "\n", "#333333")

        self._append_colored("=" * 50 + "\n", "#555555")
        self._append_colored("Simulation finished.\n", "#4CAF50")
        self.run_btn.setEnabled(True)
        self.plot_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Simulation completed.")

    def _on_simulation_error(self, error: str):
        """Called when simulation encounters an error."""
        self._append_colored("ERROR: " + error + "\n", "#F44336")
        self.run_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Simulation failed.")
        self._show_error("Simulation failed:\n\n" + error)

    def _append_colored(self, text: str, color: str):
        """Append colored text to the output log."""
        cursor = self.output_log.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        self.output_log.setTextCursor(cursor)
        self.output_log.ensureCursorVisible()

    def _show_graph(self):
        """Plot simulation results from .mat file."""
        if not self._last_exe_path:
            return
        mat_path = os.path.join(
            os.path.dirname(self._last_exe_path),
            "TwoConnectedTanks_res.mat"
        )
        if not os.path.exists(mat_path):
            self._show_error("Results file not found:\n" + mat_path)
            return
        plot_results(mat_path)

    def _save_log(self):
        """Save output log to a text file."""
        path, _ = QFileDialog.getSaveFileName(
            self,
            caption="Save Log File",
            directory="simulation_log.txt",
            filter="Text Files (*.txt);;All Files (*)",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.output_log.toPlainText())
            self.status_bar.showMessage("Log saved to: " + path)

    def _show_error(self, message: str):
        """Display a modal error dialog."""
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Icon.Critical)
        dialog.setWindowTitle("Error")
        dialog.setText(message)
        dialog.exec()