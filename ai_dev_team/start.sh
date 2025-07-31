#!/bin/bash

# AI Development Team Startup Script

echo "🤖 AI Development Team - Startup Script"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "src/ai_dev_team/main.py" ]; then
    echo "❌ Please run this script from the ai_dev_team directory"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🐍 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found. Please run setup_dev_team.py first."
    exit 1
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🚀 Starting Ollama..."
    ollama serve &
    sleep 5
fi

# Check if required models are available
echo "🔍 Checking AI models..."
if ! ollama list | grep -q "llama3.2:3b"; then
    echo "📥 Downloading llama3.2:3b model..."
    ollama pull llama3.2:3b
fi

if ! ollama list | grep -q "codellama:7b"; then
    echo "📥 Downloading codellama:7b model..."
    ollama pull codellama:7b
fi

if ! ollama list | grep -q "nomic-embed-text"; then
    echo "📥 Downloading nomic-embed-text model..."
    ollama pull nomic-embed-text
fi

echo "✅ All models ready!"
echo ""

# Show usage options
echo "🎯 Usage Options:"
echo "1. Full development workflow:"
echo "   python src/ai_dev_team/main.py "Your project description""
echo ""
echo "2. Custom workflow:"
echo "   python src/ai_dev_team/main.py --custom"
echo ""
echo "3. Interactive mode:"
echo "   python src/ai_dev_team/main.py"
echo ""

# Ask user what they want to do
read -p "Choose an option (1/2/3) or press Enter to exit: " choice

case $choice in
    1)
        read -p "Enter your project description: " project_desc
        python src/ai_dev_team/main.py "$project_desc"
        ;;
    2)
        python src/ai_dev_team/main.py --custom
        ;;
    3)
        python src/ai_dev_team/main.py
        ;;
    *)
        echo "👋 Goodbye!"
        ;;
esac

# Deactivate virtual environment
deactivate
