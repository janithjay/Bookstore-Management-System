"""
Bookstore Management System - Streamlit Dashboard
Production-ready UI for simulation monitoring and control
"""

import streamlit as st
import sys
from pathlib import Path
import time
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from simulation.bookstore_model import BookstoreModel
from ontology.bookstore_ontology import bookstore_ontology

# Page configuration
st.set_page_config(
    page_title="Bookstore Simulation Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'simulation_data' not in st.session_state:
        st.session_state.simulation_data = {
            'steps': [],
            'revenue': [],
            'transactions': [],
            'customers': [],
            'employees': [],
            'stock': []
        }
    if 'total_steps' not in st.session_state:
        st.session_state.total_steps = 0


def create_sidebar():
    """Create sidebar with configuration controls"""
    with st.sidebar:
        st.markdown("## ⚙️ Simulation Configuration")
        
        # Simulation parameters
        st.markdown("### 📊 Agent Configuration")
        num_customers = st.slider("Number of Customers", 5, 100, 20, 5)
        num_employees = st.slider("Number of Employees", 2, 20, 5, 1)
        num_books = st.slider("Number of Books", 20, 500, 100, 20)
        
        st.markdown("### ⏱️ Time Configuration")
        simulation_hours = st.slider("Simulation Hours", 1, 24, 8, 1)
        
        st.markdown("### 🎲 Advanced Settings")
        seed = st.number_input("Random Seed (optional)", min_value=0, value=0, 
                              help="Set to 0 for random, or specify for reproducible results")
        if seed == 0:
            seed = None
        
        use_realtime = st.checkbox("Real-time Mode", value=True,
                                   help="Run simulation step-by-step with visualization")
        
        if use_realtime:
            step_delay = st.slider("Step Delay (seconds)", 0.0, 2.0, 0.1, 0.1,
                                  help="Delay between simulation steps")
        else:
            step_delay = 0
        
        st.markdown("---")
        
        # Control buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ Start", use_container_width=True, disabled=st.session_state.running):
                start_simulation(num_customers, num_employees, num_books, 
                               simulation_hours, seed)
        
        with col2:
            if st.button("⏹️ Stop", use_container_width=True, disabled=not st.session_state.running):
                stop_simulation()
        
        if st.button("🔄 Reset", use_container_width=True):
            reset_simulation()
        
        return {
            'num_customers': num_customers,
            'num_employees': num_employees,
            'num_books': num_books,
            'simulation_hours': simulation_hours,
            'seed': seed,
            'realtime': use_realtime,
            'step_delay': step_delay
        }


def start_simulation(num_customers, num_employees, num_books, simulation_hours, seed):
    """Initialize and start the simulation"""
    try:
        # Reset ontology before starting new simulation
        bookstore_ontology.reset()
        
        st.session_state.model = BookstoreModel(
            num_customers=num_customers,
            num_employees=num_employees,
            num_books=num_books,
            simulation_hours=simulation_hours,
            seed=seed
        )
        st.session_state.running = True
        st.session_state.total_steps = 0
        st.session_state.simulation_data = {
            'steps': [],
            'revenue': [],
            'transactions': [],
            'customers': [],
            'employees': [],
            'stock': []
        }
        st.success("✅ Simulation initialized successfully!")
    except Exception as e:
        st.error(f"❌ Error starting simulation: {e}")


def stop_simulation():
    """Stop the running simulation"""
    if st.session_state.model:
        st.session_state.model.running = False
    st.session_state.running = False
    st.info("⏹️ Simulation stopped")


def reset_simulation():
    """Reset the simulation to initial state"""
    # Reset ontology
    bookstore_ontology.reset()
    
    st.session_state.model = None
    st.session_state.running = False
    st.session_state.simulation_data = {
        'steps': [],
        'revenue': [],
        'transactions': [],
        'customers': [],
        'employees': [],
        'stock': []
    }
    st.session_state.total_steps = 0
    st.success("🔄 Simulation reset complete")
    st.rerun()


def run_simulation_step():
    """Execute one simulation step and collect data"""
    if st.session_state.model and st.session_state.running:
        try:
            st.session_state.model.step()
            st.session_state.total_steps += 1
            
            # Collect data for visualization
            summary = st.session_state.model.get_simulation_summary()
            inventory_status = bookstore_ontology.get_inventory_status()
            
            st.session_state.simulation_data['steps'].append(st.session_state.total_steps)
            st.session_state.simulation_data['revenue'].append(summary['daily_revenue'])
            st.session_state.simulation_data['transactions'].append(summary['total_transactions'])
            st.session_state.simulation_data['customers'].append(summary['active_customers'])
            st.session_state.simulation_data['employees'].append(summary['busy_employees'])
            st.session_state.simulation_data['stock'].append(inventory_status['total_stock'])
            
            # Check if simulation is complete
            if not st.session_state.model.running:
                st.session_state.running = False
                st.success("✅ Simulation completed!")
                
        except Exception as e:
            st.error(f"Error during simulation step: {e}")
            st.session_state.running = False


def display_metrics():
    """Display key business metrics"""
    if not st.session_state.model:
        st.info("👈 Configure and start simulation using the sidebar")
        return
    
    summary = st.session_state.model.get_simulation_summary()
    inventory_status = bookstore_ontology.get_inventory_status()
    
    # Top row - Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${summary['daily_revenue']:,.2f}",
            delta=f"{summary['total_transactions']} transactions"
        )
    
    with col2:
        st.metric(
            label="🛒 Avg Transaction",
            value=f"${summary['average_transaction_value']:,.2f}",
            delta=f"{summary['total_customers_served']} served"
        )
    
    with col3:
        st.metric(
            label="😊 Customer Satisfaction",
            value=f"{summary['customer_satisfaction']:.1f}/10",
            delta=f"{summary['active_customers']} active"
        )
    
    with col4:
        st.metric(
            label="📦 Inventory Status",
            value=f"{inventory_status['total_stock']} units",
            delta=f"{inventory_status['low_stock_count']} low stock",
            delta_color="inverse"
        )
    
    # Second row - Operational metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="⏱️ Simulation Time",
            value=summary['simulation_time']
        )
    
    with col6:
        st.metric(
            label="👥 Busy Employees",
            value=f"{summary['busy_employees']}/{summary['total_employees']}"
        )
    
    with col7:
        st.metric(
            label="📚 Total Books",
            value=inventory_status['total_books']
        )
    
    with col8:
        st.metric(
            label="⚠️ Alerts",
            value=summary['inventory_alerts'],
            delta_color="inverse"
        )


