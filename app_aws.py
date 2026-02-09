from flask import Flask, render_template, request, redirect, url_for, session, flash
from groq import Groq
import boto3
import bcrypt
import os
from botocore.exceptions import ClientError

# ------------------ Flask App ------------------
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # In production, use a secure method to set this

# ------------------ AWS CONFIG (IAM ROLE USED) ------------------
REGION = "us-east-1"

dynamodb = boto3.resource("dynamodb", region_name=REGION)
sns = boto3.client("sns", region_name=REGION)

# ------------------ Groq Setup ------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set this in your environment variables
client = Groq(api_key=GROQ_API_KEY)

users_table = dynamodb.Table("VirtualCareerUsers")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:677276085504:aws_capstone_topic"

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Replace with your SNS topic ARN

def send_notification(subject, message):
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except ClientError as e:
        print("Error sending SNS notification: {e}")


# ------------------ AI FUNCTIONS ------------------
def generate_course_recommendation(user_preferences):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "system",
            "content": f"Recommend courses based on: {user_preferences}"
        }]
    )
    return response.choices[0].message.content


def generate_career_path(career_name):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "system",
            "content": f"Generate career path for {career_name}"
        }]
    )
    return response.choices[0].message.content


def generate_job_market_trends(career_name):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "system",
            "content": f"Provide job market trends for {career_name}"
        }]
    )
    return response.choices[0].message.content


# ------------------ SNS HELPER ------------------
def send_sns_alert(message):
    try:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="Virtual Career Counsellor Alert"
        )
    except Exception as e:
        print("SNS error:", e)


# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        try:
            users_table.put_item(
                Item={
                    "userId": email,
                    "password": hashed_password
                },
                ConditionExpression="attribute_not_exists(email)"
            )

            send_notification("New User Registered", f"New user registered: {email}")

            flash("Registered successfully! Please login.", "success")
            return redirect(url_for("login"))

        except ClientError:
            flash("User already exists", "error")
            return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        response = users_table.get_item(
            Key={"userId": email}   # ✅ MUST match DynamoDB key name
        )

        user = response.get("Item")

        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):
            session["user"] = email
            flash("Login successful!", "success")
            return redirect(url_for("services"))

        flash("Invalid email or password", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/services")
def services():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("services.html")


@app.route("/generate_recommendations", methods=["POST"])
def generate_recommendations():
    preferences = request.form.get("preferences")
    result = generate_course_recommendation(preferences)
    return render_template("show_recommendations.html", recommendations=result)


@app.route("/generate_career_path", methods=["POST"])
def generate_career_path_route():
    career = request.form.get("career_name")
    result = generate_career_path(career)
    return render_template("show_career_path.html", career_path=result)


@app.route("/job_market_trends", methods=["POST"])
def job_market_trends_route():
    career = request.form.get("career_name")
    result = generate_job_market_trends(career)
    return render_template("show_job_market_trends.html", job_market_trends=result)


@app.route("/about")
def about():
    return render_template("about.html")


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response


# ------------------ RUN (EC2 READY) ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


