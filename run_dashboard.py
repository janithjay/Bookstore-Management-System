"""
Quick launcher for Bookstore Dashboard
Run this file to start the Streamlit dashboard
"""

import os
import sys
from pathlib import Path

def main():
    """Launch the Streamlit dashboard"""
    # Get the project root directory
    project_root = Path(__file__).parent
    ui_app = project_root / "ui" / "streamlit_app.py"
    
    # Check if the app file exists
    if not ui_app.exists():
        print(f"❌ Error: Cannot find {ui_app}")
        print(f"   Make sure you're running this from the project root directory")
        sys.exit(1)
    
    # Check if streamlit is installed
    try:
        import streamlit
    except ImportError:
        print("❌ Error: Streamlit is not installed")
        print("   Install it with: pip install streamlit")
        sys.exit(1)
    
    print("🚀 Starting Bookstore Management Dashboard...")
    print(f"📂 Project root: {project_root}")
    print(f"🎯 App location: {ui_app}")
    print()
    print("💡 The dashboard will open in your browser at http://localhost:8501")
    print("💡 Press Ctrl+C to stop the server")
    print()
    
    # Launch streamlit
    os.system(f'streamlit run "{ui_app}"')

if __name__ == "__main__":
    main()
