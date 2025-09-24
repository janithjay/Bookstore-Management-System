"""
Bookstore Ontology Definition

This module defines the ontological structure for the bookstore management system,
including concepts, relationships, and properties for books, customers, employees,
and bookstore operations.
"""

from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


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


# Ontology instance for global use
bookstore_ontology = BookstoreOntology()