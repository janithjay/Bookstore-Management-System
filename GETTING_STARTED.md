# 🎉 Getting Started with Bookstore Management System

Welcome! This guide will get you up and running in 5 minutes.

## ✅ Step 1: Verify Installation

Your system has everything installed:
- ✅ Python 3.10.0
- ✅ Mesa 3.0.3 (simulation framework)
- ✅ Owlready2 0.48 (ontology)
- ✅ Streamlit 1.50.0 (dashboard)
- ✅ Plotly 6.3.0 (charts)
- ✅ Pandas 2.3.2 (data)

## 🚀 Step 2: Launch the Dashboard

Open PowerShell in this directory and run:

```powershell
python run_dashboard.py
```

**OR** run directly:

```powershell
streamlit run ui/streamlit_app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 🎮 Step 3: Run Your First Simulation

1. **In the sidebar (left side):**
   - Keep default settings (20 customers, 5 employees, 100 books, 8 hours)
   - Check "Real-time Mode"
   - Set "Step Delay" to 0.5 seconds

2. **Click the "▶️ Start" button**

3. **Watch the magic happen:**
   - Metrics will start updating
   - Charts will grow
   - Numbers will change in real-time

4. **After a few minutes, click "⏹️ Stop"**

5. **Explore the tabs:**
   - Click "📚 Top Books" to see best sellers
   - Click "👥 Employees" to see performance
   - Click "🛒 Customers" to see insights
   - Click "📊 Analytics" to see correlations

6. **Export your data:**
   - Scroll down to "Export & Reports"
   - Click "📥 Export CSV"
   - Click "Download CSV"

## 💡 Step 4: Try Different Scenarios

### Scenario A: Busy Store
```
Customers: 60
Employees: 12
Books: 200
Hours: 8
Real-time: OFF (for faster execution)
```
Click Start and wait 5-10 minutes for completion.

### Scenario B: Small Bookshop
```
Customers: 10
Employees: 3
Books: 50
Hours: 4
Real-time: ON
Step Delay: 0.2 seconds
```
Perfect for watching detailed behavior!

### Scenario C: Quick Test
```
Customers: 5
Employees: 2
Books: 20
Hours: 1
Seed: 123 (for reproducible results)
```
Takes just 1-2 minutes!

## 📊 Understanding the Dashboard

### Top Metrics (Always Visible)
- **💰 Total Revenue**: Money made from sales
- **🛒 Avg Transaction**: Revenue per purchase
- **😊 Customer Satisfaction**: Service quality score (0-10)
- **📦 Inventory Status**: Total books in stock

### Charts (Middle Section)
- **Revenue Over Time**: Watch income grow
- **Transactions Over Time**: Count of completed sales
- **Active Customers**: Shoppers currently in store
- **Inventory Levels**: Stock changing over time

### Detailed Tabs (Bottom Section)
- **Top Books**: Which books sell best?
- **Employees**: Who's performing well?
- **Customers**: What are people buying?
- **Analytics**: How do metrics relate?

## 🎯 What to Look For

### Good Signs ✅
- Revenue steadily increasing
- Customer satisfaction > 7.0
- Employees busy but not overwhelmed (60-80% utilization)
- Inventory decreasing (books selling)
- Few low-stock alerts

### Warning Signs ⚠️
- Revenue flat (no sales)
- Customer satisfaction < 6.0 (understaffed)
- All employees at 100% (overworked)
- Many low-stock alerts (inventory problems)

## 🛠️ Troubleshooting

### "Dashboard won't start"
Try this command instead:
```powershell
D:/Github/Bookstore-Management-System/venv/Scripts/python.exe -m streamlit run ui/streamlit_app.py
```

### "Port already in use"
Use a different port:
```powershell
streamlit run ui/streamlit_app.py --server.port 8502
```

### "Simulation is slow"
- Turn OFF "Real-time Mode" in sidebar
- Reduce number of customers/employees
- Use shorter simulation hours

### "Charts not showing"
- Make sure simulation is running (green "Running" indicator)
- Try clicking "🔄 Reset" and starting again
- Refresh your browser (Ctrl+R)

## 📚 Command Line Alternative

If you prefer the command line:

```powershell
python main.py --customers 20 --employees 5 --books 100 --hours 8
```

Results will print to console and save to `report/simulation_report_*.json`

## 🎓 Learning Path

### Day 1 (Today!)
1. ✅ Launch dashboard
2. ✅ Run default simulation
3. ✅ Explore all tabs
4. ✅ Try one scenario

### This Week
1. Test 3-5 different parameter combinations
2. Read the [Quick Reference](QUICKSTART.md)
3. Export and analyze CSV data
4. Share with colleagues!

### This Month
1. Deploy to local network (see [INSTALL.md](INSTALL.md))
2. Customize for your needs
3. Generate regular reports
4. Train team members

## 📖 Documentation

- **[README.md](README.md)**: Complete system overview
- **[ui/README.md](ui/README.md)**: Dashboard features in detail
- **[INSTALL.md](INSTALL.md)**: Installation and deployment
- **[QUICKSTART.md](QUICKSTART.md)**: Commands and tips
- **[UI_IMPLEMENTATION_SUMMARY.md](UI_IMPLEMENTATION_SUMMARY.md)**: Technical details

## 🎉 You're Ready!

Everything is set up and ready to use. The dashboard is production-ready and you can:

- ✅ Monitor simulations in real-time
- ✅ Adjust parameters on the fly
- ✅ Export data for analysis
- ✅ Share with stakeholders
- ✅ Deploy to the cloud
- ✅ Use for research or business

## 💬 Quick Tips

1. **Start small**: Use few agents at first to understand behavior
2. **Use seeds**: Set seed=123 for reproducible demonstrations
3. **Watch real-time**: Set 0.5s delay to see what's happening
4. **Export often**: Save your data for later analysis
5. **Try extremes**: Test with too few/many employees to see impacts

## 🚀 Next Command to Run

```powershell
python run_dashboard.py
```

**That's it! Enjoy your Bookstore Management System!** 📚✨

---

Need help? Check the documentation files or review the troubleshooting sections.

**Happy Simulating!** 🎊
