"""Documentation viewer page for {{cookiecutter.project_name}} Admin UI

This page displays project documentation from markdown files, providing
easy access to README, developer guides, and other documentation.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(parent_dir))

# Note: Page configuration is handled by main app.py

def load_markdown_file(file_path: Path) -> str:
    """
    Load and return the contents of a markdown file
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        String contents of the file or error message
    """
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return f"*File not found: {file_path.name}*"
    except Exception as e:
        return f"*Error loading file: {str(e)}*"

def render_documentation_content():
    """Render the documentation content with tabs for different docs"""
    
    # Get the project root directory (parent of ui directory)
    project_root = Path(__file__).parent.parent.parent
    
    # Define available documentation files
    doc_files = {
        "README": project_root / "README.md",
        "Developer Guide": project_root / "DEVELOPER_GUIDE.md", 
        "Development": project_root / "DEVELOPMENT.md",
        "Setup Guide": project_root / "SETUP_PROMPT.md"
    }
    
    # Check which files exist
    available_docs = {name: path for name, path in doc_files.items() if path.exists()}
    
    if not available_docs:
        # No local docs found, show helpful message about where to find docs
        st.info("📚 **Quick Start Documentation**")
        st.markdown("""
        This MCP server was generated from the SAAGA Cookie Cutter template.
        
        **Getting Started:**
        1. Test your server with MCP Inspector: `mcp dev {{cookiecutter.__project_slug}}/server/app.py`
        2. Run the example client: `{{cookiecutter.__project_slug}}-client "Hello World"`
        3. View logs in this UI (Logs page)
        
        **Key Files:**
        - `server/app.py` - Main MCP server implementation
        - `tools/example_tools.py` - Example tool implementations
        - `config.py` - Configuration management
        
        **Testing:**
        - Run tests: `pytest tests/`
        - Test correlation IDs: `python tests/integration/test_correlation.py`
        
        For detailed documentation, check the project repository or the external resources below.
        """)
        return
    
    # Create tabs for available documentation
    if len(available_docs) == 1:
        # Single document - no tabs needed
        name, path = list(available_docs.items())[0]
        content = load_markdown_file(path)
        st.markdown(content)
    else:
        # Multiple documents - use tabs
        tab_names = list(available_docs.keys())
        tabs = st.tabs(tab_names)
        
        for tab, (name, path) in zip(tabs, available_docs.items()):
            with tab:
                content = load_markdown_file(path)
                st.markdown(content)

def render_external_links():
    """Render links to external MCP documentation"""
    with st.expander("🔗 External Resources"):
        st.markdown("""
        ### MCP Documentation
        - [Official MCP Documentation](https://modelcontextprotocol.io/docs)
        - [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
        - [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
        - [MCP Inspector Tool](https://github.com/modelcontextprotocol/inspector)
        
        ### Community Resources
        - [MCP GitHub Repository](https://github.com/modelcontextprotocol)
        - [MCP Discord Community](https://discord.gg/modelcontextprotocol)
        """)

def main():
    """Main documentation page content"""
    # Page header
    st.title("📖 {{cookiecutter.project_name}} Documentation")
    st.markdown("Browse project documentation and resources.")
    st.markdown("---")
    
    # Render documentation content
    render_documentation_content()
    
    st.markdown("---")
    
    # External resources
    render_external_links()
    
    st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/1_Home.py")
    
    with col2:
        if st.button("⚙️ Configuration", use_container_width=True):
            st.switch_page("pages/2_Configuration.py")
    
    # Footer
    st.caption("Documentation viewer • Displays markdown files from project root")

if __name__ == "__main__":
    main()