"""Shared UI components for {{cookiecutter.project_name}} Admin UI

This module provides reusable Streamlit components including headers, alerts,
status indicators, and other common UI elements used across different pages.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

def render_header():
    """Render the main application header"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem; 
                border-bottom: 2px solid #f0f2f6;">
        <h1 style="color: #1f77b4; margin: 0;">🛠️ {{cookiecutter.project_name}} Admin</h1>
        <p style="color: #666; margin: 0.5rem 0 0 0;">MCP Server Administration Interface</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with navigation and project info"""
    with st.sidebar:
        st.markdown("### 📋 Project Info")
        st.markdown("""
        **{{cookiecutter.project_name}}**  
        Version: 0.1.0  
        Author: {{cookiecutter.author_name}}  
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Server Info")
        import sys
        st.markdown(f"""
        **Port:** {{cookiecutter.server_port}}  
        **Log Level:** INFO  
        **Python:** {sys.version_info.major}.{sys.version_info.minor}+  
        """)
        
        st.markdown("---")
        st.markdown("### 🎛️ Features")
        feature_list = []
        feature_list.append("✅ Admin UI")
        feature_list.append("✅ Example Tools")
        feature_list.append("➖ Example Tools")
        feature_list.append("✅ Parallel Processing")
        feature_list.append("➖ Parallel Processing")
        
        for feature in feature_list:
            st.markdown(f"- {feature}")

