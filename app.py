from flask import Flask, jsonify
import redis
import logging
import os

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Redis initialization
redis_client = None

def init_redis():
    global redis_client
    redis_url = os.environ.get("REDIS_URL")

    if not redis_url:
        logger.warning("REDIS_URL not set. Redis will not be initialized.")
        return

    try:
        redis_client = redis.from_url(redis_url, decode_responses=True)
        redis_client.ping()
        logger.info("Connected to Redis successfully")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        redis_client = None

# Initialize Redis when app starts
init_redis()

# Routes
@app.route("/")
def home():
    return "Hello from Flask + Redis on Render!"

@app.route("/health")
def health():
    if redis_client is None:
        logger.warning("Health check: Redis not initialized")
        return jsonify({
            "status": "DEGRADED",
            "redis": "not connected"
        }), 200

    try:
        redis_client.ping()
        return jsonify({
            "status": "OK",
            "redis": "connected"
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "DEGRADED",
            "redis": "unreachable"
        }), 200

@app.route("/count")
def count():
    if redis_client is None:
        logger.error("Redis not initialized in /count")
        return jsonify({
            "error": "Redis not initialized"
        }), 500

    try:
        visits = redis_client.incr("counter")
        logger.info(f"/count called. Visits={visits}")
        return jsonify({
            "visits": visits
        }), 200
    except Exception as e:
        logger.error(f"Error in /count endpoint: {e}")
        return jsonify({
            "error": "Redis error"
        }), 500

# App entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

