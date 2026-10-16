# AUTOMATION SCRIPTING

It is the process of writing small, targeted programs(called scripts) to execute repetitve or complex tasks automatically without requiring human intervention..

Mainly there is three part architecture to do the job:
- Trigger (what starts the script)
- Action (the core logic of the script)
- Checks (the error-handling mechanism)

# CRON-JOB

Cron-job is used to automate the running of the file, means you give the instruction in the terminal once to run the file at this time every day/week/month and it will be done and will execute until you stop it..

┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *  /path/to/command

0 17 * * 5 /usr/bin/python3 C:/Projects/Documents/automation_scripts/cleaner.py -> for every friday at 5 pm
