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

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Bookstore-Management-System
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the System

#### Option 1: Web Dashboard (Recommended) 🎨

Launch the interactive Streamlit dashboard:

```bash
streamlit run ui/streamlit_app.py
```

The dashboard provides:
- Real-time metrics and visualizations
- Interactive simulation controls
- Detailed analytics and reports
- Export capabilities

**See [UI Documentation](ui/README.md) for detailed dashboard guide**

#### Option 2: Command Line Interface 💻

Run headless simulation with terminal output:

```bash
python main.py --customers 20 --employees 5 --books 100 --hours 8
```

Available arguments:
- `--customers N`: Number of customer agents (default: 20)
- `--employees N`: Number of employee agents (default: 5)
- `--books N`: Number of books in catalog (default: 100)
- `--hours N`: Simulation duration in hours (default: 8)
- `--seed N`: Random seed for reproducibility (optional)
- `--checkpoint N`: Save checkpoints every N steps (default: 30)
- `--output DIR`: Output directory for reports (default: ./report)

Example:
```bash
python main.py --customers 50 --employees 10 --hours 12 --seed 42
```

## 📊 System Architecture

### Agent Types

#### 1. Customer Agents 🛒
- **States**: Browsing, Evaluating, Purchasing, Seeking Help
- **Behaviors**: 
  - Browse books by category/price
  - Add items to cart with stock validation
  - Complete purchases with discount application
  - Request employee assistance
  - Provide satisfaction feedback

#### 2. Employee Agents 👥
- **Roles**: Cashier, Sales Associate, Manager, Inventory Clerk, Customer Service
- **Responsibilities**:
  - Process customer transactions
  - Handle inventory restocking
  - Respond to customer inquiries
  - Monitor stock levels
  - Track performance metrics

#### 3. Book Agents 📖
- **Properties**: ISBN, title, author, category, price, stock
- **Dynamics**:
  - Dynamic pricing based on demand
  - Market trends simulation
  - Sales processing with inventory sync
  - Automatic restocking triggers
  - Demand prediction

### Data Flow

```
┌─────────────────┐
│   Ontology      │  ← Central knowledge repository
│  (Owlready2)    │     - Books, Customers, Employees
└────────┬────────┘     - Transactions, Inventory
         │              - Business rules (SWRL)
         │
    ┌────┴────┐
    │ Message │          ← Asynchronous communication
    │   Bus   │             - PURCHASE_REQUEST
    └────┬────┘             - RESTOCK_REQUEST
         │                  - INVENTORY_UPDATE
    ┌────┴─────────────────┐
    │                      │
┌───▼────┐  ┌─────▼──────┐  ┌───▼─────┐
│Customer│  │  Employee  │  │  Book   │
│ Agents │  │   Agents   │  │ Agents  │
└───┬────┘  └─────┬──────┘  └───┬─────┘
    │             │             │
    └─────────────┴─────────────┘
               │
        ┌──────▼──────┐
        │ Bookstore   │  ← Simulation orchestration
        │    Model    │     - Transaction processing
        │   (Mesa)    │     - Data collection
        └─────────────┘     - Analytics
```

### Synchronization

The system ensures data consistency through:

1. **Inventory Synchronization**: `book.stock_quantity` ↔ `inventory.current_stock`
2. **Transaction Validation**: Stock checked before processing
3. **Sales Tracking**: Employee sales = actual completed transactions
4. **Revenue Calculation**: Includes customer discounts
5. **Real-time Updates**: Message bus notifications for inventory changes

## 📈 Features

### Business Metrics
- ✅ **Revenue Tracking**: Real-time with discount application
- ✅ **Transaction Processing**: Validated with stock checking
- ✅ **Inventory Management**: Auto-restocking and low-stock alerts
- ✅ **Customer Satisfaction**: Feedback-based rating system
- ✅ **Employee Performance**: Sales, customer service, ratings

### Technical Features
- ✅ **Ontology Reasoning**: SWRL rules for business logic
- ✅ **Message-Based Communication**: Decoupled agent interaction
- ✅ **Data Collection**: Time-series analytics with Mesa
- ✅ **Checkpointing**: Periodic state snapshots
- ✅ **Report Generation**: JSON exports with complete metrics
- ✅ **Web Dashboard**: Real-time visualization with Streamlit

### Analytics
- Top performing books by sales
- Employee performance rankings
- Customer spending patterns
- Inventory turnover rates
- Revenue trends over time
- Category-wise sales breakdown

## 🗂️ Project Structure

