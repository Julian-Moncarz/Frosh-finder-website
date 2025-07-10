# 🎓 UofT Frosh Finder

A searchable web interface for University of Toronto frosh introduction posts from the @uoft_frosh.29 Instagram account.

## 🚀 What is this?

Instagram doesn't have a search feature for posts - which makes it nearly impossible to find specific introductions among thousands of posts. This tool solves that problem by providing a clean, searchable interface for all the frosh introduction posts.

**Live Website:** [View on GitHub Pages](https://julian-moncarz.github.io/Frosh-finder-website/)

## ✨ Features

- 🔍 **Smart Search**: Find posts by name, program, interests, year, or date
- 📱 **Mobile Responsive**: Works perfectly on phones and computers
- 🔗 **Instagram Integration**: Direct links to view original posts
- 📊 **Real-time Stats**: See engagement metrics (likes, comments)
- 🎨 **Clean UI**: Modern design with UofT blue theme

## 🖥️ Screenshots

The website provides a clean, searchable interface:
- Search bar for finding specific introductions
- Post cards showing introduction text with Instagram handles linked
- Direct "View on Instagram" buttons for each post

## 🏃‍♂️ Quick Start

### Option 1: Use the Live Website
Just visit: https://julian-moncarz.github.io/Frosh-finder-website/

### Option 2: Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Julian-Moncarz/Frosh-finder-website.git
   cd Frosh-finder-website
   ```

2. **Start the local server:**
   ```bash
   ./deploy-simple.sh
   ```
   
   Or manually:
   ```bash
   python3 -m http.server 8004
   ```

3. **Open in browser:**
   Visit `http://localhost:8004/simple-index.html`

## 📁 File Structure

```
├── simple-index.html     # Main website file
├── all-posts.json       # Post data (2000+ posts)
├── build_all_posts.py   # Script to update post data
├── deploy-simple.sh     # Deployment script
└── README.md           # This file
```

## 🔄 Updating the Data

To refresh the post data from Instagram:

```bash
python3 build_all_posts.py
```

This will update `all-posts.json` with the latest posts from @uoft_frosh.29.

## 🛠️ Technical Details

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks needed)
- **Data**: JSON file with post metadata
- **Search**: Client-side text matching
- **Hosting**: Can be deployed anywhere (GitHub Pages, Netlify, Vercel, etc.)

## 📊 Data Structure

Each post in `all-posts.json` contains:
- Caption text
- Date posted
- Engagement metrics (likes, comments)
- Direct Instagram URL
- Post type information

## 🚀 Deployment

### GitHub Pages (Recommended)
1. Push changes to your repository
2. Enable GitHub Pages in repository settings
3. Website will be live at `https://username.github.io/repository-name/`

### Other Platforms
Upload `simple-index.html` and `all-posts.json` to any web hosting service:
- Netlify
- Vercel
- Firebase Hosting
- Traditional web hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

Created by Julian Moncarz (inverted_badger on Discord)

## 📝 License

This project is open source and available under the MIT License.

---

*Making UofT frosh introductions searchable, one post at a time! 🎓* 