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

When given new data in a separate JSON file:

1. **Clean raw data**: Use `utils/clean_instagram_data.py` to convert raw apify output to all-posts.json format
2. **Check for new posts**: Use `utils/check_new_posts_by_caption.py` to identify which posts are truly new (compares by caption text, not URL)
3. **Analyze post dates**: Use `utils/check_post_dates.py` to see when new posts are from and group them by date
4. **Merge new posts**: Use `utils/merge_new_posts.py` to add only new posts to all-posts.json
5. The cleaning process preserves the original Instagram post timestamps in the added_at field

### Utility Scripts (in utils/ folder)

- **clean_instagram_data.py**: Converts raw Instagram scraper JSON to cleaned format matching all-posts.json structure
- **check_new_posts_by_caption.py**: Compares posts by normalized captions to identify truly new content
- **check_new_posts.py**: Compares posts by URL (less reliable for duplicates)
- **check_post_dates.py**: Analyzes timestamps of posts to show date ranges and distribution
- **merge_new_posts.py**: Safely merges only new posts into all-posts.json without creating duplicates

Note: remeber to git pull before checking if there are new posts in the seperate JSON.
