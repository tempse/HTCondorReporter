import re


def read_condor_q(report):
    report_dict = {}

    # extract scheduler
    res = re.search(r"Schedd: (.*).cern.ch", report)
    if res:
        report_dict["schedd"] = res.group(1)

    # extract number of jobs in different categories
    res = re.search(
        r"(\d+) jobs; (\d+) completed, (\d+) removed, (\d+) idle, (\d+) running, (\d+) held, (\d+) suspended",
        report,
    )
    if res:
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
-- Schedd: bigbird36.cern.ch : <123.456.789.10:1112?... @ 08/03/19 09:22:47
OWNER    BATCH_NAME                  SUBMITTED   DONE   RUN    IDLE  TOTAL JOB_IDS
username CMD: condorExecutable.sh   8/3  09:08      _     74   2156   2233 158324.0 ... 158351.11

2230 jobs; 0 completed, 0 removed, 2156 idle, 74 running, 0 held, 0 suspended
"""

    condor_report = read_condor_q(condor_q_output)
    print(condor_report)
