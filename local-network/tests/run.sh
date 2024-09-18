cd ../ && bash reset_data.sh
cd -

docker compose -f ../docker-compose.yml rm --force

echo "run.sh inside of validator"
echo "---"
cat ../validator/run.sh
echo "---"
echo "docker-compose.yml"
echo "---"
cat ../docker-compose.yml
echo "---"

echo "Run"
docker compose -f ../docker-compose.yml build > /dev/null
docker compose -f ../docker-compose.yml up -d

sleep 50

echo "Send transactions"
# WEB3_HTTP_PROVIDER=http://192.168.210.119:8549 CONTRACT_NAME=LoadTest python send_transactions.py transactions_per_block_emptyBlockPeriod > transactions_emptyBlockPeriod.log
WEB3_HTTP_PROVIDER=http://localhost:8549 CONTRACT_NAME=LoadTest python send_transactions.py transactions_per_block_emptyBlockPeriod > transactions_emptyBlockPeriod.log

docker logs local-network-validator-0-1 &> emptyBlockPeriod/local-network-validator-0-1.log
docker logs local-network-validator-1-1 &> emptyBlockPeriod/local-network-validator-1-1.log
docker logs local-network-validator-2-1 &> emptyBlockPeriod/local-network-validator-2-1.log
docker logs local-network-validator-3-1 &> emptyBlockPeriod/local-network-validator-3-1.log
docker logs local-network-general-0-1 &> emptyBlockPeriod/local-network-general-0-1.log
