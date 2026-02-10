import pandas as pd
import os

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.pilots_path = os.path.join(data_dir, "pilot_roster.csv")
        self.drones_path = os.path.join(data_dir, "drone_fleet.csv")
        self.missions_path = os.path.join(data_dir, "missions.csv")
        
        self.pilots = self._load_data(self.pilots_path)
        self.drones = self._load_data(self.drones_path)
        self.missions = self._load_data(self.missions_path)

    def _load_data(self, path):
        if os.path.exists(path):
            return pd.read_csv(path)
        return pd.DataFrame()

    def save_pilots(self):
        self.pilots.to_csv(self.pilots_path, index=False)

    def save_drones(self):
        self.drones.to_csv(self.drones_path, index=False)

    def save_missions(self):
        self.missions.to_csv(self.missions_path, index=False)
        
    def get_pilot_by_id(self, pilot_id):
        return self.pilots[self.pilots['pilot_id'] == pilot_id]

    def update_pilot_status(self, pilot_id, new_status):
        if pilot_id in self.pilots['pilot_id'].values:
            self.pilots.loc[self.pilots['pilot_id'] == pilot_id, 'status'] = new_status
            self.save_pilots()
            return True
        return False

    def update_drone_status(self, drone_id, new_status):
        if drone_id in self.drones['drone_id'].values:
            self.drones.loc[self.drones['drone_id'] == drone_id, 'status'] = new_status
            self.save_drones()
            return True
        return False

import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetDataManager(DataManager):
    def __init__(self, credentials_path="credentials.json", sheet_name="DroneOperationsData"):
        # Define scope
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        try:
            # Authenticate
            creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
            self.client = gspread.authorize(creds)
            
            # Open Sheet
            self.sheet = self.client.open(sheet_name)
            self.pilots_worksheet = self.sheet.worksheet("Pilot Roster")
            self.drones_worksheet = self.sheet.worksheet("Drone Fleet")
            self.missions_worksheet = self.sheet.worksheet("Missions")
            
            # Load Data into Pandas
            self.pilots = pd.DataFrame(self.pilots_worksheet.get_all_records())
            self.drones = pd.DataFrame(self.drones_worksheet.get_all_records())
            self.missions = pd.DataFrame(self.missions_worksheet.get_all_records())
            
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            # Fallback to local CSV if connection fails
            super().__init__()

    def save_pilots(self):
        # Update Google Sheet
        try:
            self.pilots_worksheet.update([self.pilots.columns.values.tolist()] + self.pilots.values.tolist())
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")

    def save_drones(self):
        try:
            self.drones_worksheet.update([self.drones.columns.values.tolist()] + self.drones.values.tolist())
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")

    def save_missions(self):
        try:
            self.missions_worksheet.update([self.missions.columns.values.tolist()] + self.missions.values.tolist())
        except Exception as e:
            print(f"Error saving to Google Sheets: {e}")
