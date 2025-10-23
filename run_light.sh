#!/bin/bash
# ------------------------------------------
# OSINT-Phone-Tool — run_light.sh
# Created by MJ & Elara (2025)
# ------------------------------------------

echo "🚀 Running OSINT-Phone-Tool (Light Mode)..."

# Pastikan dependencies sudah terpasang
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please run install_termux.sh first."
    exit 1
fi

# Pastikan file numbers.txt ada
if [ ! -f "numbers.txt" ]; then
    echo "⚠️  File numbers.txt not found."
    echo "Create one or copy from numbers.txt.example"
    exit 1
fi

# Jalankan tool utama
python3 osint_phone_tool_light.py numbers.txt

# Pindahkan hasil ke storage (jika folder tersedia)
if [ -d "/storage/emulated/0/Download" ]; then
    mkdir -p /storage/emulated/0/Download/osint_output
    cp -r osint_output/* /storage/emulated/0/Download/osint_output/ 2>/dev/null
    echo "📁 Results copied to internal storage: /storage/emulated/0/Download/osint_output/"
fi

echo "✅ Done! Check osint_output folder for results."
