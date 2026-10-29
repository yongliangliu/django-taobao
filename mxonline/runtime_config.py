# -*- coding: utf-8 -*-
"""Deployment configuration. Secret values must never be committed."""
import os


def required_env(name):
    value = os.environ.get(name)
    if value is None or not value.strip():
        raise RuntimeError("Missing required environment variable: " + name)
    return value
