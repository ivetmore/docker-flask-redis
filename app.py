from flask import Flask, jsonify
import redis
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Redis connection
try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=6379,
        decode_responses=True
    )
    r.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    r = None


@app.route("/")
def home():
    return "Hello from Flask and Redis with Docker Compose!"


@app.route("/count")
def count():
    try:
        visits = r.incr("counter")
        logger.info(f"/count endpoint called. Visits={visits}")
        return jsonify({"visits": visits})
    except Exception as e:
        logger.error(f"Error in /count endpoint: {e}")
        return jsonify({"error": "Redis unavailable"}), 500


@app.route("/health")
def health():
    try:
        r.ping()
        return jsonify({"status": "OK", "redis": "connected"})
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "ERROR", "redis": "disconnected"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

