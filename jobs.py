# jobs.py
# Comprehensive database containing over 100 common jobs across major industries,
# complete with requirements and years of experience.

JOB_DATABASE = {
    "engineering": [
        {"title": "Junior Software Engineer", "experience": "0-1 years", "requirements": ["Python", "Git", "Data Structures", "Basic SQL"]},
        {"title": "Full Stack Developer", "experience": "1-3 years", "requirements": ["JavaScript", "React", "Node.js", "REST APIs", "Database Management"]},
        {"title": "DevOps Engineer", "experience": "2-5 years", "requirements": ["Docker", "Kubernetes", "CI/CD Pipelines", "AWS/GCP", "Linux Scripting"]},
        {"title": "Data Scientist", "experience": "2-4 years", "requirements": ["Python", "Pandas", "Machine Learning", "Statistics", "SQL"]},
        {"title": "Senior Software Architect", "experience": "8+ years", "requirements": ["System Design", "Microservices", "Cloud Architecture", "Leadership", "Scala/Java"]},
        {"title": "VLSI Design Engineer", "experience": "1-3 years", "requirements": ["Verilog", "VHDL", "CMOS Basics", "Digital Signal Processing"]},
        {"title": "Embedded Systems Engineer", "experience": "2-4 years", "requirements": ["C/C++", "Microcontrollers", "RTOS", "PCB Design Basics"]},
        {"title": "Mechanical Design Engineer", "experience": "1-3 years", "requirements": ["SolidWorks", "AutoCAD", "Thermodynamics", "GD&T"]},
        {"title": "Civil Project Engineer", "experience": "2-5 years", "requirements": ["AutoCAD Civil 3D", "Structural Analysis", "Site Management", "Safety Compliance"]},
        {"title": "Electrical Power Engineer", "experience": "1-4 years", "requirements": ["Circuit Simulation", "AutoCAD Electrical", "Power Systems", "PLC Programming"]},
        {"title": "Chemical Process Engineer", "experience": "2-5 years", "requirements": ["Aspen Plus", "Fluid Mechanics", "Process Safety", "Mass Transfer"]},
        {"title": "Quality Assurance Engineer", "experience": "1-3 years", "requirements": ["Test Automation", "Selenium", "Python/Java", "Bug Tracking Tools"]},
        {"title": "Cybersecurity Analyst", "experience": "2-4 years", "requirements": ["Network Security", "SIEM Tools", "Penetration Testing", "Incident Response"]},
        {"title": "Cloud Infrastructure Engineer", "experience": "3-6 years", "requirements": ["AWS/Azure", "Terraform", "Networking", "IAM Policies"]},
        {"title": "AI/ML Research Engineer", "experience": "3-6 years", "requirements": ["PyTorch/TensorFlow", "Deep Learning", "Linear Algebra", "NLP/Computer Vision"]}
    ],
    "healthcare": [
        {"title": "General Practitioner", "experience": "1-3 years", "requirements": ["MBBS Degree", "State Medical Council Registration", "Clinical Diagnostics"]},
        {"title": "Resident Medical Officer", "experience": "2-5 years", "requirements": ["Emergency Care Protocols", "Patient Monitoring", "Pharmacology Knowledge"]},
        {"title": "Medical Laboratory Technician", "experience": "0-2 years", "requirements": ["Phlebotomy", "Lab Safety Protocols", "Pathology Equipment Handling"]},
        {"title": "Registered Nurse", "experience": "1-4 years", "requirements": ["Nursing License", "Patient Care", "Vitals Monitoring", "EMR Software"]},
        {"title": "Pharmacist", "experience": "1-3 years", "requirements": ["Pharm.D or B.Pharm", "Drug Dispensing", "Patient Counseling", "Inventory Control"]},
        {"title": "Radiologic Technologist", "experience": "1-3 years", "requirements": ["X-Ray/MRI Certification", "Radiation Safety", "Patient Positioning", "Imaging Software"]},
        {"title": "Physical Therapist", "experience": "2-4 years", "requirements": ["Doctor of Physical Therapy", "Rehabilitation Techniques", "Patient Assessment", "Kinesiology"]},
        {"title": "Clinical Research Associate", "experience": "1-3 years", "requirements": ["GCP Guidelines", "Data Verification", "Clinical Trial Management", "Medical Terminology"]},
        {"title": "Healthcare Administrator", "experience": "4-7 years", "requirements": ["Healthcare Compliance", "Budgeting", "Hospital Operations", "Staff Management"]},
        {"title": "Biomedical Equipment Technician", "experience": "2-4 years", "requirements": ["Electronics Troubleshooting", "Medical Device Calibration", "Safety Standards", "Repair Logs"]}
    ],
    "finance": [
        {"title": "Junior Accountant", "experience": "0-2 years", "requirements": ["Bookkeeping", "Excel", "QuickBooks", "Accounts Payable/Receivable"]},
        {"title": "Financial Analyst", "experience": "2-4 years", "requirements": ["Financial Modeling", "SQL", "Valuation Techniques", "Market Research"]},
        {"title": "Investment Banking Associate", "experience": "3-6 years", "requirements": ["M&A Analysis", "Pitchbook Creation", "Advanced Excel", "Financial Statement Analysis"]},
        {"title": "Tax Consultant", "experience": "2-5 years", "requirements": ["Tax Regulations", "Corporate Tax Filing", "Audit Preparation", "CPA/CA Certification"]},
        {"title": "Risk Management Specialist", "experience": "3-6 years", "requirements": ["Risk Modeling", "Credit Analysis", "Regulatory Compliance", "Data Analytics"]},
        {"title": "Auditor", "experience": "2-4 years", "requirements": ["Internal Controls", "Financial Auditing", "SOX Compliance", "Analytical Review"]},
        {"title": "Portfolio Manager", "experience": "5-8 years", "requirements": ["Asset Allocation", "Wealth Management", "Equity Research", "Risk Tolerance Assessment"]},
        {"title": "Loan Officer", "experience": "1-3 years", "requirements": ["Credit Evaluation", "Underwriting Basics", "Customer Service", "Financial Regulations"]},
        {"title": "Actuary", "experience": "3-6 years", "requirements": ["Probability", "Statistics", "Actuarial Exams Passed", "Risk Assessment Software"]},
        {"title": "Compliance Officer", "experience": "4-7 years", "requirements": ["Regulatory Frameworks", "AML/KYC Standards", "Policy Enforcement", "Internal Investigations"]}
    ],
    "information_technology": [
        {"title": "IT Help Desk Support", "experience": "0-1 years", "requirements": ["Troubleshooting", "Windows/macOS Support", "Active Directory", "Ticketing Systems"]},
        {"title": "Network Administrator", "experience": "2-5 years", "requirements": ["Cisco Routers/Switches", "TCP/IP", "VPN Setup", "Firewall Configuration"]},
        {"title": "Database Administrator", "experience": "3-6 years", "requirements": ["PostgreSQL/MySQL", "Database Tuning", "Backup & Recovery", "Query Optimization"]},
        {"title": "Systems Analyst", "experience": "2-5 years", "requirements": ["Requirements Gathering", "UML Modeling", "System Integration", "Workflow Analysis"]},
        {"title": "Scrum Master", "experience": "3-6 years", "requirements": ["Agile Methodologies", "Sprint Planning", "Jira/Confluence", "Conflict Resolution"]},
        {"title": "UI/UX Designer", "experience": "2-4 years", "requirements": ["Figma", "Wireframing", "User Research", "Prototyping", "Design Systems"]},
        {"title": "Product Manager", "experience": "3-6 years", "requirements": ["Product Roadmapping", "Market Analysis", "Cross-functional Leadership", "User Stories"]},
        {"title": "Salesforce Administrator", "experience": "2-4 years", "requirements": ["Salesforce Configuration", "Flows", "Reports & Dashboards", "Data Migration"]},
        {"title": "IT Security Specialist", "experience": "3-6 years", "requirements": ["Vulnerability Assessment", "Firewalls", "Encryption Protocols", "Security Audits"]},
        {"title": "Business Intelligence Analyst", "experience": "2-4 years", "requirements": ["Tableau/PowerBI", "SQL", "Data Warehousing", "ETL Processes"]}
    ],
    "marketing_and_sales": [
        {"title": "Digital Marketing Specialist", "experience": "1-3 years", "requirements": ["SEO/SEM", "Google Analytics", "Social Media Campaigns", "Content Strategy"]},
        {"title": "Content Writer", "experience": "0-2 years", "requirements": ["Copywriting", "SEO Best Practices", "Proofreading", "Blog Management"]},
        {"title": "Growth Marketing Manager", "experience": "3-6 years", "requirements": ["A/B Testing", "Funnel Optimization", "Paid Acquisition", "Data Analytics"]},
        {"title": "Social Media Manager", "experience": "1-3 years", "requirements": ["Instagram/TikTok/LinkedIn Management", "Community Engagement", "Content Calendars", "Analytics"]},
        {"title": "Brand Strategist", "experience": "4-7 years", "requirements": ["Brand Positioning", "Market Research", "Creative Direction", "Consumer Psychology"]},
        {"title": "Sales Development Representative", "experience": "0-2 years", "requirements": ["Cold Outreach", "CRM Software", "Lead Qualification", "Communication Skills"]},
        {"title": "Account Executive", "experience": "2-5 years", "requirements": ["B2B Sales", "Negotiation", "Pipeline Management", "Contract Closing"]},
        {"title": "Customer Success Manager", "experience": "2-4 years", "requirements": ["Client Retention", "Onboarding", "SaaS Metrics", "Problem Solving"]},
        {"title": "Public Relations Specialist", "experience": "2-4 years", "requirements": ["Media Outreach", "Press Release Writing", "Crisis Management", "Networking"]},
        {"title": "E-Commerce Specialist", "experience": "1-3 years", "requirements": ["Shopify/Amazon Seller Central", "Inventory Management", "Conversion Rate Optimization", "PPC Ads"]}
    ],
    "education": [
        {"title": "High School Teacher", "experience": "1-3 years", "requirements": ["State Teaching License", "Subject Matter Degree", "Lesson Planning", "Classroom Management"]},
        {"title": "University Lecturer", "experience": "3-6 years", "requirements": ["Master's/Ph.D. in Field", "Academic Research", "Public Speaking", "Curriculum Design"]},
        {"title": "Instructional Designer", "experience": "2-5 years", "requirements": ["E-Learning Tools", "Articulate Storyline", "Pedagogical Theory", "Content Authoring"]},
        {"title": "Corporate Trainer", "experience": "2-4 years", "requirements": ["Workshop Facilitation", "Presentation Skills", "Training Needs Analysis", "Employee Coaching"]},
        {"title": "Academic Advisor", "experience": "1-3 years", "requirements": ["Student Counseling", "Degree Auditing", "Higher Education Policies", "Communication"]},
        {"title": "Special Education Teacher", "experience": "1-4 years", "requirements": ["IEP Development", "Adaptive Teaching Methods", "Special Ed Certification", "Patience & Empathy"]},
        {"title": "Tutor / Learning Consultant", "experience": "0-2 years", "requirements": ["Subject Expertise", "One-on-One Coaching", "Progress Tracking", "Customized Study Plans"]},
        {"title": "School Administrator", "experience": "5-8 years", "requirements": ["Educational Leadership", "Budgeting", "Staff Evaluation", "Policy Implementation"]},
        {"title": "E-Learning Content Developer", "experience": "1-3 years", "requirements": ["Multimedia Production", "Scriptwriting", "LMS Platforms", "Interactive Modules"]},
        {"title": "Library Media Specialist", "experience": "2-4 years", "requirements": ["Library Science Degree", "Cataloging Systems", "Research Support", "Information Literacy"]}
    ],
    "legal": [
        {"title": "Paralegal", "experience": "1-3 years", "requirements": ["Legal Research", "Document Drafting", "Case Management Software", "Filing Procedures"]},
        {"title": "Corporate Lawyer", "experience": "3-7 years", "requirements": ["Juris Doctor (JD)", "Bar Admission", "Contract Law", "Corporate Governance"]},
        {"title": "Compliance Analyst", "experience": "2-4 years", "requirements": ["Regulatory Analysis", "Risk Assessment", "Audit Support", "Policy Documentation"]},
        {"title": "Legal Assistant", "experience": "0-2 years", "requirements": ["Scheduling", "Client Intake", "Transcription", "Administrative Support"]},
        {"title": "Intellectual Property Specialist", "experience": "3-6 years", "requirements": ["Patent/Trademark Filing", "IP Law", "Prior Art Searches", "Technical Writing"]},
        {"title": "Contract Administrator", "experience": "2-5 years", "requirements": ["Contract Negotiation", "Lifecycle Management", "Legal Terminology", "Vendor Relations"]},
        {"title": "Labor Relations Specialist", "experience": "3-6 years", "requirements": ["Employment Law", "Union Negotiations", "Dispute Resolution", "HR Policies"]},
        {"title": "Tax Attorney", "experience": "4-8 years", "requirements": ["LL.M in Taxation", "Tax Litigation", "IRS Regulations", "Estate Planning"]},
        {"title": "Litigation Support Specialist", "experience": "2-4 years", "requirements": ["E-Discovery", "Trial Technology", "Document Review", "Database Management"]},
        {"title": "Legal Consultant", "experience": "5+ years", "requirements": ["Specialized Legal Advice", "Risk Analysis", "Strategic Planning", "Industry Expertise"]}
    ],
    "operations_and_logistics": [
        {"title": "Supply Chain Analyst", "experience": "1-3 years", "requirements": ["Logistics Software", "Data Analysis", "Inventory Tracking", "Excel"]},
        {"title": "Logistics Coordinator", "experience": "0-2 years", "requirements": ["Freight Forwarding", "Shipping Documentation", "Vendor Communication", "Problem Solving"]},
        {"title": "Warehouse Manager", "experience": "3-6 years", "requirements": ["WMS Systems", "Inventory Control", "Team Leadership", "Safety Protocols"]},
        {"title": "Operations Manager", "experience": "5-8 years", "requirements": ["Process Optimization", "Budget Management", "KPI Tracking", "Strategic Planning"]},
        {"title": "Procurement Specialist", "experience": "2-4 years", "requirements": ["Supplier Sourcing", "Contract Negotiation", "Purchasing Systems", "Cost Analysis"]},
        {"title": "Quality Control Inspector", "experience": "1-3 years", "requirements": ["Inspection Standards", "Defect Tracking", "Measuring Tools", "Documentation"]},
        {"title": "Fleet Manager", "experience": "3-6 years", "requirements": ["Fleet Tracking Software", "Maintenance Scheduling", "DOT Regulations", "Cost Reduction"]},
        {"title": "Inventory Control Specialist", "experience": "1-3 years", "requirements": ["Cycle Counting", "ERP Systems", "Stock Reconciliation", "Data Entry"]},
        {"title": "Project Coordinator", "experience": "1-3 years", "requirements": ["Project Management Tools", "Scheduling", "Meeting Coordination", "Status Reporting"]},
        {"title": "Facilities Manager", "experience": "4-7 years", "requirements": ["Building Maintenance", "Vendor Management", "Safety Compliance", "Space Planning"]}
    ],
    "human_resources": [
        {"title": "HR Recruiter", "experience": "1-3 years", "requirements": ["Sourcing Candidates", "Applicant Tracking Systems", "Interviewing", "Screening"]},
        {"title": "HR Generalist", "experience": "2-5 years", "requirements": ["Employee Relations", "Onboarding", "HRIS Software", "Benefits Administration"]},
        {"title": "Compensation and Benefits Manager", "experience": "4-7 years", "requirements": ["Salary Benchmarking", "Insurance Plans", "Payroll Management", "Data Analysis"]},
        {"title": "Training and Development Specialist", "experience": "2-4 years", "requirements": ["Workshop Design", "Talent Assessment", "Learning Management Systems", "Public Speaking"]},
        {"title": "HR Business Partner", "experience": "5-8 years", "requirements": ["Strategic Planning", "Organizational Development", "Change Management", "Coaching"]},
        {"title": "Payroll Specialist", "experience": "1-3 years", "requirements": ["Payroll Processing", "Tax Withholdings", "Timekeeping Systems", "Attention to Detail"]},
        {"title": "Diversity and Inclusion Manager", "experience": "4-7 years", "requirements": ["DEI Program Design", "Community Outreach", "Policy Review", "Unconscious Bias Training"]},
        {"title": "Talent Acquisition Manager", "experience": "5-8 years", "requirements": ["Recruitment Strategy", "Employer Branding", "Team Leadership", "Agency Management"]},
        {"title": "Employee Relations Specialist", "experience": "3-6 years", "requirements": ["Conflict Resolution", "Disciplinary Procedures", "Labor Laws", "Investigation Skills"]},
        {"title": "HR Assistant", "experience": "0-1 years", "requirements": ["Data Entry", "Scheduling Interviews", "Record Keeping", "Basic HR Knowledge"]}
    ],
    "hospitality_and_tourism": [
        {"title": "Hotel Front Desk Agent", "experience": "0-2 years", "requirements": ["Customer Service", "Hotel Management Software", "Reservations", "Cash Handling"]},
        {"title": "Event Planner", "experience": "2-5 years", "requirements": ["Vendor Coordination", "Budgeting", "Timeline Management", "Negotiation"]},
        {"title": "Restaurant Manager", "experience": "3-6 years", "requirements": ["Staff Supervision", "POS Systems", "Food Safety Standards", "Inventory Control"]},
        {"title": "Travel Consultant", "experience": "1-3 years", "requirements": ["Booking Systems", "Itinerary Planning", "Destination Knowledge", "Customer Support"]},
        {"title": "Executive Chef", "experience": "5-8 years", "requirements": ["Culinary Expertise", "Menu Development", "Kitchen Hygiene", "Cost Control"]},
        {"title": "Tour Guide", "experience": "0-2 years", "requirements": ["Public Speaking", "Local History", "Crowd Management", "First Aid Basics"]},
        {"title": "Concierge", "experience": "1-3 years", "requirements": ["Local Networking", "Guest Services", "Problem Solving", "Multi-lingual Skills"]},
        {"title": "Food and Beverage Director", "experience": "5-8 years", "requirements": ["Operations Management", "Event Catering", "Menu Pricing", "Staff Training"]},
        {"title": "Housekeeping Supervisor", "experience": "2-4 years", "requirements": ["Cleaning Standards", "Inspection Procedures", "Staff Management", "Inventory Tracking"]},
        {"title": "Resort Activities Coordinator", "experience": "1-3 years", "requirements": ["Recreation Planning", "Guest Engagement", "Safety Protocols", "Entertainment Skills"]}
    ]
}

