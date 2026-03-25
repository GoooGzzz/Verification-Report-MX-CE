"""
Configuration settings for Samsung Field Intelligence Dashboard
"""
import os
from typing import List

# Application Settings
APP_TITLE = "SmartSense-LTD | Samsung Field Intelligence"
APP_ICON = "📊"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Authentication
PASSWORD = os.getenv('APP_PASSWORD', 'solidspy')  # TODO: Change default password

# Data Processing
REQUIRED_COLUMNS: List[str] = [
    'W', 'Shop Code', 'Shop Name', 'Brand', 'Model',
    'Sellout', 'Shelf Share', 'Price', 'Project',
    'Category', 'Price segmentation'
]

# UI Settings
MAX_FILE_SIZE_MB = 50
SUPPORTED_FILE_TYPES = ['xlsx', 'xls']

# AI Settings
ANTHROPIC_MODEL = "claude-3-haiku-20240307"
MAX_TOKENS = 4000
TEMPERATURE = 0.7

# Cache Settings
CACHE_TTL_HOURS = 1

# One UI 8 Color Palette
ONEUI_COLORS = {
    'primary': '#007aff',
    'secondary': '#636366',
    'surface': '#ffffff',
    'surface_variant': '#f2f2f7',
    'on_surface': '#1c1c1e',
    'on_surface_variant': '#3a3a3c',
    'outline': '#c6c6c8',
    'error': '#ff3b30',
    'success': '#34c759',
    'warning': '#ff9500'
}

# Border Radius
ONEUI_RADIUS = {
    'small': '8px',
    'medium': '12px',
    'large': '16px',
    'xlarge': '28px'
}