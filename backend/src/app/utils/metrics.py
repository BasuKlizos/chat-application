from prometheus_client import Counter, Gauge

HTTP_REQUESTS = Counter("http_requests_total", "Total number of HTTP requests")
CPU_USAGE = Gauge("cpu_usage_percent", "CPU usage percentage")
MEMORY_USAGE = Gauge("memory_usage_mb", "Memory usage in MB")

WS_CONNECTIONS = Counter(
    "ws_connections_total", "Total number of WebSocket connections"
)
WS_MESSAGES_RECEIVED = Counter(
    "ws_messages_received_total", "Total number of WebSocket messages received"
)
WS_MESSAGES_SENT = Counter(
    "ws_messages_sent_total", "Total number of WebSocket messages sent"
)
