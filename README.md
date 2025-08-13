# 🚀 Project Delivery Plan Dashboard

A **self-contained Streamlit web app** that displays and manages a project delivery plan entirely inside the app itself. No Excel upload/download needed - all data is stored in-memory with automatic dependency chaining and complexity-driven scheduling.

## ✨ Features

- **📊 In-Memory Data Management**: All project data stored in Python DataFrames
- **🧪 Complexity-Driven Scheduling**: Automatic effort calculation for Testing & Model Training tasks
- **🔗 Automatic Dependency Chaining**: Tasks automatically shift when dependencies change
- **📈 Interactive Gantt Charts**: Real-time visualization with Plotly
- **✏️ Editable Task Table**: Modify any field with immediate updates
- **🎛️ Smart Filtering**: Filter by site, phase, and status
- **📱 Responsive Dashboard**: Professional UI with real-time KPIs

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

2. **Default behavior**: The app loads with pre-filled demo data for multiple sites and phases
3. **Edit tasks**: Modify any field in the table for real-time updates
4. **Configure complexity**: Set complexity levels for Testing & Model Training tasks
5. **View timeline**: See the Gantt chart update automatically
6. **Reset data**: Use "Reset to Demo Data" button anytime

## 📊 Data Structure

The app includes sample data with these columns:
- **Task ID**: Unique identifier for each task
- **Task Name**: Descriptive name of the task
- **Phase**: Discovery, Procurement, Testing & Model Training, Deployment, Training
- **Site**: Site 1, Site 2, etc.
- **Status**: Yet to Start, In Progress, Completed
- **Owner**: Person responsible for the task
- **Planned Start/Finish**: Scheduled dates
- **Actual Start/Finish**: Real completion dates
- **Complexity**: Simple, Medium, Complex (for testing tasks)
- **Effort Hours**: Calculated based on complexity
- **Dependencies**: Comma-separated Task IDs

## 🧪 Testing & Model Training Features

**Automatic Complexity Mapping:**
- **Simple**: 16 hours
- **Medium**: 40 hours  
- **Complex**: 80 hours

**Timeline Calculation:**
- Duration (days) = ⌈effort_hours ÷ 8⌉
- Planned Start = day after all dependencies complete
- Planned Finish = Planned Start + Duration

## 🔗 Dependency Chaining

- **Automatic Updates**: When a predecessor's date changes, all dependent tasks shift automatically
- **Topological Sorting**: Prevents circular dependencies
- **Ripple Effect**: Delays propagate through the entire task tree
- **Real-time Validation**: Changes reflect immediately in the Gantt chart

## 🎨 User Interface

### **Sidebar Controls:**
- Reset to Demo Data button
- Site, Phase, and Status filters

### **Main Dashboard:**
1. **Project KPIs**: Total tasks, completion rate, delayed tasks, effort hours
2. **Testing Configuration**: Complexity settings with automatic recalculation
3. **Editable Task Table**: Modify any field inline
4. **Gantt Chart**: Color-coded by status with automatic updates

## 🔧 Core Functions

- `load_demo_data()` → Returns initial project plan DataFrame
- `calculate_testing_timeline()` → Applies complexity rules and calculates timelines
- `apply_dependency_chaining()` → Recalculates dependent tasks using topological sorting
- `apply_filters()` → Filters data for display
- `generate_gantt()` → Creates interactive Plotly Gantt chart
- `update_task()` → Updates individual task fields and triggers dependency recalculation

## 🎯 Behavior Rules

- **Real-time Updates**: Table changes immediately reflect in the Gantt chart
- **Automatic Chaining**: Date changes trigger dependency recalculation
- **Validation**: Date formats are validated automatically
- **Graceful Handling**: Missing dependencies are ignored safely
- **Session Persistence**: All changes persist during the session

## 📁 Sample Data

The app comes pre-loaded with realistic project data including:
- **Discovery Phase**: Site assessment, architecture design, stakeholder approval
- **Procurement Phase**: Hardware and software acquisition
- **Testing & Model Training**: Data model training, validation, performance testing
- **Deployment Phase**: Environment setup, system integration
- **Training Phase**: End user training, go-live support

## 🚨 Error Handling

- **Circular Dependencies**: Detected and reported with clear error messages
- **Missing Data**: Gracefully handled with default values
- **Date Parsing**: Robust date validation and conversion
- **Session State**: Maintains data integrity throughout the session

## 🔮 Future Enhancements

- **Data Persistence**: Save/load project plans to/from files
- **Team Collaboration**: Multi-user editing with conflict resolution
- **Advanced Analytics**: Resource allocation, critical path analysis
- **Export Options**: PDF reports, Excel export, project management tools
- **API Integration**: Connect with external project management systems

## 📝 Technical Details

- **Framework**: Streamlit
- **Data Management**: Pandas DataFrames with session state
- **Dependencies**: NetworkX for graph operations and topological sorting
- **Visualization**: Plotly for interactive Gantt charts
- **Architecture**: Modular functions with clear separation of concerns

## 📄 License

This project is open source and available under the MIT License. 