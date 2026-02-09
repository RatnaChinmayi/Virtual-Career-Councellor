🎓 Virtual Career Counsellor

The Virtual Career Counsellor is a cloud-based AI-assisted web application that provides personalized career guidance to students and job seekers. It analyzes user preferences and background information to suggest suitable career paths through an interactive interface.

📌 Problem Statement

Students often face difficulty in selecting the right career due to lack of personalized counseling and limited awareness of career options. Traditional counseling methods are not scalable and are not accessible to everyone.

💡 Solution

The Virtual Career Counsellor addresses this problem by offering:
1.Personalized career recommendations
2.Automated guidance using AI logic
3.Secure cloud-based data storage
4.Notification support for user updates
5.Scalable deployment using AWS services

🚀 Features

1.User registration and login
2.Career guidance based on interests and skills
3.AI-generated career recommendations
4.Notifications using AWS SNS
5.Secure user data storage using DynamoDB
6.Role-based secure access using AWS IAM
7.Scalable deployment using AWS ECS

🛠️ Tech Stack
Frontend
HTML
CSS
JavaScript

Backend
Python
Flask

AWS Services Used
Amazon ECS (Elastic Container Service)
Amazon DynamoDB
Amazon SNS (Simple Notification Service)
AWS IAM (Identity and Access Management)

📁 Project Structure
Virtual-Career-Councellor/
│
├── static/
│   ├── style.css
│   ├── home-bg.png
│   └── services-bg.png
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── services.html
│   ├── about.html
│   └── result.html
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Local Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/your-username/Virtual-Career-Councellor.git
cd Virtual-Career-Councellor

2️⃣ Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the application
python app.py


Application runs at:
http://127.0.0.1:5000/

☁️ Deployment on AWS ECS (Using IAM, DynamoDB & SNS)
🔐 Step 1: IAM Configuration
Create an IAM Role for ECS with the following permissions:
AmazonECSFullAccess
AmazonDynamoDBFullAccess
AmazonSNSFullAccess

Purpose of IAM:
Secure access control
Prevent hardcoding AWS credentials
Allow ECS tasks to interact with DynamoDB and SNS securely

📊 Step 2: Create DynamoDB Table
Table Name: VirtualCareerUsers
Partition Key: user_id (String)

Used to store:
User profile information
Career preferences
Generated career guidance data

📣 Step 3: Create SNS Topic
Topic Name: career-notifications
Subscription Type: Email

Used for:
User registration alerts
Career recommendation notifications

🖥️ Step 4: Launch EC2 Instance
Go to EC2 Console
Choose the Required options and then Launch instance

🔑 Step 5: Connect to EC2 Instance
Using terminal / Git Bash:
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>

🐍 Step 6: Install Required Software on EC2
Update system:
sudo yum update -y

Install Python and Git:
sudo yum install python3 git -y

Install pip:
sudo yum install python3-pip -y

📥 Step 7: Upload Project to EC2
Clone from GitHub
git clone https://github.com/your-username/Virtual-Career-Councellor.git
cd Virtual-Career-Councellor

📦 Step 8: Install Python Dependencies
pip3 install -r requirements.txt

▶️ Step 9: Run the Application on EC2
python3 app.py

Make sure Flask runs on:
app.run(host="0.0.0.0", port=5000)

🌐 Step 10: Access the Application
Open browser and visit:
http://<EC2-PUBLIC-IP>:5000

Conclusion

The Virtual Career Counsellor provides an efficient and scalable solution for personalized career guidance. By deploying the application on an AWS EC2 instance and using DynamoDB, SNS, and IAM, the system ensures secure data handling, reliable notifications, and controlled access. This project demonstrates practical use of cloud services to solve real-world problems effectively.
