import os
import dotenv
from functools import wraps
import redis
from pymongo import MongoClient
from flask_session import Session
from flask import Flask, request, jsonify, render_template, redirect, url_for, session

# Helper functions


def generate_mock_data():
    # Generate mock data for students

    students = [
        {
            "public_id": "STU2201350001",
            "student_info": {
                "name": "Ayush Parashar",
                "email": "2201350001@krmu.edu.in",
                "branch": "Computer Science",
                "year": "2",
                "resume": "https://example.com/michael_resume.pdf",
                "profile_pic": "https://example.com/michael_profile.jpg",
                "skills": [
                    "Matlab",
                    "Python",
                    "Machine Learning",
                ],
                "projects": [
                    {
                        "title": "Handwritten Digit Recognition",
                        "description": "A machine learning model to recognize handwritten digits",
                        "github": "https://github.com/ayushparashar/handwritten-digit-recognition",
                    },
                    {
                        "title": "Sentiment Analysis",
                        "description": "A machine learning model to analyze sentiment of text data",
                        "github": "https://github.com/ayushparashar/sentiment-analysis",
                    },
                ],
                "past_internships": [
                    {
                        "title": "Machine Learning Intern",
                        "company": "ABC Technologies",
                        "duration": "3 months",
                        "description": "Worked on developing machine learning models for image recognition",
                    },
                ],
                "social_links": {
                    "linkedin": "https://linkedin.com/in/ayushparashar",
                    "github": "https://github.com/ayushparashar",
                },
            },
            "account_info": {
                "password": "password",
                "last_login": "2024-04-10T10:15:00Z",
                "is_blocked": False,
            },
        }
    ]

    # Generate mock data for organizations

    organizations = [
        {
            "public_id": "ORG5423698754",
            "company_name": "Tech Innovations Inc.",
            "company_info": {
                "email": "info@techinnovations.com",
                "website": "https://techinnovations.com",
                "logo": "https://example.com/techinnovations_logo.png",
                "description": "Tech Innovations Inc. is a leading technology company specializing in software development and IT solutions.",
                "social_links": {
                    "linkedin": "https://linkedin.com/company/techinnovations",
                    "twitter": "https://twitter.com/techinnovations",
                    "facebook": "https://facebook.com/techinnovations",
                },
            },
            "account_info": {
                "last_login": "2024-04-10T10:00:00Z",
                "is_blocked": False,
                "is_verified": True,
                "password": "password",
            },
        },
        {
            "public_id": "ORG9876543210",
            "company_name": "Green Solutions Ltd.",
            "company_info": {
                "email": "info@greensolutions.com",
                "website": "https://greensolutions.com",
                "logo": "https://example.com/greensolutions_logo.png",
                "description": "Green Solutions Ltd. is an environmental consultancy firm dedicated to sustainable development and eco-friendly practices.",
                "social_links": {
                    "linkedin": "https://linkedin.com/company/greensolutions",
                    "twitter": "https://twitter.com/greensolutions",
                    "instagram": "https://instagram.com/greensolutions",
                },
            },
            "account_info": {
                "last_login": "2024-04-09T09:30:00Z",
                "is_blocked": False,
                "is_verified": True,
                "password": "password",
            },
        },
        {
            "public_id": "ORG1234567890",
            "company_name": "Global Health Foundation",
            "company_info": {
                "email": "info@globalhealthfoundation.org",
                "website": "https://globalhealthfoundation.org",
                "logo": "https://example.com/globalhealthfoundation_logo.png",
                "description": "Global Health Foundation is a non-profit organization committed to improving healthcare access and promoting public health initiatives worldwide.",
                "social_links": {
                    "linkedin": "https://linkedin.com/company/globalhealthfoundation",
                    "facebook": "https://facebook.com/globalhealthfoundation",
                    "youtube": "https://youtube.com/globalhealthfoundation",
                },
            },
            "account_info": {
                "last_login": "2024-04-08T11:45:00Z",
                "is_blocked": False,
                "is_verified": True,
                "password": "password",
            },
        },
    ]

    # Generate mock data for placement officers

    placement_officers = [
        {
            "public_id": "PLC2564785468",
            "employee_id": "E001",
            "employee_info": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "designation": "Placement Officer",
                "profile_pic": "https://example.com/john_smith.jpg",
            },
            "account_info": {
                "last_login": "2024-04-10T10:30:00Z",
                "is_blocked": False,
                "password": "password",
            },
        }
    ]

    # Insert mock data into MongoDB

    mongodb_cursor["students"].drop()
    mongodb_cursor["organizations"].drop()
    mongodb_cursor["placement_officers"].drop()

    mongodb_cursor["students"].insert_many(students)
    mongodb_cursor["organizations"].insert_many(organizations)
    mongodb_cursor["placement_officers"].insert_many(placement_officers)


# Load environment variables

dotenv.load_dotenv()

# MongoDB connection

mongodb_client = MongoClient(os.getenv("MONGODB_URI"))
mongodb_cursor = mongodb_client["career-portal-production"]

# Create Flask app

app = Flask(__name__)

# Configure Flask app

app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "career_portal"
app.config["SESSION_REDIS"] = redis.Redis.from_url(os.getenv("REDIS_URI"))
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize Flask app

Session(app)

# Middleware


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            "student" in session
            or "organization" in session
            or "placement_officer" in session
        ):
            return func(*args, **kwargs)
        return redirect(url_for("sign_in"))

    return wrapper


def is_not_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            "student" not in session
            and "organization" not in session
            and "placement_officer" not in session
        ):
            return func(*args, **kwargs)
        return redirect(url_for("home"))

    return wrapper


# Routes


@app.route("/", methods=["GET"])
@is_authenticated
def home():
    if "placement_officer" in session:
        return render_template("placement-officer/home.html")
    if "organization" in session:
        return render_template("organization/home.html")
    if "student" in session:
        return render_template("student/home.html")

    return redirect(url_for("sign_out"))


@app.route("/auth/sign-in", methods=["GET"])
@is_not_authenticated
def sign_in():
    return render_template("sign-in.html")


@app.route("/auth/sign-out", methods=["GET"])
@is_authenticated
def sign_out():
    session.clear()
    return redirect(url_for("sign_in"))


# API routes


@app.route("/api/v1/auth/sign-in", methods=["POST"])
def api_sign_in():
    data = request.json

    if data["user_type"] == "student":
        student = mongodb_cursor["students"].find_one(
            {"student_info.email": data["email"]}
        )
        if student and student["account_info"]["password"] == data["password"]:
            session["student"] = student
            return jsonify(
                {"status": "success", "message": "Sign in as student successful"}
            )
    elif data["user_type"] == "organization":
        organization = mongodb_cursor["organizations"].find_one(
            {"company_info.email": data["email"]}
        )
        if (
            organization
            and organization["account_info"]["password"] == data["password"]
        ):
            session["organization"] = organization
            return jsonify(
                {"status": "success", "message": "Sign in as organization successful"}
            )
    elif data["user_type"] == "placement_officer":
        placement_officer = mongodb_cursor["placement_officers"].find_one(
            {"employee_info.email": data["email"]}
        )
        if (
            placement_officer
            and placement_officer["account_info"]["password"] == data["password"]
        ):
            session["placement_officer"] = placement_officer
            return jsonify(
                {
                    "status": "success",
                    "message": "Sign in as placement officer successful",
                }
            )
    return jsonify(
        {"status": "error", "message": "The provided credentials are incorrect"}
    )


if __name__ == "__main__":
    app.run(debug=True)
