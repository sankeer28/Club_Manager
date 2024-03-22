# [Recreation Club Membership Application     ](    https://sankeer28.pythonanywhere.com/     )

This project focuses on managing a small amateur club where members gather for regular practices, led by an amateur coach. The club meets weekly, and members can attend as they wish. However, they are required to pay for each practice session. The treasurer handles the club's finances, including collecting payments, paying the coach, and covering monthly expenses like rent.
## Technologies Used
- **Python**
- **Flask**: web framework for Python
- **HTML5 and CSS**
- **JavaScript**
- **OpenStreetMap and Nominatim API**: Integrated for geocoding and reverse geocoding
- **CSV**: Data storage
- **jQuery**
- **Secure Cookies**: Implemented for session management
## Key Features

### 1. User Management
- **Registration:** New members can register an account with their details.
- **Login:** Members, coaches, and the treasurer can log in with their credentials.
- **Role-based Access:** Each user has specific privileges based on their role. 

### 2. Practice Management
- **Scheduling:** Coaches can schedule practice sessions, specifying the date, time, and location. 
- **Practice Attendance:** The system allows coaches to take member's attendance to sessions. 
- **Payment for Practices:** The app allows Members to schedule and pay for practice sessions. 

### 3. Financial Management
- **Track Finances:** The treasurer can view the club's income statement, including revenue and expenses. 
- **Debt Tracking:** Outstanding debts from previous months are logged, allowing the treasurer to prioritize payments. 
- **Payment Reminders:** Reminders can be sent to members with outstanding payments. 
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
<details>
<summary>If above does not work for you</summary>

1. download as [ZIP](https://github.com/sankeer28/Club_Manager/archive/refs/heads/main.zip)
2. Unzip the file
3. open the Club_Manager-main folder
4. open the 'Flask' folder in VSCode or Pycharm
5. click run on app.py
6. move users.csv and scheduled_practices.csv outside the Flask folder into the Club_Manager-main folder if you run into errors
</details>

## Video Demo 
https://github.com/sankeer28/Club_Manager/assets/112449287/ebf67fc2-a315-4975-8f90-def2d3b78de2


