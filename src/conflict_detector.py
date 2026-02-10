from datetime import datetime

class ConflictDetector:
    def __init__(self, data_manager):
        self.dm = data_manager

    def check_assignment_conflicts(self, pilot_id, drone_id, project_id):
        conflicts = []
        pilot = self.dm.get_pilot_by_id(pilot_id).iloc[0] if not self.dm.get_pilot_by_id(pilot_id).empty else None
        drone = self.dm.drones[self.dm.drones['drone_id'] == drone_id].iloc[0] if not self.dm.drones[self.dm.drones['drone_id'] == drone_id].empty else None
        project = self.dm.missions[self.dm.missions['project_id'] == project_id].iloc[0] if not self.dm.missions[self.dm.missions['project_id'] == project_id].empty else None

        if not pilot is None and not project is None:
            # 1. Check Pilot Availability (Status)
            if pilot['status'] != 'Available':
                 conflicts.append(f"Pilot {pilot['name']} is currently {pilot['status']}.")

            # 2. Check Pilot Skills
            req_skills = [s.strip() for s in str(project['required_skills']).split(',')]
            pilot_skills = str(pilot['skills'])
            missing_skills = [s for s in req_skills if s not in pilot_skills]
            if missing_skills:
                conflicts.append(f"Pilot {pilot['name']} lacks required skills: {', '.join(missing_skills)}.")

            # 3. Check Pilot Location
            if pilot['location'] != project['location']:
                conflicts.append(f"Pilot {pilot['name']} is in {pilot['location']}, but project is in {project['location']}.")

        if not drone is None and not project is None:
            # 4. Check Drone Availability
            if drone['status'] != 'Available':
                conflicts.append(f"Drone {drone['model']} is currently {drone['status']}.")
            
            # 5. Check Drone Maintenance
            # Assuming simple logic: if maintenance_due is before project end date
            maintenance_due = datetime.strptime(str(drone['maintenance_due']), '%Y-%m-%d')
            project_end = datetime.strptime(str(project['end_date']), '%Y-%m-%d')
            
            if maintenance_due < project_end:
                 conflicts.append(f"Drone {drone['model']} requires maintenance by {drone['maintenance_due']}.")

        return conflicts
