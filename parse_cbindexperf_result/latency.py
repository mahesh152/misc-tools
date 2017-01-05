import os
import sys
import tarfile
import datetime
import csv
import numpy as np

import common


def get_stats(directory):
    files = [sys.argv[1] + "/" + f for f in os.listdir(directory) if f.endswith(".tar") and "statsfile" in f]
    ret_val = {}
    for f in files:
        stat = os.stat(f)
        timestamp = stat.st_mtime
        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        tar = tarfile.open(f)
        tar.extractall()
        tar.close()
        with open('statsfile', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            data = []
            for row in spamreader:
                data.append(int(row[3].split(":")[1]))
            ret_val[timestamp] = round(np.percentile(data, 80), 2)
            os.remove("statsfile")
    return ret_val


def main():
    stats = get_stats(sys.argv[1])
    common.write_results("latency.csv", stats)
    if common.evaluate_results(stats):
        print "Latency: Test Passed!"
    else:
        print "Latency: Test Failed"

if __name__ == "__main__":
    main()
