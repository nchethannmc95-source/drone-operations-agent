from data_manager import DataManager
from managers import RosterManager, FleetManager
from assignment_manager import AssignmentManager

class DroneAgent:
    def __init__(self, data_manager=None):
        if data_manager:
            self.dm = data_manager
        else:
            self.dm = DataManager()
        
        self.roster = RosterManager(self.dm)
        self.fleet = FleetManager(self.dm)
        self.assignments = AssignmentManager(self.dm)

    def process_query(self, user_query):
        query = user_query.lower()

        if "list pilots" in query or "show pilots" in query:
            return self.roster.get_all_pilots()
        
        if "available pilots" in query:
            return self.roster.find_pilots(status="Available")

        if "list drones" in query or "show drones" in query:
            return self.fleet.get_all_drones()
        
        if "available drones" in query:
            return self.fleet.find_drones(status="Available")
        
        if "assign pilot" in query:
            # Simple parsing: "Assign pilot P001 to PRJ001"
            try:
                parts = user_query.split()
                pilot_id = [p for p in parts if p.startswith('P') and len(p) == 4][0]
                project_id = [p for p in parts if p.startswith('PRJ')][0]
                success, msgs = self.assignments.assign_pilot_to_mission(pilot_id, project_id)
                return "\n".join(msgs)
            except IndexError:
                return "Could not parse pilot ID or Project ID. Use format: 'Assign pilot P001 to PRJ001'."

        if "assign drone" in query:
             try:
                parts = user_query.split()
                drone_id = [d for d in parts if d.startswith('D') and len(d) == 4][0]
                project_id = [p for p in parts if p.startswith('PRJ')][0]
                success, msgs = self.assignments.assign_drone_to_mission(drone_id, project_id)
                return "\n".join(msgs)
             except IndexError:
                return "Could not parse drone ID or Project ID. Use format: 'Assign drone D001 to PRJ001'."

        if "find replacement" in query or "replace" in query:
             # Example: "Find replacement for P001"
             try:
                 parts = query.split()
                 original_id = [p for p in parts if (p.startswith('P') or p.startswith('D')) and len(p) == 4][0]
                 if original_id.startswith('P'):
                     # Logic to find pilot replacement
                     original_pilot = self.roster.get_pilot_details(original_id)
                     if not original_pilot: 
                         return f"Pilot {original_id} not found."
                     
                     # Find matches based on skills and location
                     # Assuming 'skills' is a string of comma-separated values
                     skills_needed = original_pilot['skills']
                     location_needed = original_pilot['location']
                     
                     candidates = self.roster.find_pilots(status="Available", location=location_needed)
                     # Filter by skill (simple containment check for now, can be improved)
                     # In real scenario, we'd parse the skills properly.
                     # For now, let's just return the available pilots in the same location.
                     if candidates.empty:
                         candidates = self.roster.find_pilots(status="Available") # Fallback to any location
                         msg = f"No available pilots in {location_needed}. Found these others:"
                     else:
                         msg = f"Found local candidates in {location_needed}:"
                     
                     return msg + "\n" + candidates.to_markdown()
                 
                 elif original_id.startswith('D'):
                     # Logic for drone replacement
                     original_drone = self.fleet.get_drone_details(original_id)
                     if not original_drone: return f"Drone {original_id} not found."
                     
                     caps_needed = original_drone['capabilities']
                     location_needed = original_drone['location']
                     
                     candidates = self.fleet.find_drones(status="Available", location=location_needed)
                     if candidates.empty:
                         candidates = self.fleet.find_drones(status="Available")
                         msg = f"No available drones in {location_needed}. Found these others:"
                     else:
                         msg = f"Found local candidates in {location_needed}:"
                     
                     return msg + "\n" + candidates.to_markdown()

             except IndexError:
                 return "Could not parse ID. Use format: 'Find replacement for P001'."

        return "I'm sorry, I didn't understand that. I can list pilots, drones, assign them, or find replacements."
