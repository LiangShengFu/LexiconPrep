#!/bin/bash
set -e

echo "Waiting for database..."
max_retries=30
retry=0
while [ $retry -lt $max_retries ]; do
  if python -c "
import asyncio
from sqlalchemy import text
from app.core.database import engine
async def check():
    async with engine.connect() as conn:
        await conn.execute(text('SELECT 1'))
asyncio.run(check())
" 2>/dev/null; then
    echo "Database is ready."
    break
  fi
  retry=$((retry + 1))
  echo "Retry $retry/$max_retries..."
  sleep 2
done

if [ $retry -eq $max_retries ]; then
  echo "Database not ready after $max_retries retries, proceeding anyway..."
fi

echo "Running init_db..."
python init_db.py

echo "Running seed..."
python seed.py

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
