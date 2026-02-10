# Decision Log: Drone Operations Coordinator AI Agent

## Key Assumptions
1. **Mock Data vs Live Data**: 
   - I am using local CSV files as the primary data source to ensure the prototype is immediately testable without requiring Google Cloud credentials. 
   - The system is designed with a `DataManager` interface that can be extended to support Google Sheets or SQL databases in the future.

2. **Conflict Detection Scope**:
   - Conflicts are checked based on:
     - Date overlaps (Pilot/Drone already assigned).
     - Skill mismatches (Pilot lacks required skill).
     - Location mismatches (Pilot/Drone not in the project location).
     - Maintenance status (Drone in maintenance).
   - I assume a simple "exact match" or "contains" logic for skills (e.g., "Mapping" in "Mapping, Survey").

3. **Urgent Reassignments**:
   - I interpret "Urgent Reassignments" as a feature to quickly find substitutes for a pilot or drone that suddenly becomes unavailable.
   - The agent will prioritize "Available" resources in the same location first to minimize travel time/cost.

## Trade-offs
- **Streamlit vs React/Node**: 
  - *Choice*: Streamlit.
  - *Why*: Speed of development for data-heavy prototypes. It allows building the UI and backend logic in a single Python codebase, fitting the 6-hour timeline.
  - *Trade-off*: Less customizability in UI layout compared to a bespoke React app, but sufficient for an internal tool.

- **Local State Management**:
  - *Choice*: In-memory pandas DataFrames + CSV persistence.
  - *Why*: Simple and effective for a prototype.
  - *Trade-off*: Not suitable for concurrent users in production, but acceptable for a single-user prototype.

## "Urgent Reassignments" Interpretation
The prompt asks to "help coordinate urgent reassignments".
**My Implementation**:
- Detect when a generic "Unavailability" event happens (e.g., Pilot marks themselves as "On Leave" while assigned).
- Immediately trigger a search for valid replacements who are:
  - Available during the conflict window.
  - Have matching skills/certs.
  - Preferably in the same location.
- Present these options to the coordinator for one-click reassignment.

## Future Improvements
- **Real-time Weather**: Integrate weather APIs to check if drone operations are possible.
- **Route Optimization**: Use map APIs to calculate actual travel time for pilots/drones between locations.
- **Push Notifications**: Integate with Slack/Email to notify pilots of assignments.
