# Docker Flask and Redis App
A Dockerized Flask application using Redis for stateful data, with CI/CD vit GitHub Actions, and deployed on Render.


##Live Demo on Render:

Live application link here: https://docker-flask-redis.onrender.com

## Endpoints

-`GET /` - Returns a welcome message.
-`GET /count` - Increments and returns a counter stored in Redis. If Redis is not available, returns 503 Service Unavailable:
{"error":"Redis not initialized"}
-`GET /health` - Returns service health. If Redis is unavailable, the service reports **DEGRADED**: ```json
{"status":"DEGRADED","redis":"not connected"}
- `GET /metrics` - Returns basic request metrics (total requests and counts by path).


```md

## Notes
This app is designed to run in a degraded mode when Redis is not available (e.g., web-only development). 
