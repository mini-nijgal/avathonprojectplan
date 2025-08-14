import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import networkx as nx
from typing import Dict, List
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Comprehensive Project Management Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
COMPLEXITY_HOURS = {
    "Simple": 16,
    "Medium": 40,
    "Complex": 80
}

STATUS_COLORS = {
    "Completed": "#00FF00",      # Green
    "In Progress": "#FFFF00",    # Yellow
    "Yet to Start": "#0000FF",   # Blue
    "Delayed": "#FF0000"        # Red
}

# User authentication
USERS = {
    "admin": "admin123",
    "pm": "pm456",
    "user": "user789"
}

# File paths
TEMPLATE_FILE = "Project-Delivery-Plan test.xlsx"
PROJECTS_DATA_FILE = "projects_data.json"

def login_page():
    """Handle user authentication"""
    st.title("🔐 Project Management Login")
    st.markdown("---")
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username in USERS and USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    # Show available users for demo
    st.markdown("---")
    st.markdown("**Demo Accounts:**")
    for user, pwd in USERS.items():
        st.code(f"Username: {user} | Password: {pwd}")

def load_demo_data() -> pd.DataFrame:
    """Load initial demo project plan data with full features"""
    
    # Sample project data with realistic tasks
    demo_data = [
        # Discovery Phase
        {
            "Task ID": "D001", "Task Name": "Site Assessment & Requirements Gathering", 
            "Phase": "Discovery", "Site": "Site 1", "Status": "Completed",
            "Owner": "Business Analyst", "Planned Start": "2025-01-15", "Planned Finish": "2025-01-22",
            "Actual Start": "2025-01-15", "Actual Finish": "2025-01-20", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": ""
        },
        {
            "Task ID": "D002", "Task Name": "Technical Architecture Design", 
            "Phase": "Discovery", "Site": "Site 1", "Status": "Completed",
            "Owner": "Solution Architect", "Planned Start": "2025-01-23", "Planned Finish": "2025-01-30",
            "Actual Start": "2025-01-23", "Actual Finish": "2025-01-28", "Complexity": "Complex",
            "Effort Hours": 80, "Duration Days": 10, "Dependencies": "D001"
        },
        {
            "Task ID": "D003", "Task Name": "Stakeholder Approval & Sign-off", 
            "Phase": "Discovery", "Site": "Site 1", "Status": "Completed",
            "Owner": "Project Manager", "Planned Start": "2025-01-31", "Planned Finish": "2025-02-05",
            "Actual Start": "2025-01-31", "Actual Finish": "2025-02-03", "Complexity": "Simple",
            "Effort Hours": 16, "Duration Days": 2, "Dependencies": "D002"
        },
        
        # Procurement Phase
        {
            "Task ID": "P001", "Task Name": "Hardware Procurement", 
            "Phase": "Procurement", "Site": "Site 1", "Status": "In Progress",
            "Owner": "Procurement Team", "Planned Start": "2025-02-06", "Planned Finish": "2025-02-20",
            "Actual Start": "2025-02-06", "Actual Finish": "", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": "D003"
        },
        {
            "Task ID": "P002", "Task Name": "Software License Acquisition", 
            "Phase": "Procurement", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "IT Admin", "Planned Start": "2025-02-21", "Planned Finish": "2025-02-28",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Simple",
            "Effort Hours": 16, "Duration Days": 2, "Dependencies": "D003"
        },
        
        # Testing & Model Training Phase
        {
            "Task ID": "T001", "Task Name": "Data Model Training - Simple Use Case", 
            "Phase": "Testing & Model Training", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "Data Scientist", "Planned Start": "2025-03-01", "Planned Finish": "2025-03-02",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Simple",
            "Effort Hours": 16, "Duration Days": 2, "Dependencies": "P001,P002"
        },
        {
            "Task ID": "T002", "Task Name": "Model Validation & Testing - Complex Use Case", 
            "Phase": "Testing & Model Training", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "ML Engineer", "Planned Start": "2025-03-03", "Planned Finish": "2025-03-12",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Complex",
            "Effort Hours": 80, "Duration Days": 10, "Dependencies": "T001"
        },
        {
            "Task ID": "T003", "Task Name": "Performance Testing & Optimization", 
            "Phase": "Testing & Model Training", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "QA Engineer", "Planned Start": "2025-03-13", "Planned Finish": "2025-03-20",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": "T002"
        },
        
        # Deployment Phase
        {
            "Task ID": "DEP001", "Task Name": "Production Environment Setup", 
            "Phase": "Deployment", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "DevOps Engineer", "Planned Start": "2025-03-21", "Planned Finish": "2025-03-28",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": "T003"
        },
        {
            "Task ID": "DEP002", "Task Name": "System Integration & Testing", 
            "Phase": "Deployment", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "Integration Team", "Planned Start": "2025-03-29", "Planned Finish": "2025-04-05",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Complex",
            "Effort Hours": 80, "Duration Days": 10, "Dependencies": "DEP001"
        },
        
        # Training Phase
        {
            "Task ID": "TR001", "Task Name": "End User Training", 
            "Phase": "Training", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "Training Team", "Planned Start": "2025-04-06", "Planned Finish": "2025-04-10",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": "DEP002"
        },
        {
            "Task ID": "TR002", "Task Name": "Go-Live Support", 
            "Phase": "Training", "Site": "Site 1", "Status": "Yet to Start",
            "Owner": "Support Team", "Planned Start": "2025-04-11", "Planned Finish": "2025-04-18",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": "TR001"
        },
        
        # Site 2 Tasks (similar structure, different dates)
        {
            "Task ID": "D004", "Task Name": "Site Assessment & Requirements Gathering", 
            "Phase": "Discovery", "Site": "Site 2", "Status": "Yet to Start",
            "Owner": "Business Analyst", "Planned Start": "2025-02-15", "Planned Finish": "2025-02-22",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Medium",
            "Effort Hours": 40, "Duration Days": 5, "Dependencies": ""
        },
        {
            "Task ID": "D005", "Task Name": "Technical Architecture Design", 
            "Phase": "Discovery", "Site": "Site 2", "Status": "Yet to Start",
            "Owner": "Solution Architect", "Planned Start": "2025-02-23", "Planned Finish": "2025-03-02",
            "Actual Start": "", "Actual Finish": "", "Complexity": "Complex",
            "Effort Hours": 80, "Duration Days": 10, "Dependencies": "D004"
        }
    ]
    
    # Convert to DataFrame
    df = pd.DataFrame(demo_data)
    
    # Convert date columns to datetime
    date_columns = ['Planned Start', 'Planned Finish', 'Actual Start', 'Actual Finish']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

