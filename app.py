from flask import Flask, render_template, request
from models import (
    register_user,
    get_all_users,
    get_user_by_id,
    allocate_cabin,
    generate_bill,
    get_priority_users  # Corrected to match the function name
)
from db import init_db

app = Flask(__name__)

# Initialize database when the application starts
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        
        # Register the user and capture user ID
        user_id = register_user(name, phone, email, password)
        
        # Pass user ID to the template
        return render_template('register.html', user_id=user_id)

    return render_template('register.html')


@app.route('/users')
def users():
    users = get_all_users()
    return render_template('users.html', users=users)

@app.route('/allocate-cabin', methods=['GET', 'POST'])
def allocate_cabin_route():
    if request.method == 'POST':
        user_id = request.form['user_id']
        result = allocate_cabin(user_id)  # Attempt to allocate cabin
        
        # Check the result and render the appropriate message
        if result == "This user doesn't exist.":
            return render_template('allocate_cabin.html', error=result)
        
        # If cabin is successfully allocated, display the result
        return render_template('allocate_cabin.html', result=result)
    
    return render_template('allocate_cabin.html')

@app.route('/generate-bill', methods=['GET', 'POST'])
def generate_bill_route():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_info, bill_amount = generate_bill(user_id)
        
        # If user doesn't exist, display the error message
        if user_info is None:
            return render_template('generate_bill.html', error=bill_amount)
        
        # If user exists, display the user info and bill
        return render_template('generate_bill.html', name=user_info['name'], hours=user_info['hours_used'], bill=bill_amount)
    
    return render_template('generate_bill.html')

@app.route('/priority-users')
def priority_users():
    priority_users = get_priority_users()  # Fixed function call to match import
    return render_template('priority_users.html', priority_users=priority_users)

if __name__ == '__main__':
    app.run(debug=True)
