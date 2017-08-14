# to be run as a service, and execute the jobs in jobs.db at their specified run times
from apscheduler.schedulers.background import BackgroundScheduler
from helper import *
from time import time


def main():
    conn = sqlite3.connect('jobs.db')
    write_logs("program started\n")

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
            write_logs(get_job_description(row))
            schedule(row, scheduler)
            set_job_scheduled(c, row[0])
            conn.commit()


def schedule(row, scheduler):
    job = job_dict[row[3]]
    date_time = get_datetime_from_row(row)
    args = get_args(row)
    scheduler.add_job(job, run_date=date_time, args=args)  # this is the real function

    # run_date = datetime.datetime.now()
    # run_date = run_date + datetime.timedelta(seconds=10)
    run_date_plus_five = date_time + datetime.timedelta(seconds=5)
    # scheduler.add_job(job, run_date=run_date, args=args)  # testing - always do jobs 10 seconds in the future

    scheduler.add_job(remove_job_from_table, run_date=run_date_plus_five, args=[row[0]])


if __name__ == "__main__":
    main()

