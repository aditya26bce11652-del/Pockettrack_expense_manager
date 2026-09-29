import sqlite3
import csv
from datetime import datetime

# pockettrack expense manager script
# todo: add authentication later?
DB_FILE = "pockettrack.db"

def init_db():
    # create table if it doesn't exist
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        payment TEXT
    )
    """)
    conn.commit()
    conn.close()

# print(datetime.now()) # debug

def add_expense():
    print("\n--- ADD NEW EXPENSE ---")

    # handle date input
    d = input("Date (YYYY-MM-DD, Enter for today): ").strip()
    if d == "" or d == None:
        d = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(d, "%Y-%m-%d")
        except:
            print("Invalid date format! Using today's date instead.")
            d = datetime.now().strftime("%Y-%m-%d")

    cat = input("Category (Food/Travel/Bills/etc): ").strip()
    if not cat:
        cat = "Other"

    desc = input("Description: ").strip()

    # get valid amount loop
    while True:
        amt_str = input("Amount: ")
        try:
            amt = float(amt_str)
            if amt <= 0:
                print("Amount must be greater than 0!")
                continue
            break
        except:
            print("Please enter a valid number...")

    pay_method = input("Payment method (Cash/Card/UPI): ").strip()
    if pay_method == "":
        pay_method = "Cash"

    # save record
    con = sqlite3.connect(DB_FILE)
    c = con.cursor()
    c.execute(
        "INSERT INTO expenses (date, category, description, amount, payment) VALUES (?, ?, ?, ?, ?)",
        (d, cat, desc, amt, pay_method)
    )
    con.commit()
    con.close()
    print(">> Expense saved successfully!")

def display_expenses(data=None):
    if data is None:
        con = sqlite3.connect(DB_FILE)
        c = con.cursor()
        c.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")
        rows = c.fetchall()
        con.close()
    else:
        rows = data

    if len(rows) == 0:
        print("\n*** No expenses found ***")
        return

    print("\n" + "="*70)
    print("ID   DATE         CATEGORY        DESCRIPTION             AMOUNT")
    print("="*70)
    for r in rows:
        # print(r) # debug print
        eid = str(r[0]).ljust(4)
        edate = str(r[1]).ljust(12)
        ecat = (str(r[2])[:12]).ljust(15)
        edesc = (str(r[3])[:20]).ljust(23)
        eamt = "Rs." + str(r[4])
        print(eid + " " + edate + " " + ecat + " " + edesc + " " + eamt)
    print("="*70)

def search_expense():
    q = input("\nEnter category or description keyword: ").strip()
    if q == "":
        print("Empty search string!")
        return

    cx = sqlite3.connect(DB_FILE)
    cur = cx.cursor()
    # SQL query for search
    cur.execute(
        "SELECT * FROM expenses WHERE category LIKE '%" + q + "%' OR description LIKE '%" + q + "%' ORDER BY date DESC"
    )
    results = cur.fetchall()
    cx.close()

    display_expenses(results)

def update_expense():
    display_expenses()
    val = input("\nEnter ID of expense to edit: ")
    try:
        e_id = int(val)
    except:
        print("Invalid ID entered.")
        return

    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = " + str(e_id))
    item = cursor.fetchone()

    if item == None:
        print("ID not found in database.")
        db.close()
        return

    print("Leave empty to keep old value:")
    new_d = input("Date [" + str(item[1]) + "]: ").strip()
    if not new_d: 
        new_d = item[1]

    new_cat = input("Category [" + str(item[2]) + "]: ").strip() or item[2]
    new_desc = input("Description [" + str(item[3]) + "]: ").strip() or item[3]
    new_pay = input("Payment [" + str(item[5]) + "]: ").strip() or item[5]

    amt_in = input("Amount [" + str(item[4]) + "]: ").strip()
    if amt_in != "":
        try:
            new_amt = float(amt_in)
            if new_amt <= 0:
                print("Invalid amount.")
                db.close()
                return
        except Exception as err:
            print("Bad number format.")
            db.close()
            return
    else:
        new_amt = item[4]

    cursor.execute("""
        UPDATE expenses
        SET date=?, category=?, description=?, amount=?, payment=?
        WHERE id=?
    """, (new_d, new_cat, new_desc, new_amt, new_pay, e_id))

    db.commit()
    db.close()
    print(">> Item updated successfully!")

def delete_stuff():
    display_expenses()
    try:
        del_id = int(input("\nEnter ID to delete: "))
    except:
        print("ID must be an integer.")
        return

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE id=?", (del_id,))
    target = cur.fetchone()

    if target is None:
        print("Record does not exist.")
        conn.close()
        return

    ans = input("Are you sure you want to delete '%s'? (y/n): " % target[3])
    if ans.lower() == 'y' or ans.lower() == 'yes':
        cur.execute("DELETE FROM expenses WHERE id=?", (del_id,))
        conn.commit()
        print("Deleted!")
    else:
        print("Cancelled deletion.")
    conn.close()

def get_reports():
    print("\n---------------- SPENDING REPORT ----------------")
    c = sqlite3.connect(DB_FILE)
    cur = c.cursor()
    cur.execute("SELECT SUM(amount), COUNT(*) FROM expenses")
    total_val, total_count = cur.fetchone()

    if total_val == None:
        total_val = 0

    print("Total spent: Rs." + str(round(total_val, 2)))
    print("Total records:", total_count)

    cur.execute("""
        SELECT category, SUM(amount), COUNT(*)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)
    cat_summary = cur.fetchall()

    if len(cat_summary) > 0:
        print("\nBreakdown by Category:")
        for row in cat_summary:
            print(f" -> {row[0]}: Rs.{round(row[1], 2)} ({row[2]} entries)")
    else:
        print("No expenses recorded yet.")
    c.close()

def export_csv_data():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY date DESC")
    all_rows = cur.fetchall()
    conn.close()

    if not all_rows:
        print("No data available to export.")
        return

    out_file = "pockettrack_expenses.csv"
    f = open(out_file, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(["ID", "Date", "Category", "Description", "Amount", "Payment"])
    for r in all_rows:
        writer.writerow(r)
    f.close()
    print("Export completed -> " + out_file)

def main():
    init_db()
    while True:
        print("\n" + "="*40)
        print("    *** POCKETTRACK EXPENSE TRACKER ***")
        print("="*40)
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expense")
        print("4. Edit Expense")
        print("5. Delete Expense")
        print("6. Spending Summary")
        print("7. Export to CSV")
        print("8. Exit")
        print("="*40)

        opt = input("Select option (1-8): ").strip()

        if opt == "1":
            add_expense()
        elif opt == "2":
            display_expenses()
        elif opt == "3":
            search_expense()
        elif opt == "4":
            update_expense()
        elif opt == "5":
            delete_stuff()
        elif opt == "6":
            get_reports()
        elif opt == "7":
            export_csv_data()
        elif opt == "8":
            print("Exiting app. Goodbye!")
            break
        else:
            print("Invalid selection! Try again.")

if __name__ == "__main__":
    main()