def display_charts():
    """Display interactive charts"""
    if not st.session_state.simulation_data['steps']:
        return
    
    # Revenue over time
    col1, col2 = st.columns(2)
    
    with col1:
        fig_revenue = go.Figure()
        fig_revenue.add_trace(go.Scatter(
            x=st.session_state.simulation_data['steps'],
            y=st.session_state.simulation_data['revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy'
        ))
        fig_revenue.update_layout(
            title="📈 Revenue Over Time",
            xaxis_title="Simulation Steps",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        fig_transactions = go.Figure()
        fig_transactions.add_trace(go.Scatter(
            x=st.session_state.simulation_data['steps'],
            y=st.session_state.simulation_data['transactions'],
            mode='lines+markers',
            name='Transactions',
            line=dict(color='#2ca02c', width=3),
            fill='tozeroy'
        ))
        fig_transactions.update_layout(
            title="🛒 Transactions Over Time",
            xaxis_title="Simulation Steps",
            yaxis_title="Total Transactions",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_transactions, use_container_width=True)
    
    # Activity metrics
    col3, col4 = st.columns(2)
    
    with col3:
        fig_customers = go.Figure()
        fig_customers.add_trace(go.Scatter(
            x=st.session_state.simulation_data['steps'],
            y=st.session_state.simulation_data['customers'],
            mode='lines',
            name='Active Customers',
            line=dict(color='#ff7f0e', width=2)
        ))
        fig_customers.update_layout(
            title="👥 Active Customers",
            xaxis_title="Simulation Steps",
            yaxis_title="Number of Customers",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_customers, use_container_width=True)
    
    with col4:
        fig_stock = go.Figure()
        fig_stock.add_trace(go.Scatter(
            x=st.session_state.simulation_data['steps'],
            y=st.session_state.simulation_data['stock'],
            mode='lines',
            name='Total Stock',
            line=dict(color='#9467bd', width=2)
        ))
        fig_stock.update_layout(
            title="📦 Inventory Levels",
            xaxis_title="Simulation Steps",
            yaxis_title="Total Stock Units",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_stock, use_container_width=True)


def display_detailed_analytics():
    """Display detailed analytics tabs"""
    if not st.session_state.model:
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Top Books", "👥 Employees", "🛒 Customers", "📊 Analytics"])
    
    with tab1:
        st.markdown("### 📚 Top Performing Books")
        top_books = st.session_state.model.get_top_performing_books(10)
        if top_books:
            df_books = pd.DataFrame(top_books)
            df_books = df_books[['title', 'author', 'category', 'total_sales', 'current_price', 'stock_quantity']]
            df_books.columns = ['Title', 'Author', 'Category', 'Sales', 'Price ($)', 'Stock']
            st.dataframe(df_books, use_container_width=True, height=400)
            
            # Sales by category
            if len(df_books) > 0:
                category_sales = df_books.groupby('Category')['Sales'].sum().reset_index()
                fig_category = px.pie(category_sales, values='Sales', names='Category',
                                     title='Sales by Category')
                st.plotly_chart(fig_category, use_container_width=True)
    
    with tab2:
        st.markdown("### 👥 Employee Performance")
        employees = st.session_state.model.get_employee_performance()
        if employees:
            df_emp = pd.DataFrame(employees)
            df_emp = df_emp[['name', 'role', 'daily_sales', 'customers_served', 
                           'performance_rating', 'customer_satisfaction']]
            df_emp.columns = ['Name', 'Role', 'Sales ($)', 'Customers', 'Rating', 'Satisfaction']
            st.dataframe(df_emp, use_container_width=True, height=400)
            
            # Employee sales chart
            if len(df_emp) > 0:
                fig_emp = px.bar(df_emp, x='Name', y='Sales ($)', color='Role',
                               title='Employee Sales Performance')
                st.plotly_chart(fig_emp, use_container_width=True)
    
    with tab3:
        st.markdown("### 🛒 Customer Insights")
        customer_insights = st.session_state.model.get_customer_insights()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Registered Customers", customer_insights['total_customers'])
        with col2:
            st.metric("Active Shoppers", customer_insights.get('participating_customers', 0))
        with col3:
            st.metric("Avg Customer Value", f"${customer_insights['average_customer_value']:,.2f}")
        with col4:
            st.metric("Total Spend", f"${customer_insights['total_customer_spend']:,.2f}")
        
        st.info("💡 Spend values reflect simulation period only, not pre-existing historical data")
        
        # Customer type breakdown
        if customer_insights['customer_type_breakdown']:
            df_customers = pd.DataFrame(customer_insights['customer_type_breakdown']).T
            st.dataframe(df_customers, use_container_width=True)
    
    with tab4:
        st.markdown("### 📊 Simulation Analytics")
        
        if st.session_state.simulation_data['steps'] and len(st.session_state.simulation_data['steps']) > 0:
            # Check if we have meaningful data to display
            has_revenue = any(st.session_state.simulation_data['revenue'])
            has_transactions = any(st.session_state.simulation_data['transactions'])
            
            if not has_revenue and not has_transactions:
                st.info("📊 No transactions yet. Analytics will appear once sales begin.")
            else:
                # Multi-metric line chart
                fig_multi = go.Figure()
                
                # Normalize values for comparison (avoid division by zero)
                max_revenue = max(st.session_state.simulation_data['revenue']) if st.session_state.simulation_data['revenue'] else 1
                max_trans = max(st.session_state.simulation_data['transactions']) if st.session_state.simulation_data['transactions'] else 1
                
                # Ensure we don't divide by zero
                max_revenue = max(max_revenue, 0.01)  # Minimum value to avoid division by zero
                max_trans = max(max_trans, 0.01)
                
                fig_multi.add_trace(go.Scatter(
                    x=st.session_state.simulation_data['steps'],
                    y=[r/max_revenue*100 for r in st.session_state.simulation_data['revenue']],
                    name='Revenue (normalized)',
                    yaxis='y'
                ))
                
                fig_multi.add_trace(go.Scatter(
                    x=st.session_state.simulation_data['steps'],
                    y=[t/max_trans*100 for t in st.session_state.simulation_data['transactions']],
                    name='Transactions (normalized)',
                    yaxis='y'
                ))
                
                fig_multi.add_trace(go.Scatter(
                    x=st.session_state.simulation_data['steps'],
                    y=st.session_state.simulation_data['customers'],
                    name='Active Customers',
                    yaxis='y2'
                ))
                
                fig_multi.update_layout(
                    title='Multi-Metric Analysis',
                    xaxis=dict(title='Simulation Steps'),
                    yaxis=dict(title='Normalized % (Revenue & Transactions)', side='left'),
                    yaxis2=dict(title='Active Customers', overlaying='y', side='right'),
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig_multi, use_container_width=True)
        else:
            st.info("📊 Start the simulation to see analytics.")


def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">📚 Bookstore Management System</h1>', unsafe_allow_html=True)
    st.markdown("### Real-time Multi-Agent Simulation Dashboard")
    
    # Sidebar configuration
    config = create_sidebar()
    
    # Main content
    if st.session_state.model:
        # Run simulation step if in real-time mode
        if st.session_state.running and config['realtime']:
            run_simulation_step()
            if config['step_delay'] > 0:
                time.sleep(config['step_delay'])
            st.rerun()
        
        # Display metrics
        display_metrics()
        
        st.markdown("---")
        
        # Display charts
        st.markdown("## 📈 Real-Time Analytics")
        display_charts()
        
        st.markdown("---")
        
        # Display detailed analytics
        display_detailed_analytics()
        
        # Export functionality
        st.markdown("---")
        st.markdown("## 💾 Export & Reports")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export CSV", use_container_width=True):
                summary = st.session_state.model.get_simulation_summary()
                df = pd.DataFrame([summary])
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Generating detailed report...")
                # Report generation logic here
        
        with col3:
            if st.button("🔍 View History", use_container_width=True):
                st.info("Historical data viewer coming soon!")
    
    else:
        # Welcome screen
        st.info("""
        ### 👋 Welcome to the Bookstore Simulation System!
        
        **Get Started:**
        1. Configure simulation parameters in the sidebar 👈
        2. Click "Start" to begin the simulation
        3. Watch real-time metrics and analytics update
        4. Export results when complete
        
        **Features:**
        - Real-time visualization of business metrics
        - Interactive charts and graphs
        - Detailed agent performance analytics
        - Export capabilities for reports
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <small>Bookstore Management System v1.0 | Multi-Agent Simulation with Ontology Integration</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
