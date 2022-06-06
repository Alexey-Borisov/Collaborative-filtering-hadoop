
# Path in docker container
SOURCE_DOCKER_PATH="/collaborative_filtering"


test -d ./data/output
if [ $? -eq 0 ];
  then
    echo "Remove ./data/output"
    rm -rf ./data/output
fi

# Same mappers and reducers count for all map-reduce tasks (why not?)
# Number of mappers
N_M=3
# Number of reducers
N_R=3
# Precision for float
FLOAT_PRECISION=3

# Copy all data and code to namenode (see also `docker cp`)
# Run Hadoop Streaming on namenode (see also `docker exec`)
# Copy results from namenode (see also `docker cp`)

docker cp ../collaborative_filtering namenode:/
docker exec namenode bash ${SOURCE_DOCKER_PATH}/run_hadoop.sh ${N_M} ${N_R} ${FLOAT_PRECISION}
docker cp namenode:${SOURCE_DOCKER_PATH}/data/output ./data



