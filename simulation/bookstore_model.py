"""
Bookstore Model

This module implements the Mesa-based simulation model for the bookstore management system.
It orchestrates the interactions between customers, employees, and books, while tracking
various metrics and analytics.
"""

import random
from typing import Dict, List, Any, Optional
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from datetime import datetime, timedelta
import uuid

from ontology.bookstore_ontology import (
    Book, Customer, Employee, Transaction, CustomerType, EmployeeRole, 
    BookCategory, bookstore_ontology
)
from agents.customer_agent import CustomerAgent
from agents.employee_agent import EmployeeAgent
from agents.book_agent import BookAgent


class BookstoreModel(Model):
    """
    Main simulation model for the bookstore management system.
    
    This model manages:
    - Customer, employee, and book agents
    - Transaction processing
    - Inventory management
    - Performance analytics
    - Business metrics tracking
    """
    
    def __init__(
        self,
        num_customers: int = 20,
        num_employees: int = 5,
        num_books: int = 100,
        simulation_hours: int = 8,
        seed: Optional[int] = None
    ):
        """
        Initialize the bookstore simulation model.
        
        Args:
            num_customers: Number of customer agents to create
            num_employees: Number of employee agents to create
            num_books: Number of book agents to create
            simulation_hours: Hours to simulate
            seed: Random seed for reproducibility
        """
        super().__init__()
        
        if seed is not None:
            random.seed(seed)
        
        # Model parameters
        self.num_customers = num_customers
        self.num_employees = num_employees
        self.num_books = num_books
        self.simulation_hours = simulation_hours
        self.steps_per_hour = 60  # Each step represents 1 minute
        self.max_steps = simulation_hours * self.steps_per_hour
        
        # Initialize scheduler
        self.schedule = RandomActivation(self)
        
        # Business metrics
        self.daily_revenue = 0.0
        self.total_transactions = 0
        self.total_customers_served = 0
        self.average_transaction_value = 0.0
        self.customer_satisfaction = 5.0
        
        # Tracking lists
        self.transactions: List[Transaction] = []
        self.customer_visits = []
        self.inventory_alerts = []
        
        # Initialize ontology with sample data
        self._initialize_sample_data()
        
        # Create agents
        self._create_book_agents()
        self._create_employee_agents()
        self._create_customer_agents()
        
        # Data collector for analytics
        self.datacollector = DataCollector(
            model_reporters={
                "Revenue": "daily_revenue",
                "Transactions": "total_transactions",
                "Active_Customers": lambda m: len([a for a in m.schedule.agents 
                                                 if isinstance(a, CustomerAgent) and a.is_shopping]),
                "Available_Employees": lambda m: len([a for a in m.schedule.agents 
                                                    if isinstance(a, EmployeeAgent) and not a.is_busy]),
                "Low_Stock_Books": lambda m: len([a for a in m.schedule.agents 
                                                if isinstance(a, BookAgent) and 
                                                a.book_data.stock_quantity <= a.reorder_point]),
                "Average_Customer_Satisfaction": "customer_satisfaction"
            },
            agent_reporters={
                "Customer_Budget": lambda a: a.budget if isinstance(a, CustomerAgent) else None,
                "Employee_Sales": lambda a: a.daily_sales if isinstance(a, EmployeeAgent) else None,
                "Book_Demand": lambda a: a.current_demand if isinstance(a, BookAgent) else None,
                "Book_Stock": lambda a: a.book_data.stock_quantity if isinstance(a, BookAgent) else None
            }
        )
        
        self.running = True
    
    def _initialize_sample_data(self):
        """Initialize the ontology with sample books, customers, and employees"""
        # Sample books
        sample_books = [
            ("978-0-123456-78-9", "The Great Adventure", "John Smith", BookCategory.FICTION, 15.99, 25),
            ("978-0-234567-89-0", "Python Programming", "Jane Doe", BookCategory.TECHNOLOGY, 49.99, 15),
            ("978-0-345678-90-1", "World History", "Bob Johnson", BookCategory.HISTORY, 29.99, 20),
            ("978-0-456789-01-2", "Mystery of the Castle", "Alice Brown", BookCategory.MYSTERY, 12.99, 30),
            ("978-0-567890-12-3", "Children's Tales", "Carol White", BookCategory.CHILDREN, 8.99, 40),
            ("978-0-678901-23-4", "Science Explained", "David Green", BookCategory.SCIENCE, 39.99, 12),
            ("978-0-789012-34-5", "Love in Spring", "Emma Davis", BookCategory.ROMANCE, 11.99, 35),
            ("978-0-890123-45-6", "Dragon Quest", "Frank Miller", BookCategory.FANTASY, 16.99, 22),
            ("978-0-901234-56-7", "Biography of Leaders", "Grace Wilson", BookCategory.BIOGRAPHY, 24.99, 18),
            ("978-0-012345-67-8", "Math Textbook", "Henry Taylor", BookCategory.TEXTBOOK, 89.99, 8)
        ]
        
        for isbn, title, author, category, price, stock in sample_books:
            book = Book(
                isbn=isbn,
                title=title,
                author=author,
                category=category,
                price=price,
                stock_quantity=stock,
                publisher=f"{author} Publications",
                publication_year=random.randint(2018, 2024),
                description=f"An excellent {category.value.lower()} book by {author}"
            )
            bookstore_ontology.books[isbn] = book
        
        # Add more random books to reach desired number
        categories = list(BookCategory)
        authors = ["Michael Johnson", "Sarah Connor", "Tom Anderson", "Lisa Park", 
                  "James Wilson", "Maria Garcia", "Robert Lee", "Jennifer Kim"]
        
        for i in range(len(sample_books), self.num_books):
            isbn = f"978-{random.randint(1000000000, 9999999999)}"
            category = random.choice(categories)
            author = random.choice(authors)
            
            book = Book(
                isbn=isbn,
                title=f"{category.value} Book {i+1}",
                author=author,
                category=category,
                price=round(random.uniform(9.99, 79.99), 2),
                stock_quantity=random.randint(5, 50),
                publisher=f"{author} Publications",
                publication_year=random.randint(2015, 2024),
                description=f"A great {category.value.lower()} book"
            )
            bookstore_ontology.books[isbn] = book
    
    def _create_book_agents(self):
        """Create book agents for all books in the ontology"""
        agent_id = 1
        for book in bookstore_ontology.books.values():
            book_agent = BookAgent(agent_id, self, book)
            self.schedule.add(book_agent)
            agent_id += 1
    
    def _create_employee_agents(self):
        """Create employee agents"""
        roles = [EmployeeRole.CASHIER, EmployeeRole.SALES_ASSOCIATE, EmployeeRole.MANAGER,
                EmployeeRole.INVENTORY_CLERK, EmployeeRole.CUSTOMER_SERVICE]
        
        names = ["Alice Johnson", "Bob Smith", "Carol Davis", "David Wilson", 
                "Emma Brown", "Frank Miller", "Grace Taylor", "Henry Anderson"]
        
        for i in range(self.num_employees):
            employee_id = f"EMP_{i+1:03d}"
            role = roles[i % len(roles)]
            name = names[i % len(names)]
            
            employee = Employee(
                employee_id=employee_id,
                name=f"{name} {i+1}",
                role=role,
                email=f"{name.lower().replace(' ', '.')}@bookstore.com",
                hire_date=datetime.now() - timedelta(days=random.randint(30, 1825)),
                salary=random.uniform(25000, 65000),
                performance_rating=random.uniform(5.0, 9.0)
            )
            
            bookstore_ontology.employees[employee_id] = employee
            
            employee_agent = EmployeeAgent(self.num_books + i + 1, self, employee)
            self.schedule.add(employee_agent)
    
    def _create_customer_agents(self):
        """Create customer agents"""
        customer_types = list(CustomerType)
        names = ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Wilson", 
                "Tom Brown", "Lisa Davis", "Chris Miller", "Anna Taylor",
                "Paul Anderson", "Mary Garcia", "Steve Martin", "Julie Lee"]
        
        for i in range(self.num_customers):
            customer_id = f"CUST_{i+1:04d}"
            customer_type = random.choice(customer_types)
            name = f"{random.choice(names)} {i+1}"
            
            customer = Customer(
                customer_id=customer_id,
                name=name,
                email=f"{name.lower().replace(' ', '.')}@email.com",
                phone=f"555-{random.randint(1000, 9999)}",
                customer_type=customer_type,
                registration_date=datetime.now() - timedelta(days=random.randint(1, 365)),
                total_purchases=random.uniform(0, 500),
                loyalty_points=random.randint(0, 100)
            )
            
            bookstore_ontology.customers[customer_id] = customer
            
            # Not all customers start shopping immediately
            if random.random() < 0.7:  # 70% chance to start shopping
                customer_agent = CustomerAgent(
                    self.num_books + self.num_employees + i + 1, self, customer
                )
                self.schedule.add(customer_agent)
    
    def step(self):
        """Execute one step of the simulation"""
        # Run all agent steps
        self.schedule.step()
        
        # Add new customers periodically
        if self.schedule.steps % 30 == 0:  # Every 30 minutes
            self._add_new_customers()
        
        # Update business metrics
        self._update_business_metrics()
        
        # Collect data
        self.datacollector.collect(self)
        
        # Check if simulation should continue
        if self.schedule.steps >= self.max_steps:
            self.running = False
    
    def _add_new_customers(self):
        """Add new customers to the simulation periodically"""
        num_new_customers = random.randint(1, 3)
        
        for _ in range(num_new_customers):
            customer_id = f"CUST_{len(bookstore_ontology.customers)+1:04d}"
            customer_type = random.choice(list(CustomerType))
            
            customer = Customer(
                customer_id=customer_id,
                name=f"New Customer {len(bookstore_ontology.customers)+1}",
                email=f"customer{len(bookstore_ontology.customers)+1}@email.com",
                phone=f"555-{random.randint(1000, 9999)}",
                customer_type=customer_type,
                registration_date=datetime.now(),
                total_purchases=0.0,
                loyalty_points=0
            )
            
            bookstore_ontology.customers[customer_id] = customer
            
            # Add customer agent to simulation
            new_agent_id = max([agent.unique_id for agent in self.schedule.agents]) + 1
            customer_agent = CustomerAgent(new_agent_id, self, customer)
            self.schedule.add(customer_agent)
    
    def record_transaction(
        self, 
        transaction_id: str, 
        customer_id: str, 
        employee_id: str, 
        books: List[Dict[str, Any]], 
        total_amount: float, 
        discount_applied: float
    ):
        """Record a completed transaction"""
        transaction = Transaction(
            transaction_id=transaction_id,
            customer_id=customer_id,
            employee_id=employee_id,
            books=books,
            total_amount=total_amount,
            discount_applied=discount_applied,
            transaction_date=datetime.now()
        )
        
        self.transactions.append(transaction)
        self.total_transactions += 1
        self.daily_revenue += (total_amount - discount_applied)
        
        # Update book sales
        for book_item in books:
            isbn = book_item['isbn']
            quantity = book_item['quantity']
            
            # Find book agent and process sale
            for agent in self.schedule.agents:
                if isinstance(agent, BookAgent) and agent.book_data.isbn == isbn:
                    agent.process_sale(quantity)
                    break
    
    def record_customer_visit(
        self, 
        customer_id: str, 
        duration: int, 
        purchased: bool, 
        interactions: int
    ):
        """Record a customer visit for analytics"""
        visit_record = {
            'customer_id': customer_id,
            'duration': duration,
            'purchased': purchased,
            'interactions': interactions,
            'step': self.schedule.steps
        }
        self.customer_visits.append(visit_record)
        
        if purchased:
            self.total_customers_served += 1
    
    def record_inventory_alert(
        self, 
        isbn: str, 
        current_stock: int, 
        suggested_quantity: int, 
        demand_level: float
    ):
        """Record inventory alert for low stock books"""
        alert = {
            'isbn': isbn,
            'current_stock': current_stock,
            'suggested_quantity': suggested_quantity,
            'demand_level': demand_level,
            'step': self.schedule.steps
        }
        self.inventory_alerts.append(alert)
    
    def _update_business_metrics(self):
        """Update business performance metrics"""
        if self.total_transactions > 0:
            self.average_transaction_value = self.daily_revenue / self.total_transactions
        
        # Calculate customer satisfaction based on various factors
        satisfaction_factors = []
        
        for agent in self.schedule.agents:
            if isinstance(agent, EmployeeAgent):
                satisfaction_factors.append(agent.customer_satisfaction_score)
        
        if satisfaction_factors:
            self.customer_satisfaction = sum(satisfaction_factors) / len(satisfaction_factors)
    
    def get_simulation_summary(self) -> Dict[str, Any]:
        """Get comprehensive simulation summary"""
        active_customers = len([a for a in self.schedule.agents 
                              if isinstance(a, CustomerAgent) and a.is_shopping])
        
        busy_employees = len([a for a in self.schedule.agents 
                            if isinstance(a, EmployeeAgent) and a.is_busy])
        
        low_stock_books = len([a for a in self.schedule.agents 
                             if isinstance(a, BookAgent) and 
                             a.book_data.stock_quantity <= a.reorder_point])
        
        return {
            'simulation_step': self.schedule.steps,
            'simulation_time': f"{self.schedule.steps // 60}h {self.schedule.steps % 60}m",
            'daily_revenue': round(self.daily_revenue, 2),
            'total_transactions': self.total_transactions,
            'average_transaction_value': round(self.average_transaction_value, 2),
            'total_customers_served': self.total_customers_served,
            'active_customers': active_customers,
            'busy_employees': busy_employees,
            'total_employees': self.num_employees,
            'low_stock_books': low_stock_books,
            'inventory_alerts': len(self.inventory_alerts),
            'customer_satisfaction': round(self.customer_satisfaction, 2),
            'customer_visits': len(self.customer_visits)
        }
    
    def get_agent_states(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get current state of all agents"""
        customers = []
        employees = []
        books = []
        
        for agent in self.schedule.agents:
            if isinstance(agent, CustomerAgent):
                customers.append(agent.get_state_info())
            elif isinstance(agent, EmployeeAgent):
                employees.append(agent.get_state_info())
            elif isinstance(agent, BookAgent):
                books.append(agent.get_state_info())
        
        return {
            'customers': customers,
            'employees': employees,
            'books': books
        }
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data from the data collector"""
        if hasattr(self.datacollector, 'model_vars'):
            return {
                'model_data': self.datacollector.get_model_vars_dataframe(),
                'agent_data': self.datacollector.get_agent_vars_dataframe()
            }
        return {'model_data': None, 'agent_data': None}
    
    def get_top_performing_books(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing books by sales"""
        book_performance = []
        
        for agent in self.schedule.agents:
            if isinstance(agent, BookAgent):
                book_info = agent.get_state_info()
                book_info['analytics'] = agent.get_analytics_summary()
                book_performance.append(book_info)
        
        # Sort by total sales
        book_performance.sort(key=lambda x: x['total_sales'], reverse=True)
        return book_performance[:limit]
    
    def get_employee_performance(self) -> List[Dict[str, Any]]:
        """Get employee performance metrics"""
        performance = []
        
        for agent in self.schedule.agents:
            if isinstance(agent, EmployeeAgent):
                performance.append(agent.get_state_info())
        
        # Sort by performance rating
        performance.sort(key=lambda x: x['performance_rating'], reverse=True)
        return performance
    
    def get_customer_insights(self) -> Dict[str, Any]:
        """Get customer behavior insights"""
        customer_type_stats = {}
        total_spent = 0
        total_customers = 0
        
        for customer in bookstore_ontology.customers.values():
            customer_type = customer.customer_type.value
            if customer_type not in customer_type_stats:
                customer_type_stats[customer_type] = {
                    'count': 0,
                    'total_spent': 0,
                    'average_spent': 0,
                    'total_loyalty_points': 0
                }
            
            customer_type_stats[customer_type]['count'] += 1
            customer_type_stats[customer_type]['total_spent'] += customer.total_purchases
            customer_type_stats[customer_type]['total_loyalty_points'] += customer.loyalty_points
            
            total_spent += customer.total_purchases
            total_customers += 1
        
        # Calculate averages
        for stats in customer_type_stats.values():
            if stats['count'] > 0:
                stats['average_spent'] = stats['total_spent'] / stats['count']
        
        return {
            'customer_type_breakdown': customer_type_stats,
            'total_customers': total_customers,
            'average_customer_value': total_spent / max(1, total_customers),
            'total_customer_spend': total_spent
        }