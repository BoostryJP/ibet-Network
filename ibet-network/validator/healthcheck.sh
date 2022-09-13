ps -ef | grep -v grep | grep "geth --http" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "$0: geth Not Running." 1>&2
  exit 1
fi