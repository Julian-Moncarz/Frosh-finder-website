# U of T Frosh Finder

live site: https://julian-moncarz.github.io/Frosh-finder-website/

A searchable web interface for University of Toronto frosh introduction posts from the @uoft_frosh.29 Instagram account.

## What is this?

Instagram doesn't have a search feature for posts - this sucks if you are looking for a roommate in a specific building or want to find people in your major. This tool solves that problem by providing a clean, searchable interface for all the frosh introduction posts.

## Getting the data

I tried a bunch of different ways, what ended up working was [apify.com](https://apify.com) - this got me ~1800 posts before I ran out of free credits.

UPDATE: The site now automatically loads new posts!

1. Instagram posts from @uoft_frosh.29 are converted to a RSS feed using [rss.app](https://rss.app)
2. GitHub Actions workflow runs every day at 9 AM UTC
3. Python script fetches new posts and and adds them to all-posts.json

## Contact

Created by Julian Moncarz (inverted_badger_ on Discord).

## License

This project is open source and available under the MIT License.
