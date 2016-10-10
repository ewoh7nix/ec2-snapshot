# ec2-snapshot
Create a snapshot from every volumes attached to running instances and delete the old if age >= 2 weeks.

Add this script to Crontab and running every week on sunday.
0 6 * * 0 /path/to/script/ec2-snapshot.py
