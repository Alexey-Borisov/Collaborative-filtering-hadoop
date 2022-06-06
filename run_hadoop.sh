SOURCE_BASE_PATH="/collaborative_filtering"

INPUT_HADOOP_DIR="/collaborative_filtering/data/input"
OUTPUT_HADOOP_DIR="/collaborative_filtering/data/output"

HADOOP_STREAMING_PATH="${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"

N_M=${1}
N_R=${2}

FLOAT_PRECISION=${3}

# ------------------------------------------------------------------------------------
# Prepare directories
hdfs dfs -test -d ${INPUT_HADOOP_DIR}
if [ $? -eq 0 ];
  then
    echo "Remove ${INPUT_HADOOP_DIR}"
    hdfs dfs -rm -r ${INPUT_HADOOP_DIR}
fi

hdfs dfs -test -d ${OUTPUT_HADOOP_DIR}
if [ $? -eq 0 ];
  then
    echo "Remove ${OUTPUT_HADOOP_DIR}"
    hdfs dfs -rm -r ${OUTPUT_HADOOP_DIR}
fi

test -d ${SOURCE_BASE_PATH}/data/output
if [ $? -eq 0 ];
  then
    echo "Remove ${SOURCE_BASE_PATH}/data/output"
    rm -rf ${SOURCE_BASE_PATH}/data/output
fi

test -d ${SOURCE_BASE_PATH}/data/output
if [ $? -eq 0 ];
  then
    echo "Remove ${SOURCE_BASE_PATH}/data/input"
    rm -rf ${SOURCE_BASE_PATH}/data/input
fi

hdfs dfs -mkdir -p ${INPUT_HADOOP_DIR}
hdfs dfs -copyFromLocal ${SOURCE_BASE_PATH}/data/input/* ${INPUT_HADOOP_DIR}

# ------------------------------------------------------------------------------------
# Stage 1
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_1.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_1.py

echo "Start stage 1: $(date)"

hadoop_streaming_arguments="\
  -D mapred.map.tasks=${N_M} \
  -D mapred.reduce.tasks=${N_R} \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper_1.py -reducer src/reducer_1.py \
  -input ${INPUT_HADOOP_DIR}/ratings.csv -output ${OUTPUT_HADOOP_DIR}/stage_1 \
  -cmdenv float_precision=${FLOAT_PRECISION} \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

echo "End stage 1: $(date)"

# -----------------------------------------------------------------------------------
# Stage 2
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_2.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_2.py

echo "Start stage 2: $(date)"

hadoop_streaming_arguments="\
  -D mapred.map.tasks=${N_M} \
  -D mapred.reduce.tasks=${N_R} \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper_2.py -reducer src/reducer_2.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_1/* -output ${OUTPUT_HADOOP_DIR}/stage_2 \
  -cmdenv float_precision=${FLOAT_PRECISION} \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

echo "End stage 2: $(date)"

# -----------------------------------------------------------------------------------
# Stage 3
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_3.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_3.py

echo "Start stage 3: $(date)"

hadoop_streaming_arguments="\
  -D mapred.map.tasks=${N_M} \
  -D mapred.reduce.tasks=${N_R} \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper_3.py -reducer src/reducer_3.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_2/*,${INPUT_HADOOP_DIR}/ratings.csv -output ${OUTPUT_HADOOP_DIR}/stage_3 \
  -cmdenv float_precision=${FLOAT_PRECISION} \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

echo "End stage 3: $(date)"

# -----------------------------------------------------------------------------------
# Stage 4
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_4.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_4.py

echo "Start stage 4: $(date)"

hadoop_streaming_arguments="\
  -D mapred.map.tasks=${N_M} \
  -D mapred.reduce.tasks=${N_R} \
  -files ${SOURCE_BASE_PATH}/src  \
  -mapper src/mapper_4.py -reducer src/reducer_4.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_3/*,${INPUT_HADOOP_DIR}/ratings.csv -output ${OUTPUT_HADOOP_DIR}/stage_4 \
  -cmdenv float_precision=${FLOAT_PRECISION} \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

echo "End stage 4: $(date)"

# -----------------------------------------------------------------------------------
# Stage 5
chmod 0777 ${SOURCE_BASE_PATH}/src/mapper_5.py
chmod 0777 ${SOURCE_BASE_PATH}/src/reducer_5.py

echo "Start stage 5: $(date)"

hadoop_streaming_arguments="\
  -D mapred.map.tasks=${N_M} \
  -D mapred.reduce.tasks=${N_R} \
  -files ${SOURCE_BASE_PATH}/src,${SOURCE_BASE_PATH}/data/input/movies.csv  \
  -mapper src/mapper_5.py -reducer src/reducer_5.py \
  -input ${OUTPUT_HADOOP_DIR}/stage_4/* -output ${OUTPUT_HADOOP_DIR}/final \
  -cmdenv float_precision=${FLOAT_PRECISION} \
"

echo "Run streaming with arguments: \n${hadoop_streaming_arguments}"
hadoop jar ${HADOOP_STREAMING_PATH} ${hadoop_streaming_arguments}

echo "End stage 5: $(date)"

# -----------------------------------------------------------------------------------
hdfs dfs -copyToLocal ${OUTPUT_HADOOP_DIR} ${SOURCE_BASE_PATH}/data

hdfs dfs -rm -r ${INPUT_HADOOP_DIR}
hdfs dfs -rm -r ${OUTPUT_HADOOP_DIR}
