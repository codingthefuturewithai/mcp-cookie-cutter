"""Log viewer page for My MCP Server Admin UI

This page provides interface for viewing, filtering, and analyzing server logs
from the SQLite logging database. Includes export capabilities and real-time updates.
"""

import streamlit as st
from pathlib import Path
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import pandas as pd

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from my_mcp_server.ui.lib.components import (
        render_log_filters,
        render_log_table,
        render_log_metrics,
        render_export_options
    )
    from my_mcp_server.ui.lib.utils import (
        load_logs_from_database,
        filter_logs,
        export_logs,
        get_log_statistics
    )
except ImportError as e:
    st.error(f"Failed to import UI components: {e}")
    st.info("Log viewer may have limited functionality.")

# Note: Page configuration is handled by main app.py

def render_correlation_id_info():
    """Render information about correlation IDs"""
    with st.expander("ℹ️ About Correlation IDs"):
        st.markdown("""
        **Correlation IDs** help track related log events across your application:
        
        - Each tool execution gets a unique ID (e.g., `req_a1b2c3d4e5f6`)
        - All logs from the same request share the same correlation ID
        - Use correlation IDs to trace complete request flows
        - Filter by correlation ID to see all related events
        """)

def render_log_metrics_section(df: pd.DataFrame):
    """Render log metrics and statistics"""
    st.subheader("📈 Log Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_logs = len(df)
        st.metric("Total Logs", f"{total_logs:,}")
    
    with col2:
        if not df.empty and 'status' in df.columns:
            error_count = len(df[df['status'] == 'error'])
            error_rate = (error_count / total_logs * 100) if total_logs > 0 else 0
            st.metric("Error Rate", f"{error_rate:.1f}%", delta=f"{error_count} errors")
        else:
            st.metric("Error Rate", "0.0%", delta="0 errors")
    
    with col3:
        if not df.empty and 'duration_ms' in df.columns:
            avg_duration = df['duration_ms'].mean()
            if pd.notna(avg_duration):
                st.metric("Avg Duration", f"{avg_duration:.0f}ms")
            else:
                st.metric("Avg Duration", "0ms")
        else:
            st.metric("Avg Duration", "0ms")
    
    with col4:
        if not df.empty and 'tool_name' in df.columns:
            unique_tools = df['tool_name'].nunique()
            st.metric("Active Tools", unique_tools)
        else:
            st.metric("Active Tools", 0)

def clear_all_filters():
    """Callback function to clear all filter values"""
    # Set to default values instead of deleting
    st.session_state.quick_log_filter = "All Levels"  # First option in radio
    st.session_state.log_level_filter = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]  # All selected
    st.session_state.log_type_filter = "All"  # First option
    st.session_state.status_filter = "All"  # First option  
    st.session_state.time_range_filter = "Last 7 Days"  # Index 2 default
    st.session_state.search_filter = ""  # Empty string for text input
    if "custom_log_levels" in st.session_state:
        del st.session_state.custom_log_levels  # This one we can delete