def load_template():
    """Load the Excel template with TASK, OWNER, COMMENT, REF LINK data"""
    try:
        # Read the Excel file
        df = pd.read_excel(TEMPLATE_FILE, sheet_name='Project Plan - First Site', header=None)
        
        # Extract the required columns based on the structure we found
        template_data = []
        
        for idx, row in df.iterrows():
            # Column 3: Task names, Column 5: Owner, Column 7: Ref Document, Column 8: Comment
            task = str(row.iloc[3]) if pd.notna(row.iloc[3]) else ""
            owner = str(row.iloc[5]) if pd.notna(row.iloc[5]) else ""
            ref_link = str(row.iloc[7]) if pd.notna(row.iloc[7]) else ""
            comment = str(row.iloc[8]) if pd.notna(row.iloc[8]) else ""
            
            # Only add rows that have actual task data
            if task.strip() and task.lower() not in ['task', 'nan', 'none', '']:
                template_data.append({
                    "TASK": task,
                    "OWNER": owner,
                    "COMMENT": comment,
                    "REF LINK": ref_link
                })
        
        return pd.DataFrame(template_data)
    
    except Exception as e:
        st.error(f"Error loading template: {str(e)}")
        # Return sample data if template fails to load
        return pd.DataFrame([
            {"TASK": "Sample Task 1", "OWNER": "Program Manager", "COMMENT": "Sample comment", "REF LINK": "sample.pdf"},
            {"TASK": "Sample Task 2", "OWNER": "FE-DevOps", "COMMENT": "Another comment", "REF LINK": "sample2.pdf"}
        ])

