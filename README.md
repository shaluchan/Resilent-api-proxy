
# Resilient API Proxy with Dockerized Services

 It demonstrates a resilient, dockerized microservices system that demonstrates API handling,Heartbeat monitoring and realtime communication.
---

##  Features

### API Proxy Service:
- Exposses `/weather?city=London` endpoint.
- Connects to 2 external APIs (OpenWeatherMap & WeatherAPI)
- Implements resilient logic:
  - API fallback
  - Retry on timeouts
  - Marks pernanently failing APIs as inactive
  - Returns stub data if all fail
- Exposes `/health` endpoint
- Publishes status updates to Heartbeat service via Redis Pub/Sub

### Heartbeat Service:
- Pings `/health` every 5 seconds
- Logs API proxy downtime
- Subscribes to real-time status updates via Redis

  Two-way inter-container communication:
- Heartbeat → API Proxy: via HTTP
- API Proxy → Heartbeat: via Redis Pub

---

##  Architecture Diagram
![arch](https://github.com/user-attachments/assets/5c51a4a2-e3d9-4ce3-97d6-4584797d56be)


---

##  Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resilient-api-proxy.git
cd resilient-api-proxy
```
### 2. Add ur API keys
Edit api-proxy/app.py and replace the placeholders in APIS with your actual API keys.

### 3.Build & Run with Docker Compose
```bash
docker-compose up --build
```
### 4. Make a Test Request
```bash
curl http://localhost:5000/weather?city=London
```
## Folder Structure
```bash
[shaluchan@shalu-nitroanv1551 Resilent-api-proxy]$ tree
.
├── README.md
└── Resilent-API
    ├── api-proxy
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── docker-compose.yaml
    └── heartbeat
        ├── Dockerfile
        ├── heartbeat.py
        └── requirements.txt
```

