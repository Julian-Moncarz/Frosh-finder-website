#!/usr/bin/env python3
"""
Check how many posts from the Instagram dataset are not in all-posts.json by comparing captions
"""
import json

def normalize_caption(caption):
    """Normalize caption for comparison - remove extra spaces and lowercase"""
    if not caption:
        return ""
    # Strip whitespace and convert to lowercase for comparison
    return ' '.join(caption.strip().lower().split())

def check_new_posts():
    """Compare posts between dataset and all-posts.json using captions"""
    
    # Load the cleaned Instagram data
    with open('cleaned_instagram_data.json', 'r', encoding='utf-8') as f:
        instagram_data = json.load(f)
    
    # Load the existing all-posts.json
    with open('all-posts.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # Create normalized caption sets for comparison
    instagram_captions = {normalize_caption(post['caption']) for post in instagram_data['posts']}
    existing_captions = {normalize_caption(post['caption']) for post in existing_data['posts']}
    
    # Find new captions (in Instagram dataset but not in all-posts.json)
    new_captions = instagram_captions - existing_captions
    
    # Find captions that are already in all-posts.json
    duplicate_captions = instagram_captions & existing_captions
    
    # Get the actual new posts
    new_posts = []
    duplicate_posts = []
    
    for post in instagram_data['posts']:
        normalized = normalize_caption(post['caption'])
        if normalized in new_captions:
            new_posts.append(post)
        elif normalized in duplicate_captions:
            duplicate_posts.append(post)
    
    print(f"📊 Dataset Analysis (by Caption):")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📁 Instagram dataset: {len(instagram_data['posts'])} posts")
    print(f"📁 all-posts.json: {len(existing_data['posts'])} posts")
    print(f"")
    print(f"🆕 NEW posts (not in all-posts.json): {len(new_posts)}")
    print(f"♻️  Duplicate posts (already exist): {len(duplicate_posts)}")
    print(f"")
    
    if new_posts:
        print(f"Sample of new posts:")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for i, post in enumerate(new_posts[:3], 1):
            caption_preview = post['caption'][:100] + "..." if len(post['caption']) > 100 else post['caption']
            print(f"{i}. {caption_preview}")
            print(f"   URL: {post['post_url']}")
            print()
    
    if duplicate_posts:
        print(f"Sample of duplicate posts:")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for i, post in enumerate(duplicate_posts[:3], 1):
            caption_preview = post['caption'][:50] + "..." if len(post['caption']) > 50 else post['caption']
            print(f"{i}. {caption_preview}")
    
    return new_posts, duplicate_posts

if __name__ == "__main__":
    new_posts, duplicate_posts = check_new_posts()