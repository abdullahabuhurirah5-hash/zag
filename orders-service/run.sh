#!/bin/bash

export POSTGRES_URI="sqlite+aiosqlite:///:memory:"
uvicorn app.main:app --reload --port 8000
