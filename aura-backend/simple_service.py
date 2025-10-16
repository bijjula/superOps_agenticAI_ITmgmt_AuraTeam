#!/usr/bin/env python3
"""
Simple Service Desk API Server
Minimal version for testing without complex dependencies
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uvicorn
from ai_ticket_analyzer import get_ai_analyzer, AIAnalysisResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/aura_servicedesk")
mongo_client = None
db = None

# Pydantic Models
class TicketResponse(BaseModel):
    """Ticket response model"""
    _id: str
    title: str
    description: str
    category: str
    priority: str
    status: str
    user_id: str
    user_email: str
    user_name: str
    department: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    attachments: List[str] = []
    created_at: datetime
    updated_at: datetime

class PaginatedTicketsResponse(BaseModel):
    """Paginated tickets response"""
    items: List[Dict[str, Any]]
    total: int
    page: int
    limit: int
    pages: int
    has_next: bool
    has_prev: bool

# Create FastAPI app
app = FastAPI(
    title="Simple Service Desk API",
    description="Minimal Service Desk API for testing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection"""
    global mongo_client, db
    try:
        mongo_client = AsyncIOMotorClient(MONGODB_URL)
        db = mongo_client.aura_servicedesk
        logger.info(f"Connected to MongoDB: {MONGODB_URL}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection"""
    if mongo_client:
        mongo_client.close()
        logger.info("Disconnected from MongoDB")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "simple-service-desk"}

