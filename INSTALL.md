# 🚀 Installation & Deployment Guide

Complete guide for setting up and deploying the Bookstore Management System.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 or higher (3.10 recommended)
- **RAM**: 4GB minimum (8GB recommended for large simulations)
- **Disk Space**: 500MB for installation + space for reports

### Required Software
- Python 3.8+ with pip
- Git (for cloning repository)
- Web browser (Chrome, Firefox, Edge, or Safari)

## 🔧 Installation

### Step 1: Clone or Download

**Option A: Using Git**
```bash
git clone <repository-url>
cd Bookstore-Management-System
```

**Option B: Download ZIP**
1. Download ZIP from repository
2. Extract to desired location
3. Open terminal/command prompt in extracted folder

### Step 2: Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed mesa-3.x.x owlready2-0.44 streamlit-1.28.x plotly-5.15.x pandas-1.5.x numpy-1.24.x ...
```

### Step 4: Verify Installation

```bash
python -c "import mesa, owlready2, streamlit, plotly; print('All dependencies installed successfully!')"
```

If successful, you should see: `All dependencies installed successfully!`

## ✅ Quick Verification

Test the system with a short simulation:

```bash
python main.py --customers 5 --employees 2 --books 20 --hours 1
```

Expected output should show:
- ✅ Simulation initialization
- ✅ Progress updates
- ✅ Final report with revenue > 0
- ✅ JSON report saved to `report/` directory

## 🎨 Running the Dashboard

### Method 1: Using Launcher Script (Easiest)

```bash
python run_dashboard.py
```

This will:
1. Check dependencies
2. Launch Streamlit server
3. Open dashboard in your default browser

### Method 2: Direct Streamlit Command

```bash
streamlit run ui/streamlit_app.py
```

### Method 3: Custom Port/Address

```bash
streamlit run ui/streamlit_app.py --server.port 8080 --server.address 0.0.0.0
```

### Expected Behavior
- Terminal shows: `You can now view your Streamlit app in your browser.`
- Browser opens automatically to `http://localhost:8501`
- Dashboard loads with sidebar controls

## 💻 Command Line Usage

### Basic Simulation

```bash
python main.py
```

Runs with default parameters (20 customers, 5 employees, 100 books, 8 hours)

### Custom Parameters

```bash
python main.py --customers 50 --employees 10 --books 200 --hours 12
```

### Reproducible Results

```bash
python main.py --seed 42
```

Use same seed for identical results across runs

### Long Simulation with Frequent Checkpoints

```bash
python main.py --hours 24 --checkpoint 15 --output ./my_reports
```

### All Available Arguments

```bash
python main.py --help
```

## 📊 Output Locations

### Reports Directory Structure
```
report/
├── simulation_report_YYYYMMDD_HHMMSS.json    # Main report
├── data/
│   ├── agent_analytics.csv                    # Time-series data
│   └── checkpoint_NNNN.json                   # State snapshots
├── charts/                                    # (Future: Auto-generated charts)
└── logs/                                      # (Future: Detailed logs)
```

### Dashboard Exports
- CSV exports go to: `simulation_YYYYMMDD_HHMMSS.csv`
- Located in current working directory

## 🌐 Deployment Options

### 1. Local Network Access

**Allow access from other computers on your network:**

```bash
streamlit run ui/streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

Then access from other devices using:
```
http://<your-ip-address>:8501
```

Find your IP:
- **Windows**: `ipconfig` (look for IPv4 Address)
- **macOS/Linux**: `ifconfig` or `ip addr`

### 2. Streamlit Cloud (Free Hosting)

**Requirements:**
- GitHub account
- Public GitHub repository

**Steps:**
1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository
6. Set main file path: `ui/streamlit_app.py`
7. Click "Deploy"

**Result:** Get public URL like `https://your-app.streamlit.app`

### 3. Docker Deployment

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and run:**
```bash
docker build -t bookstore-dashboard .
docker run -p 8501:8501 bookstore-dashboard
```

**Access:** `http://localhost:8501`

### 4. Production Server (nginx + gunicorn)

For production deployment with reverse proxy:

