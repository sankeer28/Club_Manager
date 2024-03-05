# MEM: Recreation Club Membership

This project focuses on managing a small amateur club where members gather for regular practices, led by an amateur coach. The club meets weekly, and members are free to attend as they wish. However, they are required to pay for each practice session, either individually or in advance for a month. The treasurer handles the club's finances, including collecting payments, paying the coach, and covering monthly expenses like rent.

## Key Features

### 1. User Management
- **Registration:** New members can register an account with their details.
- **Login:** Members, coaches, and the treasurer can log in with their credentials.
- **Role-based Access:** Each user has specific privileges based on their role.

### 2. Practice Management
- **Scheduling:** Coaches can schedule practice sessions, specifying the date, time, and location.
- **Practice Attendance:** The system tracks member attendance to sessions.
- **Payment for Practices:** Members can schedule and pay for practice sessions through the app.

### 3. Financial Management
- **Track Finances:** The treasurer can view the club's income statement, including revenue and expenses.
- **Debt Tracking:** Outstanding debts from previous months are logged, allowing the treasurer to prioritize payments.
- **Payment Reminders:** Reminders are sent to members with outstanding payments.

## Limitations and Future Improvements

- **Payment Method Integration:** Currently, payment processing is not integrated into the application. Integrating a payment gateway would enhance user experience.
- **Automated Notifications:** Implementing automated notifications for practice reminders and payment alerts would reduce manual effort.
- **Enhanced Reporting:** Adding detailed reports on member attendance, revenue trends, and expense breakdowns would provide deeper insights for decision-making.

## Usage Instructions

1. Clone the repository to your local machine.
2. Install the necessary dependencies.
3. Run the application using Python.
4. Register or log in as a member, coach, or treasurer.
5. Explore the available features based on your role.

## Development Roadmap

### Phase 1: Basic Functionality
- Implement user registration and login.
- Allow coaches to schedule practices.
- Enable members to pay for practice sessions.

### Phase 2: Financial Management
- Introduce financial tracking for revenue and expenses.
- Implement debt tracking and payment reminders.

### Phase 3: Enhanced Features
- Integrate payment gateway for seamless transactions.
- Implement automated notifications for practice reminders and payment alerts.
