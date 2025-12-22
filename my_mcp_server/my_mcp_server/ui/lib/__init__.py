"""Shared UI library for My MCP Server Admin interface.

This package provides reusable components, utilities, and styling
for the Streamlit admin interface.
"""

from .components import (
    render_header,
    render_sidebar,
    render_status_card,
    render_metric_card,
    render_info_section,
    render_info_card,
    render_warning_banner,
    render_config_section,
    render_log_filters,
    render_log_table,
    render_log_metrics,
    render_export_options,
    render_quick_actions,
    render_error_message,
    render_loading_spinner,
    render_footer
)

from .utils import (
    get_project_info,
    get_system_info,
    get_config_path,
    get_log_path,
    get_data_path,
    load_configuration,
    get_default_configuration,
    validate_configuration,
    save_configuration,
    load_logs_from_database,
    filter_logs,
    export_logs,
    get_log_statistics,
    format_uptime,
    format_file_size,
    is_port_available,
    get_system_paths
)

from .styles import (
    apply_custom_styles,
    apply_theme,
    apply_custom_fonts,
    create_status_indicator,
    create_badge,
    apply_page_config,
    hide_streamlit_style
)

__all__ = [
    # Components
    "render_header",
    "render_sidebar", 
    "render_status_card",
    "render_metric_card",
    "render_info_section",
    "render_info_card",
    "render_warning_banner",
    "render_config_section",
    "render_log_filters",
    "render_log_table",
    "render_log_metrics",
    "render_export_options",
    "render_quick_actions",
    "render_error_message",
    "render_loading_spinner",
    "render_footer",
    
    # Utils
    "get_project_info",
    "get_system_info",
    "get_config_path",
    "get_log_path",
    "get_data_path",
    "load_configuration",
    "get_default_configuration",
    "validate_configuration",
    "save_configuration",
    "load_logs_from_database",
    "filter_logs",
    "export_logs",
    "get_log_statistics",
    "format_uptime",
    "format_file_size",
    "is_port_available",
    "get_system_paths",
    
    # Styles
    "apply_custom_styles",
    "apply_theme",
    "apply_custom_fonts",
    "create_status_indicator",
    "create_badge",
    "apply_page_config",
    "hide_streamlit_style"
]
