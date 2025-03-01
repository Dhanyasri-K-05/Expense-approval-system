import psycopg2
from flask import Flask, request, jsonify
import json, requests
from flask_cors import CORS
from psycopg2 import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)


def connect_to_db():
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            user="postgres",
            password="tiger",
            host="localhost",
            port="5432",
            database="expense_management"
        )
        return connection
    
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)


def fetch_vacation_data():
    """Fetch vacation data from the database."""
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT department, hierarchy, vacation_start, vacation_end FROM vacation_data")
        data = cur.fetchall()
        if not data:
            return ()
        cur.close()
        conn.close()
        return data
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # Close the database connection
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed from fetch vacation data")

def is_on_vacation(vacation_start, vacation_end, check_date):
    """Check if the approver is on vacation on a given date."""
    print(vacation_start, vacation_end, check_date.date())
    print(type(vacation_start), type(vacation_end), type(check_date.date()))
    try:
        if vacation_start and vacation_end:
            if vacation_start <= check_date.date() <= vacation_end:
                return True
        return False
    except:
        print("Error in is on vecation")

def find_first_available_approver(department, assigned_role, check_date):
    """Find the first available approver within the department starting from the assigned role."""
    print(check_date, type(check_date))
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
        'Training and Education': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Hardware': [
            (10000, 'Junior Approver'),
            (25000, 'Senior Approver'),
            (50000, 'Managerial Approver'),
            (float('inf'), 'Executive Approver')
        ],
        'Transportation': [
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
                print(role)
                return role
    return False

expense_department_mapping = {
    'Office Supplies': 'operations',
    'Travel': 'operations',
    'Training & Development': 'HR',
    'Employee Welfare': 'HR',
    'Recruitment Expenses': 'HR',
    'Software Subscription': 'IT',
    'Marketing and Advertising': 'marketing',
    'Repair and Maintenance': 'operations',
    'Office Rent': 'finance'
}

# Function to determine the department responsible for approving an expense
def get_approver_department(expense_category):
    print("Get approver success")
    return expense_department_mapping.get(expense_category, 'Unknown department')

@app.route('/insert_data', methods=['POST'])
def insert_data():

    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        data = request.get_json()
        # SQL statement to insert data into the table
        insert_query = """INSERT INTO vacation_data (department, name, hierarchy, vacation_start, vacation_end)
                        VALUES (%s, %s, %s, %s, %s)"""
        hi ={
                "junior": 1,
                "senior": 2,
                "managerial": 3,
                "executive": 4
            }
        
        print(hi[data['role']])
        # Data to be inserted into the table
        data_to_insert = (
            data['department'].upper(),
            data['name'],
            hi[data['role']],
            data['vacation_start'],
            data['vacation_end']
        )

        # Execute the SQL command for each row of data
        cursor.execute(insert_query, data_to_insert)

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

        return jsonify({'message': 'Data inserted successfully!'}), 201

    except (Exception, Error) as error:
        return jsonify({'error': str(error)}), 500

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route('/login', methods=['POST'])
def get_password():
    try:
        data = request.get_json()
        username = data.get('username')

        connection = connect_to_db()
        cursor = connection.cursor()

        # SQL statement to retrieve the password based on the username
        select_query = "SELECT password, role FROM usertable WHERE username = %s"

        # Execute the SQL command to fetch the password
        cursor.execute(select_query, (username,))
        
        # Fetch the result
        password = cursor.fetchone()

        if username:
            if password:
                return jsonify({'password': password[0],'role':password[1]})
            else:
                return jsonify({'error': 404})
        else:
            return jsonify({'error': 'Username not provided'}), 400

    except (Exception, Error) as error:
        print('error in querry')
        print("Error while connecting to PostgreSQL:", error)
        return None

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route("/insert_expense", methods=['POST'])
def insert_expense():
    data = request.get_json()
    username = data['username']
    expense_category = data['expense_category']
    request_date = data['request_date']
    amount = int(data['amount'])

    print(expense_category)
    print(amount)
    payload = json.dumps({
        "expenseCategory": expense_category,
        "amount": amount
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", "http://127.0.0.1:5001/predict", headers=headers, data=payload)
    print(response.text)
    predict = json.loads(response.text)
    try:
        insert_query = ""
        record_to_insert = ()
        connection = connect_to_db()
        cursor = connection.cursor()
        # SQL query to insert data into the expenserequest table
        if(predict['predicted_class'] == 1):
        #if(False):
            insert_query = """INSERT INTO expenserequest (username, expense_category, department, request_date, amount, status, approver)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (username, expense_category, get_approver_department(expense_category), request_date, amount, "Approved", "Model")
        else:
            assigned_approver = get_assigned_approver(expense_category, amount)
            available_approver = find_first_available_approver(get_approver_department(expense_category), assigned_approver, datetime.strptime(request_date, '%Y-%m-%d'))
            insert_query = """INSERT INTO expenserequest (username, expense_category, department, request_date, amount, approver)
                            VALUES (%s, %s, %s, %s, %s, %s)"""
            record_to_insert = (username, expense_category, get_approver_department(expense_category), request_date, amount, available_approver)
        # Data to be inserted
        
        # Execute the insert query
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        return jsonify({'message': 'Expense request inserted successfully'})

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL in insert function", error)
        return jsonify({'error': 'Failed to insert expense request'}), 500
    finally:
        # Close database connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed from insert")

@app.route("/expenses") #get method
def expense():
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM expenserequest")
    expenses = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Serialize the fetched data to JSON and send it as a response
    return jsonify(expenses)

@app.route('/deleteExpense', methods=['DELETE'])
def delete_expense():
    try:
        rid = int(request.args.get('rid'))
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM expenserequest WHERE rid = %s", (rid,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({"message": f"Expense with rid {rid} deleted successfully"})
    except Error as e:
        print(f"Error deleting expense from database: {e}")
        return jsonify({"error": "Failed to delete expense"}), 500

@app.route('/update_status', methods=['POST'])
def update_poster_status():
    # Get the poster ID and new status from the request body
    data = request.get_json()
    rid = data.get('rid')
    new_status = data.get('newStatus')

    # Connect to the database
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Update the status in the database
        cursor.execute("UPDATE expenserequest SET status = %s WHERE rid = %s", (new_status, rid))
        connection.commit()
        return jsonify({'message': 'Poster status updated successfully'})
    except (Exception, Error) as error:
        print("Error updating poster status:", error)
        return jsonify({'error': 'Failed to update poster status'}), 500
    finally:
        # Close database connection
        if connection:
            cursor.close()
            connection.close()
    
if __name__ == '__main__':
    app.run(debug=True)
