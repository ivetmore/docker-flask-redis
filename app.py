from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route("/")
def home():
	return "Hello from Flask and Redis with Docker Compose!"

@app.route("/count")
def count():
	visits =  r.incr("visits")
	return jsonify({
	    "visits": visits
	})
@app.route("/health")
def health():
	return jsonify({
          "status": "OK",
          "redis": "connected"
	}) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
