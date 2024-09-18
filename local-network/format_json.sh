jq . quorum_data/v0/genesis.json > tmp.json && mv tmp.json quorum_data/g0/genesis.json
jq . quorum_data/v0/genesis.json > tmp.json && mv tmp.json quorum_data/v0/genesis.json
jq . quorum_data/v1/genesis.json > tmp.json && mv tmp.json quorum_data/v1/genesis.json
jq . quorum_data/v2/genesis.json > tmp.json && mv tmp.json quorum_data/v2/genesis.json
jq . quorum_data/v3/genesis.json > tmp.json && mv tmp.json quorum_data/v3/genesis.json