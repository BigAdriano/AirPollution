"""
Script to set environment variables from .env file
"""

import os

with open("./.env", "r") as f:
    text = f.read()
text_lines = text.splitlines()
for line in text_lines:
    if "=" in line:
        lines = line.split("=")
        env_name = str(lines[0]).upper()
        env_line = f"{env_name}={lines[1]}"
        os.environ[env_name] = env_line
        print(f"Variable name: {env_name} added")
