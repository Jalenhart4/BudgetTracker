import csv
import gspread
import datetime

# Get Current Month ->
# month_num = str(datetime.datetime.now().month)
# datetime_object = datetime.datetime.strptime(month_num, "%m")
# MONTH = datetime_object.strftime("%B")

Month = "July"
Year = datetime.datetime.now().year

# First File -> Checking Account - Second file -> Credit Account.
files = [f"WellsFargo_Checking_{Month}_{Year}.csv", f"WellsFargo_CreditCard_{Month}_{Year}.csv"]

# Commonly Occurring Bills
bills = {
    'Subscription': ["ASPEN ANKENY", "ESPN Plus", "PLAYSTATIONNETWORK"],
    'Groceries': ["HY-VEE", "ALDI", "FAREWAY", "WAL-MART"],
    'Gas': ["KWIK STAR", "CASEYS", "KUM&GO"]
}

transactions = []
for file in files:
    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:

            date = row[0]
            amount = float(row[1])
            description = row[4]
            category = 'Other'

            # Search for commonly occurring bills in each bills description
            # and assign them a category, default category = 'other'.
            for bill_type, bill_names in bills.items():
                for bill_name in bill_names:
                    if bill_name in description:
                        category = bill_type

            # Check bill description to determine Checking or Credit bill
            if "CARD 5748" in description:
                account_type = "Checking"
            else:
                account_type = "Credit"

            # Add transaction to list
            transaction = [date, amount, account_type, category, description]
            transactions.append(transaction)

for row in transactions:
    print(row)

# Connect to Google Spreadsheets 
sa = gspread.service_account()
sh = sa.open("Personal Finances")
