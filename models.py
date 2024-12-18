from sqlalchemy import Column, Integer, String, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship, declarative_base
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key = True)
    name = Column(String(), nullable = False)
    email = Column(String(), unique = True, nullable = False)

    transactions = relationship("Transaction", back_populates = "user")

    def __init__(self, name, email):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Name must be a non empty string")
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Email must be a valid string containing '@'")

        self.name = name
        self.email = email

    def __repr__(self):
        return f"User(id: '{self.id}', name: '{self.name}', email:'{self.email}')"

class Transaction(Base):

    __tablename__ = 'transactions'
    
    id = Column(Integer(), primary_key = True)
    transaction_type = Column(String(), nullable = False)
    category = Column(String(), nullable = False)
    amount = Column(Integer(), nullable = False)
    date = Column(Date, default = date.today)

    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship("User", back_populates = "transactions")

    __table_args__ = (
        CheckConstraint("amount > 0", name="positive_amount"),  # Ensures positive amount
    )

    def __init__(self, transaction_type, category, amount, date = None):
        if not transaction_type or not isinstance(transaction_type, str):
            raise ValueError("Transaction type must be a non empty string")
        if transaction_type not in ["income", "expense"]:
            raise ValueError("Transaction type must be either 'income' or 'expense' ")
        if not category or not isinstance(category, str):
            raise ValueError("Category must be a non empty string")
        if not isinstance (amount, int):
            raise ValueError("Amount must be an integer")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")


        self.transaction_type = transaction_type
        self.category = category
        self.amount = amount
        self.date = date or date.today() #defaults to today if date is not provided

    def __repr__(self):
        return (f"Transaction(id='{self.id}', "
                f"transaction_type='{self.transaction_type}', "
                f"category='{self.category}', "
                f"amount={self.amount}, "
                f"date='{self.date}')")
