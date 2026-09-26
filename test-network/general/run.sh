#!/bin/ash
mkdir -p /eth/geth

escape_toml_string() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

setup_nodekey_options() {
  NODEKEY_SOURCE="${nodekeysource:-file}"
  NODEKEY_DECRYPTION="${nodekeydecryption:-none}"

  if [ -n "${nodekey}" ]; then
    NODEKEY_OPT="--nodekey ${nodekey}"
    return 0
  fi
  if [ -n "${nodekeyhex}" ]; then
    NODEKEY_OPT="--nodekeyhex ${nodekeyhex}"
    return 0
  fi

  if [ "${NODEKEY_SOURCE}" = "aws-sm" ]; then
    if [ -z "${nodekey_aws_secret_name}" ]; then
      echo "$0: nodekey_aws_secret_name is required when nodekeysource=aws-sm." >&2
      return 1
    fi
    if [ -n "${nodekey_aws_secret_version_id}" ] && [ -n "${nodekey_aws_secret_version_stage}" ]; then
      echo "$0: nodekey_aws_secret_version_id and nodekey_aws_secret_version_stage are mutually exclusive." >&2
      return 1
    fi
    if [ -z "${nodekey_aws_secret_version_id}" ] && [ -z "${nodekey_aws_secret_version_stage}" ]; then
      echo "$0: either nodekey_aws_secret_version_id or nodekey_aws_secret_version_stage is required when nodekeysource=aws-sm." >&2
      return 1
    fi
    if [ "${NODEKEY_DECRYPTION}" = "aws-kms" ] && [ -z "${nodekey_aws_kms_key_id}" ]; then
      echo "$0: nodekey_aws_kms_key_id is required when nodekeydecryption=aws-kms." >&2
      return 1
    fi

    CONFIG_FILE="/eth/config.toml"
    {
      printf '[Node.P2P.NodeKey.ConfigAws]\n'
      printf 'SecretName = "%s"\n' "$(escape_toml_string "${nodekey_aws_secret_name}")"
      if [ -n "${nodekey_aws_secret_version_id}" ]; then
        printf 'SecretVersionId = "%s"\n' "$(escape_toml_string "${nodekey_aws_secret_version_id}")"
      fi
      if [ -n "${nodekey_aws_secret_version_stage}" ]; then
        printf 'SecretVersionStage = "%s"\n' "$(escape_toml_string "${nodekey_aws_secret_version_stage}")"
      fi
      if [ -n "${nodekey_aws_kms_key_id}" ]; then
        printf 'KmsKeyId = "%s"\n' "$(escape_toml_string "${nodekey_aws_kms_key_id}")"
      fi
      if [ -n "${nodekey_aws_kms_encryption_algorithm}" ]; then
        printf 'KmsEncryptionAlgorithm = "%s"\n' "$(escape_toml_string "${nodekey_aws_kms_encryption_algorithm}")"
      fi
    } > "${CONFIG_FILE}"
    CONFIG_OPT="--config ${CONFIG_FILE}"
  fi

  if [ -n "${nodekeysource}" ] || [ -n "${nodekeydecryption}" ] || [ "${NODEKEY_SOURCE}" = "aws-sm" ]; then
    NODEKEY_SOURCE_OPT="--nodekeysource ${NODEKEY_SOURCE}"
    NODEKEY_DECRYPTION_OPT="--nodekeydecryption ${NODEKEY_DECRYPTION}"
  fi
}

setup_nodekey_options || exit 1

test ! -z "${rpccorsdomain}" && CORS_OPT="--http.corsdomain ${rpccorsdomain}"
test ! -z "${rpcvhosts}" && VHOST_OPT="--http.vhosts ${rpcvhosts}"
test ! -z "${maxpeers}" && PEERS_OPT="--maxpeers ${maxpeers}"
test ! -z "${syncmode}" && SYNCMODE_OPT="--syncmode ${syncmode}"
test ! -z "${identity}" && IDENTITY_OPT="--identity ${identity}"
test ! -z "${cache}" && CACHE_OPT="--cache ${cache}"
test ! -z "${cache_gc}" && CACHE_GC_OPT="--cache.gc ${cache_gc}"

GETH_CMD="geth \
--http \
--http.addr 0.0.0.0 \
--http.port 8545 \
${CORS_OPT} \
${IDENTITY_OPT} \
--datadir /eth \
--port 30303 \
--http.api admin,debug,miner,txpool,eth,net,web3,istanbul,personal \
${VHOST_OPT} \
--networkid 1500002 \
--nat any \
--verbosity ${verbosity:-2} \
--nodiscover \
--allow-insecure-unlock \
--miner.gastarget 800000000 \
${PEERS_OPT} \
${SYNCMODE_OPT} \
${CACHE_OPT} \
${CONFIG_OPT} \
${NODEKEY_OPT} \
${NODEKEY_SOURCE_OPT} \
${NODEKEY_DECRYPTION_OPT} \
${CACHE_GC_OPT}"

if [ -z "${BLOCK_SYNC_MONITORING_DISABLED}" ] || [ "${BLOCK_SYNC_MONITORING_DISABLED}" -ne 1 ]; then
  ash -c "nohup python monitoring/monitor_block_sync.py > /dev/stdout 2>&1 &"
fi
ash -c "nohup ${GETH_CMD//\*/\\\*} > /dev/stdout 2>&1 &"

for i in $(seq 1 300); do
  sleep 1
  ps -ef | grep -v grep | grep "geth --http" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "$0: geth Running."
    break
  fi
done

function trap_sigint() {
  echo "$0: geth Shutdown."
  PID=$(ps -ef | grep "geth --http" | grep -v grep | awk '{print $1}')
  kill -SIGINT ${PID}
  while :; do
    ps -ef | grep -v grep | grep "geth --http" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
      break
    fi
    sleep 1
  done
  exit 0
}
trap trap_sigint SIGINT SIGTERM

while :; do
  sleep 5
done
