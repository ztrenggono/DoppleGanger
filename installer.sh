#!/bin/bash

echo "🚀 Installing Doppelgänger Toolkit..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "📦 Python3 not found. Installing Python3..."
    apt update && apt install -y python3 python3-pip
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "📦 pip not found. Installing pip..."
    apt update && apt install -y python3-pip
fi

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip3 install -r requirements.txt

# Make the script executable
chmod +x doppelganger.py

# Create global command
echo "🔗 Creating global command 'doppelganger'..."
cp doppelganger.py /usr/local/bin/doppelganger

echo "✅ Installation complete! You can now run 'doppelganger' from anywhere."
echo "⚠️ Note: Some features require root privileges. Run with sudo when needed." 