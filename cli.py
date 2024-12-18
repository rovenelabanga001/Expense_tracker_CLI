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
    user_id = int(input("Enter the user's ID to be updated: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist")
        return
    user.name = input("Enter new user name (current: {user.name}): ") or user.name
    user.email = input("Enter new user email (current: {user.email})") or user.email
    session.commit()

    print(f"User ID {user_id} updated successfully")

def delete_user():
    user_id = int(input("Enter the user's ID to be deleted: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist")
        return
    session.delete(user)
    session.commit()
    print(f"User ID {user_id} deleted successfully")

def create_transaction():
    transaction_type = input("Enter transaction type (income or expense): ")
    category = input("Enter transaction category: ")
    amount = int(input("Enter amount: "))
    date = input("Enter date: ")
    user_id = int(input("Enter User ID: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with {user_id} does not exist")
        return
    transaction = Transaction(transaction_type = transaction_type, category = category, amount = amount, date = date, user_id = user_id)
    session.add(transaction)
    session.commit()
    print(f"Transaction {category}, {amount} created successfully")

def update_transaction():
    transaction_id = int(input("Enter the ID of the transaction to be updated"))
    transaction = session.get(Transaction, transaction_id)

    if not transaction:
        print(f"Transaction with ID {transaction_id} does not exist")
        return
    transaction.transaction_type = input("Enter new transaction type (income or expense): ") or transaction.transaction_id
    transaction.category = input("Enter new transaction category: ") or transaction.category
    transaction.amount = int(input("Enter new transaction amount: ")) or transaction.amount
    transaction.date = input("Enter new transaction date: ") or transaction.date
    new_user_id = input("Enter new User ID: ") or transaction.user_id
    if new_user_id:
        new_user = session.get(User, int(new_user_id))
        if not new_user:
            print(f"User with ID {new_user_id} does not exist. Skipping user update")
        else:
            transaction.user_id = new_user_id
    session.commit()
    print(f"Transaction ID {transaction_id} updated successfully")


def delete_transaction():
    transaction_id = int(input("Enter ID of the transaction to delete: "))
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        print(f"Transaction with ID {transaction_id} does not exist")
        return
    session.delete(transaction)
    session.commit()
    print(f"Transaction ID {transaction_id} deleted successfully")

def assign_transaction():
    transaction_id = int(input("Enter transaction ID: "))
    user_id = int(input("Enter the new User ID"))
    transaction = session.get(Transaction, transaction_id)
    user = session.get(User, user_id)

    if not transaction or not user:
        print("Invalid transaction ID or User ID")
        return
    transaction.user_id = user_id
    session.commit()
    print("User assigned successfully")

def list_users():
    users = session.query(User).all()
    if not users:
        print("No users found")
    for user in users:
        print(user)

def list_transactions():
    transactions = session.query(Transaction).all()
    if not transactions:
        print("No transactions found")
    for transaction in transactions:
        print(transaction)

def view_transactions_by_user():
    user_id = int(input("Enter User ID: "))
    user = session.get(User, user_id)
    if not user:
        print(f"User with ID {user_id} does not exist")
        return
    transactions = user.transactions
    if not transactions:
        print(f"No transactions found for user with ID {user_id}")
        return
    print(f"Transactions belonging to user '{user.name}' ID '{user_id}")
    for transaction in transactions:
        print(transaction)



