"""CSS styling and theming for Post-fix Test MCP Admin UI

This module provides custom CSS styles and theming for the Streamlit admin interface,
ensuring consistent visual design and improved user experience.
"""

import streamlit as st
from typing import Optional

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit application"""
    
    custom_css = """
    <style>
    /* Main application styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2e86c1 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-weight: 600;
        font-size: 2.5rem;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .status-card {
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: box-shadow 0.3s ease;
    }
    
    .status-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .status-card-success {
        border-left: 4px solid #28a745;
    }
    
    .status-card-warning {
        border-left: 4px solid #ffc107;
    }
    
    .status-card-error {
        border-left: 4px solid #dc3545;
    }
    
    .status-card-info {
        border-left: 4px solid #17a2b8;
    }
    
    /* Metrics styling */
    .metric-container {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin: 0.25rem 0 0 0;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4 0%, #2e86c1 100%);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #1a6fa0 0%, #2874a6 100%);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-1px);
    }
    
    .stButton > button:disabled {
        background: #6c757d;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    /* Navigation styling */
    .css-1544g2n {
        padding: 0;
    }
    
    /* Table styling */
    .dataframe {
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead {
        background: #f8f9fa;
    }
    
    .dataframe th {
        padding: 0.75rem;
        font-weight: 600;
        color: #495057;
        border-bottom: 2px solid #dee2e6;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    .dataframe tbody tr:hover {
        background-color: #f8f9fa;
    }
    
    /* Alert styling */
    .alert {
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border: 1px solid transparent;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border-color: #b8daff;
        color: #0c5460;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border-color: #ffeaa7;
        color: #856404;
    }
    
    .alert-error {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
    }
    
    .alert-success {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
    
    /* Code styling */
    .stCode {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px;
        font-family: 'Monaco', 'Consolas', 'Courier New', monospace;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 6px 6px 0 0;
        font-weight: 500;
    }
    
    /* Form styling */
    .stForm {
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 0.5rem;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #1f77b4;
        box-shadow: 0 0 0 0.2rem rgba(31, 119, 180, 0.25);
        outline: none;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1f77b4 0%, #2e86c1 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8f9fa;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        border: 1px solid #e9ecef;
    }
    
    .stTabs [aria-selected="true"] {
        background: #1f77b4;
        color: white;
        border-color: #1f77b4;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom footer */
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        color: #6c757d;
        text-align: center;
        padding: 0.5rem;
        font-size: 0.8rem;
        border-top: 1px solid #e9ecef;
        z-index: 999;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .main-header h1 {
            font-size: 2rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .status-card {
            background: #2d3748;
            border-color: #4a5568;
            color: #e2e8f0;
        }
        
        .metric-container {
            background: #2d3748;
            border-color: #4a5568;
            color: #e2e8f0;
        }
        
        .dataframe {
            background: #2d3748;
            color: #e2e8f0;
        }
        
        .dataframe thead {
            background: #4a5568;
        }
    }
    
    /* Loading spinner customization */
    .stSpinner > div {
        border-top-color: #1f77b4 !important;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        border-radius: 6px;
    }
    
    .stError {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        border-radius: 6px;
    }
    
    .stWarning {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        border-radius: 6px;
    }
    
    .stInfo {
        background: #d1ecf1;
        border: 1px solid #b8daff;
        color: #0c5460;
        border-radius: 6px;
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def apply_theme(theme_name: str = "default"):
    """
    Apply a specific theme to the application
    
    Args:
        theme_name: Name of the theme to apply ("default", "dark", "light", "blue")
    """
    
    themes = {
        "default": {
            "primary_color": "#1f77b4",
            "background_color": "#ffffff",
            "secondary_background": "#f8f9fa",
            "text_color": "#262730"
        },
        "dark": {
            "primary_color": "#4CAF50",
            "background_color": "#0e1117",
            "secondary_background": "#262730",
            "text_color": "#fafafa"
        },
        "light": {
            "primary_color": "#FF6B6B",
            "background_color": "#ffffff",
            "secondary_background": "#f0f2f6",
            "text_color": "#262730"
        },
        "blue": {
            "primary_color": "#2196F3",
            "background_color": "#ffffff",
            "secondary_background": "#e3f2fd",
            "text_color": "#1a1a1a"
        }
    }
    
    if theme_name not in themes:
        theme_name = "default"
    
    theme = themes[theme_name]
    
    theme_css = """
    <style>
    :root {
        --primary-color: """ + theme["primary_color"] + """;
        --background-color: """ + theme["background_color"] + """;
        --secondary-background: """ + theme["secondary_background"] + """;
        --text-color: """ + theme["text_color"] + """;
    }
    
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }
    
    .stButton > button {
        background: var(--primary-color);
        color: white;
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-color) 100%);
    }
    
    .metric-value {
        color: var(--primary-color);
    }
    </style>
    """
    
    st.markdown(theme_css, unsafe_allow_html=True)

def apply_custom_fonts():
    """Apply custom font styling"""
    
    font_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    </style>
    """
    
    st.markdown(font_css, unsafe_allow_html=True)

def create_status_indicator(status: str, size: str = "medium") -> str:
    """
    Create a colored status indicator
    
    Args:
        status: Status type ("success", "warning", "error", "info")
        size: Size of indicator ("small", "medium", "large")
        
    Returns:
        HTML string for status indicator
    """
    
    colors = {
        "success": "#28a745",
        "warning": "#ffc107", 
        "error": "#dc3545",
        "info": "#17a2b8",
        "unknown": "#6c757d"
    }
    
    sizes = {
        "small": "8px",
        "medium": "12px",
        "large": "16px"
    }
    
    color = colors.get(status.lower(), colors["unknown"])
    indicator_size = sizes.get(size, sizes["medium"])
    
    return f"""
    <span style="
        display: inline-block;
        width: {indicator_size};
        height: {indicator_size};
        background-color: {color};
        border-radius: 50%;
        margin-right: 0.5rem;
        vertical-align: middle;
    "></span>
    """

def create_badge(text: str, color: str = "primary") -> str:
    """
    Create a styled badge
    
    Args:
        text: Badge text
        color: Badge color ("primary", "success", "warning", "error", "info")
        
    Returns:
        HTML string for badge
    """
    
    colors = {
        "primary": {"bg": "#1f77b4", "text": "#ffffff"},
        "success": {"bg": "#28a745", "text": "#ffffff"},
        "warning": {"bg": "#ffc107", "text": "#212529"},
        "error": {"bg": "#dc3545", "text": "#ffffff"},
        "info": {"bg": "#17a2b8", "text": "#ffffff"},
        "secondary": {"bg": "#6c757d", "text": "#ffffff"}
    }
    
    badge_colors = colors.get(color, colors["primary"])
    
    return f"""
    <span style="
        background-color: {badge_colors['bg']};
        color: {badge_colors['text']};
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 500;
        display: inline-block;
    ">{text}</span>
    """

def apply_page_config(page_title: str, page_icon: str = "🛠️", layout: str = "wide"):
    """
    Apply consistent page configuration
    
    Args:
        page_title: Title for the page
        page_icon: Icon for the page
        layout: Layout type ("wide" or "centered")
    """
    
    st.set_page_config(
        page_title=f"Post-fix Test MCP - {page_title}",
        page_icon=page_icon,
        layout=layout,
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': f"Post-fix Test MCP Admin UI v0.1.0"
        }
    )

def hide_streamlit_style():
    """Hide Streamlit's default styling elements"""
    
    hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """
    
    st.markdown(hide_style, unsafe_allow_html=True)
