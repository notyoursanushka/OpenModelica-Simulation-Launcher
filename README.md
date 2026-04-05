# OpenModelica Simulation Launcher

A PyQt6 desktop application to launch and control OpenModelica 
compiled simulations through a clean and simple GUI.

![Python](https://img.shields.io/badge/Python-3.6+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green)
![OpenModelica](https://img.shields.io/badge/OpenModelica-1.26.3-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [How to Use](#how-to-use)
- [Running Tests](#running-tests)
- [Known Issues](#known-issues)

---

## Overview

This project is a two-part submission:

1. **OpenModelica Model Compilation** — The `TwoConnectedTanks` 
model from the `NonInteractingTanks` package was compiled using 
OpenModelica 1.26.3 into a Windows executable.

2. **PyQt6 GUI Application** — A desktop app that allows users to 
select the compiled executable, set simulation start and stop times, 
and run the simulation — all from a clean interface.

---

## Features

- Browse and select any OpenModelica compiled executable
- Real-time input validation with color feedback (green/red)
- Run simulation in a background thread (GUI stays responsive)
- Progress bar during simulation
- Color-coded output log (blue, orange for warnings, red for errors)
- Show simulation results graph using matplotlib
- Save output log to a `.txt` file
- Clear log button

---

## Project Structure
OpenModelica_App/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── conftest.py                  # pytest configuration
├── README.md
├── app/
│   ├── init.py
│   ├── main_window.py           # Main GUI window (PyQt6)
│   ├── simulation_runner.py     # Subprocess handler (QThread)
│   ├── result_plotter.py        # Matplotlib results plotter
│   └── validators.py            # Input validation logic
├── tests/
│   ├── init.py
│   └── test_validators.py       # Unit tests (pytest)
└── model/
├── TwoConnectedTanks.exe    # Compiled OpenModelica executable
├── TwoConnectedTanks_init.xml
├── TwoConnectedTanks_info.json
├── TwoConnectedTanks_JacA.bin
└── *.dll                    # Required runtime libraries

---

## Requirements

- Python 3.6+
- PyQt6
- matplotlib
- scipy
- pytest (for tests)

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/notyoursanushka/OpenModelica-Simulation-Launcher
cd OpenModelica-Simulation-Launcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## How to Run
```bash
python main.py
```

---

## How to Use

1. Click **Browse** and select `TwoConnectedTanks.exe` 
   from the `model/` folder
2. Enter **Start Time** — must be an integer >= 0
3. Enter **Stop Time** — must be an integer, greater than 
   start time and less than 5
4. Click **▶ Run Simulation**
5. View colored output in the log box
6. Click **📊 Show Results Graph** to view simulation results
7. Click **💾 Save Log** to save output to a file

### Validation Rules
0 <= Start Time < Stop Time < 5

---

## Running Tests
```bash
python -m pytest tests/ -v
```

Expected output:
tests/test_validators.py::TestValidateTimes::test_valid_inputs         PASSED
tests/test_validators.py::TestValidateTimes::test_valid_boundary       PASSED
tests/test_validators.py::TestValidateTimes::test_non_integer_start    PASSED
tests/test_validators.py::TestValidateTimes::test_non_integer_stop     PASSED
tests/test_validators.py::TestValidateTimes::test_negative_start       PASSED
tests/test_validators.py::TestValidateTimes::test_stop_equal_to_5      PASSED
tests/test_validators.py::TestValidateTimes::test_stop_greater_than_5  PASSED
tests/test_validators.py::TestValidateTimes::test_start_equal_to_stop  PASSED
tests/test_validators.py::TestValidateTimes::test_start_greater_than_stop PASSED
tests/test_validators.py::TestValidateTimes::test_float_inputs         PASSED
10 passed

---

## Known Issues

- The `TwoConnectedTanks` model encounters a **division by zero** 
  error at initialization (tank2.Q1 = 0). This is a model-level 
  issue with initial conditions, not an application bug.
- Due to this, the results graph may not display meaningful data.
- The application handles this gracefully and displays the 
  simulation output log regardless.

## Model Executable Note
The compiled `.exe` and `.dll` files are not included
in this repository due to GitHub's 100MB file size limit.

To get them:
1. Install OpenModelica from https://openmodelica.org
2. Load the `NonInteractingTanks` package in OMEdit
3. Simulate `TwoConnectedTanks` model
4. Copy output files from:
   C:\Users\<you>\AppData\Local\Temp\OpenModelica\OMEdit\
   into the `model/` folder
5. Copy DLL files from:
   C:\Program Files\OpenModelica1.26.3-64bit\bin\
   into the `model/` folder
---

## Technologies Used

- **Python 3.6+**
- **PyQt6** — GUI framework
- **OpenModelica 1.26.3** — Model compilation
- **matplotlib** — Results plotting
- **scipy** — .mat file parsing
- **pytest** — Unit testing

