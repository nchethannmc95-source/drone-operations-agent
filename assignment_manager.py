from datetime import datetime
from conflict_detector import ConflictDetector

class AssignmentManager:
    def __init__(self, data_manager):
        self.dm = data_manager
        self.conflict_detector = ConflictDetector(data_manager)

    def assign_pilot_to_mission(self, pilot_id, project_id):
        # Check for conflicts
        conflicts = self.conflict_detector.check_assignment_conflicts(pilot_id, None, project_id)
        if conflicts:
            return False, conflicts
        
        # Assign
        # Update pilot status and assignment
        self.dm.update_pilot_status(pilot_id, "Assigned")
        self.dm.pilots.loc[self.dm.pilots['pilot_id'] == pilot_id, 'current_assignment'] = project_id
        self.dm.save_pilots()
        return True, ["Successfully assigned pilot."]

    def assign_drone_to_mission(self, drone_id, project_id):
        conflicts = self.conflict_detector.check_assignment_conflicts(None, drone_id, project_id)
        if conflicts:
            return False, conflicts
        
        self.dm.update_drone_status(drone_id, "Assigned")
        self.dm.drones.loc[self.dm.drones['drone_id'] == drone_id, 'current_assignment'] = project_id
        self.dm.save_drones()
        return True, ["Successfully assigned drone."]

    def get_mission_details(self, project_id):
        mission = self.dm.missions[self.dm.missions['project_id'] == project_id]
        if not mission.empty:
            return mission.iloc[0].to_dict()
        return None
