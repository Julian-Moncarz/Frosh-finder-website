#!/usr/bin/env python3
"""
Instagram Screenshot Collector
Just takes screenshots of posts - no OCR processing
"""

import time
import random
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

class InstagramScreenshotCollector:
    def __init__(self, headless=False):
        """Initialize the screenshot collector"""
        self.driver = None
        self.headless = headless
        self.screenshots = []
        
    def setup_driver(self):
        """Setup Chrome driver with human-like settings"""
        print("Setting up browser...")
        
        chrome_options = Options()
        
        # Human-like browser settings
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Set a realistic user agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Set window size to common desktop resolution
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            # Automatically download and setup chromedriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to hide automation indicators
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print("Browser setup complete!")
            return True
            
        except Exception as e:
            print(f"Error setting up browser: {e}")
            print("Make sure Chrome browser is installed")
            return False
    
    def human_delay(self, min_seconds=1.0, max_seconds=3.0):
        """Add random human-like delays"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def scroll_slowly(self, scrolls=3):
        """Scroll slowly like a human"""
        if not self.driver:
            return
        for i in range(scrolls):
            # Random scroll amount
            scroll_amount = random.randint(300, 800)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self.human_delay(0.5, 1.5)
    
    def go_to_profile(self, username):
        """Navigate to Instagram profile like a human"""
        if not self.driver:
            return False
            
        print(f"Navigating to @{username}...")
        
        url = f"https://www.instagram.com/{username}/"
        self.driver.get(url)
        
        # Wait for page to load
        self.human_delay(3, 5)
        
        # Check if we got redirected to login
        if "login" in self.driver.current_url:
            print("⚠️  Instagram is asking to login")
            print("The page is loaded. You can manually login if needed.")
            input("Press Enter after you've logged in (or if you want to continue without login)...")
        
        # Scroll a bit to load posts
        self.scroll_slowly(2)
        return True
    
    def find_posts(self):
        """Find all post links on the profile page"""
        if not self.driver:
            return []
            
        print("Finding posts...")
        
        # Wait for posts to load
        self.human_delay(2, 4)
        
        # Instagram post links typically start with /p/
        post_links = []
        
        try:
            # Look for post links
            posts = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
            
            for post in posts:
                href = post.get_attribute('href')
                if href and '/p/' in href:
                    post_links.append(href)
            
            # Remove duplicates
            post_links = list(set(post_links))
            print(f"Found {len(post_links)} posts")
            
            return post_links
            
        except Exception as e:
            print(f"Error finding posts: {e}")
            return []
    
    def screenshot_post(self, post_url, post_number):
        """Take screenshot of a single post"""
        if not self.driver:
            return False
            
        print(f"📸 Screenshotting post: {post_url}")
        
        # Open post in new tab to avoid losing profile page
        self.driver.execute_script(f"window.open('{post_url}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        self.human_delay(3, 5)  # Wait for post to fully load
        
        screenshot_saved = False
        
        try:
            # Wait for post to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            
            # Wait a moment for everything to render (no scrolling to keep caption visible)
            self.human_delay(1, 2)
            
            # Create output directory
            output_dir = "instagram_screenshots"
            try:
                os.makedirs(output_dir, exist_ok=True)
            except OSError as e:
                print(f"❌ Error creating directory {output_dir}: {e}")
                return False
            
            # Take screenshot with descriptive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Include milliseconds
            screenshot_filename = f"post_{post_number:03d}_{timestamp}.png"
            screenshot_path = os.path.join(output_dir, screenshot_filename)
            
            success = self.driver.save_screenshot(screenshot_path)
            
            if success:
                # Get file size for verification
                file_size = os.path.getsize(screenshot_path) / 1024  # KB
                print(f"✅ Screenshot saved: {screenshot_filename} ({file_size:.1f} KB)")
                
                # Store screenshot info
                self.screenshots.append({
                    'post_number': post_number,
                    'url': post_url,
                    'filename': screenshot_filename,
                    'timestamp': timestamp,
                    'file_size_kb': round(file_size, 1)
                })
                screenshot_saved = True
            else:
                print("❌ Failed to save screenshot")
        
        except TimeoutException:
            print("⏰ Timeout waiting for post to load")
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
        
        # Close tab and return to profile
        try:
            if len(self.driver.window_handles) > 1:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            else:
                print("⚠️  Only one tab open, not closing")
        except Exception as e:
            print(f"⚠️  Error switching tabs: {e}")
        
        return screenshot_saved
    
    def collect_screenshots(self, username, max_posts=10):
        """Main function to collect screenshots"""
        print(f"📸 Starting screenshot collection for @{username}")
        print("=" * 60)
        
        if not self.setup_driver():
            return False
        
        try:
            # Go to profile
            if not self.go_to_profile(username):
                return False
            
            # Find posts
            post_links = self.find_posts()
            
            if not post_links:
                print("No posts found")
                return False
            
            # Limit posts if requested
            if max_posts:
                post_links = post_links[:max_posts]
            
            print(f"Will screenshot {len(post_links)} posts")
            print()
            
            # Take screenshots of each post
            successful_screenshots = 0
            
            for i, post_url in enumerate(post_links, 1):
                print(f"[{i}/{len(post_links)}] Processing post...")
                
                if self.screenshot_post(post_url, i):
                    successful_screenshots += 1
                
                # Human-like delay between posts
                if i < len(post_links):  # Don't delay after last post
                    print(f"⏳ Waiting before next post...")
                    self.human_delay(3, 6)
                
                print()  # Empty line for readability
            
            print(f"📊 Screenshot Summary:")
            print(f"   ✅ Successful: {successful_screenshots}/{len(post_links)} posts")
            print(f"   📁 Saved to: instagram_screenshots/")
            
            return successful_screenshots > 0
            
        except Exception as e:
            print(f"❌ Error during screenshot collection: {e}")
            return False
        
        finally:
            if self.driver:
                print("🔒 Closing browser...")
                self.driver.quit()
    
    def create_index_file(self, username):
        """Create an index file listing all screenshots"""
        if not self.screenshots:
            return
        
        output_dir = "instagram_screenshots"
        index_file = os.path.join(output_dir, "screenshot_index.txt")
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(f"Instagram Screenshots from @{username}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Screenshots: {len(self.screenshots)}\n\n")
            
            for screenshot in self.screenshots:
                f.write(f"Post {screenshot['post_number']}:\n")
                f.write(f"  📄 File: {screenshot['filename']}\n")
                f.write(f"  🔗 URL: {screenshot['url']}\n")
                f.write(f"  📏 Size: {screenshot['file_size_kb']} KB\n")
                f.write(f"  🕐 Time: {screenshot['timestamp']}\n")
                f.write("-" * 30 + "\n")
        
        print(f"📋 Index file created: {index_file}")

def main():
    username = "uoft_frosh.29"
    max_posts = 5  # Get 5 screenshots for testing
    
    print("Instagram Screenshot Collector")
    print("Takes screenshots of Instagram posts for manual review")
    print("=" * 70)
    
    collector = InstagramScreenshotCollector(headless=False)  # Set to True to hide browser
    
    if collector.collect_screenshots(username, max_posts):
        collector.create_index_file(username)
        print("\n🎉 Screenshot collection completed successfully!")
        print("\n📁 Check the 'instagram_screenshots' folder to view the images")
        print("💡 You can now manually review the screenshots to see the captions")
    else:
        print("\n❌ Screenshot collection failed")

if __name__ == "__main__":
    main() 