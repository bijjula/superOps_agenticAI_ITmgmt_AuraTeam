#!/usr/bin/env python3
"""
Simple ticket generator that directly inserts into MongoDB via Docker
"""

import json
import random
from datetime import datetime, timedelta

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
        "priority": "high"
    },
    {
        "title": "Unable to access company VPN from home",
        "description": "I'm working from home today and cannot connect to the company VPN. I get an error message saying 'Connection failed - authentication error'. I've double-checked my credentials and they seem correct. This was working fine last week.",
        "category": "Network",
        "priority": "high"
    },
    {
        "title": "Microsoft Excel crashes when opening large spreadsheets",
        "description": "Excel keeps crashing whenever I try to open files larger than 50MB. The application starts to load the file and then suddenly closes without any error message. I need to work with these large datasets for my quarterly reports.",
        "category": "Software",
        "priority": "medium"
    },
    {
        "title": "Request access to SharePoint site for new project",
        "description": "I've been assigned to the 'Project Phoenix' team and need access to the SharePoint site. My manager mentioned I should have read/write permissions to the documents folder and read-only access to the finance folder.",
        "category": "Access",
        "priority": "medium"
    },
    {
        "title": "Email attachments not downloading in Outlook",
        "description": "When I try to download email attachments in Outlook, I get an error saying 'Temporary error, please try again later'. This has been happening for the past 3 hours. I can see the attachments are there but cannot save them to my computer.",
        "category": "Email",
        "priority": "high"
    },
    {
        "title": "Printer not responding - urgent documents needed",
        "description": "The printer on the 3rd floor (HP LaserJet Pro) is not responding to print jobs. The printer shows as online in Windows but nothing happens when I try to print. I have important contracts that need to be printed for a client meeting in 2 hours.",
        "category": "Hardware",
        "priority": "critical"
    },
    {
        "title": "Slow internet connection affecting video calls",
        "description": "My internet connection has been very slow for the past few days. Video calls keep dropping and websites take forever to load. Speed test shows only 2 Mbps download when it should be at least 50 Mbps. This is affecting my ability to attend virtual meetings.",
        "category": "Network",
        "priority": "high"
    },
    {
        "title": "Cannot install required software - admin rights needed",
        "description": "I need to install Adobe Creative Suite for a new marketing campaign but I don't have administrator rights on my computer. I get an error message saying 'Installation failed - insufficient privileges'. Can someone help me install this software?",
        "category": "Software",
        "priority": "medium"
    },
    {
        "title": "Password reset for domain account",
        "description": "I forgot my domain password and need it reset. I tried the self-service portal but it says my security questions don't match. My username is jsmith and I need access urgently as I have a presentation at 2 PM today.",
        "category": "Access",
        "priority": "high"
    },
    {
        "title": "Spam emails getting through to inbox",
        "description": "I've been receiving a lot of spam emails in my inbox over the past week. The emails are clearly spam (offers for fake products, lottery winnings, etc.) but they're not being caught by the spam filter. Can the email security be adjusted?",
        "category": "Email",
        "priority": "low"
    },
    {
        "title": "Computer running very slowly - possible malware",
        "description": "My computer has become extremely slow over the past few days. Programs take minutes to open and the fan is constantly running. I suspect there might be malware. Can someone run a security scan and help clean up my system?",
        "category": "Other",
        "priority": "high"
    },
    {
        "title": "External monitor not detected by laptop",
        "description": "I'm trying to connect my external monitor to my laptop using the HDMI cable but it's not being detected. I've tried different cables and ports but nothing works. The monitor works fine with other devices.",
        "category": "Hardware",
        "priority": "medium"
    },
    {
        "title": "Teams application keeps freezing during meetings",
        "description": "Microsoft Teams freezes frequently during video conferences. The audio continues but the video becomes unresponsive and I have to restart the application. This is very disruptive during important client calls.",
        "category": "Software",
        "priority": "high"
    },
    {
        "title": "WiFi connection dropping every 30 minutes",
        "description": "My WiFi connection keeps dropping every 30 minutes or so. I have to disconnect and reconnect to get back online. This started happening after the recent Windows update. Other devices in the office seem to work fine.",
        "category": "Network",
        "priority": "medium"
    },
    {
        "title": "Need access to CRM system for new sales role",
        "description": "I've just started in the sales team and need access to the Salesforce CRM system. My manager said I should have full access to leads and opportunities. My employee ID is EMP001234.",
        "category": "Access",
        "priority": "medium"
    },
    {
        "title": "Email signature not updating across all devices",
        "description": "I updated my email signature last week but it's not showing the changes on my mobile phone. The signature appears correctly on my desktop Outlook but shows the old version on my iPhone. How can I sync this?",
        "category": "Email",
        "priority": "low"
    },
    {
        "title": "Request for new software license - CAD software",
        "description": "Our engineering team needs an additional license for AutoCAD software. We have a new engineer starting next week and they'll need access to work on client projects. Can we purchase and install an additional license?",
        "category": "Software",
        "priority": "medium"
    },
    {
        "title": "Keyboard keys sticking - affecting productivity",
        "description": "Several keys on my keyboard are sticking, particularly the space bar and the 'e' key. This is making typing very difficult and slowing down my work. I've tried cleaning it but the problem persists.",
        "category": "Hardware",
        "priority": "medium"
    },
    {
        "title": "Cannot connect to shared network drive",
        "description": "I'm unable to access the shared network drive (S: drive) that contains our department's project files. I get an error message 'Network path not found'. Other colleagues can access it fine. I need these files for tomorrow's deadline.",
        "category": "Network",
        "priority": "high"
    },
    {
        "title": "File permissions issue - cannot edit shared documents",
        "description": "I can open shared documents in our team folder but cannot edit or save changes. I get a 'Permission denied' error when trying to save. I had edit permissions last month but something seems to have changed.",
        "category": "Access",
        "priority": "medium"
    },
    {
        "title": "Email not syncing with mobile device",
        "description": "My work emails are not syncing with my company phone. I receive emails on my desktop but they don't show up on my mobile device. I've tried removing and re-adding the account but the issue persists. The sync was working fine until yesterday.",
        "category": "Email",
        "priority": "medium"
    },
    {
        "title": "Blue Screen of Death (BSOD) occurring randomly",
        "description": "My computer has been experiencing Blue Screen of Death errors randomly throughout the day. There's no specific pattern - it happens when I'm using different applications. The error code is usually SYSTEM_SERVICE_EXCEPTION. This is affecting my ability to work.",
        "category": "Other",
        "priority": "critical"
    },
    {
        "title": "Software update stuck at 50% - system unusable",
        "description": "A Windows update started this morning and has been stuck at 50% for over 3 hours. I cannot cancel it or use my computer. I have important work to complete today and need this resolved urgently.",
        "category": "Software",
        "priority": "critical"
    },
    {
        "title": "VPN connection very slow - remote work impacted",
        "description": "When I connect to the company VPN, my internet speed drops significantly. File transfers that normally take minutes are taking hours. This is making remote work very difficult, especially when accessing cloud applications.",
        "category": "Network",
        "priority": "high"
    },
    {
        "title": "Request deactivation of former employee accounts",
        "description": "We need to deactivate all system accounts for John Doe who left the company last Friday. This includes Active Directory, email, VPN access, and any application-specific accounts. His employee ID was EMP005678. Please confirm when this is completed.",
        "category": "Access",
        "priority": "high"
    }
]

