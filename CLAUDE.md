# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the U of T Frosh Finder website - a searchable interface for University of Toronto frosh introduction posts from @uoft_frosh.29 Instagram account. The project consists of a static website hosted on GitHub Pages that allows students to search through frosh posts to find roommates or people in their programs.

## Commands

### Development
- **Run local server**: `python3 serve.py` - Starts a local HTTP server on port 8000 and auto-opens the website
- **Install dependencies**: `pip install -r requirements.txt` - Installs required Python packages (requests, feedparser, python-dateutil)

### Testing RSS Monitor
- **Test RSS monitor locally**: `RSS_FEED_URL='https://rss.app/feeds/50UzjpI64E8EaBUf.xml' python3 scripts/rss_monitor.py`
- **Manual GitHub Actions trigger**: Can be triggered manually from GitHub Actions tab with optional `force_update` parameter

## Architecture

### Data Flow
1. **RSS Feed Integration**: Instagram posts from @uoft_frosh.29 are converted to RSS feed via rss.app service
2. **Automated Updates**: GitHub Actions workflow (`rss-monitor.yml`) runs daily at 9 AM UTC to fetch new posts
3. **Data Processing**: `scripts/rss_monitor.py` fetches RSS feed, cleans HTML content, and merges new posts into `all-posts.json`
4. **Frontend**: Single-page `index.html` loads all posts from `all-posts.json` and provides client-side search functionality

### Key Files
- **all-posts.json**: Main data file containing all frosh posts with structure: `{total_posts: number, posts: [{caption, post_url, added_at}]}`
- **index.html**: Frontend with search functionality, filters (year toggle), and responsive grid layout
- **scripts/rss_monitor.py**: RSS monitoring script that handles deduplication, HTML cleaning, and data merging
- **serve.py**: Local development server for testing

### GitHub Actions Automation
The RSS monitor workflow automatically:
- Fetches new posts from RSS feed
- Merges with existing posts (deduplicates by post_url)
- Commits changes with bot account
- Updates live site via GitHub Pages

## Important Notes
- The site is static and hosted on GitHub Pages at: https://julian-moncarz.github.io/Frosh-finder-website/
- Posts are deduplicated by Instagram post URL to prevent duplicates
- The RSS monitor preserves only essential fields (caption, post_url, added_at) to minimize file size
- Year filter is enabled by default showing only current year posts

## Data Cleaning for New Instagram Datasets
When importing new Instagram data from scraping tools:
1. Use `clean_instagram_data.py` to convert raw Instagram scraper output to all-posts.json format
2. The script extracts: caption, post_url, and timestamp (uses Instagram's original timestamp as added_at)
3. Use `check_new_posts_by_caption.py` to identify which posts are truly new (compares by caption text, not URL)
4. The cleaning process preserves the original Instagram post timestamps in the added_at field