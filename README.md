# Drone Operations Coordinator AI Agent

## Overview
This is a prototype AI agent designed to help Drone Operations Coordinators manage pilots, drones, and missions. It features a conversational interface powered by simple rule-based logic (simulating an LLM) and a Streamlit dashboard.

## Features
- **Roster Management**: Track pilot status, location, and skills.
- **Fleet Management**: Track drone status and maintenance.
- **Conflict Detection**: Prevent double bookings, skill mismatches, and maintenance conflicts.
- **Assignment**: Assign pilots and drones to projects via chat.
- **Urgent Reassignment**: Quickly find replacements for unavailable resources.

## Setup & Running
1. **Prerequisites**: Python 3.8+
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App**:
   ```bash
   streamlit run src/app.py
   ```

## Project Structure
- `data/`: Contains CSV files for flight data.
- `src/`: Source code.
  - `app.py`: Main Streamlit application.
  - `agent.py`: Agent logic and query processing.
  - `managers.py`: Business logic for Roster and Fleet.
  - `conflict_detector.py`: Conflict detection logic.
  - `assignment_manager.py`: Assignment operations.
- `decision_log.md`: Implementation decisions and trade-offs.

## Usage
- Open the app in your browser (usually http://localhost:8501).
- Use the **Chat Interface** to query data ("List available pilots") or make assignments ("Assign pilot P001 to PRJ001").
- Use the **Tabs** to view full tables and manually update statuses.
