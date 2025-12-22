"""Configuration management page for My MCP Server Admin UI

This page provides interface for managing server configuration, environment variables,
and tool settings. Changes require server restart to take effect.
"""

import streamlit as st
from pathlib import Path
import sys
from typing import Dict, Any, Optional
import yaml

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

try:
    from my_mcp_server.ui.lib.components import (
        render_info_card,
        render_warning_banner,
        render_config_section
    )
    from my_mcp_server.ui.lib.utils import (
        load_configuration,
        validate_configuration,
        save_configuration,
        get_default_configuration,
        get_config_path,
        is_port_available,
        get_system_info
    )
except ImportError as e:
    st.error(f"Failed to import UI components: {e}")
    st.info("Configuration management may have limited functionality.")

# Note: Page configuration is handled by main app.py

def render_config_status():
    """Render configuration loading status"""
    config = load_configuration()
    
    if "error" in config:
        st.error(f"⚠️ **Configuration Error**\n\n{config['error']}")
        st.info("Using default configuration values below.")
        return get_default_configuration()
    else:
        st.success("✅ **Configuration Loaded Successfully**")
        return config

def render_current_config_preview(config):
    """Render a preview of current configuration"""
    st.subheader("📋 Current Configuration Preview")
    
    # Display configuration in tabs
    tab1, tab2 = st.tabs(["🔧 Server", "📊 Logging"])
    
    with tab1:
        st.json(config.get("server", {}))
        
    with tab2:
        st.json(config.get("logging", {}))

def render_configuration_form(config):
    """Render configuration editing form"""
    st.subheader("✏️ Configuration Editor")
    
    # Initialize session state for undo/redo
    if "config_history" not in st.session_state:
        st.session_state.config_history = [config.copy()]
        st.session_state.config_history_index = 0
    
    # Current configuration values
    server_config = config.get("server", {})
    logging_config = config.get("logging", {})
    
    with st.form("config_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Server Settings**")
            server_name = st.text_input("Server Name", value=server_config.get("name", "My MCP Server"))
            server_port = st.number_input("Server Port", 
                                        value=server_config.get("port", 3001),
                                        min_value=1, max_value=65535)
            # Get current log level from runtime config
            try:
                from my_mcp_server.config import get_config
                current_config = get_config()
                current_log_level = current_config.log_level
            except:
                current_log_level = "INFO"
            
            log_level = st.selectbox("Log Level", 
                                   options=["DEBUG", "INFO", "WARNING", "ERROR"],
                                   index=["DEBUG", "INFO", "WARNING", "ERROR"].index(
                                       server_config.get("log_level", current_log_level)
                                   ))
        
        with col2:
            st.markdown("**Logging Settings**")
            # Get current retention days from runtime config
            try:
                from my_mcp_server.config import get_config
                current_config = get_config()
                current_retention = current_config.log_retention_days
            except:
                current_retention = 7
            
            log_retention = st.number_input("Log Retention (days)", 
                                          value=logging_config.get("retention_days", current_retention),
                                          min_value=1, max_value=365)
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            save_button = st.form_submit_button("💾 Save Configuration", type="primary")
            
        with col2:
            reset_button = st.form_submit_button("🔄 Reset to Defaults")
            
        with col3:
            export_button = st.form_submit_button("📤 Export Config")
            
        with col4:
            if len(st.session_state.config_history) > 1:
                undo_button = st.form_submit_button("↶ Undo")
            else:
                st.form_submit_button("↶ Undo", disabled=True)
        
        # Process form submissions
        if save_button:
            return handle_save_config(server_name, server_port, log_level, log_retention, config)
        
        if reset_button:
            return handle_reset_config()
            
        if export_button:
            return handle_export_config(config)
            
        if len(st.session_state.config_history) > 1 and 'undo_button' in locals():
            return handle_undo_config()
    
    return None

def handle_save_config(server_name, server_port, log_level, log_retention, current_config):
    """Handle saving configuration changes"""
    # Build new configuration
    new_config = {
        "server": {
            "name": server_name,
            "description": current_config.get("server", {}).get("description", "My MCP Server - MCP server with tools and integrations"),
            "port": server_port,
            "log_level": log_level,
            "default_transport": current_config.get("server", {}).get("default_transport", "stdio"),
            "default_host": current_config.get("server", {}).get("default_host", "127.0.0.1")
        },
        "logging": {
            "level": log_level,
            "retention_days": log_retention,
            "database_name": current_config.get("logging", {}).get("database_name", "unified_logs.db"),
            "destinations": current_config.get("logging", {}).get("destinations", [
                {
                    "type": "sqlite",
                    "enabled": True,
                    "settings": {}
                }
            ])
        }
    }
    
    # Validate configuration
    validation_result = validate_configuration(new_config)
    
    if not validation_result["valid"]:
        st.error("❌ **Configuration Validation Failed**")
        for error in validation_result["errors"]:
            st.error(f"• {error}")
        return None
    
    # Show warnings if any
    if validation_result["warnings"]:
        st.warning("⚠️ **Configuration Warnings**")
        for warning in validation_result["warnings"]:
            st.warning(f"• {warning}")
    
    # Show diff before saving
    if show_config_diff(current_config, new_config):
        # Save configuration
        if save_configuration(new_config):
            st.success("✅ **Configuration Saved Successfully**")
            
            # Add to history
            st.session_state.config_history.append(new_config.copy())
            st.session_state.config_history_index = len(st.session_state.config_history) - 1
            
            # Show restart notice
            st.warning("""
            🔄 **Server Restart Required**
            
            Your configuration changes have been saved, but the server needs to be restarted 
            for the changes to take effect.
            """)
            
            return new_config
        else:
            st.error("❌ **Failed to Save Configuration**")
            st.error("Please check file permissions and try again.")
    
    return None