def load_projects():
    """Load existing projects from JSON file"""
    if os.path.exists(PROJECTS_DATA_FILE):
        try:
            with open(PROJECTS_DATA_FILE, 'r') as f:
                data = json.load(f)
                # Convert back to DataFrames
                projects = {}
                for project_name, project_data in data.items():
                    projects[project_name] = pd.DataFrame(project_data)
                return projects
        except Exception as e:
            st.warning(f"Error loading projects: {str(e)}")
            return {}
    return {}

def save_projects(projects):
    """Save projects to JSON file"""
    try:
        # Convert DataFrames to dictionaries for JSON serialization
        data_to_save = {}
        for project_name, project_df in projects.items():
            data_to_save[project_name] = project_df.to_dict('records')
        
        with open(PROJECTS_DATA_FILE, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving projects: {str(e)}")
        return False

def create_project(name, template_df):
    """Create a new project from template"""
    if name in st.session_state.projects:
        return False, "Project name already exists"
    
    # Create a copy of the template
    new_project = template_df.copy()
    st.session_state.projects[name] = new_project
    
    # Save to file
    if save_projects(st.session_state.projects):
        return True, f"Project '{name}' created successfully"
    else:
        return False, "Error saving project"

def delete_project(name):
    """Delete a project"""
    if name in st.session_state.projects:
        del st.session_state.projects[name]
        if save_projects(st.session_state.projects):
            return True, f"Project '{name}' deleted successfully"
        else:
            return False, "Error saving changes"
    return False, "Project not found"

def calculate_testing_timeline(df: pd.DataFrame, complexity_map: Dict[str, int]) -> pd.DataFrame:
    """Calculate timeline for Testing & Model Training tasks based on complexity"""
    df_copy = df.copy()
    
    # Find Testing & Model Training tasks
    testing_tasks = df_copy[df_copy['Phase'] == 'Testing & Model Training']
    
    for idx, task in testing_tasks.iterrows():
        # Get complexity and calculate effort hours
        complexity = task.get('Complexity', 'Medium')
        effort_hours = complexity_map.get(complexity, 40)
        
        # Calculate duration (8 hours per day)
        duration_days = max(1, int(np.ceil(effort_hours / 8)))
        
        # Update effort hours and duration
        df_copy.loc[idx, 'Effort Hours'] = effort_hours
        df_copy.loc[idx, 'Duration Days'] = duration_days
        
        # Calculate dates based on dependencies
        if pd.notna(task.get('Planned Start')) and pd.notna(task.get('Planned Finish')):
            # Dates already set, skip
            continue
        
        # Find dependency completion date
        dependency_date = find_dependency_completion_date(df_copy, task)
        
        if dependency_date:
            start_date = dependency_date + timedelta(days=1)
            finish_date = start_date + timedelta(days=duration_days - 1)
            
            df_copy.loc[idx, 'Planned Start'] = start_date
            df_copy.loc[idx, 'Planned Finish'] = finish_date
    
    return df_copy

def find_dependency_completion_date(df: pd.DataFrame, task: pd.Series):
    """Find the latest completion date of task dependencies"""
    dependencies = task.get('Dependencies', '')
    if not dependencies:
        return None
    
    # Split dependencies by comma
    dep_ids = [dep.strip() for dep in dependencies.split(',') if dep.strip()]
    
    if not dep_ids:
        return None
    
    # Find all dependency tasks
    dep_tasks = df[df['Task ID'].isin(dep_ids)]
    
    if dep_tasks.empty:
        return None
    
    # Return the latest finish date
    return dep_tasks['Planned Finish'].max()

def apply_dependency_chaining(df: pd.DataFrame) -> pd.DataFrame:
    """Recalculate dependent tasks in correct order using topological sorting"""
    df_copy = df.copy()
    
    # Create dependency graph
    G = nx.DiGraph()
    
    # Add nodes
    for _, task in df_copy.iterrows():
        G.add_node(task['Task ID'])
    
    # Add edges
    for _, task in df_copy.iterrows():
        dependencies = task.get('Dependencies', '')
        if dependencies:
            dep_ids = [dep.strip() for dep in dependencies.split(',') if dep.strip()]
            for dep_id in dep_ids:
                if dep_id in G.nodes:
                    G.add_edge(dep_id, task['Task ID'])
    
    # Check for circular dependencies
    try:
        # Get topological order
        topo_order = list(nx.topological_sort(G))
    except nx.NetworkXError:
        st.error("⚠️ Circular dependencies detected! Please fix your task dependencies.")
        return df_copy
    
    # Process tasks in topological order
    for task_id in topo_order:
        task_idx = df_copy[df_copy['Task ID'] == task_id].index[0]
        task = df_copy.loc[task_idx]
        
        # Skip if no dependencies
        if not task.get('Dependencies'):
            continue
        
        # Find dependency completion date
        dependency_date = find_dependency_completion_date(df_copy, task)
        
        if dependency_date:
            # Calculate new start date
            new_start = dependency_date + timedelta(days=1)
            
            # Calculate duration
            if task['Phase'] == 'Testing & Model Training':
                complexity = task.get('Complexity', 'Medium')
                effort_hours = COMPLEXITY_HOURS.get(complexity, 40)
                duration_days = max(1, int(np.ceil(effort_hours / 8)))
            else:
                # For non-testing tasks, calculate duration from existing dates or default
                if pd.notna(task['Planned Start']) and pd.notna(task['Planned Finish']):
                    duration_days = (task['Planned Finish'] - task['Planned Start']).days + 1
                else:
                    duration_days = 1
            
            # Update dates
            df_copy.loc[task_idx, 'Planned Start'] = new_start
            df_copy.loc[task_idx, 'Planned Finish'] = new_start + timedelta(days=duration_days - 1)
    
    return df_copy

def apply_filters(df: pd.DataFrame, site_filter: str, phase_filter: str, status_filter: str) -> pd.DataFrame:
    """Apply filters to the dataframe"""
    filtered_df = df.copy()
    
    if site_filter and site_filter != "All Sites":
        filtered_df = filtered_df[filtered_df['Site'] == site_filter]
    
    if phase_filter and phase_filter != "All Phases":
        filtered_df = filtered_df[filtered_df['Phase'] == phase_filter]
    
    if status_filter and status_filter != "All Statuses":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    
    return filtered_df

def generate_gantt(df: pd.DataFrame):
    """Generate Gantt chart using Plotly"""
    if df.empty:
        return None
    
    # Prepare data for Gantt chart
    gantt_data = []
    
    for _, task in df.iterrows():
        if pd.notna(task.get('Planned Start')) and pd.notna(task.get('Planned Finish')):
            start = task['Planned Start']
            finish = task['Planned Finish']
            
            # Determine status color
            status = task['Status']
            if status == 'Completed':
                color = STATUS_COLORS['Completed']
            elif status == 'In Progress':
                color = STATUS_COLORS['In Progress']
            elif status == 'Yet to Start':
                # Check if delayed
                if finish < datetime.now():
                    color = STATUS_COLORS['Delayed']
                else:
                    color = STATUS_COLORS['Yet to Start']
            else:
                color = STATUS_COLORS['Yet to Start']
            
            gantt_data.append(dict(
                Task=f"{task['Task ID']}: {task['Task Name']}",
                Start=start,
                Finish=finish,
                Resource=task.get('Owner', 'Unknown'),
                Status=status,
                Phase=task.get('Phase', 'Unknown'),
                Color=color
            ))
    
    if not gantt_data:
        return None
    
    # Create Gantt chart - remove index_col to show all tasks
    fig = ff.create_gantt(
        gantt_data,
        colors=[task['Color'] for task in gantt_data],
        show_colorbar=True,
        group_tasks=False,  # Don't group by status
        title='Project Timeline - Gantt Chart'
    )
    
    fig.update_layout(
        title_x=0.5,
        height=600,
        xaxis_title='Timeline',
        yaxis_title='Tasks'
    )
    
    return fig

def update_task(df: pd.DataFrame, task_id: str, field: str, value) -> pd.DataFrame:
    """Update a single task field"""
    df_copy = df.copy()
    
    # Find the task index
    task_mask = df_copy['Task ID'] == task_id
    if not task_mask.any():
        # Task not found, return original dataframe
        return df_copy
    
    task_idx = task_mask.idxmax()
    
    # Update the field
    df_copy.loc[task_idx, field] = value
    
    # If updating complexity for testing tasks, recalculate effort hours
    if field == 'Complexity' and df_copy.loc[task_idx, 'Phase'] == 'Testing & Model Training':
        effort_hours = COMPLEXITY_HOURS.get(value, 40)
        df_copy.loc[task_idx, 'Effort Hours'] = effort_hours
    
    # If updating dates, recalculate dependencies
    if field in ['Planned Start', 'Planned Finish']:
        df_copy = apply_dependency_chaining(df_copy)
    
    return df_copy

def calculate_project_kpis(df: pd.DataFrame) -> Dict[str, any]:
    """Calculate project KPIs"""
    total_tasks = len(df)
    completed_tasks = len(df[df['Status'] == 'Completed'])
    in_progress_tasks = len(df[df['Status'] == 'In Progress'])
    yet_to_start_tasks = len(df[df['Status'] == 'Yet to Start'])
    
    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Calculate delayed tasks
    delayed_tasks = len(df[
        (df['Status'] != 'Completed') & 
        (df['Planned Finish'] < datetime.now())
    ])
    
    # Calculate total effort hours
    total_hours = df['Effort Hours'].sum()
    
    # Calculate active phases
    active_phases = df['Phase'].nunique()
    
    return {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'yet_to_start_tasks': yet_to_start_tasks,
        'completion_rate': completion_rate,
        'delayed_tasks': delayed_tasks,
        'total_hours': total_hours,
        'active_phases': active_phases
    }

def main_app():
    """Main application after login"""
    st.title("🚀 Comprehensive Project Management Dashboard")
    st.markdown("---")
    
    # Initialize session state for projects
    if 'projects' not in st.session_state:
        st.session_state.projects = load_projects()
    
    # Load template
    template_df = load_template()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Controls")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.username}")
    st.sidebar.markdown("---")
    
    # App mode selector
    app_mode = st.sidebar.selectbox(
        "Select App Mode",
        ["📊 Project Plan Dashboard", "📁 Multi-Project Management"]
    )
    
    if app_mode == "📊 Project Plan Dashboard":
        show_project_plan_dashboard()
    else:
        show_multi_project_management(template_df)

