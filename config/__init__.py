""""
This file is used to store all the configuration variables for the application.
"""

import os
from dotenv import load_dotenv
import redis
import pymongo

load_dotenv()


class ApplicationConfig:
    """
    This class is used to store all the configuration variables for the application.
    Make sure to add the configuration variables in the .env file and load them using the dotenv library.
    """

        # Application details
    app_name = "K.R. Mangalam University Career Portal"
    app_version = "1.0.0"
    app_authors = ["Om Mishra (https://github.com/om-mishra7/)","Yash Soni (https://github.com/yash-soni7744/)","Bharat Yadav (https://github.com/bharat-yadav-11/)","Shambhavi Singh (https://github.com/Shambhavisingh123/)"]

    app_contact_email = "contact@om-mishra.com"

    # Application configuration
    secret_key = os.getenv("SECRET_KEY")
    app_debug = (
        True if os.getenv("APPLICATION_ENVIRONMENT") == "development" else False
    )
    app_host = "0.0.0.0"

    # Database configuration
    redis_client = redis.from_url(os.getenv("REDIS_URI"))
    mongodb_client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
    mongodb_database = mongodb_client["PROD"]
    
    recaptcha_secret_key = os.getenv("RECAPTCHA_SECRET_KEY")
        
    def __str__(self):
        return f"Mini Project: {self.app_name} | Version: {self.app_version} | Authors: {', '.join(self.app_authors)} | Contact Email: {self.app_contact_email}"

                

