[clusters]
nyx =
    172.16.12.33:8091
    172.16.12.41:8091
    172.16.12.9:8091,index
    172.16.12.49:8091,n1ql

[clients]
hosts =
    172.16.12.49
credentials = root:couchbase

[storage]
data = /data
index = /data

[credentials]
rest = Administrator:password
ssh = root:couchbase

[parameters]
OS = CentOS 7
CPU = Data: E5-2630 (24 vCPU), Index: CPU E5-2680 v3 (48 vCPU)
Memory = Data: 64 GB, Index: 128 GB
Disk = SSD