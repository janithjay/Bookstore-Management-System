# 📸 Dashboard Visual Guide

This document describes what you'll see in the dashboard.

## 🎨 Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    📚 Bookstore Management System                       │
│                Real-time Multi-Agent Simulation Dashboard               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────────────────────────────────────────────────┐
│              │                                                          │
│   SIDEBAR    │                    MAIN CONTENT AREA                     │
│              │                                                          │
│ ⚙️ Config    │  ┌──────────────────────────────────────────────────┐   │
│              │  │        KEY METRICS (Top Row)                     │   │
│ 👥 Customers │  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐ │   │
│    [5-100]   │  │  │   💰   │  │   🛒   │  │   😊   │  │   📦   │ │   │
│              │  │  │Revenue │  │  Avg   │  │Customer│  │Inventory│ │   │
│ 👔 Employees │  │  │$XXX.XX │  │$XX.XX  │  │  X.X   │  │ X units│ │   │
│    [2-20]    │  │  └────────┘  └────────┘  └────────┘  └────────┘ │   │
│              │  └──────────────────────────────────────────────────┘   │
│ 📚 Books     │                                                          │
│   [20-500]   │  ┌──────────────────────────────────────────────────┐   │
│              │  │     OPERATIONAL METRICS (Second Row)             │   │
│ ⏱️ Hours     │  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐ │   │
│   [1-24]     │  │  │   ⏱️   │  │   👥   │  │   📚   │  │   ⚠️   │ │   │
│              │  │  │  Time  │  │  Busy  │  │ Total  │  │Alerts  │ │   │
│ 🎲 Seed      │  │  │ Xh Ym  │  │  X/Y   │  │   X    │  │   X    │ │   │
│   [0=random] │  │  └────────┘  └────────┘  └────────┘  └────────┘ │   │
│              │  └──────────────────────────────────────────────────┘   │
│ ✅ Real-time │                                                          │
│ [ ] Mode     │  ┌──────────────────────────────────────────────────┐   │
│              │  │           📈 REAL-TIME ANALYTICS                 │   │
│ ⏱️ Delay     │  │                                                  │   │
│   [0-2s]     │  │  ┌─────────────────┐    ┌─────────────────┐    │   │
│              │  │  │   REVENUE       │    │  TRANSACTIONS   │    │   │
│ ─────────────│  │  │   ↗️ Growing    │    │   ↗️ Growing     │    │   │
│              │  │  │                 │    │                 │    │   │
│ ▶️  START    │  │  │      📈         │    │      📈         │    │   │
│              │  │  └─────────────────┘    └─────────────────┘    │   │
│ ⏹️  STOP     │  │                                                  │   │
│              │  │  ┌─────────────────┐    ┌─────────────────┐    │   │
│ 🔄 RESET     │  │  │ACTIVE CUSTOMERS │    │  INVENTORY      │    │   │
│              │  │  │   ↗️↘️ Varying   │    │   ↘️ Decreasing │    │   │
│              │  │  │                 │    │                 │    │   │
│              │  │  │      📈         │    │      📈         │    │   │
│              │  │  └─────────────────┘    └─────────────────┘    │   │
│              │  └──────────────────────────────────────────────────┘   │
│              │                                                          │
│              │  ┌──────────────────────────────────────────────────┐   │
│              │  │         DETAILED ANALYTICS TABS                  │   │
│              │  │  [📚 Top Books] [👥 Employees] [🛒 Customers]   │   │
│              │  │  [📊 Analytics]                                  │   │
│              │  │                                                  │   │
│              │  │  (Tab content shows here based on selection)     │   │
│              │  │                                                  │   │
│              │  │  📚 Top Books Tab:                               │   │
│              │  │  ┌─────────────────────────────────────────────┐│   │
│              │  │  │Title        │Author  │Sales│Price│Stock    ││   │
│              │  │  │─────────────┼────────┼─────┼─────┼─────────││   │
│              │  │  │Book Title 1 │Author 1│ 45  │$15.99│ 30     ││   │
│              │  │  │Book Title 2 │Author 2│ 38  │$12.50│ 15     ││   │
│              │  │  └─────────────────────────────────────────────┘│   │
│              │  └──────────────────────────────────────────────────┘   │
│              │                                                          │
│              │  ┌──────────────────────────────────────────────────┐   │
│              │  │         💾 EXPORT & REPORTS                      │   │
│              │  │  [📥 Export CSV] [📊 Generate Report]           │   │
│              │  │  [🔍 View History]                               │   │
│              │  └──────────────────────────────────────────────────┘   │
│              │                                                          │
└──────────────┴──────────────────────────────────────────────────────────┘
```

## 📊 Metric Cards Explained

### Top Row Metrics

#### 💰 Total Revenue
```
┌─────────────────┐
│  💰 Total Revenue│
│                 │
│    $2,456.78    │ ← Current total revenue
│                 │
│ ▲ 157 transactions│ ← Number of sales
└─────────────────┘
```

#### 🛒 Average Transaction
```
┌─────────────────┐
│ 🛒 Avg Transaction│
│                 │
│     $15.65      │ ← Revenue per sale
│                 │
│ ▲ 157 served    │ ← Customers helped
└─────────────────┘
```

#### 😊 Customer Satisfaction
```
┌─────────────────┐
│😊 Customer Satisfaction│
│                 │
│      8.3/10     │ ← Service rating
│                 │
│ ▲ 12 active     │ ← Currently shopping
└─────────────────┘
```

#### 📦 Inventory Status
```
┌─────────────────┐
│📦 Inventory Status│
│                 │
│   2,543 units   │ ← Total stock
│                 │
│ ▼ 12 low stock  │ ← Items running low
└─────────────────┘
```

### Second Row Metrics

#### ⏱️ Simulation Time
```
┌─────────────────┐
│ ⏱️ Simulation Time│
│                 │
│    8h 0m 0s     │ ← Current sim time
└─────────────────┘
```

#### 👥 Busy Employees
```
┌─────────────────┐
│  👥 Busy Employees│
│                 │
│      3/5        │ ← Active/Total
└─────────────────┘
```

#### 📚 Total Books
```
┌─────────────────┐
│   📚 Total Books │
│                 │
│       100       │ ← Catalog size
└─────────────────┘
```

#### ⚠️ Alerts
```
┌─────────────────┐
│    ⚠️ Alerts     │
│                 │
│        3        │ ← Critical items
└─────────────────┘
```

## 📈 Chart Descriptions

### Revenue Over Time Chart
```
Revenue ($)
  300 │                             ╱
      │                        ╱───╯
  200 │                   ╱───╯
      │              ╱───╯
  100 │         ╱───╯
      │    ╱───╯
    0 └────┴────┴────┴────┴────┴────┴──→ Steps
       0   100  200  300  400  500  600

