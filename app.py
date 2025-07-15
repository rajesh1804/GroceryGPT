# app.py
import os
import sys
import streamlit.web.cli as stcli

# Add the app directory to path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app/streamlit_app.py"]
    sys.exit(stcli.main())
