#!/usr/bin/env python3
"""
Merge new posts from cleaned_instagram_data.json into all-posts.json
"""
import json

def normalize_caption(caption):
    """Normalize caption for comparison"""
    if not caption:
        return ""
    return ' '.join(caption.strip().lower().split())

def merge_new_posts():
    """Merge only new posts into all-posts.json"""
    
    # Load the cleaned Instagram data
    with open('cleaned_instagram_data.json', 'r', encoding='utf-8') as f:
        instagram_data = json.load(f)
    
    # Load the existing all-posts.json
    with open('all-posts.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # Create normalized caption set for existing posts
    existing_captions = {normalize_caption(post['caption']) for post in existing_data['posts']}
    
    # Find and add only new posts
    new_posts_added = 0
    for post in instagram_data['posts']:
        normalized = normalize_caption(post['caption'])
        if normalized not in existing_captions:
            existing_data['posts'].append(post)
            existing_captions.add(normalized)  # Prevent duplicates within this run
            new_posts_added += 1
    
    # Update total count
    existing_data['total_posts'] = len(existing_data['posts'])
    
    # Save the updated data
    with open('all-posts.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Added {new_posts_added} new posts to all-posts.json")
    print(f"📊 Total posts now: {existing_data['total_posts']}")
    
    return new_posts_added

if __name__ == "__main__":
    merge_new_posts()