import re


def read_condor_q(report):
    report_dict = {}

    task_headers = []
    switch_mode_detailed_task = False

    for line in report.split("\n"):
        # extract the scheduler
        if line.startswith("-- Schedd:"):
            res = re.search(r"Schedd: (.*).cern.ch", line)
            if res:
                report_dict["schedd"] = res.group(1)

        # extract the column headers of the tasks report
        elif line.startswith("OWNER"):
            switch_mode_detailed_task = True  # the following lines are tasks reports
            for h in line.split():
                task_headers.append(h)

        # extract the values of a task report line
        elif switch_mode_detailed_task:
            if line != "\n" and line != "":
                line_elements = line.split()
                job_id = line_elements[1] + " " + line_elements[2]
                submit_datetime = line_elements[3] + " " + line_elements[4]
                report_dict[job_id] = {"SUBMITTED": submit_datetime}
                for k,v in zip(task_headers[3:], line_elements[5:]):
                    report_dict[job_id][k] = v
            else:
                # an empty line denotes the end of the task report(s)
                switch_mode_detailed_task = False

        else:
            # extract cumulative numbers of jobs
            res = re.search(
                    r"Total for query: (\d+) jobs; (\d+) completed, (\d+) removed, (\d+) idle, (\d+) running, (\d+) held, (\d+) suspended",
                report
            )
            report_dict["total_jobs"] = int(res.group(1))
            report_dict["completed_jobs"] = int(res.group(2))
            report_dict["removed_jobs"] = int(res.group(3))
            report_dict["idle_jobs"] = int(res.group(4))
            report_dict["running_jobs"] = int(res.group(5))
            report_dict["held_jobs"] = int(res.group(6))
            report_dict["suspended_jobs"] = int(res.group(7))

    return report_dict


if __name__ == "__main__":
    condor_q_output = """
-- Schedd: bigbird36.cern.ch : <123.456.789.10:1112?... @ 12/09/19 21:43:53
OWNER    BATCH_NAME    SUBMITTED   DONE   RUN    IDLE  TOTAL JOB_IDS
username ID: 704081  12/9  16:36    222    33     286    541 704081.0-285
username ID: 704082  12/9  16:36    2     123     500    625 704081.0-499

Total for query: 1166 jobs; 224 completed, 0 removed, 786 idle, 156 running, 0 held, 0 suspended 
Total for username: 1166 jobs; 0 completed, 0 removed, 786 idle, 156 running, 0 held, 0 suspended 
Total for all users: 5013 jobs; 2 completed, 0 removed, 3753 idle, 1224 running, 34 held, 0 suspended
"""

    condor_report = read_condor_q(condor_q_output)
    for k in condor_report:
        print("{}: {}".format(k, condor_report[k]))
