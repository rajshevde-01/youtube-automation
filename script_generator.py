import re

def clean_text(text):
    """Remove weird characters that might break TTS or overlay."""
    text = re.sub(r'[^A-Za-z0-9 .,!?\'\"]', '', text)
    return text.strip()

def extract_core_entity(title):
    """
    Very basic heuristic to pull the main subject out of the title so it fits in a Short.
    For example: "Hackers Exploit New Microsoft Exchange Flaw to Deploy Ransomware" 
    becomes -> "Microsoft Exchange Flaw" or just uses the whole title if short enough.
    """
    if len(title) < 50:
        return title
    
    # Try to grab the first part of the sentence or before punctuation
    parts = re.split(r'[:|\-]', title)
    return str(parts[0]).strip()

def generate_script(topic_data):
    """
    Uses the trending data from RSS to structure a YouTube Shorts script.
    Since we cannot use paid OpenAI APIs, we use dynamic template mapping
    based on the real-world article data.
    """
    title = str(clean_text(topic_data.get("title", "")))
    desc = str(clean_text(topic_data.get("description", "")))
    source = str(clean_text(topic_data.get("source", "Cyber Security News")))
    genre = str(topic_data.get("genre", "Cybersecurity"))
    
    # If the description is too long, we truncate it for a 60-second read (around 120-150 words total)
    # We want max 2 sentences for the body
    sentences = re.split(r'(?<=[.!?]) +', desc)
    short_desc = " ".join(sentences[:2]) if len(sentences) > 0 else desc

    entity = extract_core_entity(title)

    # We dynamically create the script sections
    
    if genre == "Bug Bounty":
        hook = f"URGENT: Have you seen this major {entity} bounty dropped today?"
        cta = "Start hunting for similar flaws immediately, and subscribe to The Exploit Feed for daily exploits."
    elif genre == "SOC analyst tips":
        hook = f"SOC Analysts: Do you have defenses against this {entity} alert from today?"
        cta = "Check your SIEM immediately, patch your software, and subscribe to The Exploit Feed for daily intel."
    else:
        # Generic cybersecurity fallback
        hook = f"URGENT: Have you seen this major {entity} alert from today?"
        cta = "Patch your systems immediately, and subscribe to The Exploit Feed for daily zero-day alerts."
    
    body = f"According to {source}, {title}. Here is what you need to know: {short_desc}. This is actively being exploited right now."
    
    full_script = f"{hook} {body} {cta}"
    
    # Overcome text too long for overlay by returning just the title as the visual text
    display_title = title if len(title) < 60 else title[:57] + "..."
    display_title = str(display_title)

    print("--- Generated Dynamic Script ---")
    print(full_script)
    print("--------------------------------")
    
    return {
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_text": full_script,
        "title": display_title
    }
