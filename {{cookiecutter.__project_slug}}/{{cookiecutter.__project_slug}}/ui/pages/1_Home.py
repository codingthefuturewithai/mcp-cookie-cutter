"""Home/Dashboard page for {{cookiecutter.project_name}} Admin UI

This page provides an overview of the MCP server status, project information,
and quick access to common administrative tasks.
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from {{cookiecutter.__project_slug}}.ui.lib.components import (
        render_status_card, 
        render_metric_card,
        render_info_section,
        render_quick_actions
    )
    from {{cookiecutter.__project_slug}}.ui.lib.utils import (
        check_server_status,
        get_project_info,
        get_system_info,
        format_uptime
    )
except ImportError as e:
    st.error(f"Failed to import UI components: {e}")
    st.info("Running in standalone mode with limited functionality.")

# Note: Page configuration is handled by main app.py

def render_server_status_section():
    """Render the server status monitoring section"""
    st.subheader("🔧 Server Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Server status
        try:
            status = check_server_status()
            if status == "running":
                st.success("🟢 Server Running")
            elif status == "stopped":
                st.error("🔴 Server Stopped")
            else:
                st.warning("🟡 Status Unknown")
        except:
            st.warning("🟡 Status Check Failed")
    
    with col2:
        # Admin UI status
        st.info("🟢 Admin UI Active")
    
    with col3:
        # Last updated
        current_time = datetime.now().strftime("%H:%M:%S")
        st.metric("Last Check", current_time)
    
    with col4:
        # Refresh button
        if st.button("🔄 Refresh Status", key="refresh_status"):
            st.rerun()

def render_project_overview():
    """Render project information overview"""
    st.subheader("📋 Project Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Project Details:**
        - **Name:** {{cookiecutter.project_name}}
        - **Description:** {{cookiecutter.description}}
        - **Author:** {{cookiecutter.author_name}}
        - **Email:** {{cookiecutter.email}}
        """)
        
    with col2:
        import sys
        from {{cookiecutter.__project_slug}}.config import get_config
        config = get_config()
        st.markdown(f"""
        **Configuration:**
        - **Python Version:** {sys.version_info.major}.{sys.version_info.minor}
        - **Server Port:** {{cookiecutter.server_port}}
        - **Log Level:** {config.log_level}
        - **Log Retention:** {config.log_retention_days} days
        """)

def render_feature_status():
    """Render feature enablement status"""
    st.subheader("⚙️ Feature Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Admin UI
        st.success("✅ Admin UI")
        st.caption("Web-based administration interface")
        
    with col2:
        # Example tools
        st.success("✅ Example Tools")
        st.info("➖ Example Tools")
        st.caption("Sample MCP tools for demonstration")
        
    with col3:
        # Parallel processing
        st.success("✅ Parallel Processing")
        st.info("➖ Parallel Processing")
        st.caption("Parallel execution examples")

def render_quick_actions_section():
    """Render quick action buttons"""
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⚙️ Configuration", 
                    help="Edit server configuration",
                    use_container_width=True):
            st.switch_page("pages/2_Configuration.py")
    
    with col2:
        if st.button("📊 View Logs", 
                    help="Browse and analyze server logs",
                    use_container_width=True):
            st.switch_page("pages/3_Logs.py")
    
    with col3:
        if st.button("🔄 Restart Server", 
                    help="Restart the MCP server (manual)",
                    use_container_width=True):
            st.warning("⚠️ Manual restart required")
            st.info("Stop the server process and restart it manually.")
    
    with col4:
        if st.button("📖 Documentation", 
                    help="View project documentation",
                    use_container_width=True):
            st.info("📚 Documentation will open in a new tab")

def render_system_info():
    """Render system information in an expandable section"""
    with st.expander("🔍 System Information"):
        try:
            system_info = get_system_info()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Runtime Environment:**")
                st.code(f"""
Python Version: {system_info.get('python_version', 'Unknown')}
Platform: {system_info.get('platform', 'Unknown')}
Architecture: {system_info.get('architecture', 'Unknown')}
""")
            
            with col2:
                st.markdown("**Application Paths:**")
                st.code(f"""
Config Path: {system_info.get('config_path', 'Not configured')}
Log Path: {system_info.get('log_path', 'Not configured')}
Data Path: {system_info.get('data_path', 'Not configured')}
""")
                
        except Exception as e:
            st.error(f"Failed to load system information: {e}")

def main():
    """Main page content"""
    # Page header
    st.title("🏠 {{cookiecutter.project_name}} Admin Dashboard")
    st.markdown("Welcome to the administrative interface for your MCP server.")
    st.markdown("---")
    
    # Server status section
    render_server_status_section()
    st.markdown("---")
    
    # Project overview
    render_project_overview()
    st.markdown("---")
    
    # Feature status
    render_feature_status()
    st.markdown("---")
    
    # Quick actions
    render_quick_actions_section()
    st.markdown("---")
    
    # System information (collapsible)
    render_system_info()
    
    # Footer
    st.markdown("---")
    st.caption(f"{{cookiecutter.project_name}} Admin UI • Generated with SAAGA MCP Server Cookie Cutter")

if __name__ == "__main__":
    main()
