#!/usr/bin/env python3
"""
Test script for AI ticket analysis functionality
"""

import asyncio
import json
from datetime import datetime
from ai_ticket_analyzer import get_ai_analyzer

# Sample test ticket
TEST_TICKET = {
    "id": "test123",
    "title": "Computer running very slowly after Windows update",
    "description": "My computer has become extremely slow after installing the latest Windows update yesterday. Programs take forever to load, the system freezes frequently, and the fan is running constantly. I've tried restarting multiple times but the issue persists.",
    "category": "Software",
    "priority": "high",
    "status": "open",
    "user_id": "USR001",
    "user_email": "test.user@company.com",
    "user_name": "Test User",
    "department": "Engineering",
    "created_at": datetime.utcnow().isoformat()
}

# Sample historical tickets
HISTORICAL_TICKETS = [
    {
        "title": "Slow computer performance - malware suspected",
        "category": "Software",
        "priority": "high",
        "status": "resolved",
        "assigned_to": "Alice Johnson",
        "resolution": "Performed full system scan and removed malware"
    },
    {
        "title": "Windows update causing blue screen errors",
        "category": "Software",
        "priority": "critical",
        "status": "resolved",
        "assigned_to": "Dave Brown",
        "resolution": "Rolled back problematic update and applied alternative patch"
    }
]

async def test_ai_analysis():
    """Test AI ticket analysis"""
    print("🧪 Testing AI Ticket Analysis")
    print("=" * 50)
    
    try:
        # Get AI analyzer
        analyzer = get_ai_analyzer()
        print("✅ AI Analyzer initialized successfully")
        
        # Test analysis
        print(f"\n📝 Analyzing test ticket: '{TEST_TICKET['title']}'")
        analysis = await analyzer.analyze_ticket(TEST_TICKET, HISTORICAL_TICKETS)
        
        print("\n🤖 AI Analysis Results:")
        print("-" * 30)
        
        # Suggested Processor
        processor = analysis.suggested_processor
        print(f"👨‍💼 Suggested Processor: {processor['name']}")
        print(f"   Reason: {processor['reason']}")
        print(f"   Confidence: {processor['confidence']:.2%}")
        print(f"   Skills: {', '.join(processor['skills_match'])}")
        print(f"   Availability: {processor['availability_status']}")
        
        # Self-fix suggestions
        print(f"\n💡 Self-Fix Suggestions ({len(analysis.self_fix_suggestions)} items):")
        for i, suggestion in enumerate(analysis.self_fix_suggestions, 1):
            print(f"   {i}. {suggestion}")
        
        # Other insights
        print(f"\n⏱️  Estimated Resolution Time: {analysis.estimated_resolution_time}")
        print(f"🎯 Priority Recommendation: {analysis.priority_recommendation}")
        print(f"📊 Category Confidence: {analysis.category_confidence:.2%}")
        
        # Similar tickets
        if analysis.similar_tickets:
            print(f"\n🔍 Similar Tickets ({len(analysis.similar_tickets)} found):")
            for ticket in analysis.similar_tickets:
                print(f"   • {ticket['title']} (Similarity: {ticket['similarity_score']:.2%})")
        
        # Additional insights
        if analysis.additional_insights:
            print(f"\n🔎 Additional Insights:")
            for insight in analysis.additional_insights:
                print(f"   • {insight}")
        
        print("\n✅ AI Analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ AI Analysis failed: {e}")
        print("   This might be due to missing OpenAI API key or other configuration issues")
        return False

def test_fallback_analysis():
    """Test fallback analysis when AI is not available"""
    print("\n🔄 Testing Fallback Analysis")
    print("=" * 50)
    
    try:
        from ai_ticket_analyzer import TicketAIAnalyzer
        analyzer = TicketAIAnalyzer()
        
        # Test fallback method directly
        analysis = analyzer._get_default_analysis(TEST_TICKET)
        
        print("✅ Fallback analysis working correctly:")
        print(f"   Suggested Agent: {analysis.suggested_processor['name']}")
        print(f"   Reason: {analysis.suggested_processor['reason']}")
        print(f"   Self-fix suggestions: {len(analysis.self_fix_suggestions)} items")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback analysis failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Starting AI Ticket Analysis Tests")
    print("=" * 60)
    
    # Test 1: AI Analysis (might fail without API key)
    ai_success = await test_ai_analysis()
    
    # Test 2: Fallback Analysis (should always work)
    fallback_success = test_fallback_analysis()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   AI Analysis: {'✅ PASS' if ai_success else '❌ FAIL'}")
    print(f"   Fallback Analysis: {'✅ PASS' if fallback_success else '❌ FAIL'}")
    
    if not ai_success:
        print("\n💡 To enable full AI analysis:")
        print("   1. Set your OpenAI API key in the .env file")
        print("   2. Make sure you have OpenAI API credits")
        print("   3. Check your internet connection")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
