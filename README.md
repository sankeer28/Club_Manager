# Recreation Club Membership Application

This project focuses on managing a small amateur club where members gather for regular practices, led by an amateur coach. The club meets weekly, and members can attend as they wish. However, they are required to pay for each practice session, either individually or in advance for a month. The treasurer handles the club's finances, including collecting payments, paying the coach, and covering monthly expenses like rent.

## Key Features

### 1. User Management
- **Registration:** New members can register an account with their details.✅
- **Login:** Members, coaches, and the treasurer can log in with their credentials.✅
- **Role-based Access:** Each user has specific privileges based on their role. ✅

### 2. Practice Management
- **Scheduling:** Coaches can schedule practice sessions, specifying the date, time, and location. ✅
- **Practice Attendance:** The system allows coaches to take member's attendance to sessions. ✅
- **Payment for Practices:** The app allows Members to schedule and pay for practice sessions. ✅

### 3. Financial Management
- **Track Finances:** The treasurer can view the club's income statement, including revenue and expenses. ✅
- **Debt Tracking:** Outstanding debts from previous months are logged, allowing the treasurer to prioritize payments. ✅
- **Payment Reminders:** Reminders can be sent to members with outstanding payments. ✅
### Try out the [Live Demo](https://sankeer28.pythonanywhere.com/)
## Usage Instructions
- You are expected to have a relatively new version of Python and Git installed
1. Clone the repository to your local machine.
```
 git clone https://github.com/sankeer28/Club_Manager.git
 cd Club_Manager
```
2. Install the necessary dependencies. Was tested on Python 3.11.6, Should work on modern Python versions
```
 pip install Flask
```
4. Open the Flask folder
```
 cd Flask
```
3. Run the application 
```
 flask run
```
4. You will get a message like ``` * Running on http://127.0.0.1:5000 ``` ctrl + click on it or copy-paste into browser. Mac users may encounter issues where AirPlay Receiver is using port 5000, there are tutorials online on how to fix.
5. Register or log in as a member, coach, or treasurer.
6. Explore the available features based on your role.
- If this does not work for you, download as [ZIP](https://github.com/sankeer28/Club_Manager/archive/refs/heads/main.zip), Unzip, open the Club_Manager-main folder, then open the 'Flask' folder in VSCode or Pycharm and click run on app.py, also move users.csv and scheduled_practices.csv outside the Flask folder into the Club_Manager-main folder if you run into errors.


### Working Features:
- set schedule uses OpenStreetMap and Nominatim API to turn coordinates from clicking on the map to a named location
- coach can add and delete members
- member, coach and treasurer can register accounts and logout
- The treasurer can schedule practice and delete practice
- member can view scheduled practices
- The treasurer can add a new coach and delete a coach
- when a coach or member is removed they can get an optional email telling them they have been removed from the club
- Dashboard for coach and member has a greeting with their name 
- when member or treasurer schedules practice it saves to csv that says who scheduled the practice
- coach and treasurer dashboard has a container at the top of their dashboard saying which members scheduled a practice (in-app notification)
- members can now pay the amount they owe based on attendance
- treasurer and coach can see a table with members and sort based on if they paid or not and attendance
- in the list of members, if they have unpaid, coach or treasurer can send them email reminding them
- Treasurer can see total revenue, coach expenses, hall expenses, and profit can also see how much each member paid and how much they owe