📈 Shows revenue growth over simulation
   - Y-axis: Dollar amount
   - X-axis: Simulation steps
   - Area fill: Blue gradient
   - Hover: Shows exact values
```

### Transactions Over Time Chart
```
Transactions
  150 │                             ╱
      │                        ╱───╯
  100 │                   ╱───╯
      │              ╱───╯
   50 │         ╱───╯
      │    ╱───╯
    0 └────┴────┴────┴────┴────┴────┴──→ Steps
       0   100  200  300  400  500  600

🛒 Shows cumulative transaction count
   - Y-axis: Number of transactions
   - X-axis: Simulation steps
   - Line: Green
```

### Active Customers Chart
```
Customers
   20 │    ╱╲       ╱╲    ╱╲
      │   ╱  ╲     ╱  ╲  ╱  ╲
   10 │  ╱    ╲   ╱    ╲╱    ╲
      │ ╱      ╲ ╱            ╲
    0 └─┴────┴──┴─┴────┴────┴──┴→ Steps
       0  100  200 300  400  500

👥 Shows customer activity fluctuation
   - Y-axis: Number of active customers
   - X-axis: Simulation steps
   - Line: Orange, varies up and down
```

### Inventory Levels Chart
```
Stock Units
 2600 │╲
      │ ╲
 2500 │  ╲___
      │      ╲___
 2400 │          ╲___
      │              ╲___
 2300 └────┴────┴────┴────┴────┴──→ Steps
       0   100  200  300  400  500

📦 Shows inventory depletion
   - Y-axis: Total stock units
   - X-axis: Simulation steps
   - Line: Purple, generally decreasing
