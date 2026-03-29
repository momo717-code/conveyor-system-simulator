# conveyor-system-simulator
Conveyor System Production Simulator
A Python-based production line simulator with real-time hour-by-hour output, dual production modes, maintenance scheduling, and persistent data storage between sessions.
Overview
This software engineering project simulates an industrial conveyor belt system that tracks cumulative production hours and items manufactured. The system enforces mandatory maintenance inspections after a configurable threshold, supports two production modes with different output rates, and persists all data between runs via file I/O.
Features

Dual production modes — Optimised (1.5 items/min) and Full (2.0 items/min) with user selection at each shift start
Real-time simulation — 1-second delay per production hour with live output of hourly item counts
Maintenance scheduling — Automatic maintenance inspection triggered at 35 operating hours, with mandatory confirmation before production can resume
Persistent data storage — Cumulative hours and items saved to file between sessions, with error handling for missing or corrupted data
Input validation — Robust handling of invalid user inputs throughout all menu interactions

Tech Stack

Python — standard library only (time, os)
No external dependencies required

Project Structure
├── conveyor_system (UPDATED).py    # Main production simulator
├── conveyor_system_req8.py         # Extended version (requirement 8)
├── conveyor_system_req9.py         # Extended version (requirement 9)
├── productivity_data.txt           # Persistent data file (auto-generated)
└── README.md
How to Run
bashpython "conveyor_system (UPDATED).py"
The program will create productivity_data.txt automatically if it doesn't exist. Data persists between runs — restart the program to continue from where you left off.
Key Design Decisions

File-based persistence chosen over database for simplicity and portability
Maintenance threshold check runs both at startup and during production to prevent any operation beyond safe limits
Production loop exits on either daily hour limit (10 hours) or maintenance threshold, whichever comes first

Academic Context
MSc AI for Software Development — Software Development module, University of Dundee (2026).
