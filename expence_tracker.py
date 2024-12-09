"""
This module handles the user's expense tracking by allowing them to input their 
expenses, save them to a CSV file, and summarize the expenses based on categories. 
It also calculates remaining budget and provides a daily budget suggestion.
This module also have used colorama library with to colores some lines on termianal and stylize them

Features:
- Allows user to input expenses with a name, amount, and category.
- Saves expenses to a CSV file for persistent storage.
- Summarizes the total spending by category.
- Calculates the remaining budget and daily budget for the rest of the month.

Limitations:
- Only supports a predefined set of categories: "Food", "Bills", "Clothing", "Medicine", "Miscellaneous".
- The budget is fixed and hardcoded.
- The program doesn't handle errors related to incorrect input types (e.g., strings for amount).
"""

from expences import Expence
import datetime
import calendar
from colorama import init, Fore, Style

# Initialize colorama (important for Windows)
init()

def main():
    # declare a file path variable for storing expences and hardcoded monthly budget
    expence_file_path = "expences.csv"
    budget = 256717.80

    # calling function to get users new expences
    new_expence = get_user_expence()

    # calling function to write new expences on csv file
    save_expence_to_file(new_expence, expence_file_path)

    # calling function to summarize expences
    summarize_expence(expence_file_path, budget)

"""
Prompts the user to enter the name, amount, and category of an expense.
Validates the category selection, ensures the amount is a positive number,
and creates an Expense object.

Returns:
Expence: A new expense object with the user's input.
"""

def get_user_expence():
    print(f"Getting user expence")      # Ask user to enter the name and amount of the expense
    expence_name = input("Enter expence name:")
    expence_amount = float(input("Enter amount spend on expence:"))

    expence_categories = [
        "Food",
        "Bills",
        "Transportation",
        "Housing/rent",
        "Health",
        "Education",
        "Technology",
        "Personal care",
        "investments/Savings",
        "Miscellaneous"
    ]

    while True:
        print(Fore.CYAN +"Select from category:" + Style.RESET_ALL )
        for i, category_name in enumerate(expence_categories):    # Display available categories using enumerate and allow user to select a category
            print(f"{i+1}, {category_name}")
        
        value_range = f"(1 - {len(expence_categories)})"    # range of list printes as 1 - 5
        selected_index = int(input(Fore.CYAN + f"Enter a category number between {value_range} :" + Style.RESET_ALL)) - 1 #-1 beacuse we added 1 for printing purpose

        # Ensure user selects a valid category, otherwise ask again
        if selected_index in range(len(expence_categories)):
            selected_category = expence_categories[selected_index]  # value at selected index is selected category
            
            # initializing a object of Expence class
            users_new_expence = Expence(
                name = expence_name, category = selected_category, amount = expence_amount
                )
            return users_new_expence
        else:
            print("Invalid Category! try again")    # loop runs till user enter valid category

"""
Saves the expense details (name, category, amount) to the specified CSV file.

Args:
new_expence (Expence): The expense object containing name, category, and amount.
expence_file_path (str): The file path where the expense data will be saved.

Returns:
None
"""

def save_expence_to_file(new_expence: Expence, expence_file_path):

    # Open the expense file in append mode and save expense details in CSV format
    with open(expence_file_path, 'a') as File:  # files can be opened and also be created if does not exsists
        File.write(f"{new_expence.name},{new_expence.category},{new_expence.amount}\n") # saves every attribute of object in comma seperated manner

"""
Reads the expense data from the file, summarizes the spending by category,
and calculates the remaining budget. It also provides a daily budget suggestion.

Args:
expence_file_path (str): The file path where expenses are stored.
budget (float): The total budget for the month.

Returns:
None
"""

def summarize_expence(expence_file_path, budget):
    print(Fore.CYAN + f"Summary of expences" + Style.RESET_ALL)
    expences : list[Expence] = []
    with open(expence_file_path, 'r') as File:  # files is opened to read only
        lines = File.readlines()  # reading each line
        for line in lines: 
            striped_lines = line.strip()    # remove extra new line characters from each line using buitlin function
            # Parse means analyzing and converting raw data into usefull structured form
            # Parse the line by splitting it at commas to extract each value (name, category, amount)
            new_expences_name, new_expences_category, new_expence_amount = striped_lines.split(",") 
            print(Style.BRIGHT + new_expences_name, new_expences_category, new_expence_amount + Style.RESET_ALL)
             
            # Convert the amount back to a float (it was stored as a string in the CSV)
            # Recreate the Expence object with the parsed data 
            expence_object = Expence(
                name = new_expences_name, category = new_expences_category, amount = float(new_expence_amount)
            )
            expences.append(expence_object)   # appending recreated expence objects into list expences

    # summarize spend amount on each category
    amount_by_category = {} # A dictionary to store tptal amount spend per category
    for expense in expences:    # key in dictionary is category name
        key = expense.category
        if key in amount_by_category:   
            amount_by_category[key] += expense.amount     # Add amount to exsisting if key already exsists in dictionary
        else:
            amount_by_category[key] = expense.amount    # Add a new entry to dictionary (category with amount)

    print(Fore.CYAN + "Amount Spent on each category" + Style.RESET_ALL)
    # Print the summarized amounts for each category
    for key, amount in amount_by_category.items():
        print(Fore.LIGHTBLUE_EX + f"    {key}:  Rs.{amount:.2f}" + Style.RESET_ALL)   # formated string where amount with upto 2 decimal places

    # Calculating total amount spent on expences
    total_spent = 0
    for ex in expences:
        total_spent += ex.amount
    print(Fore.GREEN + f"you've spent Rs.{total_spent:.2f} this month" + Style.RESET_ALL)

# Calculating remaining budget
    remaining_budget = budget - total_spent
    if remaining_budget < 0:
        print(Fore.RED + "Bad news! you've gone out of budget, stop expenditures now")
    else: 
        print(Fore.GREEN + f"You're remaining budget is: Rs.{remaining_budget:.2f}")

        # to get todays date
        today = datetime.date.today()
        
        # to get last date of month
        last_day_of_month = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
        
        # Calculate remaining days
        remaining_days = (last_day_of_month - today).days
        
        print(f"Remaining days in month: {remaining_days}")
        # calculate budget for each day with reference of remaining amount and days in month
        daily_budget = remaining_budget / remaining_days
        print(Style.BRIGHT + f"Budget per day is : Rs.{daily_budget:.2f}" + Style.RESET_ALL)

# Check if the script is being run directly and call the main function
if __name__ == "__main__": 
    main()
