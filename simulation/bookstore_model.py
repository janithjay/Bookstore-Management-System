"""Mesa-based bookstore simulation model with agent orchestration and metrics tracking."""

import random
from typing import Dict, List, Any, Optional
from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from datetime import datetime, timedelta
import uuid

from ontology.bookstore_ontology import (
    Book, Customer, Employee, Transaction, Order, Inventory, CustomerType, EmployeeRole, 
    BookCategory, bookstore_ontology
)
from agents.customer_agent import CustomerAgent
from agents.employee_agent import EmployeeAgent
from agents.book_agent import BookAgent
from communication.message_bus import message_bus, MessageType


class BookstoreModel(Model):
    """Main simulation model managing customer, employee, and book agents with transaction processing."""
    
    def __init__(
        self,
        num_customers: int = 20,
        num_employees: int = 5,
        num_books: int = 100,
        simulation_hours: int = 8,
        seed: Optional[int] = None
    ):
        super().__init__()
        
        if seed is not None:
            random.seed(seed)
        
        # Initialize message bus for the simulation
        message_bus.clear_history()  # Clear any previous simulation data
        
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
        self.orders: List[Order] = []
        self.customer_visits = []
        self.inventory_alerts = []
        
        # Initialize ontology with sample data
        self._initialize_sample_data()
        
        # Initialize Owlready2 ontology with our data
        self._initialize_owl_ontology()
        
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
            
            # Create corresponding inventory item
            inventory_item = Inventory(
                isbn=isbn,
                current_stock=stock,
                minimum_threshold=5,
                maximum_capacity=100,
                reorder_quantity=25,
                last_restocked=datetime.now(),
                supplier=f"{author} Publications",
                location=f"Section {category.value[0]}-{isbn[-1]}"
            )
            bookstore_ontology.inventory[isbn] = inventory_item
        
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
            
            # Create corresponding inventory item
            inventory_item = Inventory(
                isbn=isbn,
                current_stock=book.stock_quantity,
                minimum_threshold=5,
                maximum_capacity=100,
                reorder_quantity=20,
                last_restocked=datetime.now(),
                supplier=f"Supplier for {author}",
                location=f"Section {category.value[0]}-{i%10}"
            )
            bookstore_ontology.inventory[isbn] = inventory_item
    
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
        
        # Process any pending messages in the message bus
        self._process_system_messages()
        
        # Apply SWRL rules if ontology is available
        self._apply_swrl_rules()
        
        # Add new customers periodically
        if self.schedule.steps % 30 == 0:  # Every 30 minutes
            self._add_new_customers()
        
        # Update business metrics
        self._update_business_metrics()
        
        # Update Owlready2 ontology if available
        self._update_owl_ontology()
        
        # Collect data
        self.datacollector.collect(self)
        
        # Check if simulation should continue
        if self.schedule.steps >= self.max_steps:
            self.running = False
    
    def _process_system_messages(self):
        """Process system-level messages and coordination"""
        # Get message bus statistics
        stats = message_bus.get_message_statistics()
        
        # Log interesting message activity
        if stats['pending_messages'] > 10:
            print(f"High message activity: {stats['pending_messages']} pending messages")
    
    def _apply_swrl_rules(self):
        """Apply SWRL rules across the system"""
        if hasattr(bookstore_ontology, 'owl_ontology') and bookstore_ontology.owl_ontology:
            # Check for low inventory items and apply rules
            for isbn, book in bookstore_ontology.books.items():
                if book.stock_quantity <= 5:
                    inventory_item = bookstore_ontology.inventory.get(isbn)
                    if inventory_item:
                        rule_result = bookstore_ontology.owl_ontology.apply_swrl_rule(
                            'low_inventory_triggers_restock',
                            inventory_item
                        )
                        if rule_result:
                            # Send message to employees about restock need
                            message_bus.publish(
                                'system',
                                MessageType.RESTOCK_REQUEST,
                                {
                                    'isbn': isbn,
                                    'current_stock': book.stock_quantity,
                                    'reorder_quantity': inventory_item.reorder_quantity,
                                    'priority': 'high' if book.stock_quantity <= 2 else 'medium'
                                },
                                priority=4 if book.stock_quantity <= 2 else 3
                            )
    
    def _initialize_owl_ontology(self):
        """Initialize Owlready2 ontology with simulation data"""
        if hasattr(bookstore_ontology, 'owl_ontology') and bookstore_ontology.owl_ontology:
            # Add all books to ontology
            for isbn, book in bookstore_ontology.books.items():
                bookstore_ontology.owl_ontology.add_book(book)
            
            # Add all customers to ontology
            for customer_id, customer in bookstore_ontology.customers.items():
                bookstore_ontology.owl_ontology.add_customer(customer)
            
            # Add all employees to ontology
            for employee_id, employee in bookstore_ontology.employees.items():
                bookstore_ontology.owl_ontology.add_employee(employee)
            
            print("Initialized Owlready2 ontology with simulation data")
    
    def _update_owl_ontology(self):
        """Update Owlready2 ontology with current simulation state"""
        if hasattr(bookstore_ontology, 'owl_ontology') and bookstore_ontology.owl_ontology:
            # Run reasoner every 60 steps (1 hour)
            if self.schedule.steps % 60 == 0:
                try:
                    bookstore_ontology.owl_ontology.run_reasoner()
                except Exception as e:
                    print(f"Warning: Reasoner error - {e}")
    
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
    ) -> bool:
        """
        Record a completed transaction
        
        Returns:
            True if transaction successful, False if any book out of stock
        """
        # Validate all books have sufficient stock before processing
        for book_item in books:
            isbn = book_item['isbn']
            quantity = book_item['quantity']
            
            book = bookstore_ontology.books.get(isbn)
            if not book or book.stock_quantity < quantity:
                print(f"Transaction {transaction_id} failed: Book {isbn} insufficient stock")
                return False
        
        # All validations passed, process the transaction
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
        
        # Calculate actual revenue (after discount)
        actual_revenue = total_amount - discount_applied
        self.daily_revenue += actual_revenue
        
        # Update book sales and stock
        for book_item in books:
            isbn = book_item['isbn']
            quantity = book_item['quantity']
            
            # Find book agent and process sale
            for agent in self.schedule.agents:
                if isinstance(agent, BookAgent) and agent.book_data.isbn == isbn:
                    agent.process_sale(quantity, customer_id=customer_id)
                    break
        
        # Notify employee of successful transaction (for their sales tracking)
        for agent in self.schedule.agents:
            if isinstance(agent, EmployeeAgent) and agent.employee_data.employee_id == employee_id:
                agent.record_successful_transaction(actual_revenue)
                break
        
        return True
    
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
        
        # Calculate discount statistics
        total_discounts = sum(t.discount_applied for t in self.transactions)
        total_original_amount = sum(t.total_amount for t in self.transactions)
        avg_discount_percentage = (total_discounts / total_original_amount * 100) if total_original_amount > 0 else 0
        
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
            'customer_visits': len(self.customer_visits),
            'total_discounts_given': round(total_discounts, 2),
            'average_discount_percentage': round(avg_discount_percentage, 1)
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
        """Get customer behavior insights
        
        Note: Returns ONLY simulation period purchases, not historical pre-simulation data.
        This ensures consistency with daily_revenue metric.
        """
        customer_type_stats = {}
        
        # Get actual customer agents that participated in simulation
        customer_agents = [a for a in self.schedule.agents if isinstance(a, CustomerAgent)]
        
        simulation_spent = 0
        participating_customers = 0
        
        for agent in customer_agents:
            customer = agent.customer_data
            customer_type = customer.customer_type.value
            
            # Calculate simulation-period purchases by looking at interaction history
            agent_purchases = sum(
                interaction['amount'] 
                for interaction in agent.interaction_history 
                if interaction['type'] == 'purchase'
            )
            
            if customer_type not in customer_type_stats:
                customer_type_stats[customer_type] = {
                    'count': 0,
                    'total_spent': 0,
                    'average_spent': 0,
                    'total_loyalty_points': 0,
                    'customers': 0
                }
            
            customer_type_stats[customer_type]['count'] += 1
            customer_type_stats[customer_type]['customers'] += 1
            customer_type_stats[customer_type]['total_spent'] += agent_purchases
            customer_type_stats[customer_type]['total_loyalty_points'] += customer.loyalty_points
            
            simulation_spent += agent_purchases
            participating_customers += 1
        
        # Calculate averages
        for stats in customer_type_stats.values():
            if stats['count'] > 0:
                stats['average_spent'] = stats['total_spent'] / stats['count']
        
        # Total customers includes all registered, but spend is only from active shoppers
        total_registered_customers = len(bookstore_ontology.customers)
        
        return {
            'customer_type_breakdown': customer_type_stats,
            'total_customers': total_registered_customers,
            'participating_customers': participating_customers,
            'average_customer_value': simulation_spent / max(1, participating_customers),
            'total_customer_spend': simulation_spent,
            'note': 'Spend values reflect simulation period only, not historical data'
        }
    
    def get_recent_transactions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent transactions with discount information
        
        Args:
            limit: Maximum number of transactions to return (default 20)
            
        Returns:
            List of transaction dictionaries with detailed information
        """
        recent = self.transactions[-limit:] if len(self.transactions) > limit else self.transactions
        
        transaction_list = []
        for trans in reversed(recent):  # Most recent first
            # Calculate discount percentage
            discount_percentage = (trans.discount_applied / trans.total_amount * 100) if trans.total_amount > 0 else 0
            
            # Get customer and employee names
            customer_name = bookstore_ontology.customers.get(trans.customer_id, None)
            employee_name = bookstore_ontology.employees.get(trans.employee_id, None)
            
            # Calculate final amount
            final_amount = trans.total_amount - trans.discount_applied
            
            # Get book details
            book_details = []
            for book_item in trans.books:
                book = bookstore_ontology.books.get(book_item['isbn'])
                if book:
                    book_details.append({
                        'title': book.title,
                        'isbn': book_item['isbn'],
                        'quantity': book_item['quantity'],
                        'unit_price': book_item.get('unit_price', book.price),
                        'subtotal': book_item['quantity'] * book_item.get('unit_price', book.price)
                    })
            
            transaction_list.append({
                'transaction_id': trans.transaction_id,
                'customer_id': trans.customer_id,
                'customer_name': customer_name.name if customer_name else 'Unknown',
                'employee_id': trans.employee_id,
                'employee_name': employee_name.name if employee_name else 'Unknown',
                'books': book_details,
                'book_count': len(trans.books),
                'total_items': sum(book_item['quantity'] for book_item in trans.books),
                'subtotal': trans.total_amount,
                'discount_amount': trans.discount_applied,
                'discount_percentage': round(discount_percentage, 1),
                'final_amount': final_amount,
                'transaction_date': trans.transaction_date,
                'payment_method': trans.payment_method
            })
        
        return transaction_list