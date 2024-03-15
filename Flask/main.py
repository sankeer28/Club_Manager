from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from club import Club, User
import secrets
import csv
import os

app = Flask(__name__, static_url_path='/static')
app.secret_key = secrets.token_hex(24) 

club = Club()
club.load_users_from_csv() 


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
            next(reader)  
        for row in reader:
            if len(row) >= 3:
                practice = {'Date': row[0], 'Time': row[1], 'Location': row[2]}
                scheduled_practices.append(practice)
    return scheduled_practices


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
        club.save_users_to_csv() 
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in club.users if user.username == username and user.password == password), None)
        if user:
            session['username'] = user.username  
            session['role'] = user.role  
            if user.role == "Coach":
                return redirect(url_for('coach_dashboard'))
            elif user.role == "Treasurer":
                return redirect(url_for('treasurer_dashboard'))
            elif user.role == "Member":
                return redirect(url_for('member_dashboard'))
        else:
            return render_template('index.html', message="Invalid credentials. Please try again.")
    return render_template('index.html')



@app.route('/email_members')
def email_members():
    return render_template('email.html')

@app.route('/coach_dashboard')
def coach_dashboard():

    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == session['username']:
                coach_name = row['name']
                break

    return render_template('coach_dashboard.html', coach_name=coach_name)



def process_csv():
    members = []
    csv_path = os.path.join(os.path.dirname(__file__), 'users.csv')
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['role'].lower() == 'member':
                members.append({
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone']
                })
    return members


@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
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
        club.save_users_to_csv()
        return redirect(url_for('coach_dashboard'))
    return render_template('add_member.html')


@app.route('/add_coach', methods=['GET', 'POST'])
def add_coach():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'Coach'  
        email = request.form['email']
        phone = request.form['phone']
        name = request.form.get('name')
        address = request.form.get('address')
        payment_preferences = request.form.get('payment_preferences')
        new_coach = User(username, password, role, email, phone, name, address, payment_preferences)
        club.users.append(new_coach)
        club.save_users_to_csv()
        return redirect(url_for('treasurer_dashboard'))
    return render_template('add_coach.html')


@app.route('/schedule_practice', methods=['GET', 'POST'])
def schedule_practice():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        save_practice_to_csv(date, time, location)  
        return redirect(url_for('treasurer_dashboard'))

    return render_template('schedule_practice.html')

@app.route('/remove_member')
def remove_member():
    return render_template('remove_member.html')

@app.route('/api/remove_member', methods=['POST'])
def api_remove_member():
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username')
            
            
            user_to_remove = next((user for user in club.users if user.username == username), None)
            if user_to_remove:
                club.users.remove(user_to_remove)
                club.save_users_to_csv()            
                return jsonify({'message': 'Member removed successfully'}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500






@app.route('/remove_coach')
def remove_coach():
    return render_template('remove_coach.html')

@app.route('/api/remove_coach', methods=['POST'])
def api_remove_coach():
    if request.method == 'POST':
        try:
            data = request.json
            username = data.get('username')
            coach_to_remove = next((coach for coach in club.users if coach.username == username and coach.role == 'Coach'), None)
            if coach_to_remove:
                club.users.remove(coach_to_remove)
                club.save_users_to_csv() 
                return jsonify({'message': 'Coach removed successfully'}), 200
            else:
                return jsonify({'error': 'Coach not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
def read_users_from_csv():
    users = []
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append({
                'username': row['username'],
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone'],
                'role': row['role']
            })
    return users



@app.route('/api/members')
def get_members():
    members = []
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['role'] == 'Member':
                members.append({
                    'username': row['username'],
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'],   
                })
    return jsonify(members)


@app.route('/api/coaches')
def api_get_coaches():
    coaches_data = [{'username': coach['username'], 'name': coach['name'], 'email': coach['email']} for coach in read_users_from_csv() if coach['role'] == 'Coach']
    return jsonify(coaches_data)

@app.route('/view_attendance')
def view_attendance():
    attendance_data = {'username1': 10, 'username2': 15}  
    return render_template('view_attendance.html', attendance_data=attendance_data)

@app.route('/treasurer_dashboard')
def treasurer_dashboard():
    return render_template('treasurer_dashboard.html')


@app.route('/member_dashboard')
def member_dashboard():

    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == session['username']:
                user_name = row['name']
                break

    return render_template('member_dashboard.html', user_name=user_name)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  
    return redirect(url_for('index'))

@app.route('/view_schedule')
def view_schedule():
    scheduled_practices = get_scheduled_practices()  
    return render_template('view_schedule.html', scheduled_practices=scheduled_practices)

@app.route('/delete_practice', methods=['POST'])
def delete_practice():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        delete_practice_from_csv(date, time, location)  
        return redirect(url_for('treasurer_dashboard'))  
    return redirect(url_for('coach_dashboard'))  


@app.route('/manage_schedule', methods=['GET', 'POST'])
def manage_schedule():
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            date = request.form.get('date')
            time = request.form.get('time')
            location = request.form.get('location')
            delete_practice_from_csv(date, time, location)
    scheduled_practices = get_scheduled_practices(skip_header=True)  
    return render_template('manage_schedule.html', scheduled_practices=scheduled_practices)


if __name__ == '__main__':
    app.run(debug=False)
