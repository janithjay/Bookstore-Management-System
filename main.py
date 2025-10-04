#!/usr/bin/env python3
"""
Bookstore Management System with Ontology and Multi-Agent Simulation

Main entry point for running the bookstore simulation. This script provides
a command-line interface for configuring and running the simulation, as well
as generating reports and analytics.

Usage:
    python main.py [options]

Options:
    --customers N       Number of customer agents (default: 20)
    --employees N       Number of employee agents (default: 5)
    --books N          Number of book agents (default: 100)
    --hours N          Simulation hours (default: 8)
    --steps N          Max simulation steps (overrides hours)
    --seed N           Random seed for reproducibility
    --output DIR       Output directory for reports (default: ./report)
    --verbose         Enable verbose output
    --gui             Run with graphical visualization (if available)
    --report          Generate detailed report at end
"""

import argparse
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from simulation.bookstore_model import BookstoreModel
from ontology.bookstore_ontology import bookstore_ontology


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Bookstore Management System Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        '--customers', 
        type=int, 
        default=20, 
        help='Number of customer agents (default: 20)'
    )
    
    parser.add_argument(
        '--employees', 
        type=int, 
        default=5, 
        help='Number of employee agents (default: 5)'
    )
    
    parser.add_argument(
        '--books', 
        type=int, 
        default=100, 
        help='Number of book agents (default: 100)'
    )
    
    parser.add_argument(
        '--hours', 
        type=int, 
        default=8, 
        help='Simulation hours (default: 8)'
    )
    
    parser.add_argument(
        '--steps', 
        type=int, 
        help='Max simulation steps (overrides hours)'
    )
    
    parser.add_argument(
        '--seed', 
        type=int, 
        help='Random seed for reproducibility'
    )
    
    parser.add_argument(
        '--output', 
        type=str, 
        default='./report', 
        help='Output directory for reports (default: ./report)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--gui', 
        action='store_true', 
        help='Run with graphical visualization (if available)'
    )
    
    parser.add_argument(
        '--report', 
        action='store_true', 
        help='Generate detailed report at end'
    )
    
    parser.add_argument(
        '--quick', 
        action='store_true', 
        help='Run quick simulation (1 hour, fewer agents)'
    )
    
    return parser.parse_args()


