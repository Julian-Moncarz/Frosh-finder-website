#!/usr/bin/env python3
"""
Check how many posts from the Instagram dataset are not in all-posts.json
"""
import json

def check_new_posts():
    """Compare posts between dataset and all-posts.json"""
    
    # Load the cleaned Instagram data
    with open('cleaned_instagram_data.json', 'r', encoding='utf-8') as f:
        instagram_data = json.load(f)
    
    # Load the existing all-posts.json
    with open('all-posts.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    # Extract URLs from both datasets
    instagram_urls = {post['post_url'] for post in instagram_data['posts']}
    existing_urls = {post['post_url'] for post in existing_data['posts']}
    
    # Find new posts (in Instagram dataset but not in all-posts.json)
    new_urls = instagram_urls - existing_urls
    
    # Find posts that are already in all-posts.json
    duplicate_urls = instagram_urls & existing_urls
    
    # Get the actual new posts
    new_posts = [post for post in instagram_data['posts'] if post['post_url'] in new_urls]
    
    print(f"📊 Dataset Analysis:")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📁 Instagram dataset: {len(instagram_urls)} posts")
    print(f"📁 all-posts.json: {len(existing_urls)} posts")
    print(f"")
    print(f"🆕 NEW posts (not in all-posts.json): {len(new_urls)}")
    print(f"♻️  Duplicate posts (already exist): {len(duplicate_urls)}")
    print(f"")
    
    if new_urls:
        print(f"Sample of new posts:")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        for i, post in enumerate(new_posts[:3], 1):
            caption_preview = post['caption'][:100] + "..." if len(post['caption']) > 100 else post['caption']
            print(f"{i}. {caption_preview}")
            print(f"   URL: {post['post_url']}")
            print()
    
    return new_posts

if __name__ == "__main__":
    new_posts = check_new_posts()