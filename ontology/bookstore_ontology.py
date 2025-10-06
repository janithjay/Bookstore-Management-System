"""
Bookstore Ontology Definition with Owlready2 Integration

This module defines the ontological structure for the bookstore management system,
including concepts, relationships, and properties for books, customers, employees,
and bookstore operations using Owlready2 for formal ontology representation.
"""

import os
from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# Owlready2 imports for ontology management
try:
    from owlready2 import *
    OWLREADY_AVAILABLE = True
except ImportError:
    print("Warning: Owlready2 not available. Ontology will use basic Python classes.")
    OWLREADY_AVAILABLE = False


class BookCategory(Enum):
    """Enumeration of book categories"""
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science"
    TECHNOLOGY = "Technology"
    HISTORY = "History"
    BIOGRAPHY = "Biography"
    CHILDREN = "Children"
    REFERENCE = "Reference"
    TEXTBOOK = "Textbook"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    FANTASY = "Fantasy"


class CustomerType(Enum):
    """Enumeration of customer types"""
    REGULAR = "Regular"
    PREMIUM = "Premium"
    STUDENT = "Student"
    SENIOR = "Senior"


class EmployeeRole(Enum):
    """Enumeration of employee roles"""
    CASHIER = "Cashier"
    SALES_ASSOCIATE = "Sales Associate"
    MANAGER = "Manager"
    INVENTORY_CLERK = "Inventory Clerk"
    CUSTOMER_SERVICE = "Customer Service"


@dataclass
class Book:
    """Book entity definition"""
    isbn: str
    title: str
    author: str
    category: BookCategory
    price: float
    stock_quantity: int
    publisher: str
    publication_year: int
    description: str = ""
    
    def __post_init__(self):
        """Validate book data"""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")


@dataclass
class Customer:
    """Customer entity definition"""
    customer_id: str
    name: str
    email: str
    phone: str
    customer_type: CustomerType
    registration_date: datetime
    total_purchases: float = 0.0
    purchase_history: List[str] = None
    loyalty_points: int = 0
    
    def __post_init__(self):
        """Initialize purchase history if None"""
        if self.purchase_history is None:
            self.purchase_history = []


@dataclass
class Employee:
    """Employee entity definition"""
    employee_id: str
    name: str
    role: EmployeeRole
    email: str
    hire_date: datetime
    salary: float
    performance_rating: float = 0.0
    sales_count: int = 0
    
    def __post_init__(self):
        """Validate employee data"""
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")
        if not (0 <= self.performance_rating <= 10):
            self.performance_rating = 0.0


@dataclass
class Order:
    """Order entity definition"""
    order_id: str
    customer_id: str
    employee_id: str
    books: List[Dict[str, Any]]  # List of {isbn, quantity, unit_price}
    total_amount: float
    status: str  # "pending", "processing", "completed", "cancelled"
    order_date: datetime
    completion_date: datetime = None
    
    def calculate_total(self) -> float:
        """Calculate total order amount"""
        return sum(book['quantity'] * book['unit_price'] for book in self.books)


@dataclass
class Inventory:
    """Inventory entity definition"""
    isbn: str
    current_stock: int
    minimum_threshold: int
    maximum_capacity: int
    reorder_quantity: int
    last_restocked: datetime
    supplier: str = ""
    location: str = ""  # Shelf location in store
    
    def needs_restock(self) -> bool:
        """Check if inventory item needs restocking"""
        return self.current_stock <= self.minimum_threshold
    
    def can_fulfill_order(self, quantity: int) -> bool:
        """Check if inventory can fulfill an order"""
        return self.current_stock >= quantity
    
    def update_stock(self, quantity_change: int) -> bool:
        """Update stock quantity (positive for addition, negative for removal)"""
        new_stock = self.current_stock + quantity_change
        if new_stock < 0:
            return False
        self.current_stock = new_stock
        return True


@dataclass
class Transaction:
    """Transaction entity definition"""
    transaction_id: str
    customer_id: str
    employee_id: str
    books: List[Dict[str, Any]]  # List of {isbn, quantity, unit_price}
    total_amount: float
    discount_applied: float
    transaction_date: datetime
    payment_method: str = "Cash"
    
    def calculate_total(self) -> float:
        """Calculate total transaction amount"""
        subtotal = sum(book['quantity'] * book['unit_price'] for book in self.books)
        return subtotal - self.discount_applied


