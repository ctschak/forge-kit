#!/usr/bin/env python3
"""Run one turn and kill it as soon as a ledger row reaches ✅ (interrupt/resume scenario Q6).

usage: interrupt_after.py <run-dir> <plugin-dir> "<message>" <item-id, e.g. SPEC-1.TASK1> [timeout-secs]
Then resume with a fresh session:  mv <run>/.session <run>/.session.killed && turn.sh <run> <plugin> "/forge:forge"
"""
import glob
import os
import signal
import subprocess
import sys
import time

run, plug, msg, item = sys.argv[1:5]
timeout = int(sys.argv[5]) if len(sys.argv) > 5 else 600
turn = os.path.join(os.path.dirname(os.path.abspath(__file__)), "turn.sh")
p = subprocess.Popen([turn, run, plug, msg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)
t0, killed = time.time(), False
while p.poll() is None and time.time() - t0 < timeout:
    for led in glob.glob(os.path.join(run, "docs", "forge", "tasks", "*", "impl-tasks", "ledger.md")):
        with open(led, encoding="utf-8") as fh:
            rows = [l for l in fh if l.startswith("| " + item + " ")]
        if rows and "✅" in rows[0]:
            os.killpg(p.pid, signal.SIGTERM)
            killed = True
    if killed:
        break
    time.sleep(2)
p.wait()
print("killed after %s ✅" % item if killed else "turn finished before %s reached ✅" % item, "(%ds)" % (time.time() - t0))
sys.exit(0 if killed else 1)
