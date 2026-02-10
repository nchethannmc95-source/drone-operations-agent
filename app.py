import streamlit as st
import pandas as pd
from agent import DroneAgent
from managers import RosterManager, FleetManager
from assignment_manager import AssignmentManager
from data_manager import DataManager, GoogleSheetDataManager
import os

# Initialize Agent
if 'agent' not in st.session_state:
    # Check if credentials exist for Google Sheets, otherwise use local CSV
    if os.path.exists("credentials.json"):
        st.session_state.dm = GoogleSheetDataManager()
        st.sidebar.success("Connected to Google Sheets")
    else:
        st.session_state.dm = DataManager()
        st.sidebar.warning("Using Local Mock Data (CSV)")
        
    st.session_state.agent = DroneAgent(st.session_state.dm)

st.set_page_config(page_title="Skylark Drone Ops", layout="wide")

st.title("🚁 Skylark Drone Operations Coordinator")

# Sidebar
st.sidebar.header("Quick Stats")
roster = st.session_state.agent.roster
fleet = st.session_state.agent.fleet
assignments = st.session_state.agent.assignments

active_pilots = len(roster.find_pilots(status="Assigned"))
available_pilots = len(roster.find_pilots(status="Available"))
active_drones = len(fleet.find_drones(status="Assigned"))
available_drones = len(fleet.find_drones(status="Available"))

st.sidebar.metric("Active Pilots", active_pilots)
st.sidebar.metric("Available Pilots", available_pilots)
st.sidebar.metric("Active Drones", active_drones)
st.sidebar.metric("Available Drones", available_drones)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 Coordinator Agent", "👤 Pilot Roster", "🛸 Drone Fleet", "⚠️ Conflict Check"])

with tab1:
    st.header("AI Assistant")
    st.info("Ask me to 'List pilots', 'List drones', 'Assign pilot P001 to PRJ001', etc.")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What do you need help with?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.agent.process_query(prompt)
        
        # Determine if response is a DataFrame or String
        with st.chat_message("assistant"):
            if isinstance(response, pd.DataFrame):
                st.dataframe(response)
                st.session_state.messages.append({"role": "assistant", "content": response.to_markdown()})
            else:
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

with tab2:
    st.header("Pilot Roster")
    st.dataframe(roster.get_all_pilots())
    
    st.subheader("Update Pilot Status")
    with st.form("pilot_status_form"):
        p_id = st.text_input("Pilot ID")
        p_status = st.selectbox("New Status", ["Available", "Assigned", "On Leave", "Unavailable"])
        if st.form_submit_button("Update Status"):
            if roster.update_status(p_id, p_status):
                st.success(f"Updated {p_id} to {p_status}")
                st.rerun()
            else:
                st.error("Pilot ID not found.")

with tab3:
    st.header("Drone Fleet")
    st.dataframe(fleet.get_all_drones())
    
    st.subheader("Update Drone Status")
    with st.form("drone_status_form"):
        d_id = st.text_input("Drone ID")
        d_status = st.selectbox("New Status", ["Available", "Assigned", "Maintenance", "In Transit"])
        if st.form_submit_button("Update Status"):
            if fleet.update_status(d_id, d_status):
                st.success(f"Updated {d_id} to {d_status}")
                st.rerun()
            else:
                st.error("Drone ID not found.")

with tab4:
    st.header("Conflict Detection & Resolution")
    st.write("Check for conflicts in current assignments.")
    # In a real app, this would loop through all active assignments. 
    # For now, let's provide a tool to check a specific hypothetical assignment.
    
    c1, c2, c3 = st.columns(3)
    check_pid = c1.text_input("Pilot ID (e.g. P001)")
    check_did = c2.text_input("Drone ID (e.g. D001)")
    check_prjid = c3.text_input("Project ID (e.g. PRJ001)")
    
    if st.button("Check Conflicts"):
        conflicts = assignments.conflict_detector.check_assignment_conflicts(check_pid if check_pid else None, 
                                                                           check_did if check_did else None, 
                                                                           check_prjid)
        if conflicts:
            st.error("Conflicts Detected:")
            for c in conflicts:
                st.write(f"- {c}")
        else:
            st.success("No conflicts detected for this combination.")

