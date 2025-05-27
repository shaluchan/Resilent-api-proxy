from flask import Flask, request, jsonify
import requests
import redis
import time
import threading

app = Flask(__name__)

r = redis.Redis(host='redis', port=6379, db=0)

APIS = [
    {
        "name": "OpenWeatherMap",
        "url": "https://api.openweathermap.org/data/2.5/weather",
        "key": "3f9950f17f2e8ba67391b5d212d7c2c9"
    },
    {
        "name": "WeatherAPI",
        "url": "http://api.weatherapi.com/v1/current.json",
        "key": "248676ee8f5a4a1b9b385601252705"
    }
]

inactive_apis = set()

from requests.exceptions import Timeout, ConnectionError

@app.route("/weather")
def weather():
    city = request.args.get("city", "London")
    for api in APIS:
        if api["name"] in inactive_apis:
            continue  # skip inactive APIs
        try:
            if "openweathermap" in api["url"]:
                res = requests.get(api["url"], params={"q": city, "appid": api["key"]}, timeout=5)
            else:
                res = requests.get(api["url"], params={"q": city, "key": api["key"]}, timeout=5)
            if res.status_code == 429:
                r.publish('status', f"Rate limit on {api['name']}, switching API")
                continue  # try next one
            if res.status_code == 401:
                inactive_apis.add(api["name"])
                r.publish('status', f"Invalid key for {api['name']}, marking inactive")
                continue
            r.publish('status', f"Success with {api['name']}")
            return res.json()
        except Timeout:
            r.publish('status', f"Timeout on {api['name']}, retrying...")
            continue
        except ConnectionError:
            r.publish('status', f"Connection error on {api['name']}, trying fallback...")
            continue


    r.publish('status', "All APIs failed, returning stub response")
    return jsonify({"message": "All APIs failed", "data": "stub"}), 503

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