def generate_ticket_data():
    """Generate 25 tickets with varied data"""
    
    tickets = []
    
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
        status_choices = ["open", "in_progress", "resolved", "closed"]
        status_weights = [0.4, 0.3, 0.2, 0.1]  # open, in_progress, resolved, closed
        status = random.choices(status_choices, weights=status_weights)[0]
        
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
            "created_at": created_time.isoformat(),
            "updated_at": created_time.isoformat()
        }
        
        # Add assigned agent and resolution for resolved/closed tickets
        if status in ["in_progress", "resolved", "closed"]:
            agents = ["Alice Johnson", "Bob Smith", "Carol Williams", "Dave Brown", "Eva Davis"]
            ticket_doc["assigned_to"] = random.choice(agents)
            
            if status in ["resolved", "closed"]:
                resolutions = [
                    "Issue resolved by restarting the service and updating drivers.",
                    "Problem fixed by adjusting network settings and clearing cache.",
                    "Resolved by reinstalling the application and configuring permissions.",
                    "Fixed by updating software and running system diagnostics.",
                    "Issue resolved through hardware replacement and configuration update."
                ]
                ticket_doc["resolution"] = random.choice(resolutions)
                # Update timestamp for resolution
                resolution_time = created_time + timedelta(hours=random.randint(1, 48))
                ticket_doc["updated_at"] = resolution_time.isoformat()
        
        tickets.append(ticket_doc)
    
    return tickets

def main():
    """Generate ticket data and save to JSON file"""
    print("🎫 Generating 25 sample tickets...")
    
    tickets = generate_ticket_data()
    
    # Save to JSON file
    with open('sample_tickets.json', 'w') as f:
        json.dump(tickets, f, indent=2, default=str)
    
    print(f"✅ Generated {len(tickets)} tickets and saved to sample_tickets.json")
    
    # Show summary statistics
    categories = {}
    priorities = {}
    statuses = {}
    
    for ticket in tickets:
        cat = ticket["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
        pri = ticket["priority"]
        priorities[pri] = priorities.get(pri, 0) + 1
        
        status = ticket["status"]
        statuses[status] = statuses.get(status, 0) + 1
    
    print("\n📊 Distribution Summary:")
    print("\n📂 Categories:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} tickets")
        
    print("\n🎯 Priorities:")
    for pri, count in priorities.items():
        print(f"  {pri}: {count} tickets")
        
    print("\n📋 Status:")
    for status, count in statuses.items():
        print(f"  {status}: {count} tickets")
    
    print("\n✨ Next steps:")
    print("1. Use Docker to insert the tickets into MongoDB")
    print("2. Run: docker exec -i aura-mongodb mongoimport --db aura_servicedesk --collection tickets --jsonArray < sample_tickets.json")

if __name__ == "__main__":
    main()
