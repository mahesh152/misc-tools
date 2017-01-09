url=$1
duration=$2
scale=$3

mkdir test
mkdir test/src

curr_dir=`pwd`
export GOPATH=$curr_dir/test

echo "get source"
go get github.com/couchbaselabs/sequoia
go get github.com/couchbase/perfrunner
go get github.com/mahesh152/misc-tools

cd $curr_dir/test/src/github.com/couchbase/perfrunner
make
cp $curr_dir/test/src/github.com/mahesh152/misc-tools/run_sequoia_longevity_2i_test/dessert.spec .
./env/bin/install -c dessert.spec -url $url

pypath=$curr_dir/test/src/github.com/couchbase/perfrunner/env/bin/python

cd $curr_dir/test/src/github.com/couchbaselabs/sequoia

echo "build sequoia"
go build

echo "build cbindexperf"
docker build -t sequoiatools/cbindexperf containers/cbindexperf

echo "run sequoia"
./sequoia -test tests/2i/test_plasma.yml -scope tests/2i/scope_plasma.yml --log_level 2 -duration $duration -scale $scale -provider file:ubuntu_dessert.yml

cd $curr_dir/test/src/github.com/mahesh152/misc-tools/parse_cbindexperf_result

$pypath latency.py $curr_dir/test/src/github.com/couchbaselabs/sequoia
$pypath throughput.py $curr_dir/test/src/github.com/couchbaselabs/sequoia