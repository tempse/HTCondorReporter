#!/usr/bin/env python

import os, sys, time
import subprocess

from HTCondorReporter.Tools.telegramNotifier import send
from HTCondorReporter.Tools.HTCondorTools import read_condor_q

# Defaults
user = os.getenv("USER")
hostname = os.getenv("HOSTNAME")
start_time = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

send(
    "{} HTCondorReporter: Start monitoring Condor jobs of user {} on {}".format(
        start_time, user, hostname
    )
)

report = subprocess.check_output(["condor_q"])
report_dict = read_condor_q(report)
schedd = report_dict["schedd"]
total_jobs = report_dict["total_jobs"]
send(
    "{} HTCondorReporter: Monitoring {} jobs on scheduler {}".format(
        start_time, total_jobs, schedd
    )
)

cnt = 0
while True:
    report = subprocess.check_output(["condor_q"])
    report_dict = read_condor_q(report)

    cnt += 1
    # send a status report once every hour
    if cnt % 12 == 0:
        send(
            "HTCondorReporter (sched: {}): Monitoring {} jobs. Completed: {}, removed: {}, idle: {}, running: {}, held: {}, suspended: {}".format(
                schedd,
                report_dict["total_jobs"],
                report_dict["completed_jobs"],
                report_dict["removed_jobs"],
                report_dict["idle_jobs"],
                report_dict["running_jobs"],
                report_dict["held_jobs"],
                report_dict["suspended_jobs"],
            )
        )
    if report_dict["total_jobs"] == 0:
        send("HTCondorReporter: Jobs finished running on scheduler {}".format(schedd))
        break

    # end reporting after 1 week
    if cnt % 2016 == 0:
        send("HTCondorReporter: Terminated after one week of running")
        sys.exit(1)

    time.sleep(300)  # sleep for 5 minutes


end_time = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
send("HTCondorReporter: Finished monitoring jobs at {}".format(end_time))