```

## 📋 Tab Content Examples

### 📚 Top Books Tab
```
┌──────────────────────────────────────────────────────────────────┐
│  Top 10 Performing Books                                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Title                 │ Author       │ Sales │ Price │ Stock   │
│  ─────────────────────┼──────────────┼───────┼───────┼────────  │
│  The Great Novel      │ John Smith   │  45   │$19.99 │  25     │
│  Mystery Book         │ Jane Doe     │  38   │$15.99 │  12 ⚠️  │
│  Science Fiction Tale │ Bob Johnson  │  32   │$22.50 │  30     │
│  Romance Story        │ Mary Wilson  │  28   │$14.99 │  18     │
│  ...                  │ ...          │  ...  │  ...  │  ...    │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Sales by Category                                               │
│                                                                  │
│       ╭─────╮                                                    │
│       │ 35% │  Fiction                                           │
│   ╭───┤     ├───╮                                                │
│   │25%│     │ 20%│                                               │
│   │   │     │    │  Non-Fiction, Science Fiction                │
│   ╰───┴─────┴────╯                                               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 👥 Employees Tab
```
┌──────────────────────────────────────────────────────────────────┐
│  Employee Performance                                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Name          │ Role    │ Sales  │ Customers │ Rating │ Sat.   │
│  ──────────────┼─────────┼────────┼───────────┼────────┼─────   │
│  Alice Johnson │ Cashier │$487.35 │    42     │  8.5   │ 8.2   │
│  Bob Smith     │ Sales   │$445.12 │    38     │  8.0   │ 7.8   │
│  Carol Davis   │ Manager │$398.75 │    35     │  7.8   │ 7.9   │
│  ...           │ ...     │  ...   │    ...    │  ...   │ ...   │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  Sales Comparison                                                │
│                                                                  │
│  Alice  ████████████████████████ $487                            │
│  Bob    ██████████████████████   $445                            │
│  Carol  ████████████████████     $398                            │
│  Dave   ███████████████          $310                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 🛒 Customers Tab
```
┌──────────────────────────────────────────────────────────────────┐
│  Customer Insights                                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │Total Customers│ │Avg Customer  │  │Total Spend   │          │
│  │              │  │Value         │  │              │          │
│  │     157      │  │  $15.65      │  │  $2,456.78   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  Customer Type Breakdown:                                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Regular     │  65 customers  │  $1,200  │  Avg: $18.46    │ │
│  │ Premium     │  42 customers  │    $950  │  Avg: $22.62    │ │
│  │ Student     │  50 customers  │    $306  │  Avg: $6.12     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 📊 Analytics Tab
```
┌──────────────────────────────────────────────────────────────────┐
│  Multi-Metric Analysis                                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Normalized Metrics (%)     │         Active Customers          │
│  100│                      ╱│   20│    ╱╲      ╱╲               │
│     │                 ╱───╯ │      │   ╱  ╲    ╱  ╲              │
│   50│            ╱───╯      │   10│  ╱    ╲  ╱    ╲             │
│     │       ╱───╯           │      │ ╱      ╲╱      ╲            │
│    0└───┴───┴───┴───┴───→  │    0└─┴───┴───┴───┴───→            │
│       Steps                 │       Steps                        │
│                            │                                    │
│  ─── Revenue (normalized)   │                                    │
│  ─── Transactions (normalized)                                   │
│  ─── Active Customers                                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## 🎨 Color Scheme

### Metric Cards
- **Green arrows ▲**: Positive metrics (revenue up, satisfaction up)
- **Red arrows ▼**: Warning metrics (low stock, declining satisfaction)
- **Gray background**: Neutral information

### Charts
- **Blue**: Revenue (primary metric)
- **Green**: Transactions (success metric)
- **Orange**: Customer activity (engagement)
- **Purple**: Inventory (resources)

### Status Indicators
- **Green**: Good (satisfaction > 7, stock > 20)
- **Yellow**: Warning (satisfaction 5-7, stock 10-20)
- **Red**: Critical (satisfaction < 5, stock < 10)

## 🖱️ Interactive Features

### Hover Actions
- **Metric Cards**: Shows full details
- **Chart Points**: Displays exact values at that step
- **Table Rows**: Highlights row for readability

### Click Actions
- **Buttons**: Triggers action (Start/Stop/Reset)
- **Tabs**: Switches content view
- **Export**: Downloads file

### Zoom & Pan
- **Charts**: Mouse wheel to zoom, click-drag to pan
- **Double-click**: Reset zoom to default

## 📱 Mobile View

On mobile devices, the layout adjusts:
```
┌────────────────┐
│    HEADER      │
├────────────────┤
│   METRICS      │
│   (Stacked)    │
├────────────────┤
│   CHARTS       │
│   (Stacked)    │
├────────────────┤
│   TABS         │
│   (Full Width) │
├────────────────┤
│   SIDEBAR      │
│   (Collapsed)  │
└────────────────┘
```

## 🎭 Animation & Updates

### Real-Time Mode
- **Metrics**: Update every step (0.1-2s based on delay setting)
- **Charts**: Smooth line drawing, points added sequentially
- **Counters**: Number animations (counting up effect)

### Batch Mode
- **Metrics**: Update only when simulation completes
- **Charts**: Draw all at once at end
- **Progress**: Show completion percentage

---

**This visual guide helps you understand what you'll see in the dashboard!**

For the actual experience, run: `python run_dashboard.py` 🚀
