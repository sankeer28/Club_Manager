from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from club import Club, User
import secrets
import csv
import os
import ast


app = Flask(__name__, static_url_path='/static')
app.secret_key = secrets.token_hex(24) 

club = Club()
club.load_users_from_csv() 



def save_practice_to_csv(date, time, location, username):
    if not os.path.exists('scheduled_practices.csv'):
        with open('scheduled_practices.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Time', 'Location', 'Username']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    with open('scheduled_practices.csv', 'a', newline='') as csvfile:
        fieldnames = ['Date', 'Time', 'Location', 'Username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Date': date, 'Time': time, 'Location': location, 'Username': username})


def get_scheduled_practices(skip_header=True):
    scheduled_practices = []
    with open('scheduled_practices.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        if skip_header:
            next(reader)  
        for row in reader:
            if len(row) >= 4:  
                practice = {'Date': row[0], 'Time': row[1], 'Location': row[2], 'User': row[3]}
                scheduled_practices.append(practice)
    return scheduled_practices



@app.route('/manage_schedule', methods=['POST'])
def delete_practice_from_csv():
    date = request.form.get('date')
    time = request.form.get('time')
    location = request.form.get('location')

    with open('scheduled_practices.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        practices = list(reader)

    updated_practices = [practice for practice in practices if practice['Date'] != date 
                         or practice['Time'] != time or practice['Location'] != location]

    with open('scheduled_practices.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_practices)

    return redirect(url_for('treasurer_dashboard'))


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
    coach_name = None
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == session['username']:
                coach_name = row['name']
                break

    scheduled_practices = get_scheduled_practices(skip_header=True)

    member_scheduled_practices = [practice for practice in scheduled_practices if 'User' in practice and practice['User'] != 'tr']

    return render_template('coach_dashboard.html', coach_name=coach_name, scheduled_practices=member_scheduled_practices)




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

        payment_history = 0

        new_member = User(username, password, role, email, phone, name, address, payment_preferences, payment_history)

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

@app.route('/member_schedule_practice', methods=['GET', 'POST'])
def member_schedule_practice():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')

        member_name = None
        for user in club.users:
            if user.username == session['username']:
                member_name = user.name
                break
        
        save_practice_to_csv(date, time, location, member_name)  
        return render_template('member_schedule_pay.html')
    
    return render_template('member_schedule_pay.html')



@app.route('/schedule_practice', methods=['GET', 'POST'])
def schedule_practice():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        username = session.get('username', 'Treasurer')  
        save_practice_to_csv(date, time, location, username)  
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
@app.route('/members')
def view_members():
    username = session.get('username')


    members = []
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['role'] == 'Member':
                attendance_count = int(row['attendance_count'])
                payment_history = row['payment_history'].strip('[]').split(',')
                valid_payment_history = [amount.strip() for amount in payment_history if amount.strip()]
                total_paid = sum(map(float, valid_payment_history)) if valid_payment_history else 0
                payment_status = "Paid" if attendance_count * 10 <= total_paid else "Unpaid"


                members.append({
                    'username': row['username'],
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'address': row['address'],
                    'payment_status': payment_status,
                    'attendance_count': attendance_count,
                    'total_paid': total_paid
                })

    return render_template('members.html', members=members)



def update_csv(username, new_attendance_count):
    with open('users.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    for row in rows:
        if row['username'] == username:
            row['attendance_count'] = str(new_attendance_count)
            break

    with open('users.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        
        
@app.route('/increase_attendance/<username>', methods=['POST'])
def increase_attendance(username):
    try:

        with open('users.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    current_attendance_count = int(row['attendance_count'])
                    break
        new_attendance_count = current_attendance_count + 1
        update_csv(username, new_attendance_count)
        return jsonify({'message': 'Attendance increased successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrease_attendance/<username>', methods=['POST'])
def decrease_attendance(username):
    try:

        with open('users.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    current_attendance_count = int(row['attendance_count'])
                    break

        if current_attendance_count > 0:
            new_attendance_count = current_attendance_count - 1
            update_csv(username, new_attendance_count)
            return jsonify({'message': 'Attendance decreased successfully'})
        else:
            return jsonify({'error': 'Attendance count cannot be negative'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_amount_owed(attendance_count, payment_history):
    if payment_history == 0:
        return attendance_count * 10 
    else:
        total_paid = sum(int(amount) for amount in payment_history.split(','))  
        amount_owed = attendance_count * 10 - total_paid
        return max(0, amount_owed)



def update_payment_history(username, amount):
    with open('users.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in rows:
        if row['username'] == username:
            payment_history_str = row.get('payment_history', '')  
            if payment_history_str:
                payment_history_list = ast.literal_eval(payment_history_str)
            else:
                payment_history_list = []
            payment_history_list.append(amount)

            payment_history_str = "[" + ",".join(map(str, payment_history_list)) + "]"

            row['payment_history'] = payment_history_str 
            break

    with open('users.csv', 'w', newline='') as csvfile:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)





@app.route('/member_schedule_pay', methods=['GET', 'POST'])
def member_schedule_pay():
    if 'username' not in session:
        return redirect(url_for('login'))

    attendance_count = 0  
    payment_history = '0'  

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        location = request.form.get('location')
        amount = request.form.get('amount')
        update_payment_history(session['username'], amount)

        return redirect(url_for('member_dashboard'))

    amount_owed = calculate_amount_owed(attendance_count, payment_history)

    return render_template('member_schedule_pay.html', amount_owed=amount_owed, payment_history=payment_history)


@app.route('/api/other_members', methods=['GET'])
def get_other_members():
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
    scheduled_practices = get_scheduled_practices(skip_header=True)
    member_scheduled_practices = [practice for practice in scheduled_practices if 'User' in practice and practice['User'] != 'tr']
    return render_template('treasurer_dashboard.html', scheduled_practices=member_scheduled_practices)

@app.route('/download_info',methods=['GET', 'POST']) 
def download_info():
    students = []
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['role'] == 'Member':
                attendance_count = int(row['attendance_count'])
                payment_history = eval(row['payment_history']) if row['payment_history'] else []
                total_paid = sum(payment_history)
                amount_owed = max(attendance_count * 10 - total_paid, 0)
                students.append({
                    'name': row['name'],
                    'attendance_count': attendance_count,
                    'total_paid': total_paid,
                    'amount_owed': amount_owed,
                })

    csv_data = "Name,Attendance Count,Total Paid ($),Amount Owed ($)\n"
    for student in students:
        csv_data += f"{student['name']},{student['attendance_count']},{student['total_paid']},{student['amount_owed']}\n"
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=financial_information.csv"}
    )




@app.route('/finances')
def club_finances():
    students = []
    total_revenue = 0
    total_coach_expenses = 0
    total_hall_expenses = 0
    unpaid_coach_expenses = 0
    unpaid_hall_expenses = 0

    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        highest_attendance = 0
        for row in reader:
            if row['role'] == 'Member':
                attendance_count = int(row['attendance_count'])
                if attendance_count > highest_attendance:
                    highest_attendance = attendance_count

                payment_history = eval(row['payment_history']) if row['payment_history'] else []
                total_paid = sum(payment_history)
                payment_status = "Paid" if attendance_count * 10 <= total_paid else "Unpaid"
                
                total_due = attendance_count * 10
                amount_owed = max(total_due - total_paid, 0)

                students.append({
                    'name': row['name'],
                    'attendance_count': attendance_count,
                    'total_paid': total_paid,
                    'amount_owed': amount_owed,
                })

                total_revenue += total_paid
    total_coach_expenses = highest_attendance * 5
    total_hall_expenses = highest_attendance * 2
    current_profit = total_revenue - total_coach_expenses - total_hall_expenses
    unpaid_coach_expenses = max(total_coach_expenses - total_revenue, 0)
    unpaid_hall_expenses = max(total_hall_expenses - total_revenue, 0)
    return render_template('finances.html', students=students, total_revenue=total_revenue, total_coach_expenses=total_coach_expenses, total_hall_expenses=total_hall_expenses, current_profit=current_profit, unpaid_coach_expenses=unpaid_coach_expenses, unpaid_hall_expenses=unpaid_hall_expenses)


@app.route('/member_dashboard')
def member_dashboard():
    username = session.get('username')
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                user_name = row['name']
                attendance_count = int(row['attendance_count'])
                payment_history_str = row['payment_history']
                payment_history = eval(payment_history_str) if payment_history_str else []  
                total_due = attendance_count * 10
                total_paid = sum(payment_history)
                amount_owed = max(total_due - total_paid, 0)

                return render_template('member_dashboard.html', user_name=user_name, amount_owed=amount_owed)

    return render_template('error.html', message="User not found")

@app.route('/amount_owed')
def amount_owed():
    username = session.get('username')

    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:

                attendance_count = int(row['attendance_count'])
                payment_history_str = row['payment_history']
                payment_history = eval(payment_history_str) if payment_history_str else []  
                total_due = attendance_count * 10
                total_paid = sum(payment_history)
                amount_owed = max(total_due - total_paid, 0)

                return render_template('amount_owed.html', user_name=username, amount_owed=amount_owed)

    return render_template('error.html', message="Error calculating amount owed")






@app.route('/pay')
def pay():
    username = session.get('username')
    with open('users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                attendance_count = int(row['attendance_count'])
                payment_history = row['payment_history'].strip('[]').split(',')
                valid_payment_history = [amount.strip() for amount in payment_history if amount.strip()]
                paid_amount = sum(map(float, valid_payment_history)) if valid_payment_history else 0
                amount_owed = max(attendance_count * 10 - paid_amount, 0)
                return render_template('pay.html', user_name=username, amount_owed=amount_owed)



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
    app.run()
