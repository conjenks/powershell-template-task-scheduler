# to be run as a service, and execute the jobs in jobs.db at their specified run times
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import sqlite3
import helper
import jobs
from time import time

job_dict = {"beginEmailForwarding": jobs.beginEmailForwarding, "beginEmailForwardingONLY": jobs.beginEmailForwardingONLY, "endEmailForwarding": jobs.endEmailForwarding}


def main():
	conn = sqlite3.connect('jobs.db')
	writeToLogs("program started\n")

	scheduler = BackgroundScheduler()
	scheduler.start()

	start = time()
	while True:
		if (time() - start) > 10:
			refresh(conn, scheduler)
			start = time()
		continue


def refresh(conn, scheduler):
	c = conn.cursor()
	c.execute("SELECT * FROM jobs")
	for row in c:
		if row[4] == 0:  # if job is not scheduled
			writeToLogs(getJobDescription(row))
			schedule(row, scheduler)
			helper.setJobScheduled(c, row[0])
			conn.commit()


def schedule(row, scheduler):
	job = job_dict[row[3]]
	dateTime = getDatetimeFromRow(row)
	args = getArgs(row)
	# scheduler.add_job(job_function, run_date=dateTime) this is the real function

	rundate = datetime.datetime.now()
	rundate = rundate + datetime.timedelta(seconds=10)
	rundatePlusFive = rundate + datetime.timedelta(seconds=5)
	scheduler.add_job(job, run_date=rundate, args=args) # testing - always do jobs 10 seconds in the future
	scheduler.add_job(jobs.removeJobFromTable, run_date=rundatePlusFive, args=[row[0]])


def getDatetimeFromRow(row):
	dateTime = datetime.datetime.strptime(row[1], "%x")
	dateTime = dateTime.replace(hour=int(row[2].split(':')[0]), minute=int(row[2].split(':')[1]))
	return dateTime

def getArgs(row): # extract the arguments from a row and return them in an array
	args = []
	i = 5
	while row[i] is not None:
		args.append(row[i])
		i += 1
	return args


def writeToLogs(string):
	with open('logs.txt', 'a') as f:
		f.write(string)
	f.close()

def getJobDescription(row):
	description = "JOB ADDED - " + str(datetime.datetime.now()) + "\n" + "Execute at:" + str(getDatetimeFromRow(row)) + "\n" + "Job: " + str(job_dict[row[3]]) + "\n" + "Arguments: " + str(getArgs(row))

	return description



if __name__ == "__main__":
	main()

