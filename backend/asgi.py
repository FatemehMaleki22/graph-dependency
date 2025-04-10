"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from starlette.routing import Mount
from graph.api import router as graph_router
from fastapi.middleware.cors import CORSMiddleware


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# FastAPI app
fastapi_app = FastAPI()
fastapi_app.include_router(graph_router)

# Django app (asgi compatible)
django_app = get_asgi_application()

from starlette.applications import Starlette

app = Starlette(
    routes=[
        Mount("/api", app=fastapi_app),    
        Mount("/", app=django_app),      
    ]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # یا پورت فرانتت
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

