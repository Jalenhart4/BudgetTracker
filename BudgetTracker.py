import csv
import gspread
import datetime
import time

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


def bill_reader(finance_files, common_bills):
    for file in finance_files:
        with open(file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for csv_row in csv_reader:

                date = csv_row[0]
                amount = float(csv_row[1])
                description = csv_row[4]
                category = 'Other'

                # Search for commonly occurring bills in each bills description
                # and assign them a category, default category = 'other'.
                for bill_type, bill_names in common_bills.items():
                    for bill_name in bill_names:
                        if bill_name in description:
                            category = bill_type

                # Check bill description to determine Checking or Credit bill
                if "CARD 5748" or "Online Transfer" or "Interest charge on purchases" in description:
                    account_type = "Checking"
                else:
                    account_type = "Credit"

                # Add transaction to list
                transaction = [date, amount, account_type, category, description]
                transactions.append(transaction)
    return transactions


if __name__ == "__main__":

    rows = bill_reader(files, bills)
    for row in rows:
        print(row)

    # Connect to Google Spreadsheets
    sa = gspread.service_account()
    sheet = sa.open("Personal Finances")
    worksheet = sheet.worksheet(f"{Month}")

    for row in rows:
        worksheet.insert_row([row[0], row[4], row[3], row[1], row[2]], 7)
        time.sleep(2)