```
Bookstore-Management-System/
├── main.py                      # CLI entry point
├── run_dashboard.py             # Dashboard launcher
├── requirements.txt             # Python dependencies
│
├── agents/                      # Agent implementations
│   ├── book_agent.py           # Book agent with pricing
│   ├── customer_agent.py       # Customer state machine
│   └── employee_agent.py       # Role-based employees
│
├── simulation/                  # Mesa simulation
│   └── bookstore_model.py      # Model orchestration
│
├── ontology/                    # Knowledge base
│   └── bookstore_ontology.py   # Owlready2 ontology + SWRL
│
├── communication/               # Message bus
│   └── message_bus.py          # Priority queue system
│
├── ui/                         # Web dashboard
│   ├── streamlit_app.py        # Main Streamlit app
│   ├── README.md               # UI documentation
│   ├── components/             # UI components
│   └── utils/                  # Helper utilities
│
└── report/                     # Output directory
    ├── simulation_report_*.json
    ├── data/
    │   ├── agent_analytics.csv
    │   └── checkpoint_*.json
    ├── charts/                 # Generated charts
    └── logs/                   # Simulation logs
```

## 🔧 Configuration

### Simulation Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| num_customers | int | 5-100 | 20 | Customer agent count |
| num_employees | int | 2-20 | 5 | Employee agent count |
| num_books | int | 20-500 | 100 | Books in catalog |
| simulation_hours | int | 1-24 | 8 | Simulation duration |
| seed | int | any | None | Random seed |
| checkpoint_interval | int | >0 | 30 | Steps between saves |

### Book Categories
- Fiction, Non-Fiction, Science Fiction, Mystery, Romance
- Biography, History, Science, Self-Help, Business
- Children, Young Adult, Comics, Poetry, Drama

### Employee Roles
- **Cashier**: Fast transaction processing
- **Sales Associate**: High customer service
- **Manager**: Balanced performance
- **Inventory Clerk**: Efficient restocking
- **Customer Service**: Excellence in assistance

## 📊 Output & Reports

### Dashboard View
- Real-time metrics cards
- Interactive Plotly charts
- Detailed agent analytics
- Export to CSV/JSON

### CLI Output
```
=== Bookstore Simulation Report ===
Simulation Time: 8h 0m 0s
Total Steps: 480

Business Metrics:
  Revenue: $2,456.78
  Transactions: 157
  Avg Transaction: $15.65
  Customer Satisfaction: 8.3/10

Inventory Status:
  Total Stock: 2,543 units
  Low Stock Items: 12
  Inventory Alerts: 3

Top Employees:
  1. Alice Johnson - $487.35 (42 customers)
  2. Bob Smith - $445.12 (38 customers)
  ...
```

### JSON Reports
Saved to `report/simulation_report_YYYYMMDD_HHMMSS.json`:
```json
{
  "simulation_config": {...},
  "business_metrics": {...},
  "agent_performance": {...},
  "inventory_status": {...},
  "top_books": [...],
  "employee_performance": [...]
}
```

## 🧪 Testing & Validation

### Quick Test
```bash
python main.py --customers 10 --employees 3 --hours 1 --seed 123
```

Expected results:
- ✅ Revenue > 0
- ✅ Transactions > 0
- ✅ Employee sales match revenue
- ✅ Inventory decreases with sales
- ✅ No negative stock values

### Performance Benchmarks
- **Small**: 20 customers, 5 employees → ~0.1s/step
- **Medium**: 50 customers, 10 employees → ~0.3s/step
- **Large**: 100 customers, 20 employees → ~0.8s/step

## 🐛 Known Issues & Solutions

### Issue: "Data not syncing"
**Solution**: Fixed in current version. Book stock now syncs with inventory objects.

### Issue: "Employee sales don't match revenue"
**Solution**: Fixed. Employees now track completed transactions only.

### Issue: "Multiple books per transaction"
**Behavior**: Expected. Customers can purchase 1-3 books per transaction.

## 🛠️ Development

### Dependencies
- Python 3.8+
- Mesa 3.0+ (agent-based modeling)
- Owlready2 0.44+ (ontology)
- Pandas, NumPy (analytics)
- Streamlit 1.28+ (UI)
- Plotly 5.15+ (visualization)

### Contributing
1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Submit pull request

### Code Style
- Black formatting
- Type hints recommended
- Docstrings for public methods

## 📚 Documentation

- **[UI Documentation](ui/README.md)**: Complete dashboard guide
- **Code Comments**: Inline documentation in all files
- **Type Hints**: Full type annotations for clarity

## 🎯 Use Cases

### Business Analysis
- Test staffing strategies
- Optimize inventory levels
- Analyze pricing impacts
- Forecast demand patterns

### Research & Education
- Study multi-agent systems
- Demonstrate ontology reasoning
- Teach agent communication
- Explore emergent behaviors

### Software Testing
- Validate synchronization
- Stress test transactions
- Test inventory algorithms
- Performance benchmarking

## 📄 License

See LICENSE file for details.

## 🙏 Acknowledgments

Built with:
- [Mesa](https://github.com/projectmesa/mesa) - Agent-based modeling
- [Owlready2](https://bitbucket.org/jibalamy/owlready2) - Ontology framework
- [Streamlit](https://streamlit.io/) - Dashboard framework
- [Plotly](https://plotly.com/) - Interactive visualizations

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: 2024
