"""

This executable will use rsync to copy the results from remote worker nodes
back to the execute node. The executable is assumed to be run from the submit
directory (e.g., where the .ini file is) and on the submit machine.
"""
import argparse
import glob
import subprocess

from bilby_pipe.utils import logger


def get_cluster_id_list(outdir):
    """Get a list of cluster IDs for every running analysis job"""
    logfile_matches = glob.glob(f"{outdir}/log_data_analysis/*.log")
    ids = []
    for logfile in logfile_matches:
        ids.append(get_cluster_id(logfile))
    return ids


def get_cluster_id(logfile):
    """Read a log files to determine the latest cluster ID

    Extract the HTCondor cluster ID from the .log file. For example, if the log
    file reads

    ```
    001 (100503183.000.000) 2022-03-07 15:22:49 Job executing on host: <10.14.4.164...>
    ```
    Then this function return the cluster ID 100503183

    Parameters
    ----------
    logfile: str
        A path to a HTCondor log file

    Returns
    -------
    cluster_id: str
        The cluster ID. If not ID is found, None is returned and a log message
        is printed.
    """

    with open(logfile, "r") as f:
        ids = []
        for line in f:
            if "Job executing on" in line:
                elements = line.split()
                ids.append(int(elements[1].lstrip("(").rstrip(")").split(".")[0]))

    if len(ids) > 0:
        return ids[-1]
    else:
        logger.info("No cluster ID found in log file")


def run_rsync(cluster_id, outdir):
    sync_path = f"{outdir}/result/"
    target = f"{cluster_id}:{sync_path}"
    cmd = ["rsync", "-v", "-r", "-e", '"condor_ssh_to_job"', target, sync_path]
    logger.info("Running " + " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True)
    if out.returncode == 0:
        logger.info(f"Synced job {cluster_id}: {out.stdout.decode('utf-8')}")
    else:
        logger.warning(f"Unable to sync job {cluster_id}: {out.stderr.decode('utf-8')}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", help="The bilby_pipe directory to sync")
    args = parser.parse_args()
    args.outdir = args.outdir.rstrip("/")
    cluster_id_list = get_cluster_id_list(args.outdir)
    for cluster_id in cluster_id_list:
        if cluster_id is not None:
            run_rsync(cluster_id, args.outdir)
