rm -rf quorum_data/g0/**/*
rm -rf quorum_data/g0/*

rm -rf quorum_data/g1/**/*
rm -rf quorum_data/g1/*

rm -rf quorum_data/v0/**/*
rm -rf quorum_data/v0/*

rm -rf quorum_data/v1/**/*
rm -rf quorum_data/v1/*

rm -rf quorum_data/v2/**/*
rm -rf quorum_data/v2/*

rm -rf quorum_data/v3/**/*
rm -rf quorum_data/v3/*

docker compose down
docker volume rm local-network_g0
docker volume rm local-network_v0
docker volume rm local-network_v1
docker volume rm local-network_v2
docker volume rm local-network_v3