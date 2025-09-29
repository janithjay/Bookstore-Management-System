"""
Message Bus System for Agent Communication

This module implements a message bus system that allows agents to communicate
with each other through structured messages for inventory updates, restock
notifications, and other bookstore operations.
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import threading
from queue import Queue


class MessageType(Enum):
    """Enumeration of message types"""
    INVENTORY_UPDATE = "inventory_update"
    RESTOCK_REQUEST = "restock_request"
    PURCHASE_COMPLETED = "purchase_completed"
    CUSTOMER_INQUIRY = "customer_inquiry"
    PRICE_UPDATE = "price_update"
    LOW_STOCK_ALERT = "low_stock_alert"
    EMPLOYEE_ASSIGNMENT = "employee_assignment"


@dataclass
class Message:
    """Message structure for agent communication"""
    message_id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime
    priority: int = 1  # 1 = low, 5 = high
    processed: bool = False
    
    def __post_init__(self):
        """Validate message priority"""
        if not 1 <= self.priority <= 5:
            self.priority = 1


class MessageBus:
    """
    Central message bus for agent communication.
    Handles message routing, queuing, and delivery between agents.
    """
    
    def __init__(self):
        """Initialize the message bus"""
        self.message_queues: Dict[str, Queue] = {}
        self.subscribers: Dict[MessageType, List[str]] = {}
        self.message_handlers: Dict[str, Dict[MessageType, Callable]] = {}
        self.message_history: List[Message] = []
        self._lock = threading.Lock()
        self._message_counter = 0
    
    def register_agent(self, agent_id: str) -> None:
        """
        Register an agent with the message bus.
        
        Args:
            agent_id: Unique identifier for the agent
        """
        with self._lock:
            if agent_id not in self.message_queues:
                self.message_queues[agent_id] = Queue()
                self.message_handlers[agent_id] = {}
    
    def subscribe(self, agent_id: str, message_type: MessageType, handler: Callable) -> None:
        """
        Subscribe an agent to specific message types.
        
        Args:
            agent_id: Agent identifier
            message_type: Type of messages to subscribe to
            handler: Function to handle received messages
        """
        with self._lock:
            if message_type not in self.subscribers:
                self.subscribers[message_type] = []
            
            if agent_id not in self.subscribers[message_type]:
                self.subscribers[message_type].append(agent_id)
            
            self.message_handlers[agent_id][message_type] = handler
    
    def publish(self, sender_id: str, message_type: MessageType, content: Dict[str, Any], 
                recipient_id: str = None, priority: int = 1) -> str:
        """
        Publish a message to the bus.
        
        Args:
            sender_id: ID of the sending agent
            message_type: Type of message
            content: Message content
            recipient_id: Specific recipient (if None, broadcast to subscribers)
            priority: Message priority (1-5)
            
        Returns:
            Message ID
        """
        with self._lock:
            self._message_counter += 1
            message_id = f"msg_{self._message_counter:06d}"
            
            # Create message
            message = Message(
                message_id=message_id,
                sender_id=sender_id,
                recipient_id=recipient_id or "broadcast",
                message_type=message_type,
                content=content,
                timestamp=datetime.now(),
                priority=priority
            )
            
            # Add to history
            self.message_history.append(message)
            
            # Route message
            if recipient_id:
                # Direct message to specific recipient
                if recipient_id in self.message_queues:
                    self.message_queues[recipient_id].put(message)
            else:
                # Broadcast to subscribers
                if message_type in self.subscribers:
                    for subscriber_id in self.subscribers[message_type]:
                        if subscriber_id in self.message_queues:
                            self.message_queues[subscriber_id].put(message)
            
            return message_id
    
    def receive_messages(self, agent_id: str) -> List[Message]:
        """
        Receive all pending messages for an agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of pending messages
        """
        if agent_id not in self.message_queues:
            return []
        
        messages = []
        queue = self.message_queues[agent_id]
        
        while not queue.empty():
            try:
                message = queue.get_nowait()
                messages.append(message)
            except:
                break
        
        # Sort by priority (higher priority first)
        messages.sort(key=lambda m: m.priority, reverse=True)
        return messages
    
    def process_messages(self, agent_id: str) -> int:
        """
        Process all pending messages for an agent using registered handlers.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Number of messages processed
        """
        messages = self.receive_messages(agent_id)
        processed_count = 0
        
        for message in messages:
            if message.message_type in self.message_handlers.get(agent_id, {}):
                handler = self.message_handlers[agent_id][message.message_type]
                try:
                    handler(message)
                    message.processed = True
                    processed_count += 1
                except Exception as e:
                    print(f"Error processing message {message.message_id}: {e}")
        
        return processed_count
    
    def get_message_statistics(self) -> Dict[str, Any]:
        """
        Get message bus statistics.
        
        Returns:
            Dictionary with message statistics
        """
        total_messages = len(self.message_history)
        processed_messages = sum(1 for msg in self.message_history if msg.processed)
        
        message_types_count = {}
        for msg in self.message_history:
            msg_type = msg.message_type.value
            message_types_count[msg_type] = message_types_count.get(msg_type, 0) + 1
        
        return {
            'total_messages': total_messages,
            'processed_messages': processed_messages,
            'pending_messages': total_messages - processed_messages,
            'registered_agents': len(self.message_queues),
            'message_types_count': message_types_count,
            'active_subscriptions': sum(len(subs) for subs in self.subscribers.values())
        }
    
    def clear_history(self) -> None:
        """Clear message history (useful for testing)"""
        with self._lock:
            self.message_history.clear()
    
    def get_agent_queue_size(self, agent_id: str) -> int:
        """Get the number of pending messages for an agent"""
        if agent_id in self.message_queues:
            return self.message_queues[agent_id].qsize()
        return 0


# Global message bus instance
message_bus = MessageBus()