def render_log_filters_section():
    """Render log filtering controls"""
    st.subheader("🔍 Filters")
    
    # First row of filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Quick filter buttons
        quick_filter = st.radio(
            "Quick Filter",
            options=["All Levels", "Errors Only", "Custom"],
            horizontal=True,
            key="quick_log_filter"
        )
        
        # Set default based on quick filter
        if quick_filter == "All Levels":
            default_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        elif quick_filter == "Errors Only":
            default_levels = ["ERROR", "CRITICAL"]
        else:
            default_levels = st.session_state.get("custom_log_levels", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        
        log_levels = st.multiselect(
            "Log Level",
            options=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            default=default_levels,
            key="log_level_filter",
            disabled=(quick_filter != "Custom")
        )
        
        # Store custom selection
        if quick_filter == "Custom":
            st.session_state["custom_log_levels"] = log_levels
    
    with col2:
        log_type = st.selectbox(
            "Log Type",
            options=["All", "tool_execution", "internal", "framework"],
            key="log_type_filter"
        )
    
    with col3:
        status_filter = st.selectbox(
            "Status",
            options=["All", "success", "error", "running"],
            key="status_filter"
        )
    
    with col4:
        time_range = st.selectbox(
            "Time Range",
            options=["Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"],
            index=2,
            key="time_range_filter"
        )
    
    # Second row for search
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input(
            "Search (correlation ID, tool name, or message)",
            placeholder="e.g., req_a1b2c3d4e5f6",
            key="search_filter"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacer
        st.button("Clear Filters", use_container_width=True, on_click=clear_all_filters)
    
    return {
        "log_levels": log_levels if log_levels else None,
        "log_type": log_type if log_type != "All" else None,
        "status": status_filter if status_filter != "All" else None,
        "time_range": time_range,
        "search": search_term if search_term else None
    }

def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """Apply filters to the log dataframe"""
    if df.empty:
        return df  # Return empty DataFrame immediately if no data
    
    filtered_df = df.copy()
    
    if filters.get("log_levels") and 'level' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['level'].isin(filters["log_levels"])]
    
    if filters.get("log_type") and 'log_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['log_type'] == filters["log_type"]]
    
    if filters.get("status") and 'status' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['status'] == filters["status"]]
    
    # Apply search filter
    if filters.get("search"):
        search_term = filters["search"].lower()
        # Check columns exist before filtering
        if all(col in filtered_df.columns for col in ['correlation_id', 'tool_name', 'message']):
            mask = (
                (filtered_df['correlation_id'].astype(str).str.lower().str.contains(search_term, na=False)) |
                (filtered_df['tool_name'].astype(str).str.lower().str.contains(search_term, na=False)) |
                (filtered_df['message'].astype(str).str.lower().str.contains(search_term, na=False))
            )
            filtered_df = filtered_df[mask]
    
    # Apply time range filter
    if 'timestamp' in filtered_df.columns:
        now = datetime.now()
        if filters["time_range"] == "Last Hour":
            cutoff = now - timedelta(hours=1)
        elif filters["time_range"] == "Last 24 Hours":
            cutoff = now - timedelta(days=1)
        elif filters["time_range"] == "Last 7 Days":
            cutoff = now - timedelta(days=7)
        elif filters["time_range"] == "Last 30 Days":
            cutoff = now - timedelta(days=30)
        else:
            cutoff = None
        
        if cutoff:
            filtered_df = filtered_df[filtered_df['timestamp'] >= cutoff]
    
    return filtered_df

def render_log_table_section(df: pd.DataFrame):
    """Render the log table with pagination"""
    st.subheader("📋 Log Entries")
    
    # Pagination controls
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        page_size = st.selectbox("Rows per page", [25, 50, 100, 200], index=1)
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Check if DataFrame is empty before sorting
    if df.empty:
        st.info("No log entries match the current filters.")
        return
    
    # Sort and paginate
    if 'timestamp' in df.columns:
        df_sorted = df.sort_values('timestamp', ascending=False)
    else:
        df_sorted = df  # Can't sort without timestamp column
    
    total_rows = len(df_sorted)
    total_pages = (total_rows + page_size - 1) // page_size
    
    if total_pages > 1:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        df_page = df_sorted.iloc[start_idx:end_idx]
    else:
        df_page = df_sorted
    
    # Display table
    if len(df_page) > 0:
        # Format timestamp for display
        df_display = df_page.copy()
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Color code status
        def color_status(val):
            if val == 'success':
                return 'background-color: #d4edda; color: #155724'
            elif val == 'error':
                return 'background-color: #f8d7da; color: #721c24'
            elif val == 'timeout':
                return 'background-color: #fff3cd; color: #856404'
            return ''
        
        # Display the styled dataframe
        styled_df = df_display.style.map(color_status, subset=['status'])
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "timestamp": "Timestamp",
                "correlation_id": "Correlation ID",
                "level": "Level",
                "log_type": "Type",
                "tool_name": "Tool",
                "status": "Status",
                "duration_ms": st.column_config.NumberColumn("Duration (ms)", format="%d ms"),
                "message": "Message",
                "input_args": "Input",
                "output_summary": "Output",
                "error_message": "Error"
            }
        )
        
        st.caption(f"Showing {len(df_page)} of {total_rows} log entries")
    else:
        st.info("No log entries match the current filters.")

