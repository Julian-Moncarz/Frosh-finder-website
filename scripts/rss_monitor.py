#!/usr/bin/env python3
"""
RSS Feed Monitor Script
Monitors Instagram RSS feeds and adds new posts to the existing all-posts.json
Only saves essential fields: caption, post_url, and added_at
"""

import os
import json
import requests
import feedparser
import re
from datetime import datetime
from pathlib import Path
from dateutil import parser as date_parser
from html import unescape

class RSSMonitor:
    def __init__(self, rss_url, data_dir="data"):
        self.rss_url = rss_url
        self.data_dir = Path(data_dir)
        self.last_check_file = self.data_dir / "last_check.json"
        self.all_posts_file = Path("all-posts.json")  # Main website file
        
        # Create data directory if it doesn't exist (only for last_check.json)
        self.data_dir.mkdir(exist_ok=True)
    
    def clean_html_content(self, html_content):
        """Clean HTML content to extract just the text for better search"""
        if not html_content:
            return ""
        
        try:
            # First, protect emoticons and special characters like <33 by temporarily replacing them
            html_content = html_content.replace('<33', '&lt;33')
            html_content = html_content.replace('<3', '&lt;3')
            
            # Remove image tags but keep the text content
            html_content = re.sub(r'<img[^>]*>', '', html_content)
            
            # Remove HTML tags but keep the text, preserving line breaks
            html_content = re.sub(r'<[^>]+>', '\n', html_content)
            
            # Unescape HTML entities (including our protected emoticons)
            html_content = unescape(html_content)
            
            # Clean up extra whitespace but preserve line breaks
            html_content = re.sub(r'[ \t]+', ' ', html_content)  # Only collapse spaces and tabs
            html_content = re.sub(r'\n+', '\n', html_content)    # Collapse multiple newlines
            html_content = html_content.strip()
            
            # Replace line breaks with spaces to make it searchable
            html_content = html_content.replace('\n', ' ')
            
            # Final cleanup of extra spaces
            html_content = re.sub(r'\s+', ' ', html_content).strip()
            
            return html_content
            
        except Exception as e:
            print(f"⚠️  Error cleaning HTML content: {e}")
            return html_content
        

    
    def load_all_posts(self):
        """Load the main all-posts.json file"""
        if self.all_posts_file.exists():
            try:
                with open(self.all_posts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Error loading all-posts.json: {e}")
                return {"total_posts": 0, "posts": []}
        return {"total_posts": 0, "posts": []}
    
    def save_all_posts(self, all_posts_data):
        """Save the updated all-posts.json file"""
        try:
            with open(self.all_posts_file, 'w', encoding='utf-8') as f:
                json.dump(all_posts_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Updated all-posts.json with {len(all_posts_data['posts'])} total posts")
        except IOError as e:
            print(f"❌ Error saving all-posts.json: {e}")
    

    def load_last_check(self):
        """Load last check timestamp"""
        if self.last_check_file.exists():
            try:
                with open(self.last_check_file, 'r') as f:
                    data = json.load(f)
                    return data.get('last_check')
            except (json.JSONDecodeError, IOError):
                pass
        return None
    
    def save_last_check(self, timestamp):
        """Save last check timestamp"""
        try:
            with open(self.last_check_file, 'w') as f:
                json.dump({'last_check': timestamp}, f)
        except IOError as e:
            print(f"⚠️  Error saving last check: {e}")
    
    def fetch_rss_feed(self):
        """Fetch and parse RSS feed"""
        try:
            print(f"📡 Fetching RSS feed from: {self.rss_url}")
            
            # Add headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; RSS-Monitor/1.0)',
                'Accept': 'application/rss+xml, application/xml, text/xml'
            }
            
            response = requests.get(self.rss_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                print(f"⚠️  RSS feed has issues: {feed.bozo_exception}")
            
            print(f"📊 Found {len(feed.entries)} entries in RSS feed")
            return feed
            
        except requests.RequestException as e:
            print(f"❌ Error fetching RSS feed: {e}")
            return None
        except Exception as e:
            print(f"❌ Error parsing RSS feed: {e}")
            return None
    
    def rss_to_simplified_format(self, rss_post):
        """Convert RSS post to simplified format (caption, post_url, added_at only)"""
        try:
            # Clean up the HTML caption for better search functionality
            raw_caption = rss_post.get('caption', '')
            cleaned_caption = self.clean_html_content(raw_caption)
            
            # Use current timestamp as added_at since this is when we're adding it
            added_at = datetime.now().isoformat()
            
            # Create simplified post with only essential fields
            simplified_post = {
                'caption': cleaned_caption,
                'post_url': rss_post.get('url', ''),
                'added_at': added_at
            }
            
            print(f"📝 Cleaned caption preview: {cleaned_caption[:100]}...")
            
            return simplified_post
            
        except Exception as e:
            print(f"⚠️  Error converting RSS post format: {e}")
            return None
    
    def parse_rss_entry(self, entry):
        """Convert RSS entry to our post format"""
        try:
            # Extract basic info
            title = entry.get('title', '')
            link = entry.get('link', '')
            description = entry.get('description', '') or entry.get('summary', '')
            
            # Parse publication date
            pub_date = entry.get('published', '') or entry.get('updated', '')
            timestamp = ''
            if pub_date:
                try:
                    dt = date_parser.parse(pub_date)
                    timestamp = dt.isoformat()
                except:
                    timestamp = pub_date
            
            # Create post object for RSS tracking
            post = {
                'url': link,
                'caption': description,
                'timestamp': timestamp,
                'rss_title': title,
                'rss_guid': entry.get('id', '') or entry.get('guid', '') or link,
                'added_at': datetime.now().isoformat()
            }
            
            return post
            
        except Exception as e:
            print(f"⚠️  Error parsing RSS entry: {e}")
            return None
    
    def merge_new_posts_with_existing(self, new_rss_posts):
        """Merge new RSS posts with existing all-posts.json"""
        print("🔄 Merging new posts with existing all-posts.json...")
        
        # Load existing all-posts.json
        all_posts_data = self.load_all_posts()
        existing_posts = all_posts_data.get('posts', [])
        
        # Get existing URLs to avoid duplicates
        existing_urls = {post.get('post_url') for post in existing_posts}
        
        # Convert new RSS posts to simplified format and filter duplicates
        new_posts_to_add = []
        for rss_post in new_rss_posts:
            simplified_post = self.rss_to_simplified_format(rss_post)
            if not simplified_post:
                continue
            
            # Check for duplicates by URL
            if simplified_post['post_url'] not in existing_urls:
                new_posts_to_add.append(simplified_post)
                print(f"✅ Adding new post: {simplified_post['caption'][:50]}...")
        
        if new_posts_to_add:
            # Add new posts to the beginning of the list (most recent first)
            updated_posts = new_posts_to_add + existing_posts
            
            # Update data structure
            all_posts_data['posts'] = updated_posts
            all_posts_data['total_posts'] = len(updated_posts)
            all_posts_data['last_updated'] = datetime.now().isoformat()
            
            # Save updated file
            self.save_all_posts(all_posts_data)
            
            print(f"✅ Added {len(new_posts_to_add)} new posts to all-posts.json")
            print(f"📊 Total posts now: {len(updated_posts)}")
            return True
        else:
            print("ℹ️  No new unique posts to add")
            return False
    
    def check_for_new_posts(self, force_update=False):
        """Check RSS feed for new posts and add them"""
        print("🔍 Checking RSS feed for new posts...")
        
        # Load existing posts from main file to get GUIDs for duplicate checking
        all_posts_data = self.load_all_posts()
        existing_posts = all_posts_data.get('posts', [])
        existing_guids = {post.get('rss_guid') for post in existing_posts if post.get('rss_guid')}
        
        # Fetch RSS feed
        feed = self.fetch_rss_feed()
        if not feed:
            print("❌ Failed to fetch RSS feed")
            return False
        
        # Process new entries
        new_posts = []
        last_check = self.load_last_check()
        
        for entry in feed.entries:
            post = self.parse_rss_entry(entry)
            if not post:
                continue
            
            # Check if this is a new post
            is_new = (
                post['rss_guid'] not in existing_guids or
                force_update
            )
            
            # Also check by timestamp if we have last check time
            if last_check and not force_update:
                try:
                    entry_time = date_parser.parse(post['timestamp'])
                    last_check_time = date_parser.parse(last_check)
                    if entry_time <= last_check_time:
                        is_new = False
                except:
                    pass  # If parsing fails, consider it new
            
            if is_new:
                new_posts.append(post)
                print(f"📝 New post found: {post['rss_title'][:50]}...")
        
        # Merge with existing all-posts.json directly (no intermediate files needed)
        if new_posts:
            has_merged = self.merge_new_posts_with_existing(new_posts)
            
            # Update last check timestamp only if we successfully merged
            if has_merged:
                self.save_last_check(datetime.now().isoformat())
            return has_merged
        else:
            print("ℹ️  No new posts found")
            # Still update last check time
            self.save_last_check(datetime.now().isoformat())
            return False

def main():
    """Main function"""
    # Get configuration from environment variables
    rss_url = os.getenv('RSS_FEED_URL', 'https://rss.app/feeds/50UzjpI64E8EaBUf.xml')
    force_update = os.getenv('FORCE_UPDATE', 'false').lower() == 'true'
    
    print("🚀 RSS Feed Monitor Starting...")
    print("=" * 50)
    print(f"RSS URL: {rss_url}")
    print(f"Force Update: {force_update}")
    print("=" * 50)
    
    # Create monitor and check for new posts
    monitor = RSSMonitor(rss_url)
    
    try:
        has_new_posts = monitor.check_for_new_posts(force_update)
        
        if has_new_posts:
            print("\n🎉 SUCCESS: New posts detected and merged!")
            print("✅ Your website now has the updated posts!")
        else:
            print("\n✅ No new posts - everything is up to date")
            
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 