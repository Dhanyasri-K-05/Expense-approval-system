def get_assigned_approvers(expense_categories, expense_amounts):
    # Define routing criteria with new approver levels
    routing_criteria = {
        'Office Supplies': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Travel': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Training & Development': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Employee Welfare': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Recruitment Expenses': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Software Subscription': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Marketing and Advertising': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Repair and Maintenance': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Office Rent': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ]
    }

    # Function to determine the approver
    def get_assigned_approver(category, amount):
        if category in routing_criteria:
            for limit, role in routing_criteria[category]:
                if amount <= limit:
                    return role
        return 'No appropriate role found'

    # Process the expense entries
    assigned_approvers = []
    for category, amount in zip(expense_categories, expense_amounts):
        assigned_approver = get_assigned_approver(category, amount)
        assigned_approvers.append(assigned_approver)

    return assigned_approvers

# Example usage
expense_categories = ['Office Supplies', 'Travel', 'Marketing and Advertising']
expense_amounts = [8000, 30000, 60000]

assigned_approvers = get_assigned_approvers(expense_categories, expense_amounts)

print(assigned_approvers)
# Now you can pass assigned_approvers to the next function
