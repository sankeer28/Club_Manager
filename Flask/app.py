from flask import Flask, render_template, request, redirect, url_for, session
from club import Club, User
import secrets
import csv

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)  # Set the secret key

club = Club()
club.load_users_from_csv()  # Update method call

# Function to save scheduled practice to CSV file
def save_practice_to_csv(date, time, location):
    with open('scheduled_practices.csv', 'a', newline='') as csvfile:
        fieldnames = ['Date', 'Time', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Date': date, 'Time': time, 'Location': location})

def get_scheduled_practices(skip_header=True):
    scheduled_practices = []
    with open('scheduled_practices.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        if skip_header:
            next(reader)  # Skip the header row
        for row in reader:
            if len(row) >= 3:
                practice = {'Date': row[0], 'Time': row[1], 'Location': row[2]}
                scheduled_practices.append(practice)
    return scheduled_practices



# Function to delete a scheduled practice from CSV file
def delete_practice_from_csv(date, time, location):
    scheduled_practices = get_scheduled_practices()
    updated_practices = [practice for practice in scheduled_practices if not (practice['Date'] == date and practice['Time'] == time and practice['Location'] == location)]
    with open('scheduled_practices.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Time', 'Location']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for practice in updated_practices:
            writer.writerow(practice)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        email = request.form['email']
        phone = request.form['phone']
        name = request.form.get('name')
        address = request.form.get('address')
        payment_preferences = request.form.get('payment_preferences')
        new_member = User(username, password, role, email, phone, name, address, payment_preferences)
        club.users.append(new_member)
        club.save_users_to_csv()  # Update method call
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in club.users if user.username == username and user.password == password), None)
        if user:
            session['username'] = user.username  # Store username in session
            if user.role == "Coach":
                return redirect(url_for('coach_dashboard'))
            elif user.role == "Treasurer":
                return redirect(url_for('treasurer_dashboard'))
            elif user.role == "Member":
                return redirect(url_for('member_dashboard'))
        else:
            return render_template('login.html', message="Invalid credentials. Please try again.")
    return render_template('login.html')

@app.route('/coach_dashboard')
def coach_dashboard():
    return render_template('coach_dashboard.html')

@app.route('/schedule_practice', methods=['GET', 'POST'])
def schedule_practice():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        save_practice_to_csv(date, time, location)  # Save practice to CSV
        return redirect(url_for('coach_dashboard'))
    return render_template('schedule_practice.html')

@app.route('/view_attendance')
def view_attendance():
    attendance_data = {'username1': 10, 'username2': 15}  # Sample data
    return render_template('view_attendance.html', attendance_data=attendance_data)

@app.route('/treasurer_dashboard')
def treasurer_dashboard():
    return render_template('treasurer_dashboard.html')

@app.route('/member_dashboard')
def member_dashboard():
    return render_template('member_dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  # Remove 'username' from session
    return redirect(url_for('index'))

@app.route('/view_schedule')
def view_schedule():
    scheduled_practices = get_scheduled_practices()  # Retrieve scheduled practices from CSV
    return render_template('view_schedule.html', scheduled_practices=scheduled_practices)

@app.route('/delete_practice', methods=['POST'])
def delete_practice():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        delete_practice_from_csv(date, time, location)  # Delete practice from CSV
        return redirect(url_for('coach_dashboard'))
    return redirect(url_for('coach_dashboard'))  # Redirect in case of a GET request

@app.route('/manage_schedule')
def manage_schedule():
    scheduled_practices = get_scheduled_practices(skip_header=True)  # Skip the header row
    return render_template('manage_schedule.html', scheduled_practices=scheduled_practices)

if __name__ == '__main__':
    app.run(debug=True)
