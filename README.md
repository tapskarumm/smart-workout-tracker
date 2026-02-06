# Smart Workout Tracker

 A recruiter-ready Python project to track workouts, analyze performance, and visualize progress.

 ## Overview

 Smart Workout Tracker is a small, professional CLI application that demonstrates Python, object-oriented design, data analysis with pandas, and visualizations with matplotlib. It stores workouts in a CSV file and provides reporting and charts to surface training progress.

 ## Features

 - Add workouts (resistance or cardio) through a terminal interface
 - Persistent storage in `workouts.csv` (auto-created)
 - Reports: workout frequency, total volume per exercise, personal records, total cardio duration
 - Charts: workout frequency and total volume per exercise (matplotlib)

 ## Installation

 Make a virtual environment (recommended) and install dependencies:

 ```bash
 python3 -m venv .venv
 source .venv/bin/activate
 pip install -r requirements.txt
 ```

 ## Usage

 Run the CLI:

 ```bash
 python tracker.py
 ```

 Menu options:
 - `1` Add workout — follow prompts to input date, exercise, sets/reps/weight or duration for cardio
 - `2` Generate report — prints summaries and displays charts
 - `3` Exit

 ## Project Structure

 ```
 smart-workout-tracker/
 ├── tracker.py
 ├── workouts.csv
 ├── requirements.txt
 └── README.md
 ```

 ## Skills Demonstrated

 - Python 3 and OOP (`dataclasses`)
 - Data manipulation with `pandas`
 - Visualization with `matplotlib`
 - CLI design and user interaction
 - CSV-based persistence for simple projects

 ## Next Steps

 - Add a web UI with Flask or a fast interactive dashboard using Streamlit
 - Add automated tests and CI
 - Add authentication and per-user storage