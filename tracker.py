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


@dataclass
class Workout:
    date: str  # YYYY-MM-DD
    exercise: str
    sets: int
    reps: int
    weight: float
    duration: float  # minutes for cardio

    def total_volume(self) -> float:
        """Calculate weight training volume (sets * reps * weight)."""
        try:
            return float(self.sets) * float(self.reps) * float(self.weight)
        except Exception:
            return 0.0


def ensure_csv_exists():
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(
            columns=["date", "exercise", "sets", "reps", "weight", "duration"]
        )
        df.to_csv(CSV_PATH, index=False)


def add_workout_interactive():
    ensure_csv_exists()
    today = datetime.today().strftime("%Y-%m-%d")
    date = input(f"Date (YYYY-MM-DD) [{today}]: ").strip() or today
    exercise = input("Exercise name: ").strip()

    # If the user types 'cardio' or provides a duration, treat as cardio
    is_cardio = False
    duration = 0.0
    sets = reps = 0
    weight = 0.0

    dur_input = input("Duration in minutes (leave blank if not cardio): ").strip()
    if dur_input:
        try:
            duration = float(dur_input)
            is_cardio = True
        except ValueError:
            print("Invalid duration; defaulting to 0")

    if not is_cardio:
        sets = int(input("Sets: ").strip() or 0)
        reps = int(input("Reps per set: ").strip() or 0)
        weight = float(input("Weight (use 0 for bodyweight): ").strip() or 0)

    w = Workout(date=date, exercise=exercise, sets=sets, reps=reps, weight=weight, duration=duration)

    # Append to CSV using pandas for robust handling
    row = {k: v for k, v in asdict(w).items()}
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    print(f"Saved workout: {w}")


def generate_report():
    ensure_csv_exists()
    df = pd.read_csv(CSV_PATH)
    if df.empty:
        print("No workouts logged yet.")
        return

    # Normalize types
    df['sets'] = pd.to_numeric(df['sets'], errors='coerce').fillna(0).astype(int)
    df['reps'] = pd.to_numeric(df['reps'], errors='coerce').fillna(0).astype(int)
    df['weight'] = pd.to_numeric(df['weight'], errors='coerce').fillna(0.0)
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0.0)

    # Compute volume per row
    df['volume'] = df['sets'] * df['reps'] * df['weight']

    # Workout frequency per exercise
    freq = df.groupby('exercise').size().sort_values(ascending=False)
    print("\nWorkout frequency per exercise:")
    print(freq.to_string())

    # Total volume per exercise
    total_vol = df.groupby('exercise')['volume'].sum().sort_values(ascending=False)
    print("\nTotal volume per exercise:")
    print(total_vol.to_string())

    # Personal records (max volume per single entry)
    pr = df.groupby('exercise')['volume'].max().sort_values(ascending=False)
    print("\nPersonal records (max volume per session):")
    print(pr.to_string())

    # Total cardio duration
    cardio_total = df['duration'].sum()
    print(f"\nTotal cardio duration (minutes): {cardio_total}")

    # Visualizations
    try:
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
    except Exception as e:
        print(f"Could not display charts: {e}")


def main_menu():
    ensure_csv_exists()
    while True:
        print("\nSmart Workout Tracker")
        print("1) Add workout")
        print("2) Generate report")
        print("3) Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_workout_interactive()
        elif choice == '2':
            generate_report()
        elif choice == '3':
            print("Goodbye")
            break
        else:
            print("Invalid choice")


if __name__ == '__main__':
    main_menu()
#!/usr/bin/env python3
"""
Smart Workout Tracker
CLI to add workouts, generate reports, and visualize progress.
"""
from __future__ import annotations
import csv
import datetime
import os
from dataclasses import dataclass, asdict
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "workouts.csv"

@dataclass
class Workout:
    date: str  # YYYY-MM-DD
    exercise: str
    sets: int
    reps: int
    weight: float
    duration: float  # minutes (for cardio)

    def total_volume(self) -> float:
        """Calculate total volume for weight training.

        Volume = sets * reps * weight
        For cardio (weight == 0), volume is 0.
        """
        try:
            return float(self.sets) * float(self.reps) * float(self.weight)
        except Exception:
            return 0.0


def ensure_csv(path: str = CSV_PATH) -> None:
    if not os.path.exists(path):
        df = pd.DataFrame(
            columns=["date", "exercise", "sets", "reps", "weight", "duration"]
        )
        df.to_csv(path, index=False)


def save_workout(workout: Workout, path: str = CSV_PATH) -> None:
    ensure_csv(path)
    df = pd.DataFrame([asdict(workout)])
    df.to_csv(path, mode="a", header=not os.path.exists(path) or os.path.getsize(path) == 0, index=False)
    print("Workout saved.")


def prompt_for_workout() -> Optional[Workout]:
    today = datetime.date.today().isoformat()
    date = input(f"Date (YYYY-MM-DD) [default: {today}]: ").strip() or today
    exercise = input("Exercise name: ").strip()
    if not exercise:
        print("Exercise name is required.")
        return None

    # Distinguish cardio by asking if it's cardio
    cardio_resp = input("Is this cardio? (y/N): ").strip().lower()
    if cardio_resp == "y":
        try:
            duration = float(input("Duration (minutes): ").strip() or "0")
        except ValueError:
            duration = 0.0
        return Workout(date=date, exercise=exercise, sets=0, reps=0, weight=0.0, duration=duration)

    # Strength exercise
    try:
        sets = int(input("Sets: ").strip() or "0")
        reps = int(input("Reps: ").strip() or "0")
        weight = float(input("Weight (per rep): ").strip() or "0")
    except ValueError:
        print("Invalid numeric input.")
        return None

    return Workout(date=date, exercise=exercise, sets=sets, reps=reps, weight=weight, duration=0.0)


def load_data(path: str = CSV_PATH) -> pd.DataFrame:
    ensure_csv(path)
    df = pd.read_csv(path, parse_dates=["date"]) if os.path.exists(path) and os.path.getsize(path) > 0 else pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight", "duration"])  # type: ignore
    # Ensure types
    for col in ["sets", "reps"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    for col in ["weight", "duration"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
    return df


def generate_report(path: str = CSV_PATH) -> None:
    df = load_data(path)
    if df.empty:
        print("No workout data available.")
        return

    # Workout frequency per exercise
    freq = df.groupby("exercise").size().sort_values(ascending=False)
    print("\nWorkout frequency per exercise:")
    print(freq.to_string())

    # Total volume per exercise (sum of sets*reps*weight per row)
    df["volume"] = df.apply(lambda r: (r.get("sets", 0) * r.get("reps", 0) * r.get("weight", 0.0)), axis=1)
    total_volume = df.groupby("exercise")["volume"].sum().sort_values(ascending=False)
    print("\nTotal volume per exercise:")
    print(total_volume.to_string())

    # Personal records (max volume per session)
    pr = df.groupby("exercise")["volume"].max().sort_values(ascending=False)
    print("\nPersonal records (max volume per exercise):")
    print(pr.to_string())

    # Total cardio duration
    cardio_total = df.loc[df["duration"] > 0, "duration"].sum()
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
