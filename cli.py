import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Transaction

DATABASE_URL = " sqlite:///transactions.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized")

def create_user():
    name = input("Enter user's name: ").strip()
    email = input("Enter user's email: ").strip()

    user = User(name = name, email = email)
    session.add(user)
    session.commit()
    print(f"User {name} with ID {user.id} created successfully")

def update_user():
    user_id = int(input("Enter the user's ID to be updated"))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist")
        return
    user.name = input("Enter new user name (current: {user.name}): ") or user.name
    user.email = input("Enter new user email (current: {user.email})") or user.email
    session.commit()

    print(f"User ID {user_id} updated successfully")

