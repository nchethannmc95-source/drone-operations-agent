import pandas as pd
from datetime import datetime

class RosterManager:
    def __init__(self, data_manager):
        self.dm = data_manager

    def get_all_pilots(self):
        return self.dm.pilots

    def get_pilot_details(self, pilot_id):
        pilot = self.dm.get_pilot_by_id(pilot_id)
        if not pilot.empty:
            return pilot.iloc[0].to_dict()
        return None

    def find_pilots(self, skill=None, location=None, status="Available"):
        df = self.dm.pilots
        if status:
            df = df[df['status'].str.lower() == status.lower()]
        if location:
            df = df[df['location'].str.contains(location, case=False, na=False)]
        if skill:
            df = df[df['skills'].str.contains(skill, case=False, na=False)]
        return df

    def update_status(self, pilot_id, new_status):
        return self.dm.update_pilot_status(pilot_id, new_status)

class FleetManager:
    def __init__(self, data_manager):
        self.dm = data_manager

    def get_all_drones(self):
        return self.dm.drones

    def get_drone_details(self, drone_id):
        drone = self.dm.drones[self.dm.drones['drone_id'] == drone_id]
        if not drone.empty:
            return drone.iloc[0].to_dict()
        return None

    def find_drones(self, capability=None, location=None, status="Available"):
        df = self.dm.drones
        if status:
            df = df[df['status'].str.lower() == status.lower()]
        if location:
            df = df[df['location'].str.contains(location, case=False, na=False)]
        if capability:
            df = df[df['capabilities'].str.contains(capability, case=False, na=False)]
        return df

    def update_status(self, drone_id, new_status):
        return self.dm.update_drone_status(drone_id, new_status)
