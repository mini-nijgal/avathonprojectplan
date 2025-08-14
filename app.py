import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Multi-Project Management Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def main_app():
    """Main application after login"""
    st.title("🚀 Multi-Project Management Dashboard")
    st.markdown("---")
    
    # Initialize session state for projects
    if 'projects' not in st.session_state:
        st.session_state.projects = load_projects()
    
    # Load template
    template_df = load_template()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Project Controls")
    
    # Logout button
    if st.sidebar.button("🚪 Logout", type="primary"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.username}")
    st.sidebar.markdown("---")
    
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
        st.header("📋 Template Preview")
        st.markdown("This is the base template that will be used for new projects:")
        st.dataframe(template_df, use_container_width=True)
        
    else:
        # Display selected project
        st.header(f"📊 Project: {selected_project}")
        
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