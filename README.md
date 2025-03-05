# Chat Application

A real-time chat application designed for scalability. This project combines a FastAPI backend, WebSocket support for real-time communication, Celery for background processing, MongoDB as the database, and Redis for caching and pub/sub messaging. The system is instrumented with Prometheus for monitoring and Grafana for visualizing metrics.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
  - [Backend Overview](#backend-overview)
    - [FastAPI & WebSockets](#fastapi--websockets)
    - [Database (MongoDB)](#database-mongodb)
    - [Caching & Pub/Sub (Redis)](#caching--pubsub-redis)
    - [Background Tasks (Celery)](#background-tasks-celery)
    - [Monitoring (Prometheus & Grafana)](#monitoring-prometheus--grafana)
  - [Frontend Overview](#frontend-overview)
- [Setup and Running](#setup-and-running)
- [Client Usage](#client-usage)
- [Testing and Load Simulation](#testing-and-load-simulation)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Overview

This chat application enables real-time messaging between users. The backend processes WebSocket connections for live chat and REST API calls for tasks such as authentication and chat history retrieval. The system offloads database operations and other heavy tasks to Celery workers while caching frequently requested chat data in Redis. Monitoring is handled via Prometheus (which scrapes application metrics) and visualized through Grafana dashboards.

## Architecture

### Backend Overview

The backend is the heart of the system and is built using FastAPI. It is responsible for handling real-time connections, storing messages, and providing a robust API for user management and chat retrieval.

#### FastAPI & WebSockets

- **REST Endpoints:**  
  FastAPI provides several HTTP endpoints for user authentication, chat history retrieval, and other functionalities.
  
- **WebSocket Endpoint:**  
  The `/ws/{user_id}` endpoint enables persistent, two-way communication. Clients connect via WebSocket to send and receive messages in real time.
  
- **CORS Configuration:**  
  CORS middleware is configured to allow requests from any origin, ensuring seamless communication with the frontend.

#### Database (MongoDB)

- **MongoDB Storage:**  
  Chat messages and user data are stored in MongoDB. The application uses the Motor asynchronous driver for efficient, non-blocking database operations.
  
- **Serialization:**  
  Custom serialization functions are implemented to convert MongoDB-specific types (such as ObjectId and datetime) into JSON-serializable formats.

#### Caching & Pub/Sub (Redis)

- **Caching:**  
  Chat histories are cached in Redis using sorted sets. Keys are constructed by sorting user IDs to maintain consistency. This cache helps in fast retrieval of chat history without querying the database every time.
  
- **Pub/Sub Messaging:**  
  Redis also facilitates real-time messaging between clients by publishing messages to specific channels, ensuring that messages are delivered across multiple instances in a distributed setup.

#### Background Tasks (Celery)

- **Task Offloading:**  
  Celery is used to offload time-consuming tasks such as storing messages to MongoDB. Tasks are queued in a message broker (Redis) and processed asynchronously by dedicated worker processes.
  
- **Event Loop Management:**  
  Celery tasks use a fresh event loop for every task to avoid issues like the "Event loop is closed" error, ensuring robust processing.
  
- **Task Monitoring:**  
  Flower is used as a monitoring dashboard to track task execution, failures, and performance metrics for Celery workers.

#### Monitoring (Prometheus & Grafana)

- **Prometheus Metrics:**  
  The application is instrumented with Prometheus. Custom middleware and counters track HTTP requests, CPU and memory usage, and WebSocket events. Metrics are exposed on a `/metrics` endpoint.
  
- **Grafana Dashboards:**  
  Grafana visualizes the metrics scraped by Prometheus, providing real-time insights into system performance and usage trends.

### Frontend Overview

- **Frontend Application:**  
  The frontend is built using a modern JavaScript framework (e.g., React, Angular, or Vue.js) and runs on a separate port (typically 3000). It handles user interactions, displays chat messages, and manages WebSocket connections.
  
- **WebSocket Client:**  
  The frontend connects to the backend WebSocket endpoint (e.g., `ws://<backend-host>:8000/ws/{user_id}`) for real-time communication.
  
- **REST API Integration:**  
  For authentication, chat history retrieval, and other functionalities, the frontend communicates with the backend through RESTful API endpoints.

## Setup and Running

### Prerequisites

- **Python 3.11+** (for backend development)
- **Node.js** (for frontend development, if applicable)
- **MongoDB** and **Redis** installed or available via cloud services
- **Celery** and **Prometheus/Grafana** are part of the deployment environment

### Running the Backend

1. **Install Dependencies:**

   ```bash
   cd backend
   pip install -r requirements.txt