def render_status_card(title: str, status: str, description: str = "", help_text: str = ""):
    """Render a status card with title, status indicator, and description"""
    if status.lower() in ["active", "running", "success", "online"]:
        color = "#28a745"
        icon = "🟢"
    elif status.lower() in ["inactive", "stopped", "error", "offline", "failed"]:
        color = "#dc3545"
        icon = "🔴"
    elif status.lower() in ["warning", "unknown", "pending"]:
        color = "#ffc107"
        icon = "🟡"
    else:
        color = "#6c757d"
        icon = "⚪"
    
    st.markdown(f"""
    <div style="border: 1px solid {color}; border-radius: 5px; padding: 1rem; margin: 0.5rem 0;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
            <strong style="color: {color};">{title}</strong>
        </div>
        <div style="margin-left: 1.7rem;">
            <div><strong>Status:</strong> {status}</div>
            {f'<div style="color: #666; font-size: 0.9rem;">{description}</div>' if description else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if help_text:
        st.caption(help_text)

def render_metric_card(title: str, value: str, delta: str = "", help_text: str = ""):
    """Render a metric card with value and optional delta"""
    st.metric(title, value, delta=delta, help=help_text)

def render_info_section(title: str, content: Dict[str, Any], columns: int = 2):
    """Render an information section with key-value pairs"""
    st.subheader(title)
    
    items = list(content.items())
    if columns > 1:
        cols = st.columns(columns)
        for i, (key, value) in enumerate(items):
            with cols[i % columns]:
                st.write(f"**{key}:** {value}")
    else:
        for key, value in items:
            st.write(f"**{key}:** {value}")

def render_info_card(title: str, content: str, card_type: str = "info"):
    """Render an information card with different types (info, warning, error, success)"""
    if card_type == "info":
        st.info(f"**{title}**\n\n{content}")
    elif card_type == "warning":
        st.warning(f"**{title}**\n\n{content}")
    elif card_type == "error":
        st.error(f"**{title}**\n\n{content}")
    elif card_type == "success":
        st.success(f"**{title}**\n\n{content}")
    else:
        st.markdown(f"**{title}**\n\n{content}")

def render_warning_banner(message: str, dismissible: bool = False):
    """Render a warning banner across the page"""
    if dismissible and st.session_state.get("banner_dismissed", False):
        return
    
    col1, col2 = st.columns([10, 1]) if dismissible else st.columns([1]), st.columns([1])
    
    with col1[0] if dismissible else st:
        st.warning(f"⚠️ {message}")
    
    if dismissible:
        with col2:
            if st.button("✕", key="dismiss_banner"):
                st.session_state.banner_dismissed = True
                st.rerun()

def render_config_section(title: str, config_data: Dict[str, Any], editable: bool = False):
    """Render a configuration section with optional editing capabilities"""
    st.subheader(title)
    
    if editable:
        st.warning("⚠️ Configuration editing not yet implemented")
    
    # Display configuration as formatted JSON
    st.json(config_data)

def render_log_filters(available_tools: List[str], available_levels: List[str]):
    """Render log filtering controls"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        level_filter = st.selectbox("Log Level", ["All"] + available_levels)
    
    with col2:
        tool_filter = st.selectbox("Tool", ["All"] + available_tools)
    
    with col3:
        date_range = st.date_input("Date Range", value=datetime.now().date())
    
    with col4:
        search_term = st.text_input("Search", placeholder="Enter search term...")
    
    return {
        "level": level_filter if level_filter != "All" else None,
        "tool": tool_filter if tool_filter != "All" else None,
        "date": date_range,
        "search": search_term if search_term else None
    }

def render_log_table(log_data: List[Dict[str, Any]], max_rows: int = 50):
    """Render a table of log entries"""
    if not log_data:
        st.info("No log entries to display.")
        return
    
    # Limit rows if needed
    display_data = log_data[:max_rows] if len(log_data) > max_rows else log_data
    
    # Create table
    for i, log_entry in enumerate(display_data):
        with st.expander(f"{log_entry.get('timestamp', 'Unknown')} - {log_entry.get('level', 'INFO')} - {log_entry.get('tool_name', 'Unknown')}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Level:** {log_entry.get('level', 'INFO')}")
                st.write(f"**Tool:** {log_entry.get('tool_name', 'Unknown')}")
                st.write(f"**Status:** {log_entry.get('status', 'Unknown')}")
                
            with col2:
                st.write(f"**Duration:** {log_entry.get('duration_ms', 'N/A')} ms")
                st.write(f"**Timestamp:** {log_entry.get('timestamp', 'Unknown')}")
            
            if log_entry.get('input_args'):
                st.write("**Input:**")
                st.code(log_entry['input_args'])
            
            if log_entry.get('output_summary'):
                st.write("**Output:**")
                st.write(log_entry['output_summary'])
            
            if log_entry.get('error_message'):
                st.write("**Error:**")
                st.error(log_entry['error_message'])
    
    if len(log_data) > max_rows:
        st.caption(f"Showing {max_rows} of {len(log_data)} entries")

def render_log_metrics(metrics: Dict[str, Any]):
    """Render log metrics in a dashboard format"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Logs", metrics.get('total_logs', 0))
    
    with col2:
        error_rate = metrics.get('error_rate', 0)
        st.metric("Error Rate", f"{error_rate:.1f}%")
    
    with col3:
        avg_duration = metrics.get('avg_duration_ms', 0)
        st.metric("Avg Duration", f"{avg_duration:.0f}ms")
    
    with col4:
        active_tools = metrics.get('active_tools', 0)
        st.metric("Active Tools", active_tools)

def render_export_options(data: Any, filename_prefix: str = "export"):
    """Render export options for data"""
    st.subheader("📥 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 CSV Export", disabled=True):
            st.info("CSV export will be implemented in Phase 4, Issue 3")
    
    with col2:
        if st.button("📊 Excel Export", disabled=True):
            st.info("Excel export will be implemented in Phase 4, Issue 3")
    
    with col3:
        if st.button("🔗 JSON Export", disabled=True):
            st.info("JSON export will be implemented in Phase 4, Issue 3")

def render_quick_actions(actions: List[Dict[str, Any]]):
    """Render a grid of quick action buttons"""
    if not actions:
        return
    
    cols = st.columns(len(actions))
    
    for i, action in enumerate(actions):
        with cols[i]:
            if st.button(
                action.get('label', 'Action'),
                help=action.get('help', ''),
                disabled=action.get('disabled', False),
                use_container_width=True
            ):
                callback = action.get('callback')
                if callback:
                    callback()
                elif action.get('page'):
                    st.switch_page(action['page'])

def render_error_message(error: Exception, context: str = ""):
    """Render a formatted error message with context"""
    st.error(f"❌ Error{f' in {context}' if context else ''}")
    st.error(str(error))
    
    with st.expander("🔍 Error Details"):
        st.code(f"Error Type: {type(error).__name__}\nMessage: {str(error)}")

def render_loading_spinner(message: str = "Loading..."):
    """Render a loading spinner with message"""
    with st.spinner(message):
        return st.empty()

def render_footer():
    """Render the application footer"""
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666; font-size: 0.8rem; padding: 1rem;'>"
        f"{{cookiecutter.project_name}} Admin UI • "
        f"Generated with SAAGA MCP Server Cookie Cutter • "
        f"Phase 4, Issue 1"
        f"</div>",
        unsafe_allow_html=True
    )
