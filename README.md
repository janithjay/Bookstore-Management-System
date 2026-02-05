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
```


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
- Real-time analytics and visualizations
- Detailed reports and export capabilities

## 📋 Features

### Multi-Agent System
- **Customer Agents**: Autonomous customers with shopping behaviors, budgets, and preferences
- **Employee Agents**: Staff members handling customer service and sales
- **Book Agents**: Inventory management with demand tracking and stock alerts

### Ontology-Based Reasoning
- **Owlready2 Integration**: Semantic web reasoning with OWL ontology
- **SWRL Rules**: Business logic rules for inventory and customer classification
- **Pellet Reasoner**: Automatic inference and consistency checking

### Communication System
- **Message Bus**: Asynchronous agent communication
- **Event-Driven Architecture**: Real-time notifications and alerts
- **Transaction Processing**: Order management and fulfillment

### Analytics Dashboard
- **Real-Time Monitoring**: Live simulation metrics and KPIs
- **Interactive Visualizations**: Plotly charts for revenue, inventory, and activity
- **Data Export**: Excel and CSV export capabilities
- **Customizable Parameters**: Adjust agents, duration, and simulation settings

## 🏗️ Project Structure

```
Bookstore-Management-System/
├── agents/                   # Agent implementations
│   ├── book_agent.py        # Book inventory management
│   ├── customer_agent.py    # Customer behavior simulation
│   └── employee_agent.py    # Employee service logic
├── communication/           # Message bus system
│   └── message_bus.py      # Event-driven communication
├── ontology/               # Ontology definitions
│   └── bookstore_ontology.py  # OWL ontology with SWRL rules
├── simulation/             # Mesa simulation model
│   └── bookstore_model.py  # Core simulation logic
├── ui/                     # User interface
│   └── streamlit_app.py    # Streamlit dashboard
├── diagrams/               # System diagrams
├── main.py                 # CLI simulation runner
├── run_dashboard.py        # Dashboard launcher
├── run.bat                 # Windows quick start script
└── requirements.txt        # Python dependencies
```

## 💻 Command-Line Usage

### Basic Simulation

Run a simulation from the command line:

```bash
python main.py
```

### Advanced Options

```bash
python main.py --customers 50 --employees 10 --books 200 --hours 12
```

**Available Arguments:**
- `--customers N`: Number of customer agents (default: 20)
- `--employees N`: Number of employee agents (default: 5)
- `--books N`: Number of book agents (default: 100)
- `--hours N`: Simulation duration in hours (default: 8)
- `--steps N`: Maximum simulation steps (overrides hours)
- `--seed N`: Random seed for reproducibility
- `--output DIR`: Output directory for reports (default: ./report)
- `--verbose`: Enable detailed logging
- `--report`: Generate comprehensive JSON report
- `--quick`: Quick test run (1 hour, fewer agents)

### Examples

**Quick test run:**
```bash
python main.py --quick
```

**Reproducible simulation:**
```bash
python main.py --seed 42 --hours 24 --report
```

**Large-scale simulation:**
```bash
python main.py --customers 100 --employees 20 --books 500 --hours 16 --verbose
```

## 🖥️ System Requirements

- **Python**: 3.8 or higher
- **Java Runtime Environment (JRE)**: 17+ (required for Pellet reasoner)
- **Memory**: 4GB RAM minimum (8GB recommended for large simulations)
- **OS**: Windows, macOS, or Linux

## 🐧 Linux/macOS Installation

### Prerequisites

Install Java Runtime Environment:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install openjdk-17-jre
```

**macOS:**
```bash
brew install openjdk@17
```

### Setup

```bash
# Clone repository
git clone https://github.com/janithjay/Bookstore-Management-System
cd Bookstore-Management-System

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run ui/streamlit_app.py
```

## 🔧 Troubleshooting

### Java Not Found Error

**Problem**: `Pellet reasoner not available` or Java-related errors

**Solution (Windows)**:
```powershell
# Add Java to PATH
$env:Path = "C:\Program Files\Eclipse Adoptium\jre-17.0.16.8-hotspot\bin;" + $env:Path
```

**Solution (Linux/macOS)**:
```bash
# Find Java installation
which java
# Add to PATH in ~/.bashrc or ~/.zshrc
export PATH="/usr/lib/jvm/java-17-openjdk/bin:$PATH"
```

### Module Not Found Errors

**Problem**: `ModuleNotFoundError: No module named 'mesa'`

**Solution**:
```bash
pip install -r requirements.txt
```

Ensure you're in the activated virtual environment.

### Streamlit Port Already in Use

**Problem**: `Address already in use` error

**Solution**:
```bash
streamlit run ui/streamlit_app.py --server.port 8502
```

### Memory Issues with Large Simulations

**Problem**: System slows down or crashes with many agents

**Solution**: Reduce the number of agents or simulation duration:
```bash
python main.py --customers 20 --employees 5 --books 50 --hours 4
```

## 🧪 Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📊 Architecture

### Agent-Based Modeling (Mesa)
The simulation uses the Mesa framework for agent-based modeling, allowing autonomous agents to interact in a shared environment with emergent behaviors.

### Ontology Layer (Owlready2)
Semantic web technologies provide:
- Formal knowledge representation
- Automated reasoning and inference
- Business rule enforcement
- Data validation and consistency

### Communication Layer
A message bus enables:
- Decoupled agent communication
- Event-driven responses
- Scalable multi-agent coordination

## 📄 License

This project is available for educational and research purposes.

## 👏 Credits

Built with:
- [Mesa](https://mesa.readthedocs.io/) - Agent-based modeling framework
- [Owlready2](https://owlready2.readthedocs.io/) - Ontology manipulation library
- [Streamlit](https://streamlit.io/) - Interactive dashboard framework
- [Plotly](https://plotly.com/) - Data visualization library

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact the repository maintainer.

---

Made with ❤️ for agent-based systems and semantic web technologies