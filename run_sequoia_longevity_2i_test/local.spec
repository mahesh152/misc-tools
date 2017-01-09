[clusters]
nyx =
    172.16.12.69:8091
    172.16.12.67:8091
    172.16.12.70:8091
    172.16.12.68:8091,index
    172.16.12.66:8091,n1ql

[clients]
hosts =
    172.16.12.69
credentials = root:couchbase

[storage]
data = /data
index = /data

[credentials]
rest = Administrator:password
ssh = root:couchbase

[parameters]
OS = CentOS 7
CPU = Data: (4-8 vCPU), Index: CPU (8 vCPU)
Memory = Data: 4-8 GB, Index: 16 GB
Disk = SSD