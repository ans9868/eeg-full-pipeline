#!/bin/bash
# Start Spark History Server to view completed Spark jobs using Docker
# Usage: ./start-spark-history.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/logs/spark-events-history"
CONTAINER_NAME="spark-history-server"
IMAGE_NAME="nour333/eeg-spark-pipeline:latest"

echo "🚀 Starting Spark History Server (Docker)..."
echo "📁 Log directory: ${LOG_DIR}"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check if log directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "❌ Log directory not found: ${LOG_DIR}"
    echo "💡 Creating directory..."
    mkdir -p "$LOG_DIR"
fi

# Stop and remove existing container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "🔄 Stopping existing container..."
    docker stop "${CONTAINER_NAME}" > /dev/null 2>&1
    docker rm "${CONTAINER_NAME}" > /dev/null 2>&1
fi

# Check if image exists
if ! docker image inspect "${IMAGE_NAME}" &> /dev/null; then
    echo "⚠️  Image ${IMAGE_NAME} not found locally"
    echo "💡 Trying to pull or use alternative..."
    # Try alternative image
    IMAGE_NAME="bitnami/spark:latest"
    if ! docker image inspect "${IMAGE_NAME}" &> /dev/null; then
        echo "📥 Pulling ${IMAGE_NAME}..."
        docker pull "${IMAGE_NAME}" || {
            echo "❌ Failed to pull image. Please ensure Docker images are available."
            exit 1
        }
    fi
fi

# Start the history server container
# Note: History server uses spark.history.fs.logDirectory config
# The start script runs in daemon mode, so we tail the log to keep container alive
echo "🚀 Starting History Server container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    -p 18080:18080 \
    -v "${LOG_DIR}:/tmp/spark-events-history" \
    -e SPARK_HOME=/opt/bitnami/spark \
    -e SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=file:///tmp/spark-events-history" \
    "${IMAGE_NAME}" \
    bash -c "cd /opt/bitnami/spark && ./sbin/start-history-server.sh && sleep 3 && LOG_FILE=\$(ls /opt/bitnami/spark/logs/spark-*HistoryServer*.out 2>/dev/null | head -1) && if [ -n \"\$LOG_FILE\" ]; then tail -f \"\$LOG_FILE\"; else tail -f /dev/null; fi"

# Wait a moment for the server to start and initialize
sleep 5

# Check if container is running
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo ""
    echo "✅ Spark History Server started successfully!"
    echo "🌐 Access at: http://localhost:18080"
    echo "📁 Reading logs from: ${LOG_DIR}"
    echo ""
    echo "📝 To view logs: docker logs ${CONTAINER_NAME}"
    echo "🛑 To stop: docker stop ${CONTAINER_NAME}"
else
    echo "❌ Container failed to start. Checking logs..."
    docker logs "${CONTAINER_NAME}" 2>&1 | tail -20
    exit 1
fi

