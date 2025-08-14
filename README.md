# 🚀 Comprehensive Project Management Dashboard

A **Streamlit web app** that combines **two powerful features** in one application:

1. **📊 Project Plan Dashboard**: Advanced project planning with dependency chaining, complexity-driven scheduling, and interactive Gantt charts
2. **📁 Multi-Project Management**: Secure multi-project management with Excel template loading, user authentication, and persistent data storage

## ✨ Combined Features

### **🔐 User Authentication**
- Secure login with username/password
- Multiple user accounts supported
- Session management and security

### **📊 Project Plan Dashboard**
- **Complexity-driven scheduling** for Testing & Model Training tasks
- **Automatic dependency chaining** with topological sorting
- **Interactive Gantt charts** with Plotly
- **Real-time KPI metrics** and project statistics
- **Editable task tables** with immediate updates
- **Smart filtering** by site, phase, and status

### **📁 Multi-Project Management**
- **Excel template loading** (TASK, OWNER, COMMENT, REF LINK)
- **Multiple project creation** from your template
- **Persistent data storage** between sessions
- **Project switching** and management
- **Template reset** capabilities

## 🛠️ Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

1. **Run the app**:
   ```bash
   streamlit run app.py
   ```

2. **Login**: Use one of the demo accounts shown on the login page
3. **Choose Mode**: Select between "Project Plan Dashboard" or "Multi-Project Management"
4. **Use Features**: Access all capabilities based on your selected mode

## 🔐 Demo Accounts

The app comes with pre-configured demo accounts:
- **Username**: `admin` | **Password**: `admin123`
- **Username**: `pm` | **Password**: `pm456`
- **Username**: `user` | **Password**: `user789`

## 🎯 Two App Modes

### **Mode 1: 📊 Project Plan Dashboard**
**Advanced project planning with full features:**
- **Complexity Mapping**: Simple (16h), Medium (40h), Complex (80h)
- **Dependency Chaining**: Automatic task rescheduling
- **Gantt Visualization**: Interactive timeline charts
- **Real-time Updates**: Immediate reflection of changes
- **KPI Metrics**: Completion rates, effort hours, delays

**Perfect for:**
- Complex project planning
- Dependency management
- Timeline visualization
- Resource allocation

### **Mode 2: 📁 Multi-Project Management**
**Template-based project management:**
- **Excel Template**: Load your existing project structure
- **Multiple Projects**: Create unlimited projects from template
- **Data Persistence**: Save and load project data
- **Inline Editing**: Modify OWNER, COMMENT, REF LINK fields
- **Project Statistics**: Overview of all projects

**Perfect for:**
- Managing multiple similar projects
- Using existing Excel templates
- Team collaboration
- Data persistence

## 📊 Data Structure

### **Project Plan Dashboard:**
- **Task ID**: Unique identifier
- **Task Name**: Descriptive name
- **Phase**: Discovery, Procurement, Testing, Deployment, Training
- **Site**: Site 1, Site 2, etc.
- **Status**: Yet to Start, In Progress, Completed
- **Owner**: Person responsible
- **Planned/Actual Dates**: Start and finish dates
- **Complexity**: Simple, Medium, Complex
- **Effort Hours**: Calculated based on complexity
- **Dependencies**: Comma-separated Task IDs

### **Multi-Project Management:**
- **TASK**: Task names (read-only, preserved from template)
- **OWNER**: Person responsible (editable)
- **COMMENT**: Task comments and notes (editable)
- **REF LINK**: Reference documents and links (editable)

## 🔧 Core Functions

### **Authentication & Security:**
- `login_page()`: User authentication
- Session state management

### **Project Plan Dashboard:**
- `load_demo_data()`: Sample project data
- `calculate_testing_timeline()`: Complexity-based scheduling
- `apply_dependency_chaining()`: Dependency management
- `generate_gantt()`: Interactive charts
- `update_task()`: Task modifications

### **Multi-Project Management:**
- `load_template()`: Excel template loading
- `create_project()`: New project creation
- `save_projects()`: Data persistence
- `delete_project()`: Project removal

## 🎨 User Interface

### **Sidebar Controls:**
- **App Mode Selector**: Switch between dashboard modes
- **Filters**: Site, Phase, Status (Project Plan mode)
- **Project Management**: Create, select, delete projects
- **Logout**: Secure session termination

### **Main Dashboard:**
- **Mode-specific content** based on selection
- **Real-time updates** and data validation
- **Professional styling** with emojis and modern layout

## 💾 Data Persistence

- **Project Plan**: Session-based with reset capabilities
- **Multi-Project**: JSON-based persistent storage
- **Template Preservation**: Original Excel data never modified
- **Automatic Saving**: Changes saved when requested

## 🔄 Workflow Examples

### **Project Planning Workflow:**
1. Login with credentials
2. Select "Project Plan Dashboard" mode
3. Configure Testing & Model Training complexity
4. Edit task dependencies and dates
5. View automatic timeline updates in Gantt chart
6. Monitor KPIs and project progress

### **Multi-Project Workflow:**
1. Login with credentials
2. Select "Multi-Project Management" mode
3. Create new project from Excel template
4. Edit project data inline
5. Save changes for persistence
6. Switch between multiple projects

## 🚨 Security Features

- **User Authentication**: Required before accessing any data
- **Session Management**: Secure session state handling
- **Data Isolation**: Users can only access authorized projects
- **No Credential Storage**: Passwords not stored in plain text

## 🆘 Troubleshooting

### **Common Issues:**
1. **Template Loading**: Ensure Excel file is in the same directory
2. **Authentication**: Use exact demo credentials
3. **Data Saving**: Check write permissions and disk space
4. **Dependencies**: Avoid circular dependencies in project planning

### **Performance Tips:**
1. **Large Projects**: Use filters to focus on specific areas
2. **Complex Dependencies**: Start with simple dependency chains
3. **Multiple Projects**: Limit the number of active projects

## 🔮 Future Enhancements

- **User Roles**: Different permission levels
- **Project Sharing**: Share projects between users
- **Data Export**: Export to Excel, PDF, or other formats
- **Advanced Analytics**: Resource allocation, critical path analysis
- **Team Collaboration**: Multi-user editing with conflict resolution
- **API Integration**: Connect with external project management systems

## 📄 Technical Details

- **Framework**: Streamlit
- **Data Management**: Pandas DataFrames with session state and JSON persistence
- **Dependencies**: NetworkX for graph operations, Plotly for visualization
- **Architecture**: Modular functions with clear separation of concerns
- **File Support**: Excel template loading, JSON data persistence

## 📄 License

This project is open source and available under the MIT License.

---

**The Ultimate Project Management Solution! 🚀**

*Get the best of both worlds: advanced project planning AND multi-project management in one powerful app.* 