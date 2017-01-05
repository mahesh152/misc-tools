import os
import sys
import tarfile
import json
import datetime
import collections
import csv


def get_scan_ops(config_path):
    with open(config_path) as f_json:
        data = json.load(f_json)
        return data["ScanSpecs"][0]["Repeat"]


def get_stats(directory, scan_ops):
    files = [sys.argv[1] + "/" + f for f in os.listdir(directory) if f.endswith(".tar") and "result" in f]
    ret_val = {}
    for f in files:
        stat = os.stat(f)
        timestamp = stat.st_mtime
        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        tar = tarfile.open(f)
        tar.extractall()
        tar.close()
        with open("result.json") as f_json:
            data = json.load(f_json)
            throughput = scan_ops / data["Duration"]
            ret_val[timestamp] = throughput
        os.remove("result.json")
    return ret_val


def write_results(stats):
    with open("results.csv", "wb") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in collections.OrderedDict(sorted(stats.items())).items():
            writer.writerow([key, value])


def evaluate_results(stats):
    max_throughput = max(stats.values())
    min_throughput = min(stats.values())
    diff = max_throughput - min_throughput
    percentage_diff = (diff / max_throughput) * 100
    print "Percentage difference : {}".format(percentage_diff)
    if percentage_diff > 10:
        return False
    return True


def main():
    scan_ops = get_scan_ops(sys.argv[1] + "/containers/cbindexperf/config.json")
    stats = get_stats(sys.argv[1], scan_ops)
    write_results(stats)
    if evaluate_results(stats):
        print "Test Passed!"
    else:
        print "Test Failed"


if __name__ == "__main__":
    main()
