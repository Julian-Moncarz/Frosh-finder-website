# U of T Frosh Finder

https://julian-moncarz.github.io/Frosh-finder-website/

A searchable web interface for University of Toronto frosh introduction posts from the @uoft_frosh.29 Instagram account.

## What is this?

Instagram doesn't have a search feature for posts - this sucks if you are looking for a roommate in a specific building or want to find people in your major. This tool solves that problem by providing a clean, searchable interface for all the frosh introduction posts.

## 🤖 Automated RSS Monitoring

This project now includes automated RSS feed monitoring using GitHub Actions! The system:

- 🔄 **Automatically checks for new posts every 15 minutes**
- 📡 **Monitors Instagram RSS feeds** via RSS.app
- 🚀 **Updates the website automatically** when new posts are found
- 📊 **Maintains post history** with timestamps and metadata
- 🔧 **Can be manually triggered** for immediate updates

### How it works:

1. **RSS Feed**: Instagram posts are converted to RSS format using RSS.app
2. **GitHub Actions**: Scheduled workflow runs every 15 minutes
3. **Python Script**: Fetches RSS feed and compares with existing posts
4. **Auto-Update**: New posts are added to the database automatically
5. **Website Rebuild**: The searchable interface is updated with new posts

### Manual Trigger:

You can manually trigger the RSS check by:
1. Going to the **Actions** tab in GitHub
2. Selecting **RSS Feed Monitor**
3. Clicking **Run workflow**
4. Optionally enabling **Force update** to re-process all posts

## Contact

Created by Julian Moncarz (inverted_badger on Discord).

## License

This project is open source and available under the MIT License.
