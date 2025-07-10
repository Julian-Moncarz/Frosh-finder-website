# UofT Instagram Posts - Simple All Posts Search

A simple, searchable database of **ALL** Instagram posts from @uoft_frosh.29 - no fancy AI processing, just raw searchable content.

## 📊 Current Data

- **1,065 total posts** from Instagram
- **3.5MB** of post data
- **Case-insensitive search** through all captions
- **Direct links** to original Instagram posts

## 🚀 Quick Start

1. **Build the data file:**
   ```bash
   python3 build_all_posts.py
   ```

2. **Start local server:**
   ```bash
   ./deploy-simple.sh
   ```

3. **Open in browser:**
   - http://localhost:8004/simple-index.html

## 📁 Files

- `simple-index.html` - The search interface (16KB)
- `all-posts.json` - All post data (3.5MB)
- `build_all_posts.py` - Data processing script
- `deploy-simple.sh` - Local deployment script

## 🔍 What You Get

Each post card shows:

- **Full caption text** (first 300 chars shown, expandable)
- **Post date** and **type** (carousel, single image, video)
- **Engagement stats** (likes, comments, images)
- **Direct link** to view the original post on Instagram

## 📱 Search Features

- **Case-insensitive** text search
- **Real-time filtering** as you type
- **Clear search** button
- **Search statistics** showing results count
- **Enter key** to search, **Escape** to clear

## 🌐 Production Deployment

For public hosting, just upload these 2 files to any static web host:

- `simple-index.html`
- `all-posts.json`

Works great with:
- GitHub Pages
- Netlify
- Vercel
- Any static hosting service

## 🔄 Updating Data

When you have new Instagram data:

1. Update `../data/posts.json` with new posts
2. Run `python3 build_all_posts.py`
3. Upload the new `all-posts.json` to your host

## 💡 Why This Approach?

- **No AI complexity** - just shows what's actually there
- **All posts included** - nothing filtered out
- **Fast and simple** - loads quickly, searches instantly
- **Static hosting** - cheap/free to deploy anywhere
- **Direct access** - one click to original Instagram posts

Perfect for anyone who wants to browse and search through ALL the content without any automated filtering! 