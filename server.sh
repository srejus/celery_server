#!/bin/bash
set -e

BASE_DIR="/home/administrator/celery_server/celery_server"
VENV_DIR="/home/administrator/celery_server/venv/bin"
PROJECT_NAME="celery_server"
PORT=1211

LOG_DIR="$BASE_DIR/logs"

GUNICORN_LOG="$LOG_DIR/gunicorn.log"
CELERY_LOG="$LOG_DIR/celery_worker.log"
BEAT_LOG="$LOG_DIR/celery_beat.log"

mkdir -p "$LOG_DIR"

start_servers() {

    echo "Starting Gunicorn..."

    "$VENV_DIR/gunicorn" "$PROJECT_NAME.wsgi:application" \
        --bind 0.0.0.0:$PORT \
        --workers 2 \
        --timeout 120 \
        --log-level info \
        --access-logfile "$GUNICORN_LOG" \
        --error-logfile "$GUNICORN_LOG" &

    DJANGO_PID=$!

    echo "Starting Celery worker..."

    "$VENV_DIR/celery" -A "$PROJECT_NAME" worker -l info \
        > "$CELERY_LOG" 2>&1 &

    CELERY_PID=$!

    echo "Starting Celery Beat..."

    "$VENV_DIR/celery" -A "$PROJECT_NAME" beat -l info \
        > "$BEAT_LOG" 2>&1 &

    BEAT_PID=$!

    echo $DJANGO_PID > "$BASE_DIR/gunicorn.pid"
    echo $CELERY_PID > "$BASE_DIR/celery.pid"
    echo $BEAT_PID > "$BASE_DIR/celerybeat.pid"

    echo "Servers started successfully."
}

stop_servers() {

    echo "Stopping servers..."

    if [ -f "$BASE_DIR/gunicorn.pid" ]; then
        kill -9 $(cat "$BASE_DIR/gunicorn.pid") || true
        rm "$BASE_DIR/gunicorn.pid"
    fi

    if [ -f "$BASE_DIR/celery.pid" ]; then
        kill -9 $(cat "$BASE_DIR/celery.pid") || true
        rm "$BASE_DIR/celery.pid"
    fi

    if [ -f "$BASE_DIR/celerybeat.pid" ]; then
        kill -9 $(cat "$BASE_DIR/celerybeat.pid") || true
        rm "$BASE_DIR/celerybeat.pid"
    fi

    echo "All servers stopped."
}

case "$1" in
    start)
        start_servers
        ;;
    stop)
        stop_servers
        ;;
    restart)
        stop_servers
        sleep 2
        start_servers
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0