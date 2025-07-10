#!/usr/bin/env python3
"""
Simple All Posts Builder - Shows every post with caption and link
No fancy AI processing, just raw searchable post data
"""

import json
from pathlib import Path
from datetime import datetime

class AllPostsExtractor:
    """Simple extractor that shows all posts"""
    
    def __init__(self, data_file="../data/posts.json"):
        self.data_file = Path(data_file)
    
    def build_all_posts(self):
        """Load all posts and format them simply"""
        if not self.data_file.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_file}")
        
        print(f"📂 Loading data from: {self.data_file}")
        
        with open(self.data_file, 'r', encoding='utf-8') as f:
            all_posts = json.load(f)
        
        print(f"📊 Loaded {len(all_posts)} posts")
        
        # Convert all posts to simple format
        simple_posts = []
        
        for post in all_posts:
            caption_text = post.get('caption', '').strip()
            
            # Skip posts with no caption
            if not caption_text:
                continue
            
            # Parse timestamp for date display
            timestamp_str = post.get('timestamp', '')
            post_date = ''
            if timestamp_str:
                try:
                    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    post_date = dt.strftime('%B %d, %Y')
                except:
                    post_date = ''
            
            simple_post = {
                'caption': caption_text,
                'post_url': post.get('url', ''),
                'post_type': post.get('type', ''),
                'likes': post.get('likesCount', 0) if post.get('likesCount') != -1 else 0,
                'comments': post.get('commentsCount', 0),
                'date': post_date,
                'has_images': len(post.get('images', [])) > 0
            }
            
            simple_posts.append(simple_post)
        
        print(f"📝 Processed {len(simple_posts)} posts with captions")
        
        response_data = {
            'total_posts': len(all_posts),
            'posts_with_captions': len(simple_posts),
            'posts': simple_posts,
            'generated_at': datetime.now().isoformat(),
            'data_source': str(self.data_file)
        }
        
        return response_data

def main():
    """Build the simple all-posts.json file"""
    print("🔨 Building simple all-posts.json...")
    print("=" * 50)
    
    try:
        # Create extractor and process data
        extractor = AllPostsExtractor()
        data = extractor.build_all_posts()
        
        # Save to all-posts.json
        output_file = Path("all-posts.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully built: {output_file}")
        print(f"📊 Total posts: {data['total_posts']}")
        print(f"📝 Posts with captions: {data['posts_with_captions']}")
        print(f"📅 Generated: {data['generated_at']}")
        print("\n🚀 Simple searchable post database ready!")
        print("📂 Files needed: simple-index.html, all-posts.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    main() 