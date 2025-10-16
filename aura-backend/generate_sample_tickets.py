#!/usr/bin/env python3
"""
Generate 25 varied ticket scenarios for the Aura Service Desk system
This script creates diverse tickets to populate the "All tickets" view with realistic scenarios
"""

import asyncio
import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

# Add the shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'shared'))

from shared.models.base import Priority, Status
from shared.utils.database import init_database_connections, db_manager, MongoRepository

# Sample data for generating varied tickets
CATEGORIES = ["Hardware", "Software", "Network", "Access", "Email", "Other"]

DEPARTMENTS = [
    "Marketing", "Sales", "Engineering", "HR", "Finance", "Operations", 
    "Customer Support", "IT", "Legal", "Product Management"
]

USER_NAMES = [
    "John Smith", "Sarah Johnson", "Michael Chen", "Emily Davis", "David Wilson",
    "Lisa Anderson", "Robert Garcia", "Jennifer Martinez", "William Brown", "Jessica Taylor",
    "James Lee", "Amanda White", "Christopher Harris", "Michelle Clark", "Daniel Lewis",
    "Rebecca Walker", "Kevin Hall", "Laura Allen", "Steven Young", "Karen King",
    "Thomas Wright", "Nancy Lopez", "Mark Hill", "Sandra Scott", "Andrew Green",
]