@app.get("/api/v1/tickets")
async def get_tickets(
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    assigned_to: Optional[str] = Query(None, description="Filter by assigned agent"),
    user_id: Optional[str] = Query(None, description="Filter by user"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page")
):
    """Get tickets with filters and pagination"""
    try:
        # Build filter
        filter_dict = {}
        if status:
            filter_dict["status"] = status
        if category:
            filter_dict["category"] = category
        if assigned_to:
            filter_dict["assigned_to"] = assigned_to
        if user_id:
            filter_dict["user_id"] = user_id

        # Calculate pagination
        skip = (page - 1) * limit

        # Get tickets from MongoDB
        cursor = db.tickets.find(filter_dict).skip(skip).limit(limit)
        tickets = []
        
        async for ticket in cursor:
            # Convert ObjectId to string
            ticket["_id"] = str(ticket["_id"])
            
            # Handle datetime fields safely
            created_at = ticket.get("created_at", datetime.now())
            updated_at = ticket.get("updated_at", datetime.now())
            
            # Convert to isoformat if not already a string
            if isinstance(created_at, datetime):
                created_at_str = created_at.isoformat()
            else:
                created_at_str = str(created_at)
                
            if isinstance(updated_at, datetime):
                updated_at_str = updated_at.isoformat()
            else:
                updated_at_str = str(updated_at)
            
            # Map fields to match frontend expectations
            ticket_mapped = {
                "id": ticket["_id"],
                "title": ticket.get("title", ""),
                "description": ticket.get("description", ""),
                "status": ticket.get("status", "open"),
                "priority": ticket.get("priority", "medium"),
                "category": ticket.get("category", "Other"),
                "created_at": created_at_str,
                "updated_at": updated_at_str,
                "assigned_to": ticket.get("assigned_to"),
                "requester": ticket.get("user_email", ticket.get("user_name", "unknown@example.com")),
                "user_id": ticket.get("user_id", ""),
                "user_email": ticket.get("user_email", ""),
                "user_name": ticket.get("user_name", ""),
                "department": ticket.get("department"),
                "resolution": ticket.get("resolution"),
                "attachments": ticket.get("attachments", [])
            }
            tickets.append(ticket_mapped)

        # Get total count
        total = await db.tickets.count_documents(filter_dict)

        # Calculate pagination info
        pages = (total + limit - 1) // limit
        has_next = page < pages
        has_prev = page > 1

        logger.info(f"Retrieved {len(tickets)} tickets (page {page}/{pages}, total: {total})")

        return {
            "items": tickets,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": pages,
            "has_next": has_next,
            "has_prev": has_prev
        }

    except Exception as e:
        logger.error(f"Error retrieving tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tickets: {str(e)}")

@app.get("/api/v1/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Get ticket by ID"""
    try:
        from bson import ObjectId
        
        # Try to convert to ObjectId
        try:
            object_id = ObjectId(ticket_id)
        except:
            # If not a valid ObjectId, search by string ID
            ticket = await db.tickets.find_one({"_id": ticket_id})
        else:
            ticket = await db.tickets.find_one({"_id": object_id})
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Convert ObjectId to string
        ticket["_id"] = str(ticket["_id"])
        
        # Map fields to match frontend expectations
        ticket_mapped = {
            "id": ticket["_id"],
            "title": ticket.get("title", ""),
            "description": ticket.get("description", ""),
            "status": ticket.get("status", "open"),
            "priority": ticket.get("priority", "medium"),
            "category": ticket.get("category", "Other"),
            "created_at": ticket.get("created_at", datetime.now()).isoformat(),
            "updated_at": ticket.get("updated_at", datetime.now()).isoformat(),
            "assigned_to": ticket.get("assigned_to"),
            "requester": ticket.get("user_email", ticket.get("user_name", "unknown@example.com")),
            "user_id": ticket.get("user_id", ""),
            "user_email": ticket.get("user_email", ""),
            "user_name": ticket.get("user_name", ""),
            "department": ticket.get("department"),
            "resolution": ticket.get("resolution"),
            "attachments": ticket.get("attachments", [])
        }

        return {"message": "Ticket retrieved successfully", "data": ticket_mapped}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve ticket: {str(e)}")

@app.post("/api/v1/tickets")
async def create_ticket(ticket_data: dict):
    """Create a new ticket"""
    try:
        # Create ticket document
        ticket_doc = {
            "title": ticket_data.get("title", ""),
            "description": ticket_data.get("description", ""),
            "category": ticket_data.get("category", "Other"),
            "priority": ticket_data.get("priority", "medium"),
            "status": "open",
            "user_id": ticket_data.get("user_id", ""),
            "user_email": ticket_data.get("user_email", ""),
            "user_name": ticket_data.get("user_name", ""),
            "department": ticket_data.get("department"),
            "attachments": ticket_data.get("attachments", []),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        # Insert into MongoDB
        result = await db.tickets.insert_one(ticket_doc)
        ticket_id = str(result.inserted_id)

        logger.info(f"Ticket created: {ticket_id}")

        return {
            "message": "Ticket created successfully",
            "data": {"ticket_id": ticket_id}
        }

    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create ticket: {str(e)}")

@app.post("/api/v1/tickets/{ticket_id}/analyze")
async def analyze_ticket(ticket_id: str):
    """Analyze a ticket using AI and provide recommendations"""
    try:
        from bson import ObjectId
        
        # Get the current ticket
        try:
            object_id = ObjectId(ticket_id)
        except:
            ticket = await db.tickets.find_one({"_id": ticket_id})
        else:
            ticket = await db.tickets.find_one({"_id": object_id})
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Convert ObjectId to string for processing
        ticket["_id"] = str(ticket["_id"])
        
        # Get all historical tickets for context
        historical_tickets = []
        cursor = db.tickets.find({}).limit(50)  # Limit for performance
        async for hist_ticket in cursor:
            hist_ticket["_id"] = str(hist_ticket["_id"])
            historical_tickets.append(hist_ticket)
        
        # Get AI analyzer and perform analysis
        try:
            analyzer = get_ai_analyzer()
            analysis = await analyzer.analyze_ticket(ticket, historical_tickets)
            
            # Convert analysis to dict for JSON serialization
            analysis_dict = {
                "suggested_processor": analysis.suggested_processor,
                "self_fix_suggestions": analysis.self_fix_suggestions,
                "category_confidence": analysis.category_confidence,
                "priority_recommendation": analysis.priority_recommendation,
                "similar_tickets": analysis.similar_tickets,
                "estimated_resolution_time": analysis.estimated_resolution_time,
                "additional_insights": analysis.additional_insights
            }
            
            logger.info(f"AI analysis completed for ticket {ticket_id}")
            
            return {
                "message": "Ticket analysis completed successfully",
                "data": {
                    "ticket_id": ticket_id,
                    "analysis": analysis_dict,
                    "analyzed_at": datetime.utcnow().isoformat()
                }
            }
        
        except Exception as ai_error:
            logger.error(f"AI analysis failed for ticket {ticket_id}: {ai_error}")
            # Return a fallback response
            return {
                "message": "AI analysis completed with fallback",
                "data": {
                    "ticket_id": ticket_id,
                    "analysis": {
                        "suggested_processor": {
                            "name": "Bob Smith",
                            "reason": "Default assignment - AI analysis temporarily unavailable",
                            "confidence": 0.6,
                            "skills_match": ["General"],
                            "availability_status": "Available"
                        },
                        "self_fix_suggestions": [
                            "Try restarting the affected application or service",
                            "Check system requirements and compatibility",
                            "Verify network connectivity if applicable",
                            "Contact IT support if issue persists"
                        ],
                        "category_confidence": 0.7,
                        "priority_recommendation": f"{ticket.get('priority', 'medium')} - maintaining current priority",
                        "similar_tickets": [],
                        "estimated_resolution_time": "2-4 hours",
                        "additional_insights": [
                            "AI analysis temporarily unavailable - using rule-based assignment",
                            "Manual review recommended for complex issues"
                        ]
                    },
                    "analyzed_at": datetime.utcnow().isoformat(),
                    "fallback_used": True
                }
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing ticket {ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze ticket: {str(e)}")

@app.post("/api/v1/tickets/load-sample-data")
async def load_sample_tickets():
    """Load sample tickets from JSON file for testing"""
    try:
        # Load sample tickets from JSON file
        sample_file_path = os.path.join(os.path.dirname(__file__), "sample_tickets.json")
        
        if not os.path.exists(sample_file_path):
            raise HTTPException(status_code=404, detail="Sample tickets file not found")
        
        with open(sample_file_path, 'r') as f:
            sample_tickets = json.load(f)
        
        # Clear existing tickets (optional - for testing)
        await db.tickets.delete_many({})
        
        # Insert sample tickets
        loaded_count = 0
        for ticket_data in sample_tickets:
            # Convert date strings to datetime objects if needed
            if isinstance(ticket_data.get('created_at'), str):
                try:
                    ticket_data['created_at'] = datetime.fromisoformat(ticket_data['created_at'].replace('Z', '+00:00'))
                except:
                    ticket_data['created_at'] = datetime.utcnow()
            
            if isinstance(ticket_data.get('updated_at'), str):
                try:
                    ticket_data['updated_at'] = datetime.fromisoformat(ticket_data['updated_at'].replace('Z', '+00:00'))
                except:
                    ticket_data['updated_at'] = datetime.utcnow()
            
            await db.tickets.insert_one(ticket_data)
            loaded_count += 1
        
        logger.info(f"Loaded {loaded_count} sample tickets")
        
        return {
            "message": f"Successfully loaded {loaded_count} sample tickets",
            "data": {"loaded_count": loaded_count}
        }
        
    except Exception as e:
        logger.error(f"Error loading sample tickets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load sample tickets: {str(e)}")

if __name__ == "__main__":
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    debug = os.getenv("DEBUG", "true").lower() == "true"

    logger.info(f"Starting Simple Service Desk API on {host}:{port}")
    logger.info(f"MongoDB URL: {MONGODB_URL}")

    # Run the application
    uvicorn.run(
        "simple_service:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
