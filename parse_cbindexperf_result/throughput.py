import os
import sys
import tarfile
import json
import datetime
import common

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


def main():
    scan_ops = get_scan_ops(sys.argv[1] + "/containers/cbindexperf/config.json")
    stats = get_stats(sys.argv[1], scan_ops)
    common.write_results("throughput.csv", stats)
    if common.evaluate_results(stats):
        print "Throughput: Test Passed!"
    else:
        print "Throughput: Test Failed"


if __name__ == "__main__":
    main()