class BookstoreOntology:
    """Main ontology class that defines relationships and rules"""
    
    def __init__(self):
        """Initialize the bookstore ontology"""
        self.books: Dict[str, Book] = {}
        self.customers: Dict[str, Customer] = {}
        self.employees: Dict[str, Employee] = {}
        self.transactions: List[Transaction] = []
        self.orders: Dict[str, Order] = {}
        self.inventory: Dict[str, Inventory] = {}
        
        # Define business rules and relationships
        self.customer_discount_rules = {
            CustomerType.PREMIUM: 0.15,
            CustomerType.STUDENT: 0.10,
            CustomerType.SENIOR: 0.12,
            CustomerType.REGULAR: 0.05
        }
        
        self.category_relationships = {
            BookCategory.FICTION: [BookCategory.MYSTERY, BookCategory.ROMANCE, BookCategory.FANTASY],
            BookCategory.SCIENCE: [BookCategory.TECHNOLOGY],
            BookCategory.NON_FICTION: [BookCategory.BIOGRAPHY, BookCategory.HISTORY]
        }
        
        # Initialize Owlready2 ontology if available
        self.owl_ontology = None
        if OWLREADY_AVAILABLE:
            self._init_owl_ontology()
    
    def reset(self):
        """Reset ontology to initial state - clears all data"""
        # Clear Python data structures
        self.books.clear()
        self.customers.clear()
        self.employees.clear()
        self.transactions.clear()
        self.orders.clear()
        self.inventory.clear()
        
        # Reset OWL ontology if available
        if OWLREADY_AVAILABLE and self.owl_ontology:
            try:
                # Clear all instances from the ontology
                with self.owl_ontology:
                    # Get all instances
                    all_instances = list(self.owl_ontology.individuals())
                    for instance in all_instances:
                        try:
                            destroy_entity(instance)
                        except:
                            pass  # Ignore errors for individual instances
                            
                print("✅ Ontology reset successfully")
            except Exception as e:
                print(f"⚠️ Warning: Could not fully reset OWL ontology: {e}")
                # Fallback: recreate the ontology
                try:
                    self.owl_ontology = None
                    self._init_owl_ontology()
                except:
                    pass
    
    def get_customer_discount(self, customer_type: CustomerType) -> float:
        """Get discount percentage for customer type"""
        return self.customer_discount_rules.get(customer_type, 0.0)
    
    def get_related_categories(self, category: BookCategory) -> List[BookCategory]:
        """Get related book categories"""
        return self.category_relationships.get(category, [])
    
    def is_book_available(self, isbn: str, quantity: int = 1) -> bool:
        """Check if book is available in required quantity"""
        book = self.books.get(isbn)
        if not book:
            return False
        return book.stock_quantity >= quantity
    
    def can_employee_process_transaction(self, employee_id: str) -> bool:
        """Check if employee can process transactions"""
        employee = self.employees.get(employee_id)
        if not employee:
            return False
        return employee.role in [EmployeeRole.CASHIER, EmployeeRole.SALES_ASSOCIATE, EmployeeRole.MANAGER]
    
    def calculate_loyalty_points(self, amount: float) -> int:
        """Calculate loyalty points based on purchase amount"""
        return int(amount // 10)  # 1 point per $10 spent
    
    def get_book_recommendations(self, customer_id: str) -> List[str]:
        """Get book recommendations based on customer purchase history"""
        customer = self.customers.get(customer_id)
        if not customer or not customer.purchase_history:
            return []
        
        # Simple recommendation based on category preferences
        purchased_categories = set()
        for isbn in customer.purchase_history:
            book = self.books.get(isbn)
            if book:
                purchased_categories.add(book.category)
        
        recommendations = []
        for category in purchased_categories:
            related_categories = self.get_related_categories(category)
            for related_cat in related_categories:
                for isbn, book in self.books.items():
                    if book.category == related_cat and isbn not in customer.purchase_history:
                        recommendations.append(isbn)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate transaction before processing"""
        # Check customer exists
        if transaction.customer_id not in self.customers:
            return False
        
        # Check employee can process transaction
        if not self.can_employee_process_transaction(transaction.employee_id):
            return False
        
        # Check all books are available
        for book_item in transaction.books:
            if not self.is_book_available(book_item['isbn'], book_item['quantity']):
                return False
        
        return True
    
    def update_book_stock(self, isbn: str, quantity_change: int) -> bool:
        """
        Update book stock and synchronize with inventory
        
        Args:
            isbn: Book ISBN
            quantity_change: Change in quantity (positive = add, negative = reduce)
            
        Returns:
            True if successful, False if would result in negative stock
        """
        if isbn not in self.books:
            return False
        
        book = self.books[isbn]
        new_stock = book.stock_quantity + quantity_change
        
        if new_stock < 0:
            return False
        
        book.stock_quantity = new_stock
        
        # Synchronize with inventory object
        if isbn in self.inventory:
            self.inventory[isbn].current_stock = new_stock
            self.inventory[isbn].last_restocked = datetime.now()
        
        return True
    
    def get_inventory_status(self) -> Dict[str, Any]:
        """Get comprehensive inventory status"""
        total_books = len(self.books)
        total_stock = sum(book.stock_quantity for book in self.books.values())
        out_of_stock = sum(1 for book in self.books.values() if book.stock_quantity == 0)
        
        # Count low stock books
        low_stock = 0
        for isbn, book in self.books.items():
            if isbn in self.inventory:
                threshold = self.inventory[isbn].minimum_threshold
                if 0 < book.stock_quantity <= threshold:
                    low_stock += 1
        
        return {
            'total_books': total_books,
            'total_stock': total_stock,
            'out_of_stock_count': out_of_stock,
            'low_stock_count': low_stock,
            'average_stock_per_book': total_stock / max(1, total_books)
        }


class OwlBookstoreOntology:
    """Owlready2-based ontology implementation with SWRL rules"""
    
    def __init__(self):
        """Initialize the Owlready2 ontology"""
        if not OWLREADY_AVAILABLE:
            return
            
        # Create ontology
        self.onto = get_ontology("http://example.org/bookstore.owl")
        
        with self.onto:
            # Define classes
            class Person(Thing):
                pass
            
            class BookEntity(Thing):
                pass
            
            class BusinessEntity(Thing):
                pass
            
            class CustomerEntity(Person):
                pass
            
            class EmployeeEntity(Person):
                pass
            
            class BookItem(BookEntity):
                pass
            
            class OrderEntity(BusinessEntity):
                pass
            
            class InventoryItem(BusinessEntity):
                pass
            
            # Define object properties (relationships)
            class hasAuthorEntity(ObjectProperty):
                domain = [BookItem]
                range = [str]
            
            class hasGenreEntity(ObjectProperty):
                domain = [BookItem]
                range = [str]
            
            class purchases(ObjectProperty):
                domain = [CustomerEntity]
                range = [BookItem]
            
            class worksAt(ObjectProperty, FunctionalProperty):
                domain = [EmployeeEntity]
                range = [str]  # Bookstore name
            
            class processesOrder(ObjectProperty):
                domain = [EmployeeEntity]
                range = [OrderEntity]
            
            class containsBook(ObjectProperty):
                domain = [OrderEntity]
                range = [BookItem]
            
            # Define data properties
            class availableQuantity(DataProperty, FunctionalProperty):
                domain = [InventoryItem]
                range = [int]
            
            class hasPrice(DataProperty, FunctionalProperty):
                domain = [BookItem]
                range = [float]
            
            class hasStock(DataProperty, FunctionalProperty):
                domain = [BookItem]
                range = [int]
            
            class hasAuthor(DataProperty, FunctionalProperty):
                domain = [BookItem]
                range = [str]
            
            class hasGenre(DataProperty, FunctionalProperty):
                domain = [BookItem]
                range = [str]
            
            class customerType(DataProperty, FunctionalProperty):
                domain = [CustomerEntity]
                range = [str]
            
            class employeeRole(DataProperty, FunctionalProperty):
                domain = [EmployeeEntity]
                range = [str]
        
        # Store references
        self.Person = Person
        self.CustomerEntity = CustomerEntity
        self.EmployeeEntity = EmployeeEntity
        self.BookItem = BookItem
        self.OrderEntity = OrderEntity
        self.InventoryItem = InventoryItem
        
        # Initialize SWRL rules
        self._init_swrl_rules()
    
    def _init_swrl_rules(self):
        """Initialize SWRL (Semantic Web Rule Language) rules"""
        if not OWLREADY_AVAILABLE:
            return
        
        # Note: SWRL rules in Owlready2 are complex to implement programmatically
        # These rules would typically be defined in the OWL file or using specialized SWRL syntax
        # For this implementation, we'll define the rule logic in Python methods
        # that can be called by the agents during simulation
        
        self.swrl_rules = {
            'purchase_reduces_stock': self._rule_purchase_reduces_stock,
            'low_inventory_triggers_restock': self._rule_low_inventory_triggers_restock,
            'premium_customer_discount': self._rule_premium_customer_discount,
            'employee_can_process_order': self._rule_employee_can_process_order
        }
    
    def _rule_purchase_reduces_stock(self, customer_id: str, book_isbn: str, quantity: int = 1):
        """SWRL Rule: If a customer purchases a book, reduce stock"""
        # This rule logic would be called when a purchase occurs
        return {
            'action': 'reduce_stock',
            'book_isbn': book_isbn,
            'quantity': quantity,
            'customer_id': customer_id
        }
    
    def _rule_low_inventory_triggers_restock(self, inventory_item):
        """SWRL Rule: If inventory is low (< threshold), trigger restock"""
        if hasattr(inventory_item, 'needs_restock') and inventory_item.needs_restock():
            return {
                'action': 'trigger_restock',
                'isbn': inventory_item.isbn,
                'current_stock': inventory_item.current_stock,
                'reorder_quantity': inventory_item.reorder_quantity
            }
        return None
    
    def _rule_premium_customer_discount(self, customer_type: str, base_price: float):
        """SWRL Rule: Premium customers get discount"""
        discounts = {
            'PREMIUM': 0.15,
            'STUDENT': 0.10,
            'SENIOR': 0.12,
            'REGULAR': 0.05
        }
        discount = discounts.get(customer_type, 0.0)
        return {
            'action': 'apply_discount',
            'discount_rate': discount,
            'final_price': base_price * (1 - discount)
        }
    
    def _rule_employee_can_process_order(self, employee_role: str):
        """SWRL Rule: Check if employee can process orders based on role"""
        authorized_roles = ['CASHIER', 'SALES_ASSOCIATE', 'MANAGER']
        return {
            'action': 'check_authorization',
            'can_process': employee_role in authorized_roles
        }
    
    def apply_swrl_rule(self, rule_name: str, *args, **kwargs):
        """Apply a specific SWRL rule"""
        if rule_name in self.swrl_rules:
            return self.swrl_rules[rule_name](*args, **kwargs)
        return None
    
    def add_customer(self, customer_data: Customer):
        """Add customer to ontology"""
        if not OWLREADY_AVAILABLE:
            return
            
        with self.onto:
            customer_instance = self.CustomerEntity(f"customer_{customer_data.customer_id}")
            customer_instance.customerType = customer_data.customer_type.value
    
    def add_book(self, book_data: Book):
        """Add book to ontology"""
        if not OWLREADY_AVAILABLE:
            return
            
        try:
            with self.onto:
                book_id = f"book_{book_data.isbn.replace('-', '_')}"
                # Check if instance already exists
                existing = self.onto.search_one(iri=f"*{book_id}")
                if existing:
                    # Update existing instance
                    existing.hasAuthor = book_data.author
                    existing.hasGenre = book_data.category.value
                    existing.hasPrice = book_data.price
                    existing.hasStock = book_data.stock_quantity
                else:
                    # Create new instance
                    book_instance = self.BookItem(book_id)
                    book_instance.hasAuthor = book_data.author
                    book_instance.hasGenre = book_data.category.value
                    book_instance.hasPrice = book_data.price
                    book_instance.hasStock = book_data.stock_quantity
        except Exception as e:
            print(f"Warning: Could not add book to OWL ontology: {e}")
    
    def add_employee(self, employee_data: Employee):
        """Add employee to ontology"""
        if not OWLREADY_AVAILABLE:
            return
            
        try:
            with self.onto:
                emp_id = f"employee_{employee_data.employee_id}"
                # Check if instance already exists
                existing = self.onto.search_one(iri=f"*{emp_id}")
                if existing:
                    # Update existing instance
                    existing.employeeRole = employee_data.role.value
                    existing.worksAt = "MainBookstore"
                else:
                    # Create new instance
                    employee_instance = self.EmployeeEntity(emp_id)
                    employee_instance.employeeRole = employee_data.role.value
                    employee_instance.worksAt = "MainBookstore"
        except Exception as e:
            print(f"Warning: Could not add employee to OWL ontology: {e}")
    
    def run_reasoner(self):
        """Run the reasoning engine to apply SWRL rules"""
        if not OWLREADY_AVAILABLE:
            return
            
        try:
            with self.onto:
                sync_reasoner_pellet([self.onto])
        except Exception as e:
            print(f"Warning: Could not run reasoner - {e}")
    
    def save_ontology(self, filepath: str = "bookstore_ontology.owl"):
        """Save ontology to OWL file"""
        if not OWLREADY_AVAILABLE:
            return
            
        try:
            self.onto.save(file=filepath, format="rdfxml")
        except Exception as e:
            print(f"Warning: Could not save ontology - {e}")


# Add Owlready2 initialization to main ontology class
def _init_owl_ontology(self):
    """Initialize Owlready2 ontology"""
    try:
        self.owl_ontology = OwlBookstoreOntology()
    except Exception as e:
        print(f"Warning: Could not initialize Owlready2 ontology - {e}")
        self.owl_ontology = None

# Add the method to BookstoreOntology class
BookstoreOntology._init_owl_ontology = _init_owl_ontology


# Ontology instance for global use
bookstore_ontology = BookstoreOntology()