"""Home/Dashboard page for Post-fix Test MCP Admin UI

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
    from post_fix_test_mcp.ui.lib.components import (
        render_info_section,
        render_quick_actions
    )
    from post_fix_test_mcp.ui.lib.utils import (
        get_project_info,
        get_system_info,
        format_uptime
    )
except ImportError as e:
    st.error(f"Failed to import UI components: {e}")
    st.info("Running in standalone mode with limited functionality.")

# Note: Page configuration is handled by main app.py

def render_admin_ui_status():
    """Render the admin UI status section"""
    st.subheader("📊 Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Admin UI status
        st.success("✅ Admin UI Active")
        st.caption("Web interface running")
    
    with col2:
        # Project info
        project_info = get_project_info()
        st.info(f"📦 Version {project_info.get('version', '0.1.0')}")
        st.caption("Project version")
    
    with col3:
        # Python version
        st.info(f"🐍 Python {project_info.get('python_version', 'Unknown')}")
        st.caption("Runtime version")

def render_project_overview():
    """Render project information overview"""
    st.subheader("📋 Project Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Project Details:**
        - **Name:** Post-fix Test MCP
        - **Description:** Post-fix Test MCP - MCP server with tools and integrations
        - **Author:** tim
        - **Email:** t@gmail.com
        """)
        
    with col2:
        import sys
        from post_fix_test_mcp.config import get_config
        config = get_config()
        st.markdown(f"""
        **Configuration:**
        - **Python Version:** {sys.version_info.major}.{sys.version_info.minor}
        - **Server Port:** 3001
        - **Log Level:** {config.log_level}
        - **Log Retention:** {config.log_retention_days} days
        """)

def render_system_status():
    """Render system resource and capabilities status"""
    st.subheader("⚙️ System Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Admin UI
        st.success("✅ Admin UI")
        st.caption("Web-based administration interface")
        
    with col2:
        # MCP Server
        st.info("🔧 MCP Server")
        st.caption("Model Context Protocol server")
        
    with col3:
        # Logging System
        st.success("✅ Unified Logging")
        st.caption("SQLite-based log aggregation")

def render_quick_actions_section():
    """Render quick action buttons"""
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
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
        if st.button("📖 Documentation", 
                    help="View project documentation",
                    use_container_width=True):
            st.switch_page("pages/4_Documentation.py")

def render_system_info():
    """Render system information in an expandable section"""
    with st.expander("🔍 System Information"):
        try:
            from post_fix_test_mcp.ui.lib.utils import get_system_paths
            system_info = get_system_info()
            system_paths = get_system_paths()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Runtime Environment:**")
                st.code(f"""
Python Version: {system_info.get('python_version', 'Unknown')}
Platform: {system_info.get('platform', 'Unknown')}
Architecture: {system_info.get('architecture', 'Unknown')}
""")
            
            with col2:
                st.markdown("**System Paths:**")
                st.code(f"""
Configuration File:
{system_paths.get('configuration_file', 'Unknown')}

Logging Database:
{system_paths.get('logging_database', 'Unknown')}

Application Directory:
{system_paths.get('application_directory', 'Unknown')}
""")
                
        except Exception as e:
            st.error(f"Failed to load system information: {e}")

def main():
    """Main page content"""
    # Page header
    st.title("🏠 Post-fix Test MCP Admin Dashboard")
    st.markdown("Welcome to the administrative interface for your MCP server.")
    st.markdown("---")
    
    # Admin UI status section
    render_admin_ui_status()
    st.markdown("---")
    
    # Project overview
    render_project_overview()
    st.markdown("---")
    
    # System status
    render_system_status()
    st.markdown("---")
    
    # Quick actions
    render_quick_actions_section()
    st.markdown("---")
    
    # System information (collapsible)
    render_system_info()
    
    # Footer
    st.markdown("---")
    st.caption(f"Post-fix Test MCP Admin UI • Generated with SAAGA MCP Server Cookie Cutter")

if __name__ == "__main__":
    main()
