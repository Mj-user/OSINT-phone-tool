#!/bin/bash
# ------------------------------------------
# OSINT-Phone-Tool — install_termux.sh
# Created by MJ & Elara (2025)
# ------------------------------------------

echo "📦 Starting installation for OSINT-Phone-Tool..."
echo "Updating packages..."
pkg update -y && pkg upgrade -y

echo "Installing Python & Git..."
pkg install python git -y

echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Creating output folder..."
mkdir -p osint_output logs

echo "✅ Installation complete!"
echo "You can now run: python osint_phone_tool_light.py numbers.txt"
