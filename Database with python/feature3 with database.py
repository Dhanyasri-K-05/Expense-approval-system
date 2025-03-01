import psycopg2
from datetime import datetime

# Database connection parameters
db_params = {
    "dbname": "expense_management",
    "user": "postgres",
    "password": "tiger",
    "host": "localhost",
    "port": "5432"
}

def fetch_vacation_data():
    """Fetch vacation data from the database."""
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT department, hierarchy, vacation_start, vacation_end FROM vacation_data")
    data = cur.fetchall()
    if not data:
        print("not data is true")
        return None
    cur.close()
    conn.close()
    return data

def is_on_vacation(vacation_start, vacation_end, check_date):
    print(vacation_start, vacation_end, check_date.date())
    print(type(vacation_start), type(vacation_end), type(check_date.date()))
    """Check if the approver is on vacation on a given date."""
    if vacation_start and vacation_end:
        print("having value")
        if vacation_start <= check_date.date() <= vacation_end:
            print("In between")
            return True
        print("Not in between")
    return False

def find_first_available_approver(department, assigned_role, check_date):
    """Find the first available approver within the department starting from the assigned role."""
    vacation_data = fetch_vacation_data()
    start_iteration = False
    for approver_info in approval_hierarchy[department]:
        if approver_info["role"] == assigned_role:
            start_iteration = True
        if start_iteration:
            approver_vacation_data = next((a for a in vacation_data if a[0] == department and a[1] == approver_info["hierarchy"]), None)
            if not approver_vacation_data or not is_on_vacation(approver_vacation_data[2], approver_vacation_data[3], check_date):
                return approver_info["role"]
    return None

def print_first_available_approver(department, assigned_role, check_date):
    """Print the first available approver within the department starting from the assigned role."""
    first_available_approver = find_first_available_approver(department, assigned_role, check_date)
    if first_available_approver:
        final_result="The report is routed to {first_available_approver}of+ {department} department"
        print(f"The report is routed to {first_available_approver} of {department} department")
        
    else:
        print("No approver is available.")

# Simulated data representing approval hierarchy
approval_hierarchy = {
    "finance": [
        {"role": "Junior Approver", "hierarchy": 1},
        {"role": "Senior Approver", "hierarchy": 2},
        {"role": "Managerial Approver", "hierarchy": 3},
        {"role": "Executive Approver", "hierarchy": 4}
    ],
    "HR": [
        {"role": "Junior Approver", "hierarchy": 1},
        {"role": "Senior Approver", "hierarchy": 2},
        {"role": "Managerial Approver", "hierarchy": 3},
        {"role": "Executive Approver", "hierarchy": 4}
    ],
    "IT": [
        {"role": "Junior Approver", "hierarchy": 1},
        {"role": "Senior Approver", "hierarchy": 2},
        {"role": "Managerial Approver", "hierarchy": 3},
        {"role": "Executive Approver", "hierarchy": 4}
    ],
    "marketing": [
        {"role": "Junior Approver", "hierarchy": 1},
        {"role": "Senior Approver", "hierarchy": 2},
        {"role": "Managerial Approver", "hierarchy": 3},
        {"role": "Executive Approver", "hierarchy": 4}
    ],
    "sales": [
        {"role": "Junior Approver", "hierarchy": 1},
        {"role": "Senior Approver", "hierarchy": 2},
        {"role": "Managerial Approver", "hierarchy": 3},
        {"role": "Executive Approver", "hierarchy": 4}
    ],
    "operations": [
        {"role": "Junior Approver", "hierarchy": 1},
        {"role": "Senior Approver", "hierarchy": 2},
        {"role": "Managerial Approver", "hierarchy": 3},
        {"role": "Executive Approver", "hierarchy": 4}
    ]
}

# Set default values for department, assigned role, and submission date
department = "finance"
assigned_role = "Junior Approver"
submission_date = "2024-06-11"

# Print the first available approver based on the provided inputs
print_first_available_approver(department, assigned_role, datetime.strptime(submission_date, '%Y-%m-%d'))
print(datetime.strptime('2024-06-07', '%Y-%m-%d'))