**Install gunicorn:**
```bash
pip install gunicorn
```

**Run with gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8501 --timeout 120 ui.streamlit_app:main
```

**nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 Security Considerations

### For Production Deployment

1. **Authentication**: Add Streamlit authentication
```python
# In streamlit_app.py
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)
```

2. **HTTPS**: Use SSL certificates (Let's Encrypt)
```bash
certbot --nginx -d your-domain.com
```

3. **Firewall**: Configure firewall rules
```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

4. **Environment Variables**: Use for sensitive config
```python
import os
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
```

## 🐛 Troubleshooting

### Installation Issues

**Problem: `pip install` fails with permission error**
```bash
# Solution: Use --user flag
pip install --user -r requirements.txt
```

**Problem: `ImportError: No module named 'mesa'`**
```bash
# Solution: Ensure virtual environment is activated
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

**Problem: `Python version 3.x required`**
```bash
# Solution: Check Python version
python --version
# Should show 3.8 or higher
```

### Dashboard Issues

**Problem: Dashboard won't start - port already in use**
```bash
# Solution: Use different port
streamlit run ui/streamlit_app.py --server.port 8502
```

**Problem: Browser doesn't open automatically**
```
# Manually open: http://localhost:8501
```

**Problem: "Streamlit not found"**
```bash
# Solution: Install Streamlit specifically
pip install streamlit
```

### Simulation Issues

**Problem: Simulation runs very slowly**
```
# Solutions:
1. Reduce agent counts
2. Use batch mode (uncheck "Real-time Mode")
3. Decrease simulation hours
```

**Problem: "Out of memory" error**
```
# Solutions:
1. Reduce number of books/customers
2. Lower checkpoint frequency
3. Run shorter simulations
```

**Problem: Results not reproducible**
```bash
# Solution: Always specify seed
python main.py --seed 42
```

### Performance Optimization

**For Large Simulations:**
1. Use CLI instead of dashboard for runs > 1000 steps
2. Increase checkpoint interval (--checkpoint 100)
3. Disable real-time visualizations
4. Close other applications

**For Multiple Users:**
1. Deploy on dedicated server
2. Use nginx load balancer
3. Increase server resources
4. Consider containerization

## 📦 Updating the System

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Pull Latest Changes (Git)

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

### Verify After Update

```bash
python main.py --customers 5 --employees 2 --hours 1
```

## 🧪 Testing Installation

### Run Test Suite

```bash
pytest tests/ -v
```

### Manual Testing Checklist

- [ ] CLI simulation runs successfully
- [ ] Dashboard launches without errors
- [ ] Metrics update in real-time
- [ ] Charts render correctly
- [ ] Export functions work
- [ ] Checkpoints are saved
- [ ] Reports generate properly

## 📚 Next Steps

After successful installation:

1. **Learn the Dashboard**: Read [UI Documentation](ui/README.md)
2. **Run Example**: Try `python main.py --seed 123`
3. **Explore Features**: Launch dashboard and experiment
4. **Review Output**: Check `report/` directory
5. **Customize**: Modify parameters for your use case

## 💡 Tips for First-Time Users

1. **Start Small**: Begin with 10 customers, 3 employees, 1 hour
2. **Use Seeds**: Set `--seed 123` for reproducible learning
3. **Watch Real-time**: Use dashboard to understand agent behaviors
4. **Read Reports**: Examine JSON reports for detailed metrics
5. **Experiment**: Try different parameter combinations

## 🆘 Getting Help

If issues persist:

1. Check this troubleshooting section
2. Review [main README](README.md)
3. Check [UI README](ui/README.md)
4. Verify all dependencies are installed
5. Test with minimal parameters first

## 📄 System Information

Check your installation details:

```bash
python -c "import mesa, owlready2, streamlit, plotly, pandas, numpy; print(f'Mesa: {mesa.__version__}\nOwlready2: {owlready2.__version__}\nStreamlit: {streamlit.__version__}\nPlotly: {plotly.__version__}\nPandas: {pandas.__version__}\nNumPy: {numpy.__version__}')"
```

---

**Installation Support Version**: 1.0.0  
**Last Updated**: 2024
