def get_mock_tickets():
    return {
        "project": "Mobile App — Sprint 4",
        "sprint": "Sprint 4",
        "total_tickets": 12,
        "tickets": [
            {
                "id": "MOB-101",
                "summary": "Payment gateway integration",
                "description": "Integrate Razorpay payment gateway into checkout flow. Backend complete but frontend blocked waiting for API keys from vendor.",
                "status": "In Progress",
                "priority": "Critical",
                "assignee": "Rahul Sharma",
                "story_points": 8
            },
            {
                "id": "MOB-102",
                "summary": "Login screen bug on Android",
                "description": "Critical bug found in QA — login fails on Android 12 devices. Affects 40% of our user base. Must be fixed before launch.",
                "status": "In Progress",
                "priority": "Critical",
                "assignee": "Priya Nair",
                "story_points": 5
            },
            {
                "id": "MOB-103",
                "summary": "Push notification service",
                "description": "Implement Firebase push notifications for order updates. Work has not started. Delayed due to dependency on backend team.",
                "status": "To Do",
                "priority": "High",
                "assignee": "Unassigned",
                "story_points": 6
            },
            {
                "id": "MOB-104",
                "summary": "Product listing page",
                "description": "Build the product listing page with filters and sorting. Completed and tested successfully.",
                "status": "Done",
                "priority": "High",
                "assignee": "Amit Verma",
                "story_points": 5
            },
            {
                "id": "MOB-105",
                "summary": "User profile settings",
                "description": "Allow users to update their profile, address, and preferences. Complete and merged to main branch.",
                "status": "Done",
                "priority": "Medium",
                "assignee": "Sneha Patel",
                "story_points": 3
            },
            {
                "id": "MOB-106",
                "summary": "Order history screen",
                "description": "Display past orders with status and tracking. In review, waiting for design approval before final merge.",
                "status": "In Review",
                "priority": "Medium",
                "assignee": "Rahul Sharma",
                "story_points": 4
            },
            {
                "id": "MOB-107",
                "summary": "Performance optimization",
                "description": "App loads slowly on low-end devices. Need to optimize image loading and reduce API calls. Not yet started.",
                "status": "To Do",
                "priority": "Medium",
                "assignee": "Unassigned",
                "story_points": 5
            },
            {
                "id": "MOB-108",
                "summary": "Search functionality",
                "description": "Implement product search with autocomplete. Blocked — search API from backend is not ready yet.",
                "status": "Blocked",
                "priority": "High",
                "assignee": "Priya Nair",
                "story_points": 6
            },
            {
                "id": "MOB-109",
                "summary": "Checkout flow",
                "description": "Multi-step checkout including cart, address, and payment screens. Complete and passed QA.",
                "status": "Done",
                "priority": "Critical",
                "assignee": "Amit Verma",
                "story_points": 8
            },
            {
                "id": "MOB-110",
                "summary": "Crash on app launch — iOS 17",
                "description": "Critical crash reported on iOS 17.2 during app launch. Affects new iPhone users. Escalated to engineering lead.",
                "status": "In Progress",
                "priority": "Critical",
                "assignee": "Sneha Patel",
                "story_points": 3
            },
            {
                "id": "MOB-111",
                "summary": "Analytics tracking",
                "description": "Add Mixpanel event tracking across all screens. Minor task, not yet started but low priority.",
                "status": "To Do",
                "priority": "Low",
                "assignee": "Unassigned",
                "story_points": 2
            },
            {
                "id": "MOB-112",
                "summary": "Accessibility improvements",
                "description": "Add screen reader support and improve contrast ratios. Nice to have for this sprint.",
                "status": "To Do",
                "priority": "Low",
                "assignee": "Unassigned",
                "story_points": 3
            }
        ]
    }