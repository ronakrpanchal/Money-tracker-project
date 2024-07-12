import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3
import datetime

#Credentials for sending mail through smtplib.
my_email = "Sender's email"
password = "your_password"
email="Reciever's email"

#Creating a database.
db_path="your database path where you want/created the database"
con = sqlite3.connect(db_path)
c=con.cursor()

#Calulate the last week's starting and ending dates
today=datetime.datetime.today()
sow=today-datetime.timedelta(days=today.weekday(),weeks=1)
eow=sow+datetime.timedelta(days=6)
sow=sow.strftime("%Y-%m-%d")
eow=eow.strftime("%Y-%m-%d")

#Getting the data from the database
c.execute("""
          SELECT DATE , AMOUNT , DETAILS 
          FROM YOURFINANCE 
          WHERE DATE BETWEEN ? AND ?
          ORDER BY DATE
          """,(sow,eow))

#fetches rows from the table 
rows=c.fetchall()

#fetches the data from the second last week
sotw=today-datetime.timedelta(days=today.weekday(),weeks=2)
eotw=sotw+datetime.timedelta(days=6)
sotw=sotw.strftime("%Y-%m-%d")
eotw=eotw.strftime("%Y-%m-%d")

c.execute("""
          SELECT DATE , AMOUNT , DETAILS 
          FROM YOURFINANCE 
          WHERE DATE BETWEEN ? AND ?
          ORDER BY DATE
          """,(sotw,eotw))

sweek=c.fetchall()

#Calculating the total amount spend or recieved during second week
total_amount_2=0
for i in range(len(sweek)):
    total_amount_2+=sweek[i][1]

#creates a table in html format and adds relevant info in the table
if rows:
    report = """
    <html>
    <head>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
    </head>
    <body>
    <h2>Last Week's Budget Report</h2>
    <table>
    <tr>
        <th>Date</th>
        <th>Amount</th>
        <th>Description</th>
    </tr>
    """
    for row in rows:
        date = row[0]
        amount = row[1]
        description = row[2]
        amount_display = f"₹{-amount}" if amount < 0 else f"₹{amount}"
        amount_style = "color:red;" if amount < 0 else "color:green;"
        report += f"""
        <tr>
            <td>{date}</td>
            <td style="{amount_style}">{amount_display}</td>
            <td>{description}</td>
        </tr>
        """
    total_amount = 0
    for a in range(len(rows)):
        total_amount+=rows[a][1]
    total_amount_display = f"₹{-total_amount}" if total_amount < 0 else f"₹{total_amount}"
    total_amount_style = "color:red;" if total_amount < 0 else "color:green;"
    sr="spend" if total_amount < 0 else "recieved"
    emoji=""
    if total_amount > 0:
        emoji="🤑"
    elif total_amount == 0:
        emoji="😌"
    else:
        emoji="🙂‍↕️"
    ud=''
    ml=''
    if total_amount<0 and total_amount_2<0:
        total_amount=-total_amount
        total_amount_2=-total_amount_2
        if total_amount>total_amount_2:
            pr=(total_amount-total_amount_2)/total_amount
            ud='🔺'
            ml='more'
        elif total_amount_2>total_amount:
            pr=(total_amount_2-total_amount)/total_amount_2
            ud='🔻'
            ml='less'
    elif total_amount>0 and total_amount_2>0:
        if total_amount>total_amount_2:
            pr=(total_amount-total_amount_2)/total_amount
            ud='🔺'
            ml='more'
        elif total_amount_2>total_amount:
            pr=(total_amount_2-total_amount)/total_amount_2
            ud='🔻'
            ml='less'
    report += f"""
    </table>
    <p style="{total_amount_style}">You {sr} {total_amount_display} last week {emoji}.
    {round(pr*100,2)}% {ud} {ml} than last week
    </p>
    </body>
    </html>
    """
else:
    report = """
    <html>
    <body>
    <h2>Last Week's Budget Report</h2>
    <p>No transactions found for the last week.</p>
    </body>
    </html>
    """

#Sending mail through smtplib.
try:
    with smtplib.SMTP("smtp.gmail.com",port=587) as server:
        server.starttls()
        server.login(user=my_email,password=password)
        msg=MIMEMultipart()
        msg['From']=my_email
        msg['To']=email
        msg['Subject']="Last Week's Expense Report!"
        msg.attach(MIMEText(report,'html'))
        server.send_message(msg)
        print("Email sent successfully")
except Exception as e:
    print("Something went wrong")