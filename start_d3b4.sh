#!/bin/bash
export A0_ROOT=/d3b4
export PYTHONPATH=/d3b4
export VIRTUAL_ENV=/d3b4/.venv
export PATH="/d3b4/.venv/bin:$PATH"
export IS_DOCKERIZED=true
export SHELL_INTERFACE=local
export A0_SET_SHELL_INTERFACE=local
export A0_SET_CODE_EXEC_SSH_ENABLED=false

# Initialize required directories and files
mkdir -p /d3b4/usr /d3b4/logs /d3b4/tmp /d3b4/usr/chats

# Initialize .env if missing
if [ ! -s /d3b4/usr/.env ] && [ -f /d3b4/.env ]; then
    cp /d3b4/.env /d3b4/usr/.env
    echo "[d3b4] Initialized /d3b4/usr/.env from base .env"
elif [ ! -f /d3b4/usr/.env ]; then
    touch /d3b4/usr/.env
    echo "[d3b4] Created empty /d3b4/usr/.env"
fi

echo "[d3b4] Born of deby-lite. Starting on 0.0.0.0:${PORT:-8080}..."
cd /d3b4
exec /d3b4/.venv/bin/python run_ui.py --port ${PORT:-8080} --host 0.0.0.0 --dockerized=true