def show_project_plan_dashboard():
    """Show the original project plan dashboard with dependency chaining"""
    st.header("📊 Project Plan Dashboard")
    st.markdown("---")
    
    # Initialize demo data
    if 'project_data' not in st.session_state:
        st.session_state.project_data = load_demo_data()
    
    # Reset button
    if st.button("🔄 Reset to Demo Data", type="primary"):
        st.session_state.project_data = load_demo_data()
        st.rerun()
    
    # Filters
    st.sidebar.header("🔍 Filters")
    
    # Get unique values for filters
    sites = ["All Sites"] + list(st.session_state.project_data['Site'].unique())
    phases = ["All Phases"] + list(st.session_state.project_data['Phase'].unique())
    statuses = ["All Statuses"] + list(st.session_state.project_data['Status'].unique())
    
    site_filter = st.sidebar.selectbox("Site", sites)
    phase_filter = st.sidebar.selectbox("Phase", phases)
    status_filter = st.sidebar.selectbox("Status", statuses)
    
    # Apply filters
    filtered_data = apply_filters(
        st.session_state.project_data, 
        site_filter, 
        phase_filter, 
        status_filter
    )
    
    # Calculate KPIs
    kpis = calculate_project_kpis(filtered_data)
    
    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", kpis['total_tasks'])
        st.metric("Completion Rate", f"{kpis['completion_rate']:.1f}%")
    
    with col2:
        st.metric("Completed", kpis['completed_tasks'])
        st.metric("In Progress", kpis['in_progress_tasks'])
    
    with col3:
        st.metric("Yet to Start", kpis['yet_to_start_tasks'])
        st.metric("Delayed Tasks", kpis['delayed_tasks'])
    
    with col4:
        st.metric("Total Effort Hours", f"{kpis['total_hours']:.0f}")
        st.metric("Active Phases", kpis['active_phases'])
    
    st.markdown("---")
    
    # Testing & Model Training Configuration
    st.header("🧪 Testing & Model Training Configuration")
    
    testing_tasks = filtered_data[filtered_data['Phase'] == 'Testing & Model Training']
    
    if not testing_tasks.empty:
        for idx, task in testing_tasks.iterrows():
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.write(f"**{task['Task Name']}** ({task['Task ID']})")
            
            with col2:
                complexity = st.selectbox(
                    "Complexity",
                    list(COMPLEXITY_HOURS.keys()),
                    key=f"complexity_{task['Task ID']}",
                    index=list(COMPLEXITY_HOURS.keys()).index(task.get('Complexity', 'Medium'))
                )
                
                # Update complexity if changed
                if complexity != task['Complexity']:
                    st.session_state.project_data = update_task(
                        st.session_state.project_data, 
                        task['Task ID'], 
                        'Complexity', 
                        complexity
                    )
                    st.rerun()
            
            with col3:
                effort_hours = COMPLEXITY_HOURS[complexity]
                duration_days = max(1, int(np.ceil(effort_hours / 8)))
                st.write(f"**{effort_hours}h** ({duration_days} days)")
        
        # Recalculate timeline after complexity changes
        st.session_state.project_data = calculate_testing_timeline(
            st.session_state.project_data, 
            COMPLEXITY_HOURS
        )
    
    st.markdown("---")
    
    # Editable Task Table
    st.header("📋 Project Tasks")
    
    # Create editable dataframe
    edited_df = st.data_editor(
        filtered_data[['Task ID', 'Task Name', 'Phase', 'Site', 'Status', 'Owner', 
                      'Planned Start', 'Planned Finish', 'Actual Start', 'Actual Finish',
                      'Complexity', 'Effort Hours', 'Duration Days', 'Dependencies']],
        num_rows="dynamic",
        use_container_width=True,
        key="task_editor"
    )
    
    # Update original dataframe with edits
    for idx, row in edited_df.iterrows():
        if idx < len(filtered_data):
            original_task_id = filtered_data.iloc[idx]['Task ID']
            
            for col in edited_df.columns:
                new_value = row[col]
                original_value = filtered_data.iloc[idx][col]
                
                if new_value != original_value:
                    st.session_state.project_data = update_task(
                        st.session_state.project_data,
                        original_task_id,
                        col,
                        new_value
                    )
    
    st.markdown("---")
    
    # Gantt Chart
    st.header("📊 Project Timeline")
    
    gantt_fig = generate_gantt(filtered_data)
    if gantt_fig:
        st.plotly_chart(gantt_fig, use_container_width=True)
    else:
        st.warning("No valid date data found for Gantt chart generation.")

