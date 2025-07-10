# Instagram Post Crawler - Selenium

A Python-based Instagram post scraper that uses Selenium WebDriver to capture screenshots of Instagram posts, bypassing anti-bot detection systems.

## 🚀 Overview

This project scrapes Instagram post content by controlling a real Chrome browser to take screenshots of each post. Unlike traditional scrapers that parse HTML directly, this approach mimics human browsing behavior to avoid Instagram's bot detection systems.

## ✨ Features

- **Human-like browsing**: Uses real Chrome browser with realistic delays and scrolling
- **Screenshot capture**: Takes high-quality screenshots of Instagram posts
- **Anti-detection**: Bypasses Instagram's anti-bot systems through browser automation
- **Batch processing**: Captures multiple posts in sequence with rate limiting
- **Progress tracking**: Real-time feedback and screenshot indexing
- **Error handling**: Robust error handling and recovery

## 🛠️ Tech Stack

- **Python 3.8+**
- **Selenium WebDriver** - Browser automation
- **Chrome + ChromeDriver** - Real browser control
- **Pillow** - Image processing (optional for OCR)
- **pytesseract** - OCR text extraction (optional)

## 📋 Requirements

- Python 3.8 or higher
- Google Chrome browser
- Internet connection

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Julian-Moncarz/Instagram-Post-Crawler-Selenium.git
   cd Instagram-Post-Crawler-Selenium
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv insta_scraper_env
   source insta_scraper_env/bin/activate  # On Windows: insta_scraper_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install selenium webdriver-manager pillow pytesseract
   ```

4. **Verify Chrome is installed**
   The script automatically downloads and manages ChromeDriver.

## 🚀 Usage

### Basic Screenshot Collection

```bash
python instagram_screenshot_only.py
```

### Configuration

Edit the `main()` function in `instagram_screenshot_only.py`:

```python
def main():
    username = "uoft_frosh.29"  # Target Instagram username
    max_posts = 5               # Number of posts to capture (set to None for all)
    
    # Set headless=True to hide browser window
    collector = InstagramScreenshotCollector(headless=False)
```

## 📸 Output

Screenshots are saved to `instagram_screenshots/` with the following structure:

```
instagram_screenshots/
├── post_001_20250710_145106_695.png
├── post_002_20250710_145117_362.png
├── post_003_20250710_145128_722.png
├── screenshot_index.txt
└── ...
```

Each screenshot includes:
- **Sequential numbering**: `post_001`, `post_002`, etc.
- **Timestamp**: Date and time with milliseconds
- **Index file**: `screenshot_index.txt` with metadata

## ⚙️ How It Works

1. **Browser Setup**: Launches Chrome with human-like settings
2. **Profile Navigation**: Goes to target Instagram profile
3. **Post Discovery**: Finds all post links on the profile page
4. **Screenshot Loop**: For each post:
   - Opens post in new tab
   - Waits for content to load
   - Takes full-page screenshot
   - Saves with timestamped filename
   - Returns to profile page
5. **Human Delays**: Random delays between actions (3-6 seconds)

## 🔒 Privacy & Ethics

- **Rate Limiting**: Built-in delays to respect Instagram's servers
- **Public Content Only**: Only accesses publicly visible posts
- **No Authentication**: Doesn't require login credentials
- **Screenshot Approach**: Captures only what's visible to regular users

## ⚠️ Limitations

- **Rate Limiting**: Instagram may temporarily block requests if too many are made
- **Public Profiles Only**: Cannot access private accounts
- **Manual Text Extraction**: Screenshots require manual review or OCR for text extraction
- **Browser Dependent**: Requires Chrome browser installation

## 🔧 Troubleshooting

### Common Issues

**"Instagram is asking to login"**
- This is normal; you can login manually or continue without login for public profiles

**Browser crashes or hangs**
- Ensure Chrome is up to date
- Try running with `headless=False` to see what's happening

**No posts found**
- Check if the profile is public
- Verify the username is correct
- Instagram may be rate limiting

### Performance

- **~10-11 seconds per screenshot** (including delays)
- **5 posts**: ~1 minute total
- **11 posts**: ~2 minutes total

## 🚧 Future Enhancements

- [ ] OCR text extraction from screenshots
- [ ] Support for Instagram Stories
- [ ] Bulk username processing
- [ ] Database storage for extracted content
- [ ] Comment and metadata extraction

## 📄 License

This project is for educational purposes only. Please respect Instagram's Terms of Service and robots.txt when using this tool.

## 🤝 Contributing

Feel free to open issues or submit pull requests for improvements!

---

**Note**: This tool is designed for educational and research purposes. Always respect website terms of service and rate limits. 