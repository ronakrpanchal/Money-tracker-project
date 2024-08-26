# Money Tracker Project

The Python project that manages your daily finances using sqlite3 library.This project demonstrates the use of SQL in python.

There are 2 files:
1. main.py - handles the database and gives various budget report daily , weekly , monthly , etc
2. send_weekly_fin_report - it is a script that is used to send mail using smtp library that contains weekly expense report. 

### Usage 

```bash
python3 main.py
```
```bash
python3 send_weekly_fin_report.py
```

You can store your daily finances in your database and can schedule your script either with crontab or pythonanywhere

1. Using crontab

In your terminal 

```bash
crontab -e
```
vi editor will be opened

we can schedule the task in the following way:- 
```bash
* * * * * path_to_your_python3 path_to_your_script
```

Here’s a breakdown of the schedule syntax:

	•	* * * * *: This represents the time schedule. The five fields are:
	•	Minute (0 - 59)
	•	Hour (0 - 23)
	•	Day of the Month (1 - 31)
	•	Month (1 - 12)
	•	Day of the Week (0 - 7) (Sunday can be 0 or 7)

2. Using pythonanywhere

first upload the required file such as your python file and database file. 
go to tasks

[![temp-Image-H6-RHk-G.avif](https://i.postimg.cc/Kv86Q26p/temp-Image-H6-RHk-G.avif)](https://postimg.cc/Rq2pVjVw)

time is in UTC so keep it in mind.
add the path where you have uploaded your python script.
it will run your python file at a particular time.
