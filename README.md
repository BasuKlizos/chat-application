# Scalable Real-Time Chat Application

A **high-performance, real-time chat application** built with **FastAPI**, **Redis**, **MongoDB**, **Loki**, **Prometheus**, **Grafana**, and **Docker**. Designed for **horizontal scalability**, it ensures efficient handling of high traffic, large user bases, and seamless communication. With real-time messaging, persistent data storage, monitoring, and centralized logging, this application is ideal for large-scale deployments requiring reliability and performance. **Docker** simplifies deployment and scaling, making the setup process easy and efficient.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#1-clone-the-repository)
  - [Run the Application with Docker](#2-run-the-application-with-docker)
- [System Architecture](#system-architecture)
  - [Scalability](#scalability)
  - [Pub/Sub Messaging and Caching with Redis](#pubsub-messaging-and-caching-with-redis)
  - [WebSocket Instance Management](#websocket-instance-management)
  - [Persistent Data with MongoDB](#persistent-data-with-mongodb)
  - [Monitoring & Logging](#monitoring--logging)
- [Scaling the Application](#scaling-the-application)
  - [Scaling FastAPI](#scaling-fastapi)
  - [Scaling Redis and MongoDB](#scaling-redis-and-mongodb)

## Overview
This chat application enables **real-time messaging**, **scalable online status tracking**, and **robust monitoring** using modern backend technologies. 

### How It Works:

1. **Client Interaction (Frontend)**:
   - Users interact with the frontend via a web or mobile application, which connects to the backend using **WebSockets** for real-time messaging.
   - Messages are sent and received instantly, ensuring a seamless chat experience.
   - User authentication is managed via **JWT tokens**, allowing secure access to the chat platform.

2. **Backend Processing (FastAPI & Redis Pub/Sub)**:
   - The **FastAPI** backend processes API requests and WebSocket connections.
   - When a user sends a message, it is published to a **Redis Pub/Sub channel**.
   - All active FastAPI instances subscribe to Redis channels, enabling instant message broadcasting.

3. **Data Storage & Persistence (MongoDB)**:
   - Chat messages are stored persistently in **MongoDB**, ensuring message history is maintained even after service restarts.
   - MongoDB supports **replication and sharding**, allowing for high availability and scalability.

4. **Monitoring & Logging (Prometheus, Grafana, Loki)**:
   - **Prometheus** collects system metrics like API requests, WebSocket connections, and resource usage.
   - **Grafana** provides real-time dashboards to visualize system performance.
   - **Loki** aggregates logs, making debugging and system monitoring more efficient.

5. **Deployment & Scaling (Docker & Docker Compose)**:
   - The entire application runs inside **Docker containers**, ensuring portability and easy setup.
   - **Docker Compose** simplifies the orchestration of multiple services.
   - Horizontal scaling is achieved by running multiple FastAPI instances behind a **load balancer**.

This architecture ensures a **scalable, high-performance chat experience** while maintaining real-time communication, persistent data storage, and robust system monitoring.

## Key Features

- **Real-Time Messaging**: Low-latency chat system powered by Redis Pub/Sub.
- **Horizontal Scalability**: Runs multiple FastAPI instances behind a load balancer.
- **Pub/Sub Architecture**: Uses Redis for message distribution.
- **Persistent Chat History**: Stores messages in MongoDB.
- **Monitoring & Logging**:
  - **Prometheus** for metrics collection.
  - **Grafana** for visualization.
  - **Loki** for centralized logging.

## Tech Stack

- **FastAPI** - High-performance Python web framework.
- **Redis** - In-memory database for real-time Pub/Sub messaging and online status tracking.
- **MongoDB** - NoSQL database for persistent chat storage.
- **Prometheus** - Metrics collection and monitoring.
- **Grafana** - Dashboard visualization for system performance.
- **Loki** - Centralized logging solution for debugging and analytics.
- **Docker** - Containerization for simplified deployment and scaling.

## Installation & Setup

### Prerequisites

- **Python 3.11**
- **Git**
- **Docker & Docker Compose** (if using containers)

### 1. Clone the Repository

```bash
git clone https://github.com/BasuKlizos/chat-application.git
cd chat-application
```

### 2. Run the Application with Docker

The entire system runs inside **Docker containers**, so there is no need to manually install dependencies.

#### Start All Services with Docker Compose

```bash
docker-compose up --build
```

- **Frontend** will be accessible at `http://localhost:3000`.
- **Backend (FastAPI)** will be accessible at `http://localhost:8000`.
- **Grafana** dashboard available at `http://localhost:3001`.
- **Loki logs** can be queried via Grafana.

## System Architecture

### Scalability

The system scales horizontally using **FastAPI replicas** behind a load balancer. Redis and MongoDB efficiently handle increased traffic.

### Pub/Sub Messaging and Caching with Redis

- **FastAPI publishes chat messages** to a Redis channel.
- **All instances subscribe to Redis**, ensuring real-time message delivery.
- **Messages are cached using Redis Sorted Sets**, allowing quick retrieval of recent messages.
- **Clients receive instant updates** when a message is published, and messages are returned from the cache for efficiency.

### WebSocket Instance Management

- A dedicated **WebSocket instance** is created for each user upon connection.
- If **100 users** connect, **100 separate WebSocket instances** are managed, ensuring independent real-time communication.
- This allows for **scalability** while maintaining efficient handling of concurrent connections.

### Persistent Data with MongoDB

- Stores chat history persistently.
- Supports **replication and sharding** for high availability.
- **User message history is fetched** and displayed when they reconnect.


### Monitoring & Logging

This application integrates **Prometheus, Grafana, and Loki** for real-time monitoring, logging, and visualization.

#### Prometheus Metrics

Monitoring is implemented using **Prometheus** with the following key metrics:

- **HTTP Metrics**
  - `http_requests_total`: Total number of HTTP requests.
- **System Resource Metrics**
  - `cpu_usage_percent`: CPU usage percentage.
  - `memory_usage_mb`: Memory usage in MB.
  - `disk_usage_percent`: Disk usage percentage.
- **WebSocket Metrics**
  - `ws_connections_active`: Number of active WebSocket connections.
  - `ws_messages_received_total`: Total WebSocket messages received.
  - `ws_messages_sent_total`: Total WebSocket messages sent.
  - `ws_database_queries_total`: Total database queries during WebSocket sessions.
  - `ws_messages_total`: Total WebSocket messages sent and received.
  - `ws_disconnections_total`: Total WebSocket disconnections.
- **Redis Metrics**
  - `redis_queries_total`: Total number of Redis queries executed.
  - `redis_channels_created_total`: Total Redis Pub/Sub channels created.

#### Grafana Dashboards

- Provides real-time monitoring for system performance and resource usage.
- Fetches metrics from **Prometheus**.
- Displays interactive graphs for **WebSocket activity, system health, Redis performance, and API metrics**.

#### Loki for Logging

- Centralized log aggregation for **backend, Redis, and WebSocket events**.
- Logs can be searched and filtered via **Grafana**.
- Helps in debugging **real-time issues and performance bottlenecks**.

## Scaling the Application

### Scaling FastAPI

Modify `docker-compose.yml` to increase FastAPI replicas:

```yaml
services:
  fastapi:
    deploy:
      replicas: 3  # Adjust replicas as needed
```

### Scaling Redis and MongoDB

- **Redis Cluster**: Deploy multiple Redis instances for high availability.
- **MongoDB Sharding**: Scale MongoDB horizontally by distributing data across shards.

## Acknowledgments

We appreciate your interest in this project! 🎉 This chat application was built with scalability, performance, and real-time communication in mind. A big thank you to all contributors and open-source projects that made this possible.

If you find this project helpful, feel free to ⭐️ the repository, contribute, or share your feedback. Happy coding! 🚀

