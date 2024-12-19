import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Transaction
from datetime import datetime, date
from datetime import datetime, date

DATABASE_URL = "sqlite:///transactions.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind = engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    print("Database initialized")

def validate_date(date_str):
    """
    Validates if the input date string is of YYYY-MM-DD format
    Returns a valid date string or None if invalid
    """
    try:
        valid_date = datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

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
    user.name = input(f"Enter new user name (current: {user.name}): ") or user.name
    user.email = input(f"Enter new user email (current: {user.email})") or user.email
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
  
def search_user_by_name():
    user_name = input("Enter the name of the user to search: ").strip()
    users = session.query(User).filter(User.name.ilike(f"%{user_name}%")).all()
    if users:
        print(f"Users matching '{user_name}'")
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
    else:
        print(f"No users found matching '{user_name}'")

def search_user_by_id():
    try:
        user_id = int(input("Enter the user ID to search: ").strip())
    except ValueError:
        print("Invalid User ID. Please enter a valid integer")
        return

    user = session.get(User, user_id)
    if user:
        print(f"User found: ID :'{user.id}', Name: '{user.name}', Email :'{user.email}'")
    else:
        print(f"No user found with ID {user_id}")
def create_transaction():
    transaction_type = input("Enter transaction type (income or expense): ").strip()
    category = input("Enter transaction category: ").strip()
    
    # Validate amount input
    while True:
        try:
            amount = int(input("Enter transaction amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a valid integer.")

    # Validate date input
    while True:
        input_date = input("Enter transaction date (YYYY-MM-DD) [default: today]: ").strip()
        if not input_date:
            transaction_date = date.today()  # Default to today's date
            break
        try:
            transaction_date = datetime.strptime(input_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")

    # Validate user ID input
    while True:
        try:
            user_id = int(input("Enter User ID: "))
            break
        except ValueError:
            print("Invalid User ID. Please enter a valid integer.")

    # Create and commit the transaction
    transaction = Transaction(
        transaction_type=transaction_type,
        category=category,
        amount=amount,
        date=transaction_date,  # Ensure this is a datetime.date object
        user_id=user_id,
    )
    session.add(transaction)
    session.commit()
    print(f"Transaction created successfully with ID: {transaction.id}")


from datetime import datetime

def update_transaction():
    try:
        transaction_id = int(input("Enter the ID of the transaction to be updated: ").strip())
    except ValueError:
        print("Invalid ID, please enter a valid integer.")
        return
    
    transaction = session.get(Transaction, transaction_id)

    if not transaction:
        print(f"Transaction with ID {transaction_id} does not exist.")
        return

    print(f"Updating Transaction ID {transaction_id}. Leave a field blank to keep the current value.")
    
    # Update transaction type
    new_transaction_type = input(f"Enter new transaction type (current: {transaction.transaction_type}): ").strip()
    if new_transaction_type:
        transaction.transaction_type = new_transaction_type

    # Update category
    new_category = input(f"Enter new transaction category (current: {transaction.category}): ").strip()
    if new_category:
        transaction.category = new_category

    # Update amount
    new_amount = input(f"Enter new transaction amount (current: {transaction.amount}): ").strip()
    if new_amount:
        try:
            transaction.amount = int(new_amount)
        except ValueError:
            print("Invalid amount entered. Keeping the current value.")

    # Update date
    while True:
        new_date = input(f"Enter new transaction date (current: {transaction.date}, format YYYY-MM-DD): ").strip()
        if not new_date:
            break
        try:
            transaction.date = datetime.strptime(new_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")

    # Update user ID
    new_user_id = input(f"Enter new User ID (current: {transaction.user_id}): ").strip()
    if new_user_id:
        try:
            new_user_id = int(new_user_id)
            new_user = session.get(User, new_user_id)
            if new_user:
                transaction.user_id = new_user_id
            else:
                print(f"User with ID {new_user_id} does not exist. Skipping user update.")
        except ValueError:
            print("Invalid User ID entered. Keeping the current value.")

    try:
        session.commit()
        print(f"Transaction ID {transaction_id} updated successfully.")
    except Exception as e:
        session.rollback()
        print(f"Failed to update transaction: {e}")


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

    if not transaction:
        print(f"Transaction with ID {transaction_id} does not exist.")
        return
    if not user:
        print(f"User with ID {user_id} does not exist.")
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
def search_transaction_by_type():
    transaction_type = input("Enter transaction type (income or expense): ").strip().lower()
    if transaction_type not in ["income", "expense"]:
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
        return

    transaction = session.query(Transaction).filter_by(transaction_type = transaction_type).all()
    if transaction:
        print(f"Transactions of type '{transaction_type}'")
        for t in transaction:
            print(f"ID : {t.id}, Category: {t.category}, Amount: {t.amount}, Date: {t.date} User ID: {t.user_id}")
    else:
        print(f"No transactions of type '{transaction_type}' found.")
def search_transaction_by_id():
    try:
        transaction_id = int(input("Enter the transaction ID to search: ").strip())
    except ValueError:
        print("Invalid transaction ID. Please enter a valid integer")
        return

    transaction = session.get(Transaction, transaction_id)
    if transaction:
        print(f"Transaction found: ID: {transaction.id}, Type:{transaction.transaction_type}, "
              f"Category: {transaction.category}, Amount: {transaction.amount}, "
              f"Date: {transaction.date}, User ID: {transaction.user_id}")
    else:
        print(f"No transaction found with ID {transaction_id}")

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
    print(f"Transactions belonging to user '{user.name}' ID '{user_id}'")
    for transaction in transactions:
        print(transaction)

def transaction_summary():
    try:
        user_id = int(input("Enter the user Id to view their transaction summary: "))
    except ValueError:
        print("Invalid User ID. Please Enter a valid integer")
        return

    user = session.get(User, user_id)
    if not user:
        print(f"No user found with ID {user_id}")
        return
    print(f"Transaction summary for User: '{user.name}', ID :'{user.id}'")

    transactions = session.query(Transaction).filter_by(user_id = user_id).all()
    if not transactions:
        print(f"No transactions found for User ID {user_id}")
        return

    income_sum = sum(t.amount for t in transactions if t.transaction_type == "income")
    expense_sum = sum(t.amount for t in transactions if t.transaction_type == "expense")
    net_balance = income_sum - expense_sum

    print("\nTransactions:")
    for t in transactions:
        print(f"ID: '{t.id}', Type: '{t.transaction_type}', Category: '{t.category}' "
              f"Amount: '{t.amount}', Date: '{t.date}'")

    print("\nSummary:")
    print(f"Total income : {income_sum}")
    print(f"Total expense: {expense_sum}")
    print(f"Net balance: {net_balance}")

def main_menu():
    while True:
        print("\nWelcome to the application. What would you like to do?")
        print("1.  Create User")
        print("2.  Update User")
        print("3.  Delete User")
        print("4.  Create Transaction")
        print("5.  Update Transaction")
        print("6.  Delete Transaction")
        print("7.  Assign Transaction to User")
        print("8.  Search for user by name")
        print("9.  Search for user by ID")
        print("10. List Users")
        print("11. List Transactions")
        print("12. View Transactions by User")
        print("13. Search for transactions by type")
        print("14. Search for transaction by ID")
        print("15. View user's transaction summary")
        print("16. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            update_user()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            create_transaction()
        elif choice == "5":
            update_transaction()
        elif choice == "6":
            delete_transaction()
        elif choice == "7":
            assign_transaction()
        elif choice == "8":
            search_user_by_name()
        elif choice == "9":
            search_user_by_id()
        elif choice == "10":
            list_users()
        elif choice == "11":
            list_transactions()
        elif choice == "12":
            view_transactions_by_user()
        elif choice == "13":
            search_transaction_by_type()
        elif choice == "14":
            search_transaction_by_id()
        elif choice == "15":
            transaction_summary()
        elif choice == "16":
            print("Exiting ...")
            session.close()
            sys.exit()
        else:
            print("Invalid choice please try again")


if __name__ == "__main__":
    init_db()
    main_menu()



