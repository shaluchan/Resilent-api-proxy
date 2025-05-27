import requests
import time
import redis
from threading import Thread

r = redis.Redis(host='redis', port=6379, db=0)

def monitor_health():
    while True:
        try:
            res = requests.get("http://api-proxy:5000/health", timeout=5)
            print("[Heartbeat] Health OK:", res.json())
        except:
            print("[Heartbeat] API Proxy not responding!")
        time.sleep(5)

def listen_for_status():
    pubsub = r.pubsub()
    pubsub.subscribe('status')
    for message in pubsub.listen():
        if message['type'] == 'message':
            print("[Realtime Status]", message['data'].decode())

if __name__ == "__main__":
    Thread(target=monitor_health).start()
    Thread(target=listen_for_status).start()

    while True:
        time.sleep(1)