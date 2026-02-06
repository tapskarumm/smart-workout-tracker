#!/usr/bin/env python3
"""Smart Workout Tracker

CLI app to add workouts, analyze performance, and visualize progress.
"""
from __future__ import annotations
import csv
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "workouts.csv")
# CSV column format: date,exercise,sets,reps,weight,duration
# Example row: 2026-02-01,Push-ups,3,15,0,0
# Keeping an explicit example here helps reviewers quickly understand the data layout.


@dataclass
class Workout:
    date: str  # YYYY-MM-DD
    exercise: str
    sets: int
    reps: int
    weight: float
    duration: float  # minutes for cardio

    #!/usr/bin/env python3
    """Smart Workout Tracker

    This script implements a small, recruiter-friendly CLI that:
    - stores workouts in a CSV file
    - computes simple analytics (frequency, total volume, PRs)
    - plots visual summaries using matplotlib

    The comments below are intentionally friendly and descriptive — think clear,
    conversational explanations you'd share in a well-documented college project.
    """

    from __future__ import annotations
    import os
    from dataclasses import dataclass, asdict
    from datetime import datetime, date
    from typing import Optional

    import pandas as pd
    import matplotlib.pyplot as plt


    # Path to the CSV file that stores workouts. We keep it next to this script
    # so the project is self-contained and easy to inspect for recruiters.
    CSV_PATH = os.path.join(os.path.dirname(__file__), "workouts.csv")


    @dataclass
    class Workout:
        """Simple data model for a single workout entry.

        Fields:
        - date: ISO date string (YYYY-MM-DD)
        - exercise: name of the exercise or activity
        - sets, reps, weight: for resistance training
        - duration: minutes for cardio (set to 0 for strength work)

        This class includes a convenience method `total_volume()` which computes
        the training volume for resistance exercises (sets * reps * weight).
        """

        date: str
        exercise: str
        sets: int
        reps: int
        weight: float
        duration: float

        def total_volume(self) -> float:
            """Return the numeric training volume for this entry.

            This gracefully returns 0.0 if any numeric fields are missing or invalid.
            """
            # Note: bodyweight exercises typically have weight==0; callers can still
            # rely on volume==0 while tracking reps/sets separately.
            try:
                return float(self.sets) * float(self.reps) * float(self.weight)
            except Exception:
                return 0.0


    def ensure_csv(path: str = CSV_PATH) -> None:
        """Create an empty CSV with the correct headers if it doesn't exist yet.

        This keeps the rest of the code simple because we can always assume the
        CSV exists and has the expected columns.
        """
        if not os.path.exists(path):
            # We define the canonical header order here so saved files are
            # consistent across machines and easy to open in Excel or pandas.
            df = pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight", "duration"])
            df.to_csv(path, index=False)


    def save_workout(workout: Workout, path: str = CSV_PATH) -> None:
        """Append a `Workout` to the CSV file using pandas.

        Using pandas here makes the CSV handling robust and concise; it also keeps
        the file easily readable for recruiters who want to peek at sample data.
        """
        ensure_csv(path)
        row = pd.DataFrame([asdict(workout)])
        # Append without rewriting the entire file header each time.
        # If the file doesn't exist or is empty, write headers. Otherwise append.
        header = not os.path.exists(path) or os.path.getsize(path) == 0
        row.to_csv(path, mode="a", header=header, index=False)
        # Friendly confirmation so interactive users know their input was saved.
        # (Helps during demos where people want immediate feedback.)


    def prompt_for_workout() -> Optional[Workout]:
        """Interactively prompt the user for a workout record.

        The prompts are intentionally forgiving: blank date defaults to today,
        numeric fields are validated gently, and cardio is handled separately.
        """
        today = date.today().isoformat()
        date_str = input(f"Date (YYYY-MM-DD) [{today}]: ").strip() or today

        exercise = input("Exercise name: ").strip()
        if not exercise:
            print("Exercise name is required — please try again.")
            return None

        # Quick check: is this cardio work? Cardio entries record duration only.
        cardio_ans = input("Is this cardio? (y/N): ").strip().lower()
        if cardio_ans == "y":
            try:
                duration = float(input("Duration (minutes): ").strip() or 0)
            except ValueError:
                print("Could not parse duration, defaulting to 0.")
                duration = 0.0
            return Workout(date=date_str, exercise=exercise, sets=0, reps=0, weight=0.0, duration=duration)

        # If it's not cardio, we collect strength metrics. The UI keeps it simple
        # but ensures that values are numbers — we avoid crashing on bad user input.
        # Strength-type entry: ask for sets/reps/weight and validate inputs.
        try:
            sets = int(input("Sets: ").strip() or 0)
            reps = int(input("Reps per set: ").strip() or 0)
            weight = float(input("Weight (per rep, use 0 for bodyweight): ").strip() or 0.0)
        except ValueError:
            print("Invalid number entered — please try again.")
            return None

        return Workout(date=date_str, exercise=exercise, sets=sets, reps=reps, weight=weight, duration=0.0)


    def load_data(path: str = CSV_PATH) -> pd.DataFrame:
        """Load the CSV into a pandas DataFrame and normalize column types.

        Returning a DataFrame simplifies downstream reporting and plotting logic.
        """
        ensure_csv(path)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            df = pd.read_csv(path)
        else:
            df = pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight", "duration"])  # type: ignore

        # Coerce numeric types and fill missing values sensibly.
        df['sets'] = pd.to_numeric(df.get('sets', 0), errors='coerce').fillna(0).astype(int)
        df['reps'] = pd.to_numeric(df.get('reps', 0), errors='coerce').fillna(0).astype(int)
        df['weight'] = pd.to_numeric(df.get('weight', 0.0), errors='coerce').fillna(0.0)
        df['duration'] = pd.to_numeric(df.get('duration', 0.0), errors='coerce').fillna(0.0)

        return df


    def generate_report(path: str = CSV_PATH) -> None:
        """Compute and print summary statistics, then show charts.

        The printed output is concise for quick inspection, while the charts give
        an immediate visual summary recruiters (and humans) appreciate.
        """
        df = load_data(path)
        if df.empty:
            print("No workouts logged yet — add your first workout to get started.")
            return

        # Compute per-row training volume for strength entries
        df['volume'] = df['sets'] * df['reps'] * df['weight']

        # Frequency: how many sessions per exercise
        freq = df.groupby('exercise').size().sort_values(ascending=False)
        print("\nWorkout frequency per exercise:")
        print(freq.to_string())

        # Total accumulated volume per exercise across all sessions
        total_vol = df.groupby('exercise')['volume'].sum().sort_values(ascending=False)
        print("\nTotal volume per exercise:")
        print(total_vol.to_string())

        # Personal records: the highest single-session volume per exercise
        pr = df.groupby('exercise')['volume'].max().sort_values(ascending=False)
        print("\nPersonal records (max single-session volume):")
        print(pr.to_string())

        # Cardio summary: total minutes
        cardio_total = df['duration'].sum()
        print(f"\nTotal cardio duration (minutes): {cardio_total}")

        # Plotting: two simple bar charts that pop up automatically
        try:
            # We attempt to display charts; in CI or headless servers this may fail,
            # which is why we catch exceptions. Local users (or recruiters) will
            # typically see the visuals in an interactive session.
            plt.figure(figsize=(10, 5))
            freq.plot(kind='bar', title='Workout Frequency per Exercise')
            plt.xlabel('Exercise')
            plt.ylabel('Sessions')
            plt.tight_layout()
            plt.show()

            plt.figure(figsize=(10, 5))
            total_vol.plot(kind='bar', title='Total Volume per Exercise')
            plt.xlabel('Exercise')
            plt.ylabel('Total Volume (sets * reps * weight)')
            plt.tight_layout()
            plt.show()
        except Exception as exc:
            # We catch plotting errors so headless environments don't crash the CLI.
            print(f"Could not display charts: {exc}")


    def main_menu() -> None:
        """Main command-line loop offering a small menu of actions.

        This keeps the UX straightforward for quick demos and manual testing.
        """
        ensure_csv(CSV_PATH)
        while True:
            print("\nSmart Workout Tracker")
            print("1) Add workout")
            print("2) Generate report")
            print("3) Exit")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                w = prompt_for_workout()
                if w:
                    save_workout(w)
                    print("Saved.")
            elif choice == '2':
                generate_report()
            elif choice == '3':
                print("Goodbye — keep up the great workouts!")
                break
            else:
                print("Sorry, I didn't understand that. Please enter 1, 2, or 3.")


    if __name__ == '__main__':
        main_menu()

    print(f"\nTotal cardio duration (minutes): {cardio_total}")

    # Visualizations
    try:
        plt.style.use("seaborn-v0_8")
    except Exception:
        pass

    # Frequency chart
    if not freq.empty:
        ax = freq.plot(kind="bar", figsize=(8, 5), title="Workout Frequency per Exercise")
        ax.set_xlabel("Exercise")
        ax.set_ylabel("Sessions")
        plt.tight_layout()
        plt.show()

    # Total volume chart
    if not total_volume.empty:
        ax2 = total_volume.plot(kind="bar", figsize=(8, 5), title="Total Volume per Exercise")
        ax2.set_xlabel("Exercise")
        ax2.set_ylabel("Total Volume (sets * reps * weight)")
        plt.tight_layout()
        plt.show()


def main_loop() -> None:
    ensure_csv(CSV_PATH)
    while True:
        print("\nSmart Workout Tracker")
        print("1) Add workout")
        print("2) Generate report")
        print("3) Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            w = prompt_for_workout()
            if w:
                save_workout(w)
        elif choice == "2":
            generate_report()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main_loop()
