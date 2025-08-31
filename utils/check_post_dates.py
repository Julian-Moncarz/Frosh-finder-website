#!/usr/bin/env python3
"""
Check the dates of posts in the Instagram dataset
"""
import json
from datetime import datetime

def check_post_dates():
    """Check when the posts are from"""
    
    # Load the raw Instagram data to get timestamps
    with open('dataset_instagram-scraper_2025-08-31_13-58-44-819.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # Load the cleaned data
    with open('cleaned_instagram_data.json', 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)
    
    # Load existing posts
    with open('all-posts.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # Get normalized captions for comparison
    def normalize_caption(caption):
        if not caption:
            return ""
        return ' '.join(caption.strip().lower().split())
    
    existing_captions = {normalize_caption(post['caption']) for post in existing_data['posts']}
    
    # Collect dates for new posts
    new_post_dates = []
    all_post_dates = []
    
    for raw_post in raw_data:
        if 'timestamp' in raw_post:
            timestamp = raw_post['timestamp']
            caption = raw_post.get('caption', '')
            normalized = normalize_caption(caption)
            
            # Parse the timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                all_post_dates.append(dt)
                
                # Check if this is a new post
                if normalized and normalized not in existing_captions:
                    new_post_dates.append(dt)
            except:
                pass
    
    if new_post_dates:
        new_post_dates.sort()
        all_post_dates.sort()
        
        print(f"📅 Post Date Analysis:")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"\n📊 All posts in dataset ({len(all_post_dates)} posts):")
        print(f"  Earliest: {all_post_dates[0].strftime('%B %d, %Y at %I:%M %p')}")
        print(f"  Latest:   {all_post_dates[-1].strftime('%B %d, %Y at %I:%M %p')}")
        
        print(f"\n🆕 New posts only ({len(new_post_dates)} posts):")
        print(f"  Earliest: {new_post_dates[0].strftime('%B %d, %Y at %I:%M %p')}")
        print(f"  Latest:   {new_post_dates[-1].strftime('%B %d, %Y at %I:%M %p')}")
        
        # Group by date
        from collections import defaultdict
        posts_by_date = defaultdict(int)
        for dt in new_post_dates:
            date_key = dt.strftime('%B %d, %Y')
            posts_by_date[date_key] += 1
        
        print(f"\n📆 New posts by date:")
        for date, count in sorted(posts_by_date.items(), key=lambda x: datetime.strptime(x[0], '%B %d, %Y'), reverse=True):
            print(f"  {date}: {count} posts")

if __name__ == "__main__":
    check_post_dates()