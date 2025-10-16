"""
Base models and common schemas for Aura Backend Services
"""

from datetime import datetime
from typing import Optional, Any, Dict, List
from pydantic import BaseModel, Field
from enum import Enum


class BaseResponse(BaseModel):
    """Base response model for all API responses"""
    success: bool = True
    message: str = "Operation successful"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    service_name: str
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    dependencies: Dict[str, str] = {}


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=100)
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PaginatedResponse(BaseModel):
    """Paginated response model"""
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool


# Common Enums
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    PENDING = "pending"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# AI/ML Models
class AIRequest(BaseModel):
    """Base AI request model"""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    model: str = "gpt-3.5-turbo"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)


class AIResponse(BaseModel):
    """Base AI response model"""
    response: str
    confidence: Optional[float] = None
    tokens_used: Optional[int] = None
    model: str
    processing_time: Optional[float] = None


# Database Models
class BaseDBModel(BaseModel):
    """Base database model"""
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


# User Models
class UserRole(str, Enum):
    END_USER = "end_user"
    IT_AGENT = "it_agent"
    IT_MANAGER = "it_manager"
    SYSTEM_ADMIN = "system_admin"


class User(BaseDBModel):
    """User model"""
    email: str
    name: str
    role: UserRole
    department: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    skills: List[str] = []
    workload_capacity: int = 10


# File Upload Models
class FileUpload(BaseModel):
    """File upload model"""
    filename: str
    file_size: int
    content_type: str
    file_url: str
    uploaded_by: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


# Configuration Models
class ServiceConfig(BaseModel):
    """Service configuration model"""
    service_name: str
    version: str
    debug: bool = False
    log_level: str = "INFO"
    database_url: str
    redis_url: str
    ai_enabled: bool = True
    cors_origins: List[str] = ["*"]