def show_multi_project_management(template_df):
    """Show the multi-project management interface"""
    st.header("📁 Multi-Project Management")
    st.markdown("---")
    
    # Project management
    st.sidebar.header("📁 Project Management")
    
    # Project selector
    if st.session_state.projects:
        selected_project = st.sidebar.selectbox(
            "Select Project",
            list(st.session_state.projects.keys())
        )
    else:
        selected_project = None
        st.sidebar.info("No projects created yet")
    
    # New project creation
    st.sidebar.markdown("**Create New Project:**")
    new_project_name = st.sidebar.text_input("Project Name", key="new_project_name")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("➕ Create", key="create_btn"):
            if new_project_name.strip():
                success, message = create_project(new_project_name.strip(), template_df)
                if success:
                    st.sidebar.success(message)
                    st.rerun()
                else:
                    st.sidebar.error(message)
            else:
                st.sidebar.error("Please enter a project name")
    
    # Delete project button
    if selected_project:
        with col2:
            if st.button("🗑️ Delete", key="delete_btn"):
                success, message = delete_project(selected_project)
                if success:
                    st.sidebar.success(message)
                    st.rerun()
                else:
                    st.sidebar.error(message)
    
    st.sidebar.markdown("---")
    
    # Main content area
    if not st.session_state.projects:
        st.info("👆 Create your first project using the sidebar controls above")
        st.markdown("---")
        
        # Show template preview
        st.subheader("📋 Template Preview")
        st.markdown("This is the base template that will be used for new projects:")
        st.dataframe(template_df, use_container_width=True)
        
    else:
        # Display selected project
        st.subheader(f"📊 Project: {selected_project}")
        
        # Project actions
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**Total Tasks:** {len(st.session_state.projects[selected_project])}")
        
        with col2:
            if st.button("🔄 Reset to Template", key="reset_btn"):
                st.session_state.projects[selected_project] = template_df.copy()
                if save_projects(st.session_state.projects):
                    st.success("Project reset to template")
                    st.rerun()
                else:
                    st.error("Error saving changes")
        
        with col3:
            if st.button("💾 Save Changes", key="save_btn"):
                if save_projects(st.session_state.projects):
                    st.success("Changes saved successfully")
                else:
                    st.error("Error saving changes")
        
        st.markdown("---")
        
        # Editable project table
        st.subheader("📝 Edit Project Data")
        st.markdown("**Note:** TASK column is read-only. Edit OWNER, COMMENT, and REF LINK columns.")
        
        # Create editable dataframe
        current_project = st.session_state.projects[selected_project]
        
        edited_df = st.data_editor(
            current_project,
            num_rows="dynamic",
            use_container_width=True,
            key=f"editor_{selected_project}",
            column_config={
                "TASK": st.column_config.TextColumn("TASK", disabled=True),
                "OWNER": st.column_config.TextColumn("OWNER"),
                "COMMENT": st.column_config.TextColumn("COMMENT"),
                "REF LINK": st.column_config.TextColumn("REF LINK")
            }
        )
        
        # Update project data if changes detected
        if not edited_df.equals(current_project):
            st.session_state.projects[selected_project] = edited_df
            st.info("💡 Changes detected! Click 'Save Changes' to persist them.")
        
        # Project statistics
        st.markdown("---")
        st.subheader("📈 Project Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_tasks = len(current_project)
            st.metric("Total Tasks", total_tasks)
        
        with col2:
            unique_owners = current_project['OWNER'].nunique()
            st.metric("Unique Owners", unique_owners)
        
        with col3:
            tasks_with_comments = len(current_project[current_project['COMMENT'].str.strip() != ''])
            st.metric("Tasks with Comments", tasks_with_comments)
        
        with col4:
            tasks_with_refs = len(current_project[current_project['REF LINK'].str.strip() != ''])
            st.metric("Tasks with Ref Links", tasks_with_refs)
        
        # Show all projects summary
        st.markdown("---")
        st.subheader("📁 All Projects Overview")
        
        projects_summary = []
        for name, df in st.session_state.projects.items():
            projects_summary.append({
                "Project Name": name,
                "Total Tasks": len(df),
                "Unique Owners": df['OWNER'].nunique(),
                "Last Modified": "Today"  # Could add actual timestamp tracking
            })
        
        summary_df = pd.DataFrame(projects_summary)
        st.dataframe(summary_df, use_container_width=True)

def main():
    """Main function to handle app flow"""
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main() 