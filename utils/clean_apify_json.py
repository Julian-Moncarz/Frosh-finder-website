#!/usr/bin/env python3
"""
Clean Instagram dataset to match all-posts.json format
"""
import json
from datetime import datetime

def clean_instagram_data(input_file, output_file):
    """Clean Instagram scraper data to match all-posts.json format"""
    
    # Load the raw Instagram data
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    # Prepare cleaned posts list
    cleaned_posts = []
    
    for post in raw_data:
        # Extract only the fields we need
        cleaned_post = {
            "caption": post.get("caption", ""),
            "post_url": post.get("url", ""),
            "added_at": post.get("timestamp", datetime.now().isoformat())  # Use Instagram timestamp if available
        }
        
        # Only add posts that have both caption and URL
        if cleaned_post["caption"] and cleaned_post["post_url"]:
            cleaned_posts.append(cleaned_post)
    
    # Create the final structure matching all-posts.json
    final_data = {
        "total_posts": len(cleaned_posts),
        "posts": cleaned_posts
    }
    
    # Write the cleaned data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Cleaned {len(cleaned_posts)} posts")
    print(f"📄 Saved to: {output_file}")
    
    return final_data

if __name__ == "__main__":
    input_file = "dataset_instagram-scraper_2025-08-31_13-58-44-819.json"
    output_file = "cleaned_instagram_data.json"
    
    clean_instagram_data(input_file, output_file)