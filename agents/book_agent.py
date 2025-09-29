"""
Book Agent

This module implements the book agent for the bookstore management system.
Book agents represent individual books with behaviors like demand simulation,
pricing dynamics, and popularity tracking. Includes message bus integration
for inventory alerts and price updates.
"""

import random
from typing import Dict, Any, List
from mesa import Agent
from datetime import datetime, timedelta

from ontology.bookstore_ontology import Book, BookCategory, bookstore_ontology
from communication.message_bus import message_bus, MessageType, Message


class BookAgent(Agent):
    """
    Book agent that represents a book in the bookstore simulation.
    
    Behaviors:
    - Track popularity and demand
    - Simulate seasonal effects
    - Price elasticity simulation
    - Inventory alerts
    """
    
    def __init__(self, unique_id: int, model, book_data: Book):
        """
        Initialize a book agent.
        
        Args:
            unique_id: Unique identifier for the agent
            model: The Mesa model instance
            book_data: Book ontology data
        """
        super().__init__(model)
        self.unique_id = unique_id
        self.book_data = book_data
        
        # Register with message bus
        agent_id = f"book_{book_data.isbn}"
        message_bus.register_agent(agent_id)
        
        # Market dynamics attributes
        self.base_demand = self._calculate_base_demand()
        self.current_demand = self.base_demand
        self.popularity_score = random.uniform(0.1, 1.0)
        self.demand_trend = random.choice([-0.01, 0, 0.01])  # Daily change
        
        # Sales tracking
        self.daily_sales = 0
        self.weekly_sales = 0
        self.total_sales = 0
        self.days_since_last_sale = 0
        
        # Pricing attributes
        self.original_price = book_data.price
        self.price_elasticity = self._calculate_price_elasticity()
        self.discount_rate = 0.0
        
        # Inventory management
        self.reorder_point = random.randint(5, 15)
        self.max_stock_level = random.randint(20, 50)
        self.days_out_of_stock = 0
        
        # Seasonal factors
        self.seasonal_factor = 1.0
        self.seasonal_categories = self._get_seasonal_categories()
        
        # Competition and market factors
        self.market_competition = random.uniform(0.5, 1.5)
        self.customer_reviews_score = random.uniform(3.0, 5.0)
        
        # Analytics tracking
        self.demand_history = []
        self.price_history = []
        self.stock_history = []
    
    def _calculate_base_demand(self) -> float:
        """Calculate base demand based on book characteristics"""
        category_demand = {
            BookCategory.FICTION: 0.8,
            BookCategory.MYSTERY: 0.7,
            BookCategory.ROMANCE: 0.9,
            BookCategory.FANTASY: 0.6,
            BookCategory.SCIENCE: 0.4,
            BookCategory.TECHNOLOGY: 0.3,
            BookCategory.HISTORY: 0.5,
            BookCategory.BIOGRAPHY: 0.6,
            BookCategory.CHILDREN: 0.7,
            BookCategory.TEXTBOOK: 0.5,
            BookCategory.REFERENCE: 0.2,
            BookCategory.NON_FICTION: 0.6
        }
        
        base = category_demand.get(self.book_data.category, 0.5)
        
        # Adjust for price (higher price generally means lower demand)
        price_factor = max(0.1, 1.0 - (self.book_data.price / 100))
        
        # Random variation
        random_factor = random.uniform(0.8, 1.2)
        
        return base * price_factor * random_factor
    
    def _calculate_price_elasticity(self) -> float:
        """Calculate price elasticity based on book type"""
        elasticity_map = {
            BookCategory.TEXTBOOK: -0.3,  # Less elastic (essential)
            BookCategory.REFERENCE: -0.3,
            BookCategory.SCIENCE: -0.4,
            BookCategory.TECHNOLOGY: -0.4,
            BookCategory.FICTION: -0.8,  # More elastic (entertainment)
            BookCategory.ROMANCE: -0.9,
            BookCategory.MYSTERY: -0.8,
            BookCategory.FANTASY: -0.7,
            BookCategory.CHILDREN: -0.6,
            BookCategory.BIOGRAPHY: -0.5,
            BookCategory.HISTORY: -0.5,
            BookCategory.NON_FICTION: -0.6
        }
        
        return elasticity_map.get(self.book_data.category, -0.6)
    
    def _get_seasonal_categories(self) -> Dict[str, float]:
        """Get seasonal factors for different times of year"""
        seasonal_map = {
            BookCategory.TEXTBOOK: {'fall': 2.0, 'spring': 1.5, 'summer': 0.3, 'winter': 0.8},
            BookCategory.CHILDREN: {'fall': 1.2, 'spring': 1.0, 'summer': 1.5, 'winter': 1.8},
            BookCategory.ROMANCE: {'fall': 1.0, 'spring': 1.3, 'summer': 1.2, 'winter': 0.8},
            BookCategory.MYSTERY: {'fall': 1.2, 'spring': 1.0, 'summer': 1.1, 'winter': 1.1},
            BookCategory.FANTASY: {'fall': 1.1, 'spring': 1.0, 'summer': 1.2, 'winter': 1.0},
            BookCategory.SCIENCE: {'fall': 1.1, 'spring': 1.0, 'summer': 0.9, 'winter': 1.0},
            BookCategory.TECHNOLOGY: {'fall': 1.2, 'spring': 1.1, 'summer': 0.8, 'winter': 1.0},
            BookCategory.HISTORY: {'fall': 1.0, 'spring': 1.0, 'summer': 1.0, 'winter': 1.0},
            BookCategory.BIOGRAPHY: {'fall': 1.0, 'spring': 1.0, 'summer': 1.1, 'winter': 1.0},
            BookCategory.REFERENCE: {'fall': 1.3, 'spring': 1.2, 'summer': 0.7, 'winter': 1.0},
            BookCategory.NON_FICTION: {'fall': 1.0, 'spring': 1.0, 'summer': 1.0, 'winter': 1.0},
            BookCategory.FICTION: {'fall': 1.0, 'spring': 1.0, 'summer': 1.2, 'winter': 1.1}
        }
        
        return seasonal_map.get(self.book_data.category, 
                              {'fall': 1.0, 'spring': 1.0, 'summer': 1.0, 'winter': 1.0})
    
    def step(self):
        """Execute one step of book behavior"""
        # Update demand based on various factors
        self._update_demand()
        
        # Update pricing if needed
        self._update_pricing()
        
        # Check inventory levels and send alerts if needed
        self._check_inventory_and_alert()
        
        # Update popularity based on sales
        self._update_popularity()
        
        # Record analytics
        self._record_analytics()
        
        # Update counters
        if self.daily_sales == 0:
            self.days_since_last_sale += 1
        else:
            self.days_since_last_sale = 0
        
        # Check if out of stock
        if self.book_data.stock_quantity == 0:
            self.days_out_of_stock += 1
        else:
            self.days_out_of_stock = 0
    
    def _check_inventory_and_alert(self):
        """Check inventory levels and send alerts using message bus"""
        stock_level = self.book_data.stock_quantity
        
        # Send low stock alert if stock is below threshold
        if stock_level <= 5 and stock_level > 0:
            message_bus.publish(
                f"book_{self.book_data.isbn}",
                MessageType.LOW_STOCK_ALERT,
                {
                    'isbn': self.book_data.isbn,
                    'title': self.book_data.title,
                    'current_stock': stock_level,
                    'threshold': 5,
                    'reorder_quantity': 20,
                    'urgency': 'medium' if stock_level > 2 else 'high'
                },
                priority=3 if stock_level > 2 else 4
            )
        
        # Send out of stock alert
        elif stock_level == 0:
            message_bus.publish(
                f"book_{self.book_data.isbn}",
                MessageType.LOW_STOCK_ALERT,
                {
                    'isbn': self.book_data.isbn,
                    'title': self.book_data.title,
                    'current_stock': 0,
                    'status': 'out_of_stock',
                    'reorder_quantity': 30,
                    'urgency': 'critical'
                },
                priority=5
            )
    
    def process_sale(self, quantity: int = 1) -> bool:
        """
        Process a book sale and apply SWRL rules
        
        Args:
            quantity: Number of books sold
            
        Returns:
            True if sale successful, False otherwise
        """
        if self.book_data.stock_quantity >= quantity:
            # Apply SWRL rule for purchase reducing stock
            if hasattr(bookstore_ontology, 'owl_ontology') and bookstore_ontology.owl_ontology:
                rule_result = bookstore_ontology.owl_ontology.apply_swrl_rule(
                    'purchase_reduces_stock',
                    customer_id='current_customer',  # This would be passed from customer agent
                    book_isbn=self.book_data.isbn,
                    quantity=quantity
                )
            
            # Update stock
            self.book_data.stock_quantity -= quantity
            self.daily_sales += quantity
            self.weekly_sales += quantity
            self.total_sales += quantity
            
            # Send inventory update message
            message_bus.publish(
                f"book_{self.book_data.isbn}",
                MessageType.INVENTORY_UPDATE,
                {
                    'isbn': self.book_data.isbn,
                    'action': 'sale',
                    'quantity_sold': quantity,
                    'new_stock': self.book_data.stock_quantity,
                    'title': self.book_data.title
                }
            )
            
            return True
        return False
    
    def restock(self, quantity: int) -> None:
        """
        Restock the book
        
        Args:
            quantity: Number of books to add to stock
        """
        self.book_data.stock_quantity += quantity
        
        # Send inventory update message
        message_bus.publish(
            f"book_{self.book_data.isbn}",
            MessageType.INVENTORY_UPDATE,
            {
                'isbn': self.book_data.isbn,
                'action': 'restock',
                'quantity_added': quantity,
                'new_stock': self.book_data.stock_quantity,
                'title': self.book_data.title
            }
        )
        
        print(f"Restocked {quantity} copies of '{self.book_data.title}'. New stock: {self.book_data.stock_quantity}")
    
    def update_price(self, new_price: float) -> None:
        """
        Update book price and notify interested parties
        
        Args:
            new_price: New price for the book
        """
        old_price = self.book_data.price
        self.book_data.price = new_price
        
        # Send price update message
        message_bus.publish(
            f"book_{self.book_data.isbn}",
            MessageType.PRICE_UPDATE,
            {
                'isbn': self.book_data.isbn,
                'title': self.book_data.title,
                'old_price': old_price,
                'new_price': new_price,
                'price_change': new_price - old_price,
                'change_percentage': ((new_price - old_price) / old_price) * 100
            }
        )
    
    def _update_demand(self):
        """Update current demand based on various factors"""
        # Base demand trend
        self.base_demand += self.demand_trend
        self.base_demand = max(0.1, min(2.0, self.base_demand))  # Keep within bounds
        
        # Seasonal adjustment
        current_season = self._get_current_season()
        self.seasonal_factor = self.seasonal_categories.get(current_season, 1.0)
        
        # Popularity factor
        popularity_factor = 0.5 + (self.popularity_score * 0.5)
        
        # Stock availability factor (scarcity can increase demand)
        if self.book_data.stock_quantity < self.reorder_point:
            scarcity_factor = 1.2
        elif self.book_data.stock_quantity == 0:
            scarcity_factor = 0.0  # No demand if out of stock
        else:
            scarcity_factor = 1.0
        
        # Days since last sale factor (declining interest)
        staleness_factor = max(0.5, 1.0 - (self.days_since_last_sale * 0.05))
        
        # Customer reviews factor
        review_factor = self.customer_reviews_score / 5.0
        
        # Competition factor
        competition_factor = 1.0 / self.market_competition
        
        # Calculate final demand
        self.current_demand = (
            self.base_demand * 
            self.seasonal_factor * 
            popularity_factor * 
            scarcity_factor * 
            staleness_factor * 
            review_factor * 
            competition_factor
        )
        
        # Add some random variation
        variation = random.uniform(0.9, 1.1)
        self.current_demand *= variation
        
        # Ensure demand stays positive
        self.current_demand = max(0.0, self.current_demand)
    
    def _update_pricing(self):
        """Update book pricing based on demand and inventory"""
        # Dynamic pricing based on demand
        if self.current_demand > 1.5:  # High demand
            if self.discount_rate > 0:
                self.discount_rate = max(0, self.discount_rate - 0.05)  # Reduce discount
        elif self.current_demand < 0.5:  # Low demand
            if self.days_since_last_sale > 7:  # No sales for a week
                self.discount_rate = min(0.5, self.discount_rate + 0.1)  # Increase discount
        
        # Inventory-based pricing
        if self.book_data.stock_quantity > self.max_stock_level * 0.8:  # Overstocked
            self.discount_rate = min(0.3, self.discount_rate + 0.05)
        elif self.book_data.stock_quantity < self.reorder_point:  # Low stock
            self.discount_rate = max(0, self.discount_rate - 0.02)
        
        # Update actual price
        self.book_data.price = self.original_price * (1 - self.discount_rate)
    
    def _check_inventory(self):
        """Check inventory levels and suggest restocking"""
        if self.book_data.stock_quantity <= self.reorder_point:
            # Calculate suggested reorder quantity
            suggested_quantity = self.max_stock_level - self.book_data.stock_quantity
            
            # Factor in current demand
            demand_adjustment = int(self.current_demand * 10)
            suggested_quantity += demand_adjustment
            
            # Record inventory alert
            self.model.record_inventory_alert(
                isbn=self.book_data.isbn,
                current_stock=self.book_data.stock_quantity,
                suggested_quantity=suggested_quantity,
                demand_level=self.current_demand
            )
    
    def _update_popularity(self):
        """Update popularity score based on sales and other factors"""
        # Sales impact
        if self.daily_sales > 0:
            sales_factor = min(0.1, self.daily_sales * 0.02)
            self.popularity_score = min(1.0, self.popularity_score + sales_factor)
        else:
            # Slight decline if no sales
            decline = 0.01 if self.days_since_last_sale > 3 else 0
            self.popularity_score = max(0.1, self.popularity_score - decline)
        
        # Random events that can affect popularity
        if random.random() < 0.01:  # 1% chance of random popularity change
            change = random.uniform(-0.2, 0.2)
            self.popularity_score = max(0.1, min(1.0, self.popularity_score + change))
    
    def _get_current_season(self) -> str:
        """Get current season based on simulation step"""
        # Assuming 365 steps per year
        day_of_year = (self.model.schedule.steps % 365) + 1
        
        if 80 <= day_of_year < 172:  # Mar 21 - Jun 21
            return 'spring'
        elif 172 <= day_of_year < 266:  # Jun 21 - Sep 23
            return 'summer'
        elif 266 <= day_of_year < 356:  # Sep 23 - Dec 22
            return 'fall'
        else:  # Dec 22 - Mar 21
            return 'winter'
    
    def _record_analytics(self):
        """Record analytics data for reporting"""
        self.demand_history.append(self.current_demand)
        self.price_history.append(self.book_data.price)
        self.stock_history.append(self.book_data.stock_quantity)
        
        # Keep only last 30 days of history
        if len(self.demand_history) > 30:
            self.demand_history.pop(0)
            self.price_history.pop(0)
            self.stock_history.pop(0)
    
    def process_sale(self, quantity: int):
        """Process a book sale"""
        if quantity <= self.book_data.stock_quantity:
            self.book_data.stock_quantity -= quantity
            self.daily_sales += quantity
            self.weekly_sales += quantity
            self.total_sales += quantity
            
            # Update customer reviews (slight improvement with each sale)
            if random.random() < 0.1:  # 10% chance
                review_change = random.uniform(-0.1, 0.2)  # Slightly biased positive
                self.customer_reviews_score = max(1.0, min(5.0, 
                    self.customer_reviews_score + review_change))
            
            return True
        return False
    
    def restock(self, quantity: int):
        """Restock the book"""
        self.book_data.stock_quantity += quantity
        self.book_data.stock_quantity = min(self.book_data.stock_quantity, 
                                          self.max_stock_level)
    
    def get_demand_forecast(self, days_ahead: int = 7) -> List[float]:
        """Get demand forecast for the next few days"""
        forecast = []
        base_demand = self.current_demand
        
        for i in range(days_ahead):
            # Simple trend-based forecast
            trend_effect = self.demand_trend * i
            seasonal_variation = random.uniform(0.95, 1.05)
            
            forecasted_demand = (base_demand + trend_effect) * seasonal_variation
            forecasted_demand = max(0.0, forecasted_demand)
            forecast.append(forecasted_demand)
        
        return forecast
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get current state information for reporting"""
        return {
            'isbn': self.book_data.isbn,
            'title': self.book_data.title,
            'author': self.book_data.author,
            'category': self.book_data.category.value,
            'current_price': round(self.book_data.price, 2),
            'original_price': round(self.original_price, 2),
            'discount_rate': round(self.discount_rate, 3),
            'stock_quantity': self.book_data.stock_quantity,
            'current_demand': round(self.current_demand, 3),
            'popularity_score': round(self.popularity_score, 3),
            'daily_sales': self.daily_sales,
            'total_sales': self.total_sales,
            'days_since_last_sale': self.days_since_last_sale,
            'days_out_of_stock': self.days_out_of_stock,
            'customer_reviews_score': round(self.customer_reviews_score, 2),
            'seasonal_factor': round(self.seasonal_factor, 2),
            'reorder_point': self.reorder_point,
            'needs_restock': self.book_data.stock_quantity <= self.reorder_point
        }
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get analytics summary for reporting"""
        if not self.demand_history:
            return {}
        
        return {
            'average_demand': round(sum(self.demand_history) / len(self.demand_history), 3),
            'demand_trend': round(self.demand_trend, 4),
            'price_volatility': round(max(self.price_history) - min(self.price_history), 2) if self.price_history else 0,
            'stock_turnover': round(self.total_sales / max(1, self.book_data.stock_quantity + self.total_sales), 3),
            'demand_forecast': self.get_demand_forecast(7)
        }