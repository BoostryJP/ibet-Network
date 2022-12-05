ps -ef | grep -v grep | grep "geth --http" > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "$0: geth Not Running." 1>&2
  exit 1
fi

if [ -z "${BLOCK_SYNC_MONITORING_DISABLED}" ] || [ "${BLOCK_SYNC_MONITORING_DISABLED}" -ne 1 ]; then
  ps -ef | grep -v grep | grep "monitor_block_sync.py" > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi