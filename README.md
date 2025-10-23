# 📚 Bookstore Management System

A sophisticated multi-agent simulation system for bookstore operations with ontology-based reasoning and real-time analytics.

## 🌟 Overview

This system simulates a complete bookstore ecosystem using:
- **Multi-Agent Architecture**: Customer, Employee, and Book agents with autonomous behaviors
- **Ontology Integration**: Owlready2-based semantic reasoning with SWRL rules
- **Message Bus Communication**: Asynchronous agent coordination
- **Real-Time Dashboard**: Production-ready Streamlit UI with interactive visualizations
- **Mesa Framework**: Agent-based modeling with data collection and analytics

## 🚀 Quick Start

### Prerequisites

**Java Runtime Environment (JRE) 17 or higher** is required for Pellet reasoner functionality.

- **Windows**: Install via winget:
  ```powershell
  winget install --id EclipseAdoptium.Temurin.17.JRE
  ```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/janithjay/Bookstore-Management-System
cd Bookstore-Management-System
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

venv\Scripts\activate


3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the System

#### Option 1: Quick Launch 🚀

Simply double-click `run.bat` or run:
```bash
.\run.bat
```

This automatically handles Java PATH setup and launches the dashboard.

#### Option 2: Manual Launch 🎨

**Windows PowerShell:**
```powershell
$env:Path = "C:\Program Files\Eclipse Adoptium\jre-17.0.16.8-hotspot\bin;" + $env:Path
streamlit run ui/streamlit_app.py
```


The dashboard provides:
- Interactive simulation controls
- Detailed analytics and reports
- Export capabilities