"""
This module defines an `Expence` class to store details of an expense, 
including its name, category, and amount. The class provides a constructor 
to initialize these attributes and a representation method to display them in 
a readable format.
"""

class Expence:

    """
    A class used to represent an Expense.

    Attributes:
        name (str): The name of the expense (e.g., "Groceries").
        category (str): The category of the expense (e.g., "Food").
        amount (float): The amount spent on the expense.

    Methods:
        __repr__(): Returns a string representation of the expense.
    """
    # A Contructor to initialize new objects of Expence class 
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount
        
    """
    Return a string representation of the Expense object.

    This method is used to generate a detailed string representation
    of an Expense instance that includes its name, category, and 
    amount in the format: <Expense: name, category, Rs.amount>. 
    The amount is displayed with two decimal points for clarity.

    Returns:
        str: A string representing the Expense object in a readable format.
    """
    
    def __repr__(self):
        return f"<Expence: {self.name}, {self.category}, Rs.{self.amount:.2f} >"