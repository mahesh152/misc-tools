import numpy
from seriesly import Seriesly

from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery


def change(val):
    if type(val) == unicode:
        return int(val)
    else:
        return val

metrics = [
    "secondary_scanlatency20M_fdb_nyx",
    "secondary_scanlatency20M_multiple_fdb_nyx",
    "secondary_scanlatency_rebalance20M_fdb_nyx",
    "secondary_scanlatency_stalefalse_20M_fdb_nyx",
    "secondary_doc_indexing_latency_20M_moi_80th_nyx_query",
    "secondary_scanlatency20M_moi_nyx",
    "secondary_scanlatency20M_multiple_moi_nyx",
    "secondary_scanlatency_rebalance20M_moi_nyx",
    "secondary_scanlatency_stalefalse_20M_100Kops_moi_nyx",
]

s = Seriesly(host='cbmonitor.sc.couchbase.com')

b = Bucket("couchbase://cbmonitor.sc.couchbase.com/benchmarks",
           password="password")

for metric in metrics:
    print "********* Metric: " + metric
    q = N1QLQuery('SELECT id,snapshots FROM benchmarks WHERE metric = "{}";'
                  .format(metric))

    for row in b.n1ql_query(q):
        doc_id = row['id']
        snapshot = row['snapshots'][0]

        if len(row['snapshots']) > 1:
            snapshot = row['snapshots'][1].replace("_apply_scanworkload", "")

        print "Snapshot: " + snapshot

        data = s['secondaryscan_latency{}'.format(snapshot)].get_all()

        if data:
            values = [change(v['Nth-latency']) for v in data.values() if 'Nth-latency' in v]
            if not values:
                values = [change(v[' Nth-latency']) for v in data.values()]
            p90 = numpy.percentile(values, 90)

            benchmark = b.get(doc_id).value
            benchmark['value'] = round(p90/1000000, 2)
            print p90
            print(b.upsert(doc_id, benchmark))

