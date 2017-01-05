import csv
import collections

def evaluate_results(stats):
    max_throughput = max(stats.values())
    min_throughput = min(stats.values())
    diff = max_throughput - min_throughput
    percentage_diff = (diff / max_throughput) * 100
    print "Percentage difference : {}".format(percentage_diff)
    if percentage_diff > 10:
        return False
    return True


def write_results(filename, stats):
    with open(filename, "wb") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in collections.OrderedDict(sorted(stats.items())).items():
            writer.writerow([key, value])
