"""Retry the 4 modeling refs that hit the 8-concurrency limit."""
import os, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_props_modeling_2 import JOBS as ALL_JOBS
from generate_props import run_to_props

WANTED = {
    "m09-harness-on-char-front.png",
    "m10-harness-on-char-side.png",
    "m11-rope-coiled.png",
    "m12-debris-sheet.png",
}

JOBS = [j for j in ALL_JOBS if j["filename"] in WANTED]


def main():
    print(f"Retry: {len(JOBS)} modeling refs")
    results = {}
    threads = [threading.Thread(target=run_to_props, args=(j, results), daemon=True) for j in JOBS]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE retry:")
    for j in JOBS:
        print(f"  {j['filename']:40s} {results.get(j['filename'], ('missing',))[0]}")


if __name__ == "__main__":
    main()
