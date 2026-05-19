"""Retry shots that failed in the main batch (typically due to concurrency limit)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_gameplay import JOBS, run, OUT_DIR
import threading, time

WANTED = {"09-pull-up.png", "10-bomb-suitcase.png"}

def main():
    todo = [j for j in JOBS if j["filename"] in WANTED]
    print(f"Retrying {len(todo)} shots: {[j['filename'] for j in todo]}")
    results = {}
    threads = [threading.Thread(target=run, args=(j, results), daemon=True) for j in todo]
    for t in threads:
        t.start(); time.sleep(0.3)
    for t in threads:
        t.join()
    print("\nDONE:")
    for j in todo:
        print(f"  {j['filename']:25s} {results.get(j['filename'], ('missing',))[0]}")

if __name__ == "__main__":
    main()