TICKET_SCENARIOS = [
    {
        "title": "Laptop screen flickering intermittently",
        "description": "My laptop screen has been flickering on and off for the past two days. It happens randomly, sometimes when I'm typing, sometimes when I'm just reading. The flickering lasts for about 5-10 seconds and then stops. I've tried restarting the laptop but the issue persists.",
        "category": "Hardware",
        "priority": Priority.HIGH,
        "keywords": ["screen", "flickering", "display", "laptop", "hardware"]
    },
    {
        "title": "Unable to access company VPN from home",
        "description": "I'm working from home today and cannot connect to the company VPN. I get an error message saying 'Connection failed - authentication error'. I've double-checked my credentials and they seem correct. This was working fine last week.",
        "category": "Network",
        "priority": Priority.HIGH,
        "keywords": ["vpn", "remote", "authentication", "connection", "home"]
    },
    {
        "title": "Microsoft Excel crashes when opening large spreadsheets",
        "description": "Excel keeps crashing whenever I try to open files larger than 50MB. The application starts to load the file and then suddenly closes without any error message. I need to work with these large datasets for my quarterly reports.",
        "category": "Software",
        "priority": Priority.MEDIUM,
        "keywords": ["excel", "crash", "spreadsheet", "large files", "quarterly reports"]
    },
    {
        "title": "Request access to SharePoint site for new project",
        "description": "I've been assigned to the 'Project Phoenix' team and need access to the SharePoint site. My manager mentioned I should have read/write permissions to the documents folder and read-only access to the finance folder.",
        "category": "Access",
        "priority": Priority.MEDIUM,
        "keywords": ["sharepoint", "access", "permissions", "project", "documents"]
    },
    {
        "title": "Email attachments not downloading in Outlook",
        "description": "When I try to download email attachments in Outlook, I get an error saying 'Temporary error, please try again later'. This has been happening for the past 3 hours. I can see the attachments are there but cannot save them to my computer.",
        "category": "Email",
        "priority": Priority.HIGH,
        "keywords": ["outlook", "attachments", "download", "error", "email"]
    },
    {
        "title": "Printer not responding - urgent documents needed",
        "description": "The printer on the 3rd floor (HP LaserJet Pro) is not responding to print jobs. The printer shows as online in Windows but nothing happens when I try to print. I have important contracts that need to be printed for a client meeting in 2 hours.",
        "category": "Hardware",
        "priority": Priority.CRITICAL,
        "keywords": ["printer", "urgent", "contracts", "client meeting", "3rd floor"]
    },
    {
        "title": "Slow internet connection affecting video calls",
        "description": "My internet connection has been very slow for the past few days. Video calls keep dropping and websites take forever to load. Speed test shows only 2 Mbps download when it should be at least 50 Mbps. This is affecting my ability to attend virtual meetings.",
        "category": "Network",
        "priority": Priority.HIGH,
        "keywords": ["internet", "slow", "video calls", "speed test", "meetings"]
    },
    {
        "title": "Cannot install required software - admin rights needed",
        "description": "I need to install Adobe Creative Suite for a new marketing campaign but I don't have administrator rights on my computer. I get an error message saying 'Installation failed - insufficient privileges'. Can someone help me install this software?",
        "category": "Software",
        "priority": Priority.MEDIUM,
        "keywords": ["adobe", "install", "admin rights", "privileges", "marketing"]
    },
    {
        "title": "Password reset for domain account",
        "description": "I forgot my domain password and need it reset. I tried the self-service portal but it says my security questions don't match. My username is jsmith and I need access urgently as I have a presentation at 2 PM today.",
        "category": "Access",
        "priority": Priority.HIGH,
        "keywords": ["password", "reset", "domain", "security questions", "presentation"]
    },
    {
        "title": "Spam emails getting through to inbox",
        "description": "I've been receiving a lot of spam emails in my inbox over the past week. The emails are clearly spam (offers for fake products, lottery winnings, etc.) but they're not being caught by the spam filter. Can the email security be adjusted?",
        "category": "Email",
        "priority": Priority.LOW,
        "keywords": ["spam", "filter", "inbox", "security", "fake products"]
    },
    {
        "title": "Computer running very slowly - possible malware",
        "description": "My computer has become extremely slow over the past few days. Programs take minutes to open and the fan is constantly running. I suspect there might be malware. Can someone run a security scan and help clean up my system?",
        "category": "Other",
        "priority": Priority.HIGH,
        "keywords": ["slow", "malware", "security scan", "performance", "cleanup"]
    },
    {
        "title": "External monitor not detected by laptop",
        "description": "I'm trying to connect my external monitor to my laptop using the HDMI cable but it's not being detected. I've tried different cables and ports but nothing works. The monitor works fine with other devices.",
        "category": "Hardware",
        "priority": Priority.MEDIUM,
        "keywords": ["monitor", "hdmi", "laptop", "detection", "cable"]
    },
    {
        "title": "Teams application keeps freezing during meetings",
        "description": "Microsoft Teams freezes frequently during video conferences. The audio continues but the video becomes unresponsive and I have to restart the application. This is very disruptive during important client calls.",
        "category": "Software",
        "priority": Priority.HIGH,
        "keywords": ["teams", "freezing", "video conference", "client calls", "disruptive"]
    },
    {
        "title": "WiFi connection dropping every 30 minutes",
        "description": "My WiFi connection keeps dropping every 30 minutes or so. I have to disconnect and reconnect to get back online. This started happening after the recent Windows update. Other devices in the office seem to work fine.",
        "category": "Network",
        "priority": Priority.MEDIUM,
        "keywords": ["wifi", "dropping", "windows update", "reconnect", "30 minutes"]
    },
    {
        "title": "Need access to CRM system for new sales role",
        "description": "I've just started in the sales team and need access to the Salesforce CRM system. My manager said I should have full access to leads and opportunities. My employee ID is EMP001234.",
        "category": "Access",
        "priority": Priority.MEDIUM,
        "keywords": ["crm", "salesforce", "sales team", "leads", "opportunities"]
    },
    {
        "title": "Email signature not updating across all devices",
        "description": "I updated my email signature last week but it's not showing the changes on my mobile phone. The signature appears correctly on my desktop Outlook but shows the old version on my iPhone. How can I sync this?",
        "category": "Email",
        "priority": Priority.LOW,
        "keywords": ["signature", "mobile", "sync", "iphone", "outlook"]
    },
    {
        "title": "Request for new software license - CAD software",
        "description": "Our engineering team needs an additional license for AutoCAD software. We have a new engineer starting next week and they'll need access to work on client projects. Can we purchase and install an additional license?",
        "category": "Software",
        "priority": Priority.MEDIUM,
        "keywords": ["license", "autocad", "engineering", "new engineer", "client projects"]
    },
    {
        "title": "Keyboard keys sticking - affecting productivity",
        "description": "Several keys on my keyboard are sticking, particularly the space bar and the 'e' key. This is making typing very difficult and slowing down my work. I've tried cleaning it but the problem persists.",
        "category": "Hardware",
        "priority": Priority.MEDIUM,
        "keywords": ["keyboard", "sticking", "space bar", "productivity", "cleaning"]
    },
    {
        "title": "Cannot connect to shared network drive",
        "description": "I'm unable to access the shared network drive (S: drive) that contains our department's project files. I get an error message 'Network path not found'. Other colleagues can access it fine. I need these files for tomorrow's deadline.",
        "category": "Network",
        "priority": Priority.HIGH,
        "keywords": ["shared drive", "network path", "project files", "deadline", "s drive"]
    },
    {
        "title": "File permissions issue - cannot edit shared documents",
        "description": "I can open shared documents in our team folder but cannot edit or save changes. I get a 'Permission denied' error when trying to save. I had edit permissions last month but something seems to have changed.",
        "category": "Access",
        "priority": Priority.MEDIUM,
        "keywords": ["permissions", "edit", "shared documents", "team folder", "save"]
    },
    {
        "title": "Email not syncing with mobile device",
        "description": "My work emails are not syncing with my company phone. I receive emails on my desktop but they don't show up on my mobile device. I've tried removing and re-adding the account but the issue persists. The sync was working fine until yesterday.",
        "category": "Email",
        "priority": Priority.MEDIUM,
        "keywords": ["sync", "mobile", "company phone", "desktop", "re-adding"]
    },
    {
        "title": "Blue Screen of Death (BSOD) occurring randomly",
        "description": "My computer has been experiencing Blue Screen of Death errors randomly throughout the day. There's no specific pattern - it happens when I'm using different applications. The error code is usually SYSTEM_SERVICE_EXCEPTION. This is affecting my ability to work.",
        "category": "Other",
        "priority": Priority.CRITICAL,
        "keywords": ["bsod", "blue screen", "random", "system service exception", "critical"]
    },
    {
        "title": "Software update stuck at 50% - system unusable",
        "description": "A Windows update started this morning and has been stuck at 50% for over 3 hours. I cannot cancel it or use my computer. I have important work to complete today and need this resolved urgently.",
        "category": "Software",
        "priority": Priority.CRITICAL,
        "keywords": ["windows update", "stuck", "50%", "unusable", "urgent"]
    },
    {
        "title": "VPN connection very slow - remote work impacted",
        "description": "When I connect to the company VPN, my internet speed drops significantly. File transfers that normally take minutes are taking hours. This is making remote work very difficult, especially when accessing cloud applications.",
        "category": "Network",
        "priority": Priority.HIGH,
        "keywords": ["vpn", "slow", "remote work", "file transfers", "cloud applications"]
    },
    {
        "title": "Request deactivation of former employee accounts",
        "description": "We need to deactivate all system accounts for John Doe who left the company last Friday. This includes Active Directory, email, VPN access, and any application-specific accounts. His employee ID was EMP005678. Please confirm when this is completed.",
        "category": "Access",
        "priority": Priority.HIGH,
        "keywords": ["deactivation", "former employee", "active directory", "email", "vpn"]
    }
]

