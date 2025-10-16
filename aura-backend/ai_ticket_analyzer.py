#!/usr/bin/env python3
"""
AI Ticket Analyzer Service
Integrates with OpenAI to provide intelligent ticket analysis and recommendations
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalysisResponse(BaseModel):
    """AI Analysis response model"""
    suggested_processor: Dict[str, Any]
    self_fix_suggestions: List[str]
    category_confidence: float
    priority_recommendation: str
    similar_tickets: List[Dict[str, Any]]
    estimated_resolution_time: str
    additional_insights: List[str]

class TicketAIAnalyzer:
    """AI-powered ticket analyzer using OpenAI"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_PERSONAL_KEY") or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_PERSONAL_KEY or OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("AI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("AI_MAX_TOKENS", "1500"))
        
        # IT agents with their skills
        self.agents = {
            "Alice Johnson": {
                "skills": ["Email", "Software", "Other"],
                "experience": "Senior",
                "specialties": ["Microsoft Office", "Email clients", "General troubleshooting"],
                "availability": "Available"
            },
            "Bob Smith": {
                "skills": ["Network", "Access", "Hardware"],
                "experience": "Expert",
                "specialties": ["Network infrastructure", "WiFi", "VPN", "Access management"],
                "availability": "Available"
            },
            "Carol Williams": {
                "skills": ["Hardware", "Software", "Other"],
                "experience": "Senior",
                "specialties": ["Printer support", "Hardware troubleshooting", "System maintenance"],
                "availability": "Busy"
            },
            "Dave Brown": {
                "skills": ["Access", "Network", "Software"],
                "experience": "Expert",
                "specialties": ["Security", "Access controls", "User management"],
                "availability": "Available"
            },
            "Eva Davis": {
                "skills": ["Network", "Hardware", "Other"],
                "experience": "Senior",
                "specialties": ["Network optimization", "Performance issues", "System diagnostics"],
                "availability": "Available"
            }
        }
    
    def load_historical_tickets(self, tickets_data: List[Dict]) -> str:
        """Convert tickets data to context for AI analysis"""
        context = "Historical IT Support Tickets:\n\n"
        
        for ticket in tickets_data[:15]:  # Limit to avoid token limits
            context += f"Ticket #{ticket.get('user_id', 'N/A')}: {ticket.get('title', 'No title')}\n"
            context += f"Category: {ticket.get('category', 'Unknown')}\n"
            context += f"Priority: {ticket.get('priority', 'Unknown')}\n"
            context += f"Status: {ticket.get('status', 'Unknown')}\n"
            context += f"Department: {ticket.get('department', 'Unknown')}\n"
            context += f"Description: {ticket.get('description', 'No description')[:200]}...\n"
            
            if ticket.get('assigned_to'):
                context += f"Assigned to: {ticket.get('assigned_to')}\n"
            if ticket.get('resolution'):
                context += f"Resolution: {ticket.get('resolution')}\n"
            context += "\n---\n\n"
        
        return context
    
    async def analyze_ticket(self, current_ticket: Dict[str, Any], historical_tickets: List[Dict[str, Any]]) -> AIAnalysisResponse:
        """Analyze a ticket using OpenAI and return recommendations"""
        try:
            # Prepare context
            historical_context = self.load_historical_tickets(historical_tickets)
            agents_context = json.dumps(self.agents, indent=2)
            
            # Create the prompt
            prompt = f"""
As an AI IT Support Assistant, analyze the following support ticket and provide comprehensive recommendations based on historical tickets and available IT agents.

CURRENT TICKET:
Title: {current_ticket.get('title', 'No title')}
Description: {current_ticket.get('description', 'No description')}
Category: {current_ticket.get('category', 'Unknown')}
Priority: {current_ticket.get('priority', 'Unknown')}
Department: {current_ticket.get('department', 'Unknown')}
User: {current_ticket.get('user_name', 'Unknown')} ({current_ticket.get('user_email', 'Unknown')})

AVAILABLE IT AGENTS:
{agents_context}

{historical_context}

Based on this information, provide a detailed analysis in the following JSON format:

{{
    "suggested_processor": {{
        "name": "Agent Name",
        "reason": "Detailed explanation of why this agent is best suited",
        "confidence": 0.85,
        "skills_match": ["skill1", "skill2"],
        "availability_status": "Available/Busy"
    }},
    "self_fix_suggestions": [
        "Step-by-step suggestion 1 that the user can try",
        "Step-by-step suggestion 2 with specific instructions",
        "Step-by-step suggestion 3 if applicable"
    ],
    "category_confidence": 0.92,
    "priority_recommendation": "high/medium/low/critical with justification",
    "similar_tickets": [
        {{
            "title": "Similar ticket title",
            "similarity_score": 0.85,
            "resolution_approach": "How it was resolved"
        }}
    ],
    "estimated_resolution_time": "2-4 hours",
    "additional_insights": [
        "Insight about potential root cause",
        "Preventive measures suggestion",
        "Related system impact analysis"
    ]
}}

Make sure to:
1. Choose the best agent based on skills, experience, and availability
2. Provide practical self-fix steps that are safe for end users
3. Consider similar historical tickets for pattern recognition
4. Give realistic time estimates based on complexity
5. Provide actionable insights for prevention and improvement
"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert IT support AI assistant specializing in ticket analysis, agent routing, and user self-service recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse the response
            ai_response = response.choices[0].message.content.strip()
            logger.info(f"AI Response: {ai_response[:200]}...")
            
            # Extract JSON from the response
            try:
                # Find JSON content between curly braces
                start_idx = ai_response.find('{')
                end_idx = ai_response.rfind('}') + 1
                json_content = ai_response[start_idx:end_idx]
                
                analysis_data = json.loads(json_content)
                
                # Validate and create response
                return AIAnalysisResponse(
                    suggested_processor=analysis_data.get("suggested_processor", {
                        "name": "Bob Smith",
                        "reason": "Default assignment based on general expertise",
                        "confidence": 0.7,
                        "skills_match": ["General"],
                        "availability_status": "Available"
                    }),
                    self_fix_suggestions=analysis_data.get("self_fix_suggestions", [
                        "Try restarting the application or service",
                        "Check for system updates and install if available",
                        "Clear browser cache or application data if applicable"
                    ]),
                    category_confidence=analysis_data.get("category_confidence", 0.8),
                    priority_recommendation=analysis_data.get("priority_recommendation", "medium - standard support ticket"),
                    similar_tickets=analysis_data.get("similar_tickets", []),
                    estimated_resolution_time=analysis_data.get("estimated_resolution_time", "2-4 hours"),
                    additional_insights=analysis_data.get("additional_insights", [
                        "Consider checking system logs for error patterns",
                        "May require additional user training"
                    ])
                )
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                # Return default response
                return self._get_default_analysis(current_ticket)
                
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return self._get_default_analysis(current_ticket)
    
    def _get_default_analysis(self, ticket: Dict[str, Any]) -> AIAnalysisResponse:
        """Return default analysis when AI fails"""
        category = ticket.get('category', 'Other').lower()
        
        # Simple rule-based agent assignment
        if category in ['email']:
            agent_name = "Alice Johnson"
        elif category in ['network', 'access']:
            agent_name = "Bob Smith"
        elif category in ['hardware']:
            agent_name = "Carol Williams"
        elif category in ['software']:
            agent_name = "Dave Brown"
        else:
            agent_name = "Eva Davis"
        
        return AIAnalysisResponse(
            suggested_processor={
                "name": agent_name,
                "reason": f"Assigned based on category expertise ({category})",
                "confidence": 0.7,
                "skills_match": [category.title()],
                "availability_status": self.agents[agent_name]["availability"]
            },
            self_fix_suggestions=[
                "Try restarting the affected application or service",
                "Check if the issue persists after a system reboot",
                "Verify all cables and connections are secure",
                "Check for any recent system or software updates"
            ],
            category_confidence=0.8,
            priority_recommendation=f"{ticket.get('priority', 'medium')} - based on current categorization",
            similar_tickets=[],
            estimated_resolution_time="2-4 hours",
            additional_insights=[
                "Standard troubleshooting procedures should be followed",
                "Consider escalation if issue persists after initial attempts"
            ]
        )

# Global analyzer instance
ai_analyzer = None

def get_ai_analyzer():
    """Get or create AI analyzer instance"""
    global ai_analyzer
    if ai_analyzer is None:
        ai_analyzer = TicketAIAnalyzer()
    return ai_analyzer
