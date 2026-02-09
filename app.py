import os
from flask import Flask, render_template, request, redirect, url_for, session
from groq import Groq  # make sure: pip install groq
from flask import Flask, render_template, request, redirect, url_for, session, flash


# ------------------ Flask App ------------------
app = Flask(__name__)
app.secret_key = "local_secret_key"

# ------------------ Temporary Local Storage ------------------
users = {}   # email : password

# ------------------ Groq Setup (keep key if you want AI pages later) ------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

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

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        users[email] = password

        flash("Registered successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email in users and users[email] == password:
            session["user"] = email
            flash("Login successful!", "success")
            return redirect(url_for("services"))
        else:
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

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/about")
def about():
    return render_template("about.html")



# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)
