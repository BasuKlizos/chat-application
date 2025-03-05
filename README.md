# Real-Time Chat Application with Horizontal Scalability

A high-performance, real-time chat application built with **FastAPI**, **Redis**, **MongoDB**, **Loki**, **Prometheus**, and **Grafana**. Designed for **horizontal scalability**, it efficiently handles high traffic and large user bases.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
  - [Clone the Repository](#1-clone-the-repository)
  - [Setup Environment Variables](#2-setup-environment-variables)
  - [Run the Application](#3-run-the-application)
- [System Architecture](#system-architecture)
  - [Scalability](#scalability)
  - [Pub/Sub Messaging with Redis](#pubsub-messaging-with-redis)
  - [Persistent Data with MongoDB](#persistent-data-with-mongodb)
  - [Monitoring & Logging](#monitoring--logging)
- [Scaling the Application](#scaling-the-application)
  - [Scaling FastAPI](#scaling-fastapi)
  - [Scaling Redis and MongoDB](#scaling-redis-and-mongodb)
- [License](#license)

## Overview
This chat application enables **real-time messaging**, **scalable online status tracking**, and **robust monitoring** using modern backend technologies. It leverages **Docker** and **Docker Compose** to ensure seamless deployment and scalability.

## Key Features

- **Real-Time Messaging**: Low-latency chat system powered by Redis Pub/Sub.
- **Horizontal Scalability**: Runs multiple FastAPI instances behind a load balancer.
- **Pub/Sub Architecture**: Uses Redis for message distribution.
- **Persistent Chat History**: Stores messages in MongoDB.
- **Monitoring & Logging**:
  - **Prometheus** for metrics collection.
  - **Grafana** for visualization.
  - **Loki** for centralized logging.
- **Online Status Tracking**: Redis efficiently manages online users across multiple instances.

## Tech Stack

- **FastAPI** - High-performance Python web framework.
- **Redis** - In-memory database for real-time Pub/Sub messaging and online status tracking.
- **MongoDB** - NoSQL database for persistent chat storage.
- **Prometheus** - Metrics collection and monitoring.
- **Grafana** - Dashboard visualization for system performance.
- **Loki** - Centralized logging solution for debugging and analytics.

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/chatapp.git
cd chatapp
```

### 2. Setup Environment Variables

Copy the example environment file and configure necessary variables:

```bash
cp .example_env .env
```

### 3. Run the Application

Use **Docker Compose** to build and start all services:

```bash
docker-compose up --build
```

- FastAPI will be accessible at `http://localhost:8000`.
- Grafana dashboard available at `http://localhost:3000`.
- Loki logs can be queried via Grafana.

## System Architecture

### Scalability

The system scales horizontally using **FastAPI replicas** behind a load balancer. Redis and MongoDB efficiently handle increased traffic.

### Pub/Sub Messaging with Redis

- **FastAPI publishes chat messages** to a Redis channel.
- **All instances subscribe to Redis**, ensuring real-time message delivery.
- **Clients receive instant updates** when a message is published.

### Persistent Data with MongoDB

- Stores chat history persistently.
- Supports **replication and sharding** for high availability.

### Monitoring & Logging

#### Prometheus Metrics

- **HTTP Requests** (`http_requests_total`, `http_request_duration_seconds`)
- **WebSocket Metrics** (`ws_connections_active`, `ws_messages_total`)
- **System Usage** (`cpu_usage_percent`, `memory_usage_percent`)

#### Grafana Dashboards

- Provides real-time monitoring for system performance and usage.
- Fetches metrics from **Prometheus**.

#### Loki for Logging

- Centralized log aggregation.
- Easily searchable logs via Grafana.

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

## License
This project is licensed under the MIT License.
