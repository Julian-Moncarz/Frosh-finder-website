#!/bin/bash

echo "🔍 UofT Instagram Posts - Simple All Posts Deployment"
echo "======================================================"

# Check if required files exist
if [ ! -f "simple-index.html" ]; then
    echo "❌ simple-index.html not found"
    exit 1
fi

if [ ! -f "all-posts.json" ]; then
    echo "❌ all-posts.json not found - run: python3 build_all_posts.py"
    exit 1
fi

# Show file sizes
echo "✅ Required files found:"
echo "   📄 simple-index.html ($(du -h simple-index.html | cut -f1))"
echo "   📊 all-posts.json ($(du -h all-posts.json | cut -f1))"

# Kill any existing servers
pkill -f "http.server" 2>/dev/null

echo "🚀 Starting local test server on port 8004..."
echo "🌐 Open: http://localhost:8004/simple-index.html"
echo "💡 For production deployment:"
echo "   • Upload simple-index.html + all-posts.json to any web host"
echo "   • GitHub Pages, Netlify, Vercel all work great"
echo "📱 Press Ctrl+C to stop the server"

# Start server
python3 -m http.server 8004 