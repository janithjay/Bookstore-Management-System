"""
Employee Agent

This module implements the employee agent for the bookstore management system.
Employee agents represent staff members with different roles and responsibilities
like processing transactions, helping customers, and managing inventory.
"""

import random
from typing import List, Dict, Any, Optional
from mesa import Agent
from datetime import datetime

from ontology.bookstore_ontology import (
    Employee, EmployeeRole, bookstore_ontology
)


class EmployeeAgent(Agent):
    """
    Employee agent that represents a staff member in the bookstore simulation.
    
    Behaviors:
    - Process customer transactions
    - Assist customers with inquiries
    - Manage inventory (for certain roles)
    - Performance tracking
    """
    
    def __init__(self, unique_id: int, model, employee_data: Employee):
        """
        Initialize an employee agent.
        
        Args:
            unique_id: Unique identifier for the agent
            model: The Mesa model instance
            employee_data: Employee ontology data
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.employee_data = employee_data
        
        # Work state attributes
        self.is_busy = False
        self.current_customer = None
        self.current_task = "available"
        self.task_duration = 0
        self.shift_hours = 8  # 8-hour shift
        self.hours_worked = 0
        
        # Performance attributes
        self.daily_sales = 0.0
        self.customers_served = 0
        self.transactions_processed = 0
        self.customer_satisfaction_score = 5.0  # Out of 10
        
        # Role-specific capabilities
        self.capabilities = self._get_role_capabilities()
        
        # Work efficiency based on role and experience
        self.efficiency = self._calculate_efficiency()
        
        # Customer interaction history
        self.interaction_history = []
    
    def _get_role_capabilities(self) -> List[str]:
        """Get capabilities based on employee role"""
        role_capabilities = {
            EmployeeRole.CASHIER: ['process_transaction', 'handle_returns', 'customer_service'],
            EmployeeRole.SALES_ASSOCIATE: ['customer_assistance', 'product_recommendation', 
                                         'inventory_check', 'process_transaction'],
            EmployeeRole.MANAGER: ['process_transaction', 'customer_service', 'inventory_management',
                                 'staff_supervision', 'handle_complaints'],
            EmployeeRole.INVENTORY_CLERK: ['inventory_management', 'stock_replenishment', 
                                         'inventory_check'],
            EmployeeRole.CUSTOMER_SERVICE: ['customer_assistance', 'handle_complaints', 
                                          'product_recommendation', 'handle_returns']
        }
        return role_capabilities.get(self.employee_data.role, ['customer_service'])
    
    def _calculate_efficiency(self) -> float:
        """Calculate work efficiency based on role and performance"""
        base_efficiency = {
            EmployeeRole.CASHIER: 0.8,
            EmployeeRole.SALES_ASSOCIATE: 0.7,
            EmployeeRole.MANAGER: 0.9,
            EmployeeRole.INVENTORY_CLERK: 0.6,
            EmployeeRole.CUSTOMER_SERVICE: 0.75
        }
        
        role_efficiency = base_efficiency.get(self.employee_data.role, 0.7)
        performance_bonus = (self.employee_data.performance_rating / 10) * 0.3
        
        return min(1.0, role_efficiency + performance_bonus + random.uniform(-0.1, 0.1))
    
    def step(self):
        """Execute one step of employee behavior"""
        self.hours_worked += 1/60  # Assuming each step is roughly 1 minute
        
        if self.hours_worked >= self.shift_hours:
            self._end_shift()
            return
        
        # Handle current task
        if self.is_busy and self.task_duration > 0:
            self.task_duration -= 1
            return
        
        # Task completed, become available
        if self.is_busy and self.task_duration <= 0:
            self._complete_current_task()
        
        # Look for work to do
        if not self.is_busy:
            self._find_work()
    
    def _find_work(self):
        """Look for work to do based on role capabilities"""
        # Priority 1: Help waiting customers
        if 'customer_assistance' in self.capabilities or 'customer_service' in self.capabilities:
            waiting_customers = self._find_customers_needing_help()
            if waiting_customers:
                self._start_customer_assistance(random.choice(waiting_customers))
                return
        
        # Priority 2: Process transactions
        if 'process_transaction' in self.capabilities:
            customers_ready_to_buy = self._find_customers_ready_to_purchase()
            if customers_ready_to_buy:
                self._start_transaction_processing(random.choice(customers_ready_to_buy))
                return
        
        # Priority 3: Inventory management
        if 'inventory_management' in self.capabilities:
            if self._should_do_inventory_work():
                self._start_inventory_work()
                return
        
        # Priority 4: General maintenance tasks
        if random.random() < 0.1:  # 10% chance to do maintenance
            self._start_maintenance_task()
    
    def _find_customers_needing_help(self) -> List:
        """Find customers who need assistance"""
        from agents.customer_agent import CustomerAgent
        
        customers = [agent for agent in self.model.schedule.agents 
                    if isinstance(agent, CustomerAgent) 
                    and agent.current_activity == "seeking_help"
                    and agent.is_shopping]
        return customers
    
    def _find_customers_ready_to_purchase(self) -> List:
        """Find customers ready to make a purchase"""
        from agents.customer_agent import CustomerAgent
        
        customers = [agent for agent in self.model.schedule.agents 
                    if isinstance(agent, CustomerAgent) 
                    and agent.current_activity == "purchasing"
                    and agent.is_shopping]
        return customers
    
    def _start_customer_assistance(self, customer):
        """Start helping a customer"""
        self.is_busy = True
        self.current_customer = customer
        self.current_task = "customer_assistance"
        self.task_duration = random.randint(2, 5)  # 2-5 steps to help
        
        self.interaction_history.append({
            'type': 'customer_assistance_start',
            'customer_id': customer.customer_data.customer_id,
            'step': self.model.schedule.steps
        })
    
    def _start_transaction_processing(self, customer):
        """Start processing a customer transaction"""
        self.is_busy = True
        self.current_customer = customer
        self.current_task = "process_transaction"
        
        # Transaction processing time based on cart size and efficiency
        cart_size = len(customer.shopping_cart)
        base_time = max(1, cart_size)
        self.task_duration = max(1, int(base_time / self.efficiency))
        
        self.interaction_history.append({
            'type': 'transaction_start',
            'customer_id': customer.customer_data.customer_id,
            'cart_size': cart_size,
            'step': self.model.schedule.steps
        })
    
    def _start_inventory_work(self):
        """Start inventory management work"""
        self.is_busy = True
        self.current_task = "inventory_work"
        self.task_duration = random.randint(3, 8)  # 3-8 steps for inventory work
        
        self.interaction_history.append({
            'type': 'inventory_work_start',
            'step': self.model.schedule.steps
        })
    
    def _start_maintenance_task(self):
        """Start general maintenance task"""
        self.is_busy = True
        self.current_task = "maintenance"
        self.task_duration = random.randint(1, 3)
        
        self.interaction_history.append({
            'type': 'maintenance_start',
            'step': self.model.schedule.steps
        })
    
    def _complete_current_task(self):
        """Complete the current task and update metrics"""
        if self.current_task == "customer_assistance":
            self._complete_customer_assistance()
        elif self.current_task == "process_transaction":
            self._complete_transaction()
        elif self.current_task == "inventory_work":
            self._complete_inventory_work()
        elif self.current_task == "maintenance":
            self._complete_maintenance()
        
        # Reset state
        self.is_busy = False
        self.current_customer = None
        self.current_task = "available"
        self.task_duration = 0
    
    def _complete_customer_assistance(self):
        """Complete customer assistance task"""
        if self.current_customer:
            self.customers_served += 1
            
            # Update customer satisfaction based on employee performance
            satisfaction_impact = (self.employee_data.performance_rating / 10) * 2
            self.customer_satisfaction_score = min(10, 
                self.customer_satisfaction_score + satisfaction_impact * 0.1)
            
            self.interaction_history.append({
                'type': 'customer_assistance_complete',
                'customer_id': self.current_customer.customer_data.customer_id,
                'step': self.model.schedule.steps
            })
    
    def _complete_transaction(self):
        """Complete transaction processing"""
        if self.current_customer:
            self.transactions_processed += 1
            
            # Calculate transaction value
            cart_value = sum(item['price'] * item['quantity'] 
                           for item in self.current_customer.shopping_cart)
            self.daily_sales += cart_value
            
            # Update employee sales count
            self.employee_data.sales_count += 1
            
            # Performance impact based on transaction efficiency
            if self.task_duration <= 2:  # Fast service
                self.customer_satisfaction_score = min(10, 
                    self.customer_satisfaction_score + 0.1)
            
            self.interaction_history.append({
                'type': 'transaction_complete',
                'customer_id': self.current_customer.customer_data.customer_id,
                'transaction_value': cart_value,
                'step': self.model.schedule.steps
            })
    
    def _complete_inventory_work(self):
        """Complete inventory management work"""
        # Simulate inventory updates
        books_restocked = random.randint(1, 5)
        
        # Randomly select books to restock
        available_books = list(bookstore_ontology.books.values())
        books_to_restock = random.sample(available_books, 
                                       min(books_restocked, len(available_books)))
        
        for book in books_to_restock:
            restock_amount = random.randint(1, 10)
            book.stock_quantity += restock_amount
        
        self.interaction_history.append({
            'type': 'inventory_work_complete',
            'books_restocked': books_restocked,
            'step': self.model.schedule.steps
        })
    
    def _complete_maintenance(self):
        """Complete maintenance task"""
        self.interaction_history.append({
            'type': 'maintenance_complete',
            'step': self.model.schedule.steps
        })
    
    def _should_do_inventory_work(self) -> bool:
        """Check if inventory work is needed"""
        # Check if any books are low in stock
        low_stock_books = [book for book in bookstore_ontology.books.values() 
                          if book.stock_quantity < 5]
        
        return len(low_stock_books) > 0 and random.random() < 0.3
    
    def assist_customer(self, customer, help_type: str):
        """Assist a customer with specific help type"""
        if help_type == "recommendation":
            recommendations = bookstore_ontology.get_book_recommendations(
                customer.customer_data.customer_id
            )
            if not recommendations:
                # Provide random recommendations from preferred categories
                available_books = [book for book in bookstore_ontology.books.values() 
                                 if book.category in customer.preferred_categories 
                                 and book.stock_quantity > 0]
                recommendations = [book.isbn for book in 
                                 random.sample(available_books, 
                                             min(3, len(available_books)))]
            
            customer.receive_recommendation(recommendations)
        
        elif help_type == "location":
            # Help customer find books (increase patience)
            customer.current_patience += 2
        
        elif help_type == "price_info":
            # Provide price information (slight patience boost)
            customer.current_patience += 1
        
        # Record the assistance
        self.interaction_history.append({
            'type': 'customer_assistance',
            'customer_id': customer.customer_data.customer_id,
            'help_type': help_type,
            'step': self.model.schedule.steps
        })
    
    def _end_shift(self):
        """End employee shift and update performance"""
        # Update daily performance rating
        performance_factors = [
            self.daily_sales / 1000,  # Sales performance
            self.customers_served / 10,  # Customer service
            self.customer_satisfaction_score / 10,  # Satisfaction
            self.efficiency  # Work efficiency
        ]
        
        daily_performance = sum(performance_factors) / len(performance_factors) * 10
        
        # Update overall performance rating (weighted average)
        weight = 0.1  # New day weight
        self.employee_data.performance_rating = (
            (1 - weight) * self.employee_data.performance_rating + 
            weight * daily_performance
        )
        
        # Reset daily counters
        self.daily_sales = 0.0
        self.customers_served = 0
        self.transactions_processed = 0
        self.hours_worked = 0
        
        # Remove from simulation (end of shift)
        self.model.schedule.remove(self)
    
    def is_available(self) -> bool:
        """Check if employee is available to help customers"""
        return not self.is_busy and 'process_transaction' in self.capabilities
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information for reporting"""
        return {
            'employee_id': self.employee_data.employee_id,
            'name': self.employee_data.name,
            'role': self.employee_data.role.value,
            'is_busy': self.is_busy,
            'current_task': self.current_task,
            'hours_worked': round(self.hours_worked, 2),
            'daily_sales': self.daily_sales,
            'customers_served': self.customers_served,
            'transactions_processed': self.transactions_processed,
            'performance_rating': round(self.employee_data.performance_rating, 2),
            'customer_satisfaction': round(self.customer_satisfaction_score, 2),
            'efficiency': round(self.efficiency, 2)
        }