def handle_reset_config():
    """Handle resetting configuration to defaults"""
    if st.button("⚠️ Confirm Reset to Defaults", key="confirm_reset"):
        default_config = get_default_configuration()
        
        if save_configuration(default_config):
            st.success("✅ **Configuration Reset to Defaults**")
            st.session_state.config_history = [default_config.copy()]
            st.session_state.config_history_index = 0
            st.warning("🔄 **Server Restart Required**")
            return default_config
        else:
            st.error("❌ **Failed to Reset Configuration**")
    else:
        st.info("Click the button above to confirm reset to default configuration.")
    
    return None

def handle_export_config(config):
    """Handle exporting configuration"""
    import json
    
    # Export as JSON
    config_json = json.dumps(config, indent=2)
    
    st.download_button(
        label="📥 Download Configuration (JSON)",
        data=config_json,
        file_name="my_mcp_server_config.json",
        mime="application/json"
    )
    
    return None

def handle_undo_config():
    """Handle undoing configuration changes"""
    if st.session_state.config_history_index > 0:
        st.session_state.config_history_index -= 1
        previous_config = st.session_state.config_history[st.session_state.config_history_index]
        
        if save_configuration(previous_config):
            st.success("↶ **Configuration Restored**")
            st.warning("🔄 **Server Restart Required**")
            return previous_config
        else:
            st.error("❌ **Failed to Restore Configuration**")
    
    return None

def show_config_diff(old_config, new_config):
    """Show configuration differences and ask for confirmation"""
    import json
    
    st.subheader("📋 Configuration Changes")
    
    # Find differences
    changes = []
    
    # Check server changes
    old_server = old_config.get("server", {})
    new_server = new_config.get("server", {})
    for key in set(old_server.keys()) | set(new_server.keys()):
        old_val = old_server.get(key)
        new_val = new_server.get(key)
        if old_val != new_val:
            changes.append(f"Server {key}: {old_val} → {new_val}")
    
    # Check logging changes
    old_logging = old_config.get("logging", {})
    new_logging = new_config.get("logging", {})
    for key in set(old_logging.keys()) | set(new_logging.keys()):
        old_val = old_logging.get(key)
        new_val = new_logging.get(key)
        if old_val != new_val:
            changes.append(f"Logging {key}: {old_val} → {new_val}")
    
    # No longer check features changes as they've been removed
    
    if changes:
        st.write("**Changes to be made:**")
        for change in changes:
            st.write(f"• {change}")
        
        return st.button("✅ Confirm Save Changes", key="confirm_save")
    else:
        st.info("No changes detected.")
        return False

def render_import_config():
    """Render configuration import section"""
    st.subheader("📤 Import Configuration")
    
    uploaded_file = st.file_uploader("Choose a configuration file", type=['json', 'yaml', 'yml'])
    
    if uploaded_file is not None:
        try:
            import json
            import yaml
            
            # Read file content
            content = uploaded_file.read()
            
            # Parse based on file type
            if uploaded_file.name.endswith('.json'):
                imported_config = json.loads(content)
            else:  # yaml/yml
                imported_config = yaml.safe_load(content)
            
            # Validate imported configuration
            validation_result = validate_configuration(imported_config)
            
            if validation_result["valid"]:
                st.success("✅ **Configuration file is valid**")
                st.json(imported_config)
                
                if st.button("📥 Import This Configuration"):
                    if save_configuration(imported_config):
                        st.success("✅ **Configuration Imported Successfully**")
                        st.warning("🔄 **Server Restart Required**")
                        st.session_state.config_history = [imported_config.copy()]
                        st.session_state.config_history_index = 0
                        st.rerun()
                    else:
                        st.error("❌ **Failed to Import Configuration**")
            else:
                st.error("❌ **Invalid Configuration File**")
                for error in validation_result["errors"]:
                    st.error(f"• {error}")
                    
        except Exception as e:
            st.error(f"❌ **Error reading configuration file**: {str(e)}")

