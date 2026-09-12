# recruiters_dict.py

RECRUITERS_BOX = {
    "john doe": {
        "name": "John Doe",
        "company": "Google LLC",
        "title": "Senior Technical Recruiter",
        "email": "johndoe@google.com",
        "verified": True,
        "profile_url": "https://linkedin.com/in/johndoe-recruiter"
    },
    "jane smith": {
        "name": "Jane Smith",
        "company": "Microsoft Corporation",
        "title": "Talent Acquisition Lead",
        "email": "jsmith@microsoft.com",
        "verified": True,
        "profile_url": "https://linkedin.com/in/janesmith-talent"
    },
    "alex johnson": {
        "name": "Alex Johnson",
        "company": "Amazon.com, Inc.",
        "title": "HR Business Partner",
        "email": "alexj@amazon.com",
        "verified": True,
        "profile_url": "https://linkedin.com/in/alexjohnson-hr"
    },
    "sarah williams": {
        "name": "Sarah Williams",
        "company": "Apple Inc.",
        "title": "University Recruiter",
        "email": "swilliams@apple.com",
        "verified": True,
        "profile_url": "https://linkedin.com/in/sarahwilliams-apple"
    },
    "michael brown": {
        "name": "Michael Brown",
        "company": "Meta Platforms, Inc.",
        "title": "Technical Sourcing Specialist",
        "email": "mbrown@meta.com",
        "verified": True,
        "profile_url": "https://linkedin.com/in/michaelbrown-meta"
    }
}

for i in range(6, 51):
    key = f"recruiter placeholder {i}"
    RECRUITERS_BOX[key] = {
        "name": f"Recruiter Placeholder {i}",
        "company": f"Enterprise Company Placeholder {i} LLC",
        "title": "Talent Acquisition Specialist",
        "email": f"recruiter{i}@placeholder.com",
        "verified": False,
        "profile_url": f"https://linkedin.com/in/recruiter-placeholder-{i}"
    }
    