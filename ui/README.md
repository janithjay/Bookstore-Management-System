# Bookstore Management System - UI Dashboard

A production-ready Streamlit dashboard for real-time simulation monitoring and control.

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Dashboard

**Option 1: Using Streamlit directly**
```bash
streamlit run ui/streamlit_app.py
```

**Option 2: From project root**
```bash
cd d:\Github\Bookstore-Management-System
python -m streamlit run ui/streamlit_app.py
```

The dashboard will open automatically in your default browser at `http://localhost:8501`

## 📊 Features

### Real-Time Monitoring
- **Live Metrics Dashboard**: Track revenue, transactions, customer satisfaction, and inventory in real-time
- **Interactive Charts**: Dynamic visualizations using Plotly for revenue trends, customer activity, and inventory levels
- **Multi-Agent Analytics**: Detailed insights into agent behavior and performance

### Simulation Control
- **Start/Stop/Reset**: Full control over simulation execution
- **Parameter Configuration**: Adjust customers, employees, books, and simulation duration via intuitive sliders
- **Real-time Mode**: Step-by-step execution with configurable delays for detailed observation
- **Batch Mode**: Fast execution for long simulations

### Analytics & Insights
- **Top Performing Books**: Track best sellers with sales, pricing, and stock data
- **Employee Performance**: Monitor individual employee sales, customer service, and ratings
- **Customer Insights**: Analyze customer behavior, spending patterns, and satisfaction
- **Inventory Management**: Real-time stock levels and low-stock alerts

### Export & Reporting
- **CSV Export**: Download simulation data for external analysis
- **Historical Reports**: Access past simulation results
- **Detailed Analytics**: Comprehensive multi-metric analysis

## 🎨 Dashboard Sections

### 1. Sidebar - Configuration Panel
- **Agent Configuration**: Set number of customers (5-100), employees (2-20), books (20-500)
- **Time Configuration**: Simulation duration (1-24 hours)
- **Advanced Settings**: Random seed, real-time mode, step delay
- **Control Buttons**: Start, Stop, Reset

### 2. Main Dashboard - Key Metrics
Top row displays:
- 💰 Total Revenue (with transaction count)
- 🛒 Average Transaction Value (with customers served)
- 😊 Customer Satisfaction (with active customers)
- 📦 Inventory Status (with low stock alerts)

Second row shows:
- ⏱️ Simulation Time (current time in simulation)
- 👥 Busy Employees (active/total ratio)
- 📚 Total Books (catalog size)
- ⚠️ Inventory Alerts (critical stock warnings)

### 3. Real-Time Charts
- **Revenue Over Time**: Line chart with area fill showing cumulative revenue
- **Transactions Over Time**: Track total transactions completed
- **Active Customers**: Monitor customer activity throughout simulation
- **Inventory Levels**: Watch stock changes in real-time

### 4. Detailed Analytics Tabs

**📚 Top Books Tab**
- Table view of top 10 performing books
- Sales by category pie chart
- Stock and pricing information

**👥 Employees Tab**
- Employee performance table with sales, customers served, ratings
- Bar chart comparing employee sales by role
- Customer satisfaction ratings

**🛒 Customers Tab**
- Total customers and average customer value metrics
- Customer type breakdown analysis
- Total spending overview

**📊 Analytics Tab**
- Multi-metric normalized comparison chart
- Revenue, transactions, and customer activity correlation
- Advanced trend analysis

## ⚙️ Configuration Options

### Simulation Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Customers | 5-100 | 20 | Number of customer agents |
| Employees | 2-20 | 5 | Number of employee agents |
| Books | 20-500 | 100 | Number of books in catalog |
| Simulation Hours | 1-24 | 8 | Duration of simulation |
| Random Seed | 0+ | 0 (random) | Reproducibility seed |
| Step Delay | 0-2s | 0.1s | Delay between steps (real-time mode) |

### Operating Modes

**Real-time Mode** (Default)
- Executes one step at a time with visualization updates
- Configurable delay between steps (0-2 seconds)
- Best for: Detailed observation, demonstrations, learning

**Batch Mode**
- Runs entire simulation without delays
- Updates only on completion
- Best for: Long simulations, data collection, testing

## 🎯 Use Cases

### 1. Business Analysis
- Test different staffing levels (employees)
- Optimize inventory (books count)
- Analyze customer demand patterns
- Evaluate pricing strategies

### 2. Research & Education
- Demonstrate multi-agent systems
- Study emergent behaviors
- Test ontology-based reasoning
- Analyze agent communication patterns

### 3. System Testing
- Validate synchronization across agents
- Test inventory management algorithms
- Verify transaction processing
- Stress test with high customer volumes

### 4. Production Monitoring
- Real-time business metrics tracking
- Alert system for low inventory
- Employee performance monitoring
- Customer satisfaction tracking

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit (Python-native web framework)
- **Visualization**: Plotly (interactive charts)
- **Backend**: Mesa (agent-based modeling)
- **Data**: Pandas (analytics), Owlready2 (ontology)

### Session State Management
The dashboard uses Streamlit's session state to maintain:
- `model`: Current BookstoreModel instance
- `running`: Simulation execution state
- `simulation_data`: Time-series data for charts
- `total_steps`: Cumulative step counter

### Performance
- **Updates**: Real-time with configurable refresh rate
- **Data Collection**: Efficient time-series storage
- **Charts**: Hardware-accelerated rendering via Plotly
- **Memory**: Efficient circular buffers for long simulations

## 📝 Tips & Best Practices

### For Optimal Performance
1. Use batch mode for simulations > 100 steps
2. Reduce step delay to 0 for faster execution
3. Monitor memory usage with large agent counts
4. Export data periodically for long-running simulations

### For Best Visualizations
1. Use real-time mode with 0.1-0.5s delay
2. Keep customer count reasonable (20-50) for visibility
3. Monitor multiple metrics simultaneously in Analytics tab
4. Use category breakdown charts for pattern recognition

### For Reproducible Results
1. Set a specific random seed (not 0)
2. Use consistent agent counts
3. Run for sufficient duration (8+ hours recommended)
4. Export results immediately after completion

## 🐛 Troubleshooting

**Dashboard won't start**
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Ensure no port conflicts (8501)

**Simulation runs slowly**
- Reduce step delay in real-time mode
- Switch to batch mode for long runs
- Decrease agent counts if system resources limited

**Charts not updating**
- Ensure real-time mode is enabled
- Check that simulation is running (not stopped)
- Verify step delay > 0 for visible updates

**Data export issues**
- Ensure simulation has completed at least one step
- Check write permissions in current directory
- Verify sufficient disk space

## 🔒 Production Deployment

### Local Deployment
```bash
streamlit run ui/streamlit_app.py --server.port 8501 --server.address localhost
```

### Network Deployment
```bash
streamlit run ui/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub repository
2. Connect to Streamlit Cloud (https://streamlit.io/cloud)
3. Deploy with one click
4. Access via public URL

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t bookstore-dashboard .
docker run -p 8501:8501 bookstore-dashboard
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Mesa Documentation](https://mesa.readthedocs.io/)
- [Owlready2 Documentation](https://owlready2.readthedocs.io/)

## 📧 Support

For issues, questions, or feature requests, please refer to the main project documentation.

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**License**: See main project LICENSE file
