"""
result_plotter.py
-----------------
Parses the OpenModelica .mat results file and
plots tank levels over time using matplotlib.
"""

import os
import numpy as np
import matplotlib.pyplot as plt


def plot_results(mat_path: str) -> None:
    """
    Load and plot simulation results from an OpenModelica .mat file.

    OpenModelica uses a specific .mat format (version 4) with:
        - 'name'   : variable names as a char matrix
        - 'data_2' : simulation data rows

    Args:
        mat_path: Full path to the _res.mat file.
    """
    try:
        import scipy.io
        mat = scipy.io.loadmat(mat_path)

        # Extract variable names — stored as char array, each column is a name
        raw_names = mat.get("name", None)
        data = mat.get("data_2", None)

        if raw_names is None or data is None:
            _plot_unavailable(mat_path)
            return

        # Convert char matrix to list of strings
        var_names = []
        for col in range(raw_names.shape[1]):
            chars = raw_names[:, col]
            name = "".join(
                chr(int(c)) for c in chars if int(c) != 0
            ).strip()
            var_names.append(name)

        # Find time variable
        time_idx = next(
            (i for i, n in enumerate(var_names) if n == "time"), None
        )
        if time_idx is None:
            _plot_unavailable(mat_path)
            return

        time = np.array(data[time_idx], dtype=float)

        # Plot all variables except time
        fig, ax = plt.subplots(figsize=(10, 5))

        for i, name in enumerate(var_names):
            if name == "time":
                continue
            try:
                values = np.array(data[i], dtype=float)
                ax.plot(time, values, label=name)
            except Exception:
                continue

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Value")
        ax.set_title("TwoConnectedTanks Simulation Results")
        ax.legend(loc="best")
        ax.grid(True, linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

    except Exception as exc:
        print(f"Could not plot results: {exc}")
        _plot_unavailable(mat_path)


def _plot_unavailable(mat_path: str) -> None:
    """Show a message plot if results cannot be parsed."""
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.text(
        0.5, 0.5,
        f"Could not parse results from:\n{os.path.basename(mat_path)}\n\n"
        "The simulation may not have produced valid output.",
        ha="center", va="center",
        transform=ax.transAxes,
        fontsize=10,
        color="red"
    )
    ax.axis("off")
    plt.tight_layout()
    plt.show()