def setup_output_directory(output_dir: str) -> Path:
    """Setup output directory for reports"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (output_path / 'data').mkdir(exist_ok=True)
    (output_path / 'charts').mkdir(exist_ok=True)
    (output_path / 'logs').mkdir(exist_ok=True)
    
    return output_path


def print_simulation_header(args):
    """Print simulation configuration header"""
    print("=" * 60)
    print("BOOKSTORE MANAGEMENT SYSTEM SIMULATION")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  Customers: {args.customers}")
    print(f"  Employees: {args.employees}")
    print(f"  Books: {args.books}")
    print(f"  Duration: {args.hours} hours")
    if args.seed:
        print(f"  Random Seed: {args.seed}")
    print(f"  Output Directory: {args.output}")
    print(f"  Verbose Mode: {args.verbose}")
    print("-" * 60)


def run_simulation(model: BookstoreModel, args, output_path: Path):
    """Run the main simulation loop"""
    start_time = time.time()
    step_interval = 60 if args.verbose else 120  # Print progress every N steps
    
    print(f"Starting simulation at {datetime.now().strftime('%H:%M:%S')}")
    print("Press Ctrl+C to stop simulation early\n")
    
    try:
        step_count = 0
        while model.running:
            model.step()
            step_count += 1
            
            # Print progress
            if args.verbose and step_count % step_interval == 0:
                summary = model.get_simulation_summary()
                inventory_status = bookstore_ontology.get_inventory_status()
                print(f"Step {step_count:4d} | "
                      f"Time: {summary['simulation_time']} | "
                      f"Revenue: ${summary['daily_revenue']:6.2f} | "
                      f"Transactions: {summary['total_transactions']:3d} | "
                      f"Active Customers: {summary['active_customers']:2d} | "
                      f"Total Stock: {inventory_status['total_stock']:4d} | "
                      f"Low Stock: {inventory_status['low_stock_count']:2d}")
            
            # Periodic data export (every 30 minutes of sim time)
            if step_count % 30 == 0:
                export_checkpoint_data(model, output_path, step_count)
    
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user")
        model.running = False
    
    simulation_time = time.time() - start_time
    print(f"\nSimulation completed in {simulation_time:.2f} seconds")
    print(f"Total simulation steps: {step_count}")
    
    return step_count


def export_checkpoint_data(model: BookstoreModel, output_path: Path, step: int):
    """Export checkpoint data during simulation"""
    checkpoint_file = output_path / 'data' / f'checkpoint_{step:06d}.json'
    
    try:
        summary = model.get_simulation_summary()
        inventory_status = bookstore_ontology.get_inventory_status()
        
        # Add inventory status to summary
        summary['inventory_status'] = inventory_status
        
        with open(checkpoint_file, 'w') as f:
            json.dump(summary, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save checkpoint data: {e}")


def generate_final_report(model: BookstoreModel, output_path: Path, args):
    """Generate comprehensive final report"""
    print("\nGenerating final report...")
    
    # Get all simulation data
    summary = model.get_simulation_summary()
    agent_states = model.get_agent_states()
    analytics = model.get_analytics_data()
    top_books = model.get_top_performing_books(20)
    employee_performance = model.get_employee_performance()
    customer_insights = model.get_customer_insights()
    inventory_status = bookstore_ontology.get_inventory_status()
    
    # Create final report data
    report_data = {
        'simulation_config': {
            'customers': args.customers,
            'employees': args.employees,
            'books': args.books,
            'hours': args.hours,
            'seed': args.seed
        },
        'simulation_summary': summary,
        'inventory_status': inventory_status,
        'agent_states': agent_states,
        'top_books': top_books,
        'employee_performance': employee_performance,
        'customer_insights': customer_insights,
        'transactions': [
            {
                'id': t.transaction_id,
                'customer_id': t.customer_id,
                'employee_id': t.employee_id,
                'total_amount': t.total_amount,
                'discount_applied': t.discount_applied,
                'books_count': len(t.books)
            } for t in model.transactions
        ],
        'inventory_alerts': model.inventory_alerts,
        'customer_visits': model.customer_visits
    }
    
    # Save comprehensive report
    report_file = output_path / f'simulation_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2, default=str)
    
    # Save analytics data if available
    if analytics['model_data'] is not None:
        analytics_file = output_path / 'data' / 'model_analytics.csv'
        analytics['model_data'].to_csv(analytics_file, index=False)
    
    if analytics['agent_data'] is not None:
        agent_analytics_file = output_path / 'data' / 'agent_analytics.csv'
        analytics['agent_data'].to_csv(agent_analytics_file, index=False)
    
    print(f"Final report saved to: {report_file}")
    return report_file


def print_simulation_summary(model: BookstoreModel):
    """Print simulation summary to console"""
    summary = model.get_simulation_summary()
    top_books = model.get_top_performing_books(5)
    employee_performance = model.get_employee_performance()
    customer_insights = model.get_customer_insights()
    inventory_status = bookstore_ontology.get_inventory_status()
    
    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)
    
    print("\n📊 Business Metrics:")
    print(f"  Total Revenue: ${summary['daily_revenue']:,.2f}")
    print(f"  Transactions: {summary['total_transactions']}")
    print(f"  Avg Transaction: ${summary['average_transaction_value']:,.2f}")
    print(f"  Customers Served: {summary['total_customers_served']}")
    print(f"  Customer Satisfaction: {summary['customer_satisfaction']:.1f}/10")
    
    print("\n📚 Top Performing Books:")
    for i, book in enumerate(top_books, 1):
        print(f"  {i}. {book['title']} - {book['total_sales']} sales")
    
    print("\n👥 Employee Performance:")
    for emp in employee_performance[:3]:
        print(f"  {emp['name']}: ${emp['daily_sales']:,.2f} sales, "
              f"{emp['customers_served']} customers")
    
    print("\n🛒 Customer Insights:")
    print(f"  Total Customers: {customer_insights['total_customers']}")
    print(f"  Average Customer Value: ${customer_insights['average_customer_value']:,.2f}")
    
    print("\n📦 Inventory Status:")
    print(f"  Total Books: {inventory_status['total_books']}")
    print(f"  Total Stock: {inventory_status['total_stock']} units")
    print(f"  Out of Stock: {inventory_status['out_of_stock_count']} books")
    print(f"  Low Stock: {inventory_status['low_stock_count']} books")
    print(f"  Avg Stock/Book: {inventory_status['average_stock_per_book']:.1f} units")
    print(f"  Inventory Alerts: {summary['inventory_alerts']}")
    
    print("=" * 60)


def run_gui_mode(args):
    """Run simulation with GUI visualization (if Mesa visualization is available)"""
    try:
        from mesa.visualization.ModularVisualization import ModularServer
        from mesa.visualization.modules import ChartModule, TextElement
        print("GUI mode is not yet implemented.")
        print("Running in console mode instead...")
        return False
    except ImportError:
        print("Mesa visualization not available. Running in console mode...")
        return False


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Quick mode adjustments
    if args.quick:
        args.customers = 10
        args.employees = 3
        args.books = 50
        args.hours = 1
    
    # Setup output directory
    output_path = setup_output_directory(args.output)
    
    # Print configuration
    print_simulation_header(args)
    
    # Try GUI mode if requested
    if args.gui and run_gui_mode(args):
        return
    
    try:
        # Create and configure model
        simulation_hours = args.hours
        if args.steps:
            simulation_hours = args.steps // 60
        
        model = BookstoreModel(
            num_customers=args.customers,
            num_employees=args.employees,
            num_books=args.books,
            simulation_hours=simulation_hours,
            seed=args.seed
        )
        
        # Override max steps if specified
        if args.steps:
            model.max_steps = args.steps
        
        # Run simulation
        total_steps = run_simulation(model, args, output_path)
        
        # Print summary
        print_simulation_summary(model)
        
        # Generate detailed report if requested
        if args.report:
            report_file = generate_final_report(model, output_path, args)
            print(f"\n📄 Detailed report available at: {report_file}")
        
        print(f"\n📁 All output saved to: {output_path}")
        
    except Exception as e:
        print(f"\nError: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()