from prometheus_client import Counter, Gauge


# Users
USER_REGISTRATIONS = Counter(
    "user_registrations_total", "Total number of registered users"
)

# HTTP Metrics
HTTP_REQUESTS = Counter("http_requests_total", "Total number of HTTP requests")

# System Resource Metrics
CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage percentage")
MEMORY_USAGE = Gauge("memory_usage_mb", "Memory usage in MB")
DISK_USAGE = Gauge("disk_usage_percent", "Disk usage percentage")

# WebSocket Metrics
WS_CONNECTIONS = Gauge(
    "ws_connections_active", "Number of active WebSocket connections"
)
WS_MESSAGES_RECEIVED = Counter(
    "ws_messages_received_total", "Total WebSocket messages received"
)
WS_MESSAGES_SENT = Counter("ws_messages_sent_total", "Total WebSocket messages sent")
WS_DB_QUERIES = Counter(
    "ws_database_queries_total",
    "Total number of database queries during WebSocket sessions",
)
WS_MESSAGES_TOTAL = Counter(
    "ws_messages_total", "Total number of WebSocket messages sent and received"
)
WS_CONNECTIONS_DISC = Gauge(
    "ws_disconnections_total", "Total number of WebSocket disconnections"
)

# Redis Metrics
REDIS_QUERIES_TOTAL = Counter(
    "redis_queries_total", "Total number of Redis queries executed"
)
REDIS_CHANNELS_CREATED = Counter(
    "redis_channels_created_total", "Total Redis Pub/Sub channels created"
)