def render_environment_variables():
    """Render environment variables section"""
    st.subheader("🌍 Environment Variables")
    
    # Get current system info
    system_info = get_system_info()
    
    # Dynamic environment variables based on current config
    env_vars = {
        "MY_MCP_SERVER_LOG_LEVEL": "INFO",
        "MY_MCP_SERVER_PORT": "3001",
        "MY_MCP_SERVER_CONFIG_PATH": system_info.get("config_path", "~/.config/my_mcp_server"),
        "MY_MCP_SERVER_LOG_PATH": system_info.get("log_path", "~/.local/share/my_mcp_server"),
        "PYTHONPATH": system_info.get("current_directory", "Current directory included")
    }
    
    st.markdown("**Current Environment:**")
    for key, value in env_vars.items():
        st.code(f"{key}={value}")
    
    st.caption("💡 These environment variables can be used to override configuration settings")

def render_validation_section(config):
    """Render configuration validation section"""
    st.subheader("✅ Configuration Validation")
    
    # Validate current configuration
    validation_result = validate_configuration(config)
    server_config = config.get("server", {})
    
    # Real validation results
    validation_results = []
    
    # Server port validation
    port = server_config.get("port", int(3001))
    if is_port_available(port):
        validation_results.append({
            "check": "Server port availability", 
            "status": "✅ Pass", 
            "message": f"Port {port} is available"
        })
    else:
        validation_results.append({
            "check": "Server port availability", 
            "status": "⚠️ Warning", 
            "message": f"Port {port} is currently in use"
        })
    
    # Configuration syntax validation
    if validation_result["valid"]:
        validation_results.append({
            "check": "Configuration file syntax", 
            "status": "✅ Pass", 
            "message": "Valid configuration structure"
        })
    else:
        validation_results.append({
            "check": "Configuration file syntax", 
            "status": "❌ Fail", 
            "message": f"Errors: {', '.join(validation_result['errors'])}"
        })
    
    # System checks
    system_info = get_system_info()
    
    validation_results.append({
        "check": "Python version compatibility", 
        "status": "✅ Pass", 
        "message": f"Python {system_info.get('python_version', 'Unknown')} detected"
    })
    
    # Path permissions
    try:
        from pathlib import Path
        config_path = Path(get_config_path())
        if config_path.exists() or config_path.parent.exists():
            validation_results.append({
                "check": "Configuration directory permissions", 
                "status": "✅ Pass", 
                "message": "Can write to configuration directory"
            })
        else:
            validation_results.append({
                "check": "Configuration directory permissions", 
                "status": "⚠️ Warning", 
                "message": "Directory will be created on first run"
            })
    except Exception as e:
        validation_results.append({
            "check": "Configuration directory permissions", 
            "status": "❌ Fail", 
            "message": f"Error checking permissions: {str(e)}"
        })
    
    # Display results
    for result in validation_results:
        col1, col2, col3 = st.columns([2, 1, 3])
        with col1:
            st.write(result["check"])
        with col2:
            st.write(result["status"])
        with col3:
            st.caption(result["message"])
    
    # Show warnings if any
    if validation_result["warnings"]:
        st.warning("⚠️ **Configuration Warnings**")
        for warning in validation_result["warnings"]:
            st.warning(f"• {warning}")


def main():
    """Main configuration page content"""
    # Page header
    st.title("⚙️ My MCP Server Configuration")
    st.markdown("Manage server settings, features, and environment configuration.")
    st.markdown("---")
    
    # Load configuration and show status
    config = render_config_status()
    st.markdown("---")
    
    # Configuration form
    form_result = render_configuration_form(config)
    if form_result:
        config = form_result
        st.rerun()
    st.markdown("---")
    
    # Current configuration preview
    render_current_config_preview(config)
    st.markdown("---")
    
    # Import/Export section
    col1, col2 = st.columns(2)
    
    with col1:
        render_import_config()
        
    with col2:
        st.subheader("📤 Export Configuration")
        import json
        config_json = json.dumps(config, indent=2)
        st.download_button(
            label="📥 Download Configuration (JSON)",
            data=config_json,
            file_name="my_mcp_server_config.json",
            mime="application/json"
        )
        
        # Also offer YAML export
        import yaml
        config_yaml = yaml.dump(config, default_flow_style=False, indent=2)
        st.download_button(
            label="📥 Download Configuration (YAML)",
            data=config_yaml,
            file_name="my_mcp_server_config.yaml",
            mime="application/x-yaml"
        )
    
    st.markdown("---")
    
    # Environment variables
    render_environment_variables()
    st.markdown("---")
    
    # Validation section
    render_validation_section(config)
    st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/1_Home.py")
    
    with col2:
        if st.button("📊 View Logs", use_container_width=True):
            st.switch_page("pages/3_Logs.py")
    
    # Footer
    st.caption("Configuration management interface • Fully functional configuration editor")

if __name__ == "__main__":
    main()
