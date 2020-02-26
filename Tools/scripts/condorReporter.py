#!/usr/bin/env python

import os, sys, time
import random
import subprocess

from Tools.python.telegramNotifier import send
from Tools.python.HTCondorTools import read_condor_q

# Defaults
user = os.getenv("USER")
hostname = os.getenv("HOSTNAME")
start_time = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

send(
    "\xE2\x8F\xB0 {} HTCondorReporter: Start monitoring Condor jobs of user {} on {}".format(
        start_time, user, hostname
    )
)

report = subprocess.check_output(["condor_q"])
report_dict = read_condor_q(report)
schedd = report_dict["schedd"]
total_jobs = report_dict["total_jobs"]

cnt = 0
while True:
    report = subprocess.check_output(["condor_q"])
    report_dict = read_condor_q(report)

    # send a status report once every hour
    if cnt % 6 == 0:
        tasks = {
            job_id: report_dict[job_id]
            for job_id in report_dict
            if job_id.startswith("ID:")
        }
        message = "\xE2\x8C\x9B HTCondorReporter: Monitoring {} jobs in {} tasks:".format(
            report_dict["total_jobs"], len(tasks)
        )
        for task in tasks:
            message += "\n\n\xE2\x9E\xA1 {} ({}) - DONE: {}, RUN: {}, IDLE: {}".format(
                task,
                tasks[task]["SUBMITTED"],
                tasks[task]["DONE"],
                tasks[task]["RUN"],
                tasks[task]["IDLE"],
            )
            for s in tasks[task]:
                if s not in ("HOLD", "SUSPENDED"):
                    continue
                message += ", {}: {}".format(s, tasks[task][s])

        message += "\n\nSUMMARY: Completed: {}, removed: {}, idle: {}, running: {}, held: {}, suspended: {}. Scheduler: {}".format(
            report_dict["completed_jobs"],
            report_dict["removed_jobs"],
            report_dict["idle_jobs"],
            report_dict["running_jobs"],
            report_dict["held_jobs"],
            report_dict["suspended_jobs"],
            schedd,
        )

        send(message)

    if report_dict["total_jobs"] == 0:
        send(
            "\xE2\x9C\x85 HTCondorReporter: Jobs finished running on scheduler {}".format(
                schedd
            )
        )
        break

    cnt += 1

    # end reporting after 1 week
    if cnt % 2016 == 0:
        send("\xE2\x9D\x8C HTCondorReporter: Terminated after one week of running")
        sys.exit(1)

    time.sleep(300)  # sleep for 5 minutes


end_time = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
success_emojis = (
    "\xF0\x9F\x9A\x80",
    "\xF0\x9F\x99\x8C",
    "\xE2\x9C\x8C",
    "\xE2\x9C\x94",
    "\xE2\x98\x95",
    "\xF0\x9F\x8E\x89",
    "\xF0\x9F\x91\x8C",
    "\xF0\x9F\x91\x8D",
    "\xF0\x9F\x91\x8F",
    "\xF0\x9F\x91\x90",
    "\xF0\x9F\x92\xAA",
    "\xF0\x9F\x98\x8E",
)
send(
    "{} HTCondorReporter: Finished monitoring jobs at {}".format(
        random.choice(success_emojis), end_time
    )
)