def render_export_section(df: pd.DataFrame):
    """Render export options"""
    st.subheader("📥 Export Logs")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export CSV", disabled=True):
            st.info("CSV export will be available in Phase 4, Issue 3")
    
    with col2:
        if st.button("📊 Export Excel", disabled=True):
            st.info("Excel export will be available in Phase 4, Issue 3")
    
    with col3:
        if st.button("🔗 Export JSON", disabled=True):
            st.info("JSON export will be available in Phase 4, Issue 3")

def render_log_maintenance_section():
    """Render log maintenance section with purge functionality"""
    st.subheader("🧹 Log Maintenance")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        # Get current retention days from config
        try:
            from my_mcp_server.config import get_config
            config = get_config()
            current_retention = config.log_retention_days
        except:
            current_retention = 7
        
        retention_days = st.number_input(
            "Log Retention (days)",
            min_value=1,
            max_value=365,
            value=current_retention,
            help="Logs older than this will be deleted when purging"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacer
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        st.info(f"Will delete logs before: {cutoff_date.strftime('%Y-%m-%d')}")
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacer
        if st.button("🗑️ Purge Old Logs", type="primary", use_container_width=True):
            try:
                # Import and use the SQLite logger's cleanup method
                from my_mcp_server.decorators.sqlite_logger import get_sqlite_sink
                
                sqlite_sink = get_sqlite_sink()
                if sqlite_sink:
                    # Update the config's retention days temporarily for this cleanup
                    sqlite_sink.config.log_retention_days = retention_days
                    sqlite_sink.cleanup_old_logs()
                    st.success(f"✅ Successfully purged logs older than {retention_days} days")
                    st.rerun()  # Refresh the page to show updated data
                else:
                    st.error("❌ SQLite logging not initialized")
            except Exception as e:
                st.error(f"❌ Failed to purge logs: {str(e)}")

def main():
    """Main logs page content"""
    # Page header
    st.title("📊 My MCP Server Logs")
    st.markdown("View and analyze server logs from the unified logging system.")
    st.markdown("---")
    
    # Correlation ID info
    render_correlation_id_info()
    
    # Load real data from database
    try:
        # Load logs from unified database
        log_entries = load_logs_from_database(limit=5000)
        
        if log_entries:
            # Convert to DataFrame
            log_data = pd.DataFrame(log_entries)
            
            # Ensure timestamp is datetime
            if 'timestamp' in log_data.columns:
                log_data['timestamp'] = pd.to_datetime(log_data['timestamp'])
            
            st.success(f"Loaded {len(log_data)} log entries from unified database")
        else:
            st.warning("No log entries found. Start using the server to generate logs.")
            log_data = pd.DataFrame()  # Empty DataFrame, NO mock data
    except Exception as e:
        st.error(f"Error loading logs: {str(e)}")
        st.error(f"Database connection failed. Please check the logs database.")
        log_data = pd.DataFrame()  # Empty DataFrame, NO mock data
    
    st.markdown("---")
    
    # Render filters
    filters = render_log_filters_section()
    
    # Apply filters
    filtered_data = apply_filters(log_data, filters)
    
    st.markdown("---")
    
    # Metrics section
    render_log_metrics_section(filtered_data)
    
    st.markdown("---")
    
    # Log table
    render_log_table_section(filtered_data)
    
    st.markdown("---")
    
    # Export section
    render_export_section(filtered_data)
    
    st.markdown("---")
    
    # Log maintenance section
    render_log_maintenance_section()
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/1_Home.py")
    
    with col2:
        if st.button("⚙️ Configuration", use_container_width=True):
            st.switch_page("pages/2_Configuration.py")
    
    # Footer
    st.caption("Unified logging system with correlation IDs and pluggable destinations")

if __name__ == "__main__":
    main()
