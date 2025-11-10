import csv
from collections import defaultdict
from datetime import datetime

FILENAME = "transactions.csv"

def load_transactions():
    transactions = []
    try:
        with open(FILENAME, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['amount'] = float(row['amount'])
                row['date'] = datetime.strptime(row['date'], "%Y-%m-%d").date()
                transactions.append(row)
    except FileNotFoundError:
        pass
    return transactions

def save_transactions(transactions):
    with open(FILENAME, 'w', newline='') as csvfile:
        fieldnames = ['amount', 'category', 'type', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in transactions:
            writer.writerow({
                'amount': t['amount'],
                'category': t['category'],
                'type': t['type'],
                'date': t['date'].strftime("%Y-%m-%d")
            })

def add_transaction(transactions):
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.\n")
        return
    t_type = input("Type (Income/Expense): ").strip().capitalize()
    if t_type not in ["Income", "Expense"]:
        print("Invalid type. Defaulting to Expense.\n")
        t_type = "Expense"
    category = input("Category: ").strip().title() or "Misc"
    date_input = input("Date (YYYY-MM-DD) or leave blank for today: ").strip()
    if date_input:
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Using today.\n")
            date = datetime.today().date()
    else:
        date = datetime.today().date()
    transactions.append({"amount": amount, "type": t_type, "category": category, "date": date})
    save_transactions(transactions)
    print("Transaction added!\n")

def view_transactions(transactions):
    if not transactions:
        print("No transactions yet.\n")
        return
    print("\nTransactions:")
    for i, t in enumerate(transactions, start=1):
        print(f"{i}. {t['date']} - {t['type']} - {t['category']} - ${t['amount']:.2f}")
    print()

def generate_report(transactions):
    if not transactions:
        print("No transactions to report.\n")
        return
    total_income = sum(t['amount'] for t in transactions if t['type'] == "Income")
    total_expense = sum(t['amount'] for t in transactions if t['type'] == "Expense")
    net = total_income - total_expense

    category_totals = defaultdict(float)
    for t in transactions:
        if t['type'] == "Expense":
            category_totals[t['category']] += t['amount']
    
    top_category = max(category_totals, key=category_totals.get, default="None")

    print("\n--- Financial Report ---")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expense:.2f}")
    print(f"Net Balance: ${net:.2f}")
    print(f"Top Spending Category: {top_category}")
    print("------------------------\n")

def main():
    transactions = load_transactions()
    while True:
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Choose (1-4): ").strip()
        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            generate_report(transactions)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
