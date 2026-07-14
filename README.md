# Vortex Tech Cybersecurity Internship – Week 2

## What this is
Week 2 task for the Vortex Tech Cybersecurity Internship Track: hands-on practice with two basic security tools — a Python password strength checker (CLI + GUI versions) and a local Nmap port scan (run only on localhost, own machine).

## What's in this repo
- `password_checker.py` — command-line Python script that rates a password as Weak, Medium, or Strong based on length, character variety, and a common-password check, with feedback on what to improve. Also includes an interactive mode to check your own password.
- `password_analyzer_gui.py` — a Tkinter desktop GUI version of the same checker, with live feedback and a visual strength meter.
- `Week2_SecurityTools_Arooj.docx` — full write-up: password checker logic and example outputs, port scan results, what open ports mean, and a reflection.

## How to run
CLI version:python3 password_checker.py
GUI version:python3 password_analyzer_gui.py
Only localhost was scanned with Nmap, in line with the task's permission requirement — no third-party network was tested.

