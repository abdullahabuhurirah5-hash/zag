#!/bin/bash

# Start both services in parallel

echo "Starting user-service on port 8002..."
cd user-service
export POSTGRES_URI="sqlite+aiosqlite:///:memory:"
uvicorn app.main:app --reload --port 8002 &
USER_SERVICE_PID=$!

echo "Starting orders-service on port 8001..."
cd ../orders-service
export POSTGRES_URI="sqlite+aiosqlite:///:memory:"
uvicorn app.main:app --reload --port 8001 &
ORDERS_SERVICE_PID=$!

echo "Both services started:"
echo "  Orders Service: http://localhost:8001/docs"
echo "  User Service: http://localhost:8002/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait $USER_SERVICE_PID $ORDERS_SERVICE_PID