async def generate_sample_tickets():
    """Generate 25 varied ticket scenarios and insert them into the database"""
    
    try:
        print("🎫 Starting sample ticket generation...")
        
        # Initialize database connections
        print("📊 Initializing database connections...")
        await init_database_connections(
            postgres_url=os.getenv("DATABASE_URL", "postgresql://aura_user:aura_password@localhost:5432/aura_main"),
            mongodb_url=os.getenv("MONGODB_URL", "mongodb://localhost:27017"),
            mongodb_name="aura_servicedesk",
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379")
        )
        
        # Get MongoDB repository for tickets
        tickets_repo = MongoRepository("tickets", db_manager.get_mongo_db())
        
        print("🔢 Generating tickets...")
        
        tickets_created = 0
        
        for i, scenario in enumerate(TICKET_SCENARIOS):
            # Generate random user data
            user_name = random.choice(USER_NAMES)
            department = random.choice(DEPARTMENTS)
            
            # Create email from name
            first_name, last_name = user_name.lower().split()
            user_email = f"{first_name}.{last_name}@company.com"
            user_id = f"USR{random.randint(10000, 99999)}"
            
            # Add some time variation - tickets created over past 30 days
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            created_time = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
            
            # Randomly assign status (most are open/in_progress, some resolved)
            status_weights = [0.4, 0.3, 0.2, 0.1]  # open, in_progress, resolved, closed
            status = random.choices(
                [Status.OPEN, Status.IN_PROGRESS, Status.RESOLVED, Status.CLOSED],
                weights=status_weights
            )[0]
            
            # Create ticket document
            ticket_doc = {
                "title": scenario["title"],
                "description": scenario["description"],
                "category": scenario["category"],
                "priority": scenario["priority"],
                "status": status,
                "user_id": user_id,
                "user_email": user_email,
                "user_name": user_name,
                "department": department,
                "attachments": [],
                "ai_suggestions": [
                    {
                        "type": "category_confidence",
                        "content": f"Automatically categorized as '{scenario['category']}' with 95% confidence",
                        "confidence": 0.95
                    }
                ],
                "created_at": created_time,
                "updated_at": created_time
            }
            
            # Add assigned agent and resolution for resolved/closed tickets
            if status in [Status.IN_PROGRESS, Status.RESOLVED, Status.CLOSED]:
                agents = ["Alice Johnson", "Bob Smith", "Carol Williams", "Dave Brown", "Eva Davis"]
                ticket_doc["assigned_to"] = random.choice(agents)
                
                if status in [Status.RESOLVED, Status.CLOSED]:
                    resolutions = [
                        "Issue resolved by restarting the service and updating drivers.",
                        "Problem fixed by adjusting network settings and clearing cache.",
                        "Resolved by reinstalling the application and configuring permissions.",
                        "Fixed by updating software and running system diagnostics.",
                        "Issue resolved through hardware replacement and configuration update."
                    ]
                    ticket_doc["resolution"] = random.choice(resolutions)
                    # Update timestamp for resolution
                    resolution_time = created_time + timedelta(
                        hours=random.randint(1, 48)
                    )
                    ticket_doc["updated_at"] = resolution_time
            
            # Insert ticket into database
            ticket_id = await tickets_repo.create(ticket_doc)
            tickets_created += 1
            
            print(f"✅ Created ticket {tickets_created}/25: {scenario['title'][:50]}...")
        
        print(f"\n🎉 Successfully generated {tickets_created} sample tickets!")
        print("📈 Ticket distribution:")
        
        # Show summary statistics
        categories = {}
        priorities = {}
        statuses = {}
        
        for scenario in TICKET_SCENARIOS:
            cat = scenario["category"]
            categories[cat] = categories.get(cat, 0) + 1
            
            pri = scenario["priority"]
            priorities[pri] = priorities.get(pri, 0) + 1
        
        # Count status distribution (approximated based on weights)
        status_dist = {
            "Open": int(25 * 0.4),
            "In Progress": int(25 * 0.3), 
            "Resolved": int(25 * 0.2),
            "Closed": int(25 * 0.1)
        }
        
        print("\n📊 Categories:")
        for cat, count in categories.items():
            print(f"  {cat}: {count} tickets")
            
        print("\n🎯 Priorities:")
        for pri, count in priorities.items():
            print(f"  {pri}: {count} tickets")
            
        print("\n📋 Status (approximate):")
        for status, count in status_dist.items():
            print(f"  {status}: {count} tickets")
            
        print("\n👥 Generated for departments:", ", ".join(DEPARTMENTS))
        print(f"⏰ Time span: Past 30 days")
        
        print("\n✨ Sample tickets have been successfully added to the database!")
        print("🌐 You can now view them in the 'All Tickets' section of the application.")
        
    except Exception as e:
        print(f"❌ Error generating sample tickets: {e}")
        raise
    finally:
        # Close database connections
        try:
            await db_manager.close_connections()
            print("🔐 Database connections closed.")
        except Exception as e:
            print(f"⚠️ Error closing connections: {e}")

def main():
    """Main function to run ticket generation"""
    print("🚀 Aura Service Desk - Sample Ticket Generator")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("shared"):
        print("❌ Error: Please run this script from the aura-backend directory")
        print("Current directory should contain the 'shared' folder")
        return 1
    
    # Run the async function
    try:
        asyncio.run(generate_sample_tickets())
        return 0
    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
