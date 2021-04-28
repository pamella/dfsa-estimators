#!/usr/bin/env python3
from core.estimators import simulate


def main():
    print("\nPlease enter the requested params below.")

    try:
        estimator = int(input("Estimator (type 0 for Lower Bound, 1 for Eom-Lee, 2 for compare Lower Bound and Eom-Lee): "))
    except Exception:
        estimator = 0

    try:
        initial_tag_amount = int(input("Initial Tag Amount: "))
    except Exception:
        initial_tag_amount = 100

    try:
        max_tag_amount = int(input("Max Tag Amount: "))
    except Exception:
        max_tag_amount = 1000

    try:
        tag_increment_interval = int(input("Tag Increment Interval: "))
    except Exception:
        tag_increment_interval = 100

    try:
        max_repetition = int(input("Max Repetition: "))
    except Exception:
        max_repetition = 2000

    try:
        initial_frame_size = int(input("Initial Frame Size: "))
    except Exception:
        initial_frame_size = 64

    print("\nRunning simulation... It might take a few seconds.\n")

    simulate(
        estimator,
        initial_tag_amount,
        max_tag_amount,
        tag_increment_interval,
        max_repetition,
        initial_frame_size,
    )

    print("\nSimulation completed.\n")


if __name__ == "__main__":
    main()
