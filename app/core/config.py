# app/core/config.py
import os

# Basic configuration variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./secure_pass.db")
RAW_DATA_DIR = os.path.join(os.getcwd(), "data", "raw")
CLEANED_DATA_DIR = os.path.join(os.getcwd(), "data", "cleaned")
TRASH_DATA_DIR = os.path.join(os.getcwd(), "data", "trash")

# You can add more configuration settings as needed
