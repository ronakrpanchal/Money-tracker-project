import sqlite3
import datetime

db_path="your database path where you want/created the database"
con = sqlite3.connect(db_path)
c = con.cursor()

def getUserInput():
    """
    Get user input for transaction details

    Returns:
    data : List,
    List containing transaction date, amount, and details 
    """
    data = []
    while True:
        if not data or input("Do you want to keep the same date? (y/n): ").lower() == 'n':
            date = int(input("Enter the date: "))
            month = int(input("Enter the month: "))
            year = int(input("Enter the year: "))
            x = datetime.datetime(year=year, month=month, day=date)
            formatted_date = x.strftime("%Y-%m-%d")
        else:
            formatted_date = data[-1][0]

        amount = float(input("Enter the amount: "))
        sr = input("Did you spend it or receive it? (s/r): ").lower()
        if sr == "s":
            description = input("Where did you spend it? ")
            amount = -amount
        elif sr == "r":
            description = input("Where did you receive it from? ")
        else:
            print("Invalid input for transaction type.")
            continue

        details = (formatted_date, amount, description)
        data.append(details)
        
        more = input("Do you want to enter another transaction? (y/n): ").lower()
        if more != 'y':
            break    
    return data 

c.execute("""
    CREATE TABLE IF NOT EXISTS YourFinance (
        Date DATE,
        Amount DECIMAL(10, 2),
        Details TEXT
    )
""")

not_exit = True
while not_exit:
    print("1. Enter data into the database.")
    print("2. Show database.")
    print("3. Show daily expenses.")
    print("4. Show Weekly Expenses.")
    print("5. Show monthly expenses.")
    print("6. Show yearly expenses.")
    print("7. Delete the database.")
    print("8. Exit.")
    print("Enter your choice:")
    choice = int(input())
    match choice:
        case 1:
            data = getUserInput()
            c.executemany("INSERT INTO YourFinance VALUES (?, ?, ?)", data)
            con.commit()
        case 2:
            c.execute("SELECT * FROM YourFinance ORDER BY Date")
            rows = c.fetchall()
            if not rows:
                print("No database found. Create one.")
            else:
                print("Date\t\tAmount\t\tDescription")
                for row in rows:
                    print(f"{row[0]}\t{row[1]}\t\t{row[2]}")
        case 3:      
            c.execute("""SELECT Date, SUM(Amount) AS Total_Amount 
                      FROM YourFinance 
                      GROUP BY Date""")
            rows = c.fetchall()
            for row in rows:
                amount = row[1]
                if amount < 0:
                    print(f"You spent ₹{-amount} on {row[0]}")
                else:
                    print(f"You received ₹{amount} on {row[0]}")
        case 4:
            c.execute("""SELECT strftime('%W',Date) as Week,
                      SUM(Amount) as Total_Amount,
                      strftime('%Y',Date) as Year 
                      FROM YourFinance 
                      GROUP BY Week 
                      ORDER BY Year""")
            rows=c.fetchall()
            amount=rows[-1][1]
            week=int(rows[-1][0])
            current_week=datetime.datetime.now().isocalendar()[1]
            if week == current_week:
                if amount < 0:
                    print(f"This week, You spent ₹{-amount}")
                else:
                    print(f"This week, You received ₹{amount}")
            elif week == current_week-1:
                if amount < 0:
                    print(f"Last week, You spent ₹{-amount}")
                else:
                    print(f"Last week, You received ₹{amount}") 
            else:
                print("No Expenses for last week.")   
        case 5:
            c.execute("""SELECT STRFTIME('%Y-%m',Date) as Month, 
                         SUM(Amount) as Total_Amount 
                         FROM YourFinance 
                         GROUP BY MONTH 
                         ORDER BY MONTH""")
            rows = c.fetchall()
            for row in rows:
                month_num = int(row[0].split("-")[1])
                year=int(row[0].split("-")[0])
                month_name = datetime.date(1900, month_num, 1).strftime('%B')
                amount = row[1]
                if amount < 0:
                    print(f"You spent ₹{-amount} in {month_name},{year}")
                else:
                    print(f"You received ₹{amount} in {month_name},{year}")
        case 6:
            c.execute("SELECT strftime('%Y',Date) as Year, SUM(Amount) AS Total_Amount FROM YourFinance GROUP BY Year ORDER BY Year")
            rows=c.fetchall()
            for row in rows:
                year=int(row[0])
                amount=row[1]
                if amount < 0:
                    print(f"You spent ₹{-amount} in {year}")
                else:
                    print(f"You recieved ₹{amount} in {year}")
        case 7:
            c.execute("DROP TABLE IF EXISTS YourFinance")
            con.commit()
            print("Database deleted.")
        case 8:
            not_exit = False
            print("Thank you for using this program.")
        case _:
            print("Invalid choice.")
            
con.commit()
con.close()