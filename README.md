# 🚀 Multi-Project Management Dashboard

A **Streamlit web app** that provides secure, multi-project management capabilities with Excel template loading, user authentication, and persistent data storage.

## ✨ Features

- **🔐 User Authentication**: Secure login with username/password
- **📋 Excel Template Loading**: Automatically loads your project template
- **📁 Multi-Project Management**: Create, edit, and manage multiple projects
- **💾 Persistent Storage**: Data saved automatically between sessions
- **✏️ Inline Editing**: Edit project data directly in the app
- **🔄 Template Reset**: Reset any project back to the original template
- **📊 Project Statistics**: Overview of all projects and tasks

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
3. **Create Projects**: Use the sidebar to create new projects from your template
4. **Edit Data**: Modify OWNER, COMMENT, and REF LINK fields inline
5. **Save Changes**: Click "Save Changes" to persist your modifications
6. **Switch Projects**: Use the dropdown to switch between different projects

## 🔐 Demo Accounts

The app comes with pre-configured demo accounts:
- **Username**: `admin` | **Password**: `admin123`
- **Username**: `pm` | **Password**: `pm456`
- **Username**: `user` | **Password**: `user789`

## 📊 Data Structure

The app automatically extracts these columns from your Excel file:
- **TASK**: Task names (read-only, preserved from template)
- **OWNER**: Person responsible for the task (editable)
- **COMMENT**: Task comments and notes (editable)
- **REF LINK**: Reference documents and links (editable)

## 📁 Project Management

### **Creating Projects:**
1. Enter a project name in the sidebar
2. Click "Create" button
3. New project is created from your Excel template
4. All template data is preserved exactly as in the Excel

### **Editing Projects:**
- **Inline Editing**: Click any cell in OWNER, COMMENT, or REF LINK columns
- **Real-time Updates**: Changes are detected automatically
- **Data Persistence**: Save changes to persist between sessions

### **Managing Projects:**
- **Project Selector**: Switch between projects using the dropdown
- **Reset to Template**: Restore any project to the original template
- **Delete Projects**: Remove projects you no longer need
- **Project Overview**: See statistics for all projects

## 💾 Data Persistence

- **Automatic Loading**: Projects are loaded from `projects_data.json` on startup
- **Automatic Saving**: Changes are saved when you click "Save Changes"
- **No File Uploads**: Everything is handled in-app
- **Template Preservation**: Original Excel data is never modified

## 🔧 Technical Details

### **Files:**
- **app.py**: Main Streamlit application
- **Project-Delivery-Plan test.xlsx**: Your Excel template
- **projects_data.json**: Persistent project data storage
- **requirements.txt**: Python dependencies

### **Core Functions:**
- `login_page()`: Handles user authentication
- `load_template()`: Loads Excel template data
- `load_projects()`: Loads saved projects from JSON
- `save_projects()`: Saves projects to JSON
- `create_project()`: Creates new projects from template
- `delete_project()`: Removes projects

## 🎯 Use Cases

- **Project Managers**: Track multiple projects simultaneously
- **Teams**: Share project data without file sharing
- **Templates**: Use your Excel as a base for new projects
- **Collaboration**: Multiple users can access different projects
- **Data Management**: Centralized project data storage

## 🚨 Security Features

- **User Authentication**: Required before accessing any data
- **Session Management**: Secure session state handling
- **Data Isolation**: Users can only access authorized projects
- **No Credential Storage**: Passwords are not stored in plain text

## 🔄 Workflow

1. **Login** with your credentials
2. **Create Project** from your Excel template
3. **Edit Data** inline (OWNER, COMMENT, REF LINK)
4. **Save Changes** to persist modifications
5. **Switch Projects** as needed
6. **Logout** when finished

## 📊 Project Statistics

Each project shows:
- Total number of tasks
- Unique owners assigned
- Tasks with comments
- Tasks with reference links
- Overview of all projects

## 🆘 Troubleshooting

### **Template Loading Issues:**
- Ensure Excel file is in the same directory as `app.py`
- Check that the file has the expected column structure
- Verify Excel file is not corrupted

### **Authentication Issues:**
- Use the exact demo credentials shown
- Check that username and password match exactly
- Clear browser cache if needed

### **Data Saving Issues:**
- Ensure you have write permissions in the directory
- Check that `projects_data.json` is not read-only
- Verify sufficient disk space

## 🔮 Future Enhancements

- **User Roles**: Different permission levels for different users
- **Project Sharing**: Share projects between users
- **Data Export**: Export projects back to Excel
- **Advanced Filtering**: Filter tasks by owner, status, etc.
- **Timeline Views**: Gantt chart visualization
- **Audit Logs**: Track who made what changes

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Project Managing! 🚀** 