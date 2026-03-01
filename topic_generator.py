import os
import random
import feedparser
from datetime import datetime, timedelta

# Define your alternating genres here. 
# We will use the day of the year to alternate between the two most engaging niches
DAY_OF_YEAR = datetime.now().timetuple().tm_yday
TARGET_GENRE = "Bug Bounty" if DAY_OF_YEAR % 2 == 0 else "Threat intelligence"

print(f"Today's Genre Focus: {TARGET_GENRE}")

# List of trusted, high-volume cybersecurity and tech RSS feeds
# These provide trending, real-world topics daily
# We include feeds that cover both vulnerabilities and active threat campaigns
RSS_FEEDS = [
    "https://www.bleepingcomputer.com/feed/",
    "https://feeds.feedburner.com/TheHackersNews",
    "https://portswigger.net/daily-swig/rss",  # Great for ethical hacking/bug bounty
    "https://krebsonsecurity.com/feed/"
]

def get_daily_topic():
    manual_file = "manual_topic.txt"
    if os.path.exists(manual_file):
        with open(manual_file, "r") as f:
            topic = f.read().strip()
            if topic:
                print(f"Using manual topic: {topic}")
                return {
                    "source": "manual",
                    "title": topic,
                    "description": topic,
                    "link": ""
                }
    
    # If no manual topic, scrape RSS for something recent (last 48 hours)
    print("Fetching trending topics from RSS feeds...")
    recent_articles = []
    
    # We'll consider "recent" as published within the last 2 days
    two_days_ago = datetime.now() - timedelta(days=2)
    
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                # Some feeds use published, some use updated. Try both.
                pub_date_tuple = entry.get("published_parsed", entry.get("updated_parsed"))
                if pub_date_tuple:
                    pub_date = datetime(*pub_date_tuple[:6])
                    if pub_date > two_days_ago:
                        title = entry.title
                        desc = entry.get("summary", entry.get("description", "")).split('<')[0].strip()
                        
                        # Filter for out target genre (case-insensitive check against common keywords for that genre)
                        # We map genres to a set of keywords
                        genre_keywords = {
                            "Bug Bounty": ["vulnerability", "bounty", "flaw", "rce", "xss", "cve", "zero-day", "hackerone", "bugcrowd", "injection"],
                            "Cybersecurity": ["ransomware", "breach", "cyber", "attack", "malware", "phishing"],
                            "SOC analyst tips": ["alert", "siem", "splunk", "soc", "detection", "incident", "response"],
                            "Ethical hacking": ["exploit", "pentest", "red team", "bypass", "payload"],
                            "Threat intelligence": ["apt", "campaign", "actor", "botnet", "c2", "nexus"]
                        }
                        
                        keywords_to_check = genre_keywords.get(TARGET_GENRE, [TARGET_GENRE.lower()])
                        
                        text_to_search = (title + " " + desc).lower()
                        is_match = any(kw.lower() in text_to_search for kw in keywords_to_check)
                        
                        if is_match:
                            recent_articles.append({
                                "source": feed.feed.title if hasattr(feed, 'feed') and hasattr(feed.feed, 'title') else feed_url,
                                "genre": TARGET_GENRE,
                                "title": title,
                                "description": desc,
                                "link": entry.link
                            })
        except Exception as e:
            print(f"Failed to parse feed {feed_url}: {e}")
            
    if not recent_articles:
                        print(f"No recent articles found for {TARGET_GENRE}... falling back to generic topic.")
                        return {
                            "source": "fallback",
                            "genre": TARGET_GENRE,
                            "title": f"The Ultimate {TARGET_GENRE} Discovery This Week",
                            "description": f"Critical new findings in {TARGET_GENRE} have been exposed impacting enterprise systems worldwide.",
                            "link": ""
                        }
        
    # Pick a random trending article to ensure we don't just pick the top one every day
    selected = random.choice(recent_articles)
    print(f"Selected trending topic: {selected['title']}")
    return selected
