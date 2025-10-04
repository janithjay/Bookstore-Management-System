"""
Customer Agent

This module implements the customer agent for the bookstore management system.
Customer agents represent individual customers with behaviors like browsing,
purchasing, and interacting with the bookstore environment. Includes message bus
integration for agent communication.
"""

import random
from typing import List, Dict, Any, Optional
from mesa import Agent
from datetime import datetime

from ontology.bookstore_ontology import (
    Customer, CustomerType, BookCategory, bookstore_ontology
)
from communication.message_bus import message_bus, MessageType, Message


class CustomerAgent(Agent):
    """
    Customer agent that represents a customer in the bookstore simulation.
    
    Behaviors:
    - Browse books based on preferences
    - Make purchasing decisions
    - Interact with employees
    - Build loyalty over time
    """
    
    def __init__(self, unique_id: int, model, customer_data: Customer):
        """
        Initialize a customer agent.
        
        Args:
            unique_id: Unique identifier for the agent
            model: The Mesa model instance
            customer_data: Customer ontology data
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.customer_data = customer_data
        
        # Register with message bus
        agent_id = f"customer_{unique_id}"
        message_bus.register_agent(agent_id)
        
        # Subscribe to relevant message types
        message_bus.subscribe(agent_id, MessageType.PRICE_UPDATE, self._handle_price_update)
        message_bus.subscribe(agent_id, MessageType.LOW_STOCK_ALERT, self._handle_stock_alert)
        
        # Behavioral attributes
        self.preferred_categories = self._generate_preferences()
        self.budget = self._generate_budget()
        self.shopping_patience = random.randint(5, 20)  # Steps before leaving
        self.current_patience = self.shopping_patience
        
        # Shopping state
        self.shopping_cart: List[Dict[str, Any]] = []
        self.is_shopping = True
        self.current_activity = "browsing"
        self.interaction_history = []
        self.waiting_for_employee = False
        self.assigned_employee = None
        
        # Decision making parameters
        self.price_sensitivity = random.uniform(0.1, 0.9)  # 0 = price insensitive, 1 = very sensitive
        self.loyalty_factor = random.uniform(0.5, 1.0)  # Affects return probability
    
    def _generate_preferences(self) -> List[BookCategory]:
        """Generate preferred book categories for this customer"""
        num_preferences = random.randint(1, 4)
        return random.sample(list(BookCategory), num_preferences)
    
    def _generate_budget(self) -> float:
        """Generate budget based on customer type"""
        base_budgets = {
            CustomerType.PREMIUM: (100, 500),
            CustomerType.REGULAR: (50, 200),
            CustomerType.STUDENT: (20, 100),
            CustomerType.SENIOR: (30, 150)
        }
        min_budget, max_budget = base_budgets.get(
            self.customer_data.customer_type, (20, 100)
        )
        return random.uniform(min_budget, max_budget)
    
    def step(self):
        """Execute one step of customer behavior"""
        if not self.is_shopping:
            return
        
        # Process messages from other agents
        agent_id = f"customer_{self.unique_id}"
        message_bus.process_messages(agent_id)
        
        self.current_patience -= 1
        
        if self.current_patience <= 0:
            self._leave_store()
            return
        
        # Decide on action based on current activity
        if self.current_activity == "browsing":
            self._browse_books()
        elif self.current_activity == "evaluating":
            self._evaluate_purchase()
        elif self.current_activity == "purchasing":
            self._complete_purchase()
        elif self.current_activity == "seeking_help":
            self._seek_employee_help()
    
    def _handle_price_update(self, message: Message):
        """Handle price update messages"""
        isbn = message.content.get('isbn')
        new_price = message.content.get('new_price')
        
        # Check if this book is in our cart
        for item in self.shopping_cart:
            if item['isbn'] == isbn:
                item['price'] = new_price
                # Re-evaluate if we still want this book
                if new_price > self.budget * self.price_sensitivity:
                    self.shopping_cart.remove(item)
                    print(f"Customer {self.unique_id} removed book {isbn} due to price increase")
    
    def _handle_stock_alert(self, message: Message):
        """Handle low stock alerts"""
        isbn = message.content.get('isbn')
        
        # If we're interested in this book, prioritize purchase
        for item in self.shopping_cart:
            if item['isbn'] == isbn:
                if self.current_activity == "browsing":
                    self.current_activity = "purchasing"
                    print(f"Customer {self.unique_id} rushing to buy low-stock book {isbn}")
                break
    
    def _browse_books(self):
        """Browse available books based on preferences"""
        available_books = self._get_available_books()
        
        if not available_books:
            self.current_activity = "seeking_help"
            return
        
        # Select books to consider based on preferences
        preferred_books = []
        for book in available_books:
            if book.category in self.preferred_categories:
                preferred_books.append(book)
        
        # If no preferred books, consider random selection
        if not preferred_books:
            preferred_books = random.sample(
                available_books, 
                min(3, len(available_books))
            )
        else:
            # Select subset of preferred books
            preferred_books = random.sample(
                preferred_books, 
                min(3, len(preferred_books))
            )
        
        # Add books to consideration (shopping cart)
        for book in preferred_books:
            if self._should_consider_book(book):
                self._add_to_cart(book)
        
        if self.shopping_cart:
            self.current_activity = "evaluating"
        else:
            # Patience decreases faster if no interesting books found
            self.current_patience -= 1
    
    def _evaluate_purchase(self):
        """Evaluate items in shopping cart and decide whether to purchase"""
        if not self.shopping_cart:
            self.current_activity = "browsing"
            return
        
        total_cost = sum(item['price'] * item['quantity'] for item in self.shopping_cart)
        
        # Apply customer discount
        discount = bookstore_ontology.get_customer_discount(
            self.customer_data.customer_type
        )
        discounted_cost = total_cost * (1 - discount)
        
        # Decision factors
        within_budget = discounted_cost <= self.budget
        price_acceptable = self._is_price_acceptable(total_cost, discounted_cost)
        
        if within_budget and price_acceptable:
            self.current_activity = "purchasing"
        else:
            # Remove some items or leave
            if random.random() < 0.5:
                self._remove_expensive_items()
                if self.shopping_cart:
                    self.current_activity = "evaluating"  # Re-evaluate
                else:
                    self.current_activity = "browsing"
            else:
                self._leave_store()
    
    def _complete_purchase(self):
        """Complete the purchase transaction"""
        if not self.shopping_cart:
            self.current_activity = "browsing"
            return
        
        # Validate all items are still in stock before purchase
        valid_items = []
        for item in self.shopping_cart:
            book = bookstore_ontology.books.get(item['isbn'])
            if book and book.stock_quantity >= item['quantity']:
                valid_items.append(item)
            else:
                print(f"Customer {self.unique_id}: Book {item['isbn']} no longer has enough stock")
        
        # Update cart with valid items only
        self.shopping_cart = valid_items
        
        if not self.shopping_cart:
            print(f"Customer {self.unique_id}: All items out of stock, returning to browsing")
            self.current_activity = "browsing"
            return
        
        # Find available employee to process transaction
        available_employee = self._find_available_employee()
        
        if not available_employee:
            self.current_activity = "seeking_help"
            return
        
        # Create transaction
        transaction_books = []
        for item in self.shopping_cart:
            transaction_books.append({
                'isbn': item['isbn'],
                'quantity': item['quantity'],
                'unit_price': item['price']
            })
        
        total_amount = sum(item['price'] * item['quantity'] for item in self.shopping_cart)
        discount = bookstore_ontology.get_customer_discount(
            self.customer_data.customer_type
        )
        discount_amount = total_amount * discount
        
        # Record transaction in model
        transaction_id = f"TXN_{self.model.schedule.steps}_{self.unique_id}"
        
        # Process the transaction - this will update stock
        success = self.model.record_transaction(
            transaction_id=transaction_id,
            customer_id=self.customer_data.customer_id,
            employee_id=available_employee.employee_data.employee_id,
            books=transaction_books,
            total_amount=total_amount,
            discount_applied=discount_amount
        )
        
        if not success:
            print(f"Transaction {transaction_id} failed - insufficient stock")
            self.current_activity = "browsing"
            return
        
        # Update customer data
        self.customer_data.total_purchases += (total_amount - discount_amount)
        self.customer_data.loyalty_points += bookstore_ontology.calculate_loyalty_points(
            total_amount - discount_amount
        )
        
        # Update purchase history
        for item in self.shopping_cart:
            self.customer_data.purchase_history.append(item['isbn'])
        
        self.interaction_history.append({
            'type': 'purchase',
            'employee_id': available_employee.employee_data.employee_id,
            'amount': total_amount - discount_amount,
            'items_count': len(self.shopping_cart),
            'step': self.model.schedule.steps
        })
        
        # Clear cart and leave (satisfied customer)
        self.shopping_cart.clear()
        self._leave_store()
    
    def _seek_employee_help(self):
        """Seek help from an employee"""
        available_employee = self._find_available_employee()
        
        if available_employee:
            # Interact with employee
            help_type = random.choice(['recommendation', 'location', 'price_info'])
            
            self.interaction_history.append({
                'type': 'help_request',
                'employee_id': available_employee.employee_data.employee_id,
                'help_type': help_type,
                'step': self.model.schedule.steps
            })
            
            # Employee helps customer
            available_employee.assist_customer(self, help_type)
            
            # Customer becomes more patient after getting help
            self.current_patience += random.randint(2, 5)
            self.current_activity = "browsing"
        else:
            # No help available, customer becomes impatient
            self.current_patience -= 2
            if self.current_patience <= 0:
                self._leave_store()
    
    def _get_available_books(self) -> List:
        """Get list of available books from the model"""
        available_books = []
        for book in bookstore_ontology.books.values():
            if book.stock_quantity > 0:
                available_books.append(book)
        return available_books
    
    def _should_consider_book(self, book) -> bool:
        """Decide whether to consider a book for purchase"""
        # Price consideration
        if book.price > self.budget * 0.6:  # Don't consider books over 60% of budget
            return False
        
        # Category preference
        preference_bonus = 0.7 if book.category in self.preferred_categories else 0.3
        
        # Random factor
        random_factor = random.random()
        
        return random_factor < preference_bonus
    
    def _add_to_cart(self, book):
        """Add book to shopping cart"""
        # Verify book is still in stock
        if book.stock_quantity <= 0:
            return
        
        # Check if already in cart
        for item in self.shopping_cart:
            if item['isbn'] == book.isbn:
                # Only increase quantity if there's enough stock
                if item['quantity'] < book.stock_quantity:
                    item['quantity'] += 1
                return
        
        # Add new item
        self.shopping_cart.append({
            'isbn': book.isbn,
            'title': book.title,
            'price': book.price,
            'quantity': 1
        })
    
    def _is_price_acceptable(self, original_price: float, discounted_price: float) -> bool:
        """Check if the price is acceptable to the customer"""
        price_ratio = discounted_price / self.budget
        sensitivity_threshold = 1 - self.price_sensitivity
        
        return price_ratio <= sensitivity_threshold
    
    def _remove_expensive_items(self):
        """Remove most expensive items from cart"""
        if not self.shopping_cart:
            return
        
        # Sort by price (descending) and remove most expensive
        self.shopping_cart.sort(key=lambda x: x['price'], reverse=True)
        items_to_remove = max(1, len(self.shopping_cart) // 2)
        
        for _ in range(items_to_remove):
            if self.shopping_cart:
                self.shopping_cart.pop(0)
    
    def _find_available_employee(self):
        """Find an available employee to help with transaction"""
        from agents.employee_agent import EmployeeAgent
        
        employees = [agent for agent in self.model.schedule.agents 
                    if isinstance(agent, EmployeeAgent) and agent.is_available()]
        
        if employees:
            return random.choice(employees)
        return None
    
    def _leave_store(self):
        """Customer leaves the store"""
        self.is_shopping = False
        self.current_activity = "left"
        
        # Record interaction summary
        self.model.record_customer_visit(
            customer_id=self.customer_data.customer_id,
            duration=self.shopping_patience - self.current_patience,
            purchased=len([h for h in self.interaction_history if h['type'] == 'purchase']) > 0,
            interactions=len(self.interaction_history)
        )
    
    def receive_recommendation(self, recommended_books: List[str]):
        """Receive book recommendations from employee"""
        for isbn in recommended_books:
            book = bookstore_ontology.books.get(isbn)
            if book and self._should_consider_book(book):
                self._add_to_cart(book)
        
        # Increase patience after receiving help
        self.current_patience += 3
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information for reporting"""
        return {
            'customer_id': self.customer_data.customer_id,
            'customer_type': self.customer_data.customer_type.value,
            'is_shopping': self.is_shopping,
            'current_activity': self.current_activity,
            'cart_items': len(self.shopping_cart),
            'cart_value': sum(item['price'] * item['quantity'] for item in self.shopping_cart),
            'budget': self.budget,
            'patience_remaining': self.current_patience,
            'total_purchases': self.customer_data.total_purchases,
            'loyalty_points': self.customer_data.loyalty_points
        }