import os
import requests
import json
import time
import re
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys and credentials
HYPERBROWSER_API_KEY = os.getenv("HYPERBROWSER_API_KEY")
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_PHONE = os.getenv("TELEGRAM_PHONE")
TELEGRAM_PASSWORD = os.getenv("TELEGRAM_PASSWORD", "")  # 2FA password if enabled
GIRLFRIEND_USERNAME = os.getenv("GIRLFRIEND_USERNAME")

# Hyperbrowser API endpoints
SCRAPE_ENDPOINT = "https://app.hyperbrowser.ai/api/scrape"
CLAUDE_COMPUTER_USE_ENDPOINT = "https://app.hyperbrowser.ai/api/task/claude-computer-use"

# Function to extract Instagram reel URL
def extract_instagram_reel_url(text):
    regex = r'https://www\.instagram\.com/reel/[a-zA-Z0-9_-]+/?'
    match = re.search(regex, text)
    return match.group(0) if match else None

# Function to scrape Instagram reel
def scrape_instagram_reel(url):
    headers = {
        "x-api-key": HYPERBROWSER_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "sessionOptions": {
            "useStealth": True,
            "acceptCookies": True
        },
        "scrapeOptions": {
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    }
    
    # Start scrape job
    try:
        response = requests.post(SCRAPE_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        
        job_id = response.json().get("jobId")
        print(f"Scrape job started with ID: {job_id}")
        
        # Poll for scrape job completion
        max_attempts = 30
        for attempt in range(max_attempts):
            time.sleep(2)  # Wait 2 seconds between polls
            
            status_response = requests.get(
                f"{SCRAPE_ENDPOINT}/{job_id}",
                headers={"x-api-key": HYPERBROWSER_API_KEY}
            )
            
            status_response.raise_for_status()
            job_data = status_response.json()
            job_status = job_data.get("status")
            
            if job_status == "completed":
                # Return the markdown content
                return job_data.get("data", {}).get("markdown")
            elif job_status == "failed":
                print(f"Scrape job failed: {job_data.get('error')}")
                return None
            
            print(f"Job status: {job_status}, waiting... (Attempt {attempt+1}/{max_attempts})")
        
        print("Timed out waiting for scrape job")
        return None
        
    except Exception as e:
        print(f"Error in scrape_instagram_reel: {e}")
        return None

# Function to analyze content with Claude Computer Use
def analyze_with_claude(content, original_url):
    headers = {
        "x-api-key": HYPERBROWSER_API_KEY,
        "Content-Type": "application/json"
    }
    
    task = f"""
    I need to respond to an Instagram reel my girlfriend sent me. 
    Here is the content scraped from the reel: 

    {content}

    Original URL: {original_url}

    Give me a playful, very short response (you can include emojis if needed) that acknowledges what the reel is about.
    Make it sound natural and casual, like I actually watched the reel.
    
    IMPORTANT FORMAT: Put your response after a line that says "FINAL RESPONSE:" - I will only use the text after this marker.
    """
    
    payload = {
        "task": task,
        "maxSteps": 5
    }
    
    try:
        # Start Claude Computer Use task
        response = requests.post(
            CLAUDE_COMPUTER_USE_ENDPOINT, 
            headers=headers, 
            json=payload
        )
        
        response.raise_for_status()
        job_id = response.json().get("jobId")
        print(f"Claude task started with ID: {job_id}")
        
        # Poll for Claude task completion
        max_attempts = 20
        for attempt in range(max_attempts):
            time.sleep(3)  # Wait 3 seconds between polls
            
            status_response = requests.get(
                f"{CLAUDE_COMPUTER_USE_ENDPOINT}/{job_id}",
                headers={"x-api-key": HYPERBROWSER_API_KEY}
            )
            
            status_response.raise_for_status()
            job_data = status_response.json()
            job_status = job_data.get("status")
            
            if job_status == "completed":
                # Get Claude's final result
                result = job_data.get("data", {}).get("finalResult", "")
                
                # First try to find "FINAL RESPONSE:" marker
                if "FINAL RESPONSE:" in result:
                    final_part = result.split("FINAL RESPONSE:", 1)[1].strip()
                    return final_part
                
                # If that fails, try to find the last colon in the response
                elif ":" in result:
                    # Split by lines to handle multi-line responses better
                    lines = result.split('\n')
                    
                    # Find the last line with a colon
                    for line in reversed(lines):
                        if ":" in line:
                            parts = line.split(":", 1)
                            if len(parts) > 1 and len(parts[1].strip()) > 0:
                                # Check if this looks like a proper response and not just a random colon
                                if len(parts[1].strip()) > 10:  # Assuming responses will be at least 10 chars
                                    return parts[1].strip()
                    
                    # If we're here, we couldn't extract a good response from colons
                    # Try to get the last paragraph instead
                    paragraphs = result.split('\n\n')
                    return paragraphs[-1].strip()
                
                # If all else fails, just return the result
                return result
                
            elif job_status == "failed":
                print(f"Claude task failed: {job_data.get('error')}")
                return "I couldn't analyze this reel properly, but it looks interesting! 😊"
            
            print(f"Claude task status: {job_status}, waiting... (Attempt {attempt+1}/{max_attempts})")
        
        print("Timed out waiting for Claude task")
        return "Sorry, took too long to analyze. Looks like a cool reel though! 👀"
        
    except Exception as e:
        print(f"Error in analyze_with_claude: {e}")
        return "I couldn't analyze this reel properly, but it looks interesting! 😊"

# Event handler for new messages
async def handle_new_message(event):
    try:
        # Get message details
        message = event.message
        
        # Get sender
        sender = await message.get_sender()
        username = getattr(sender, 'username', None)
        
        # Print debug info
        #print(f"Received message from: {username}")
        
        # Only process messages from your girlfriend
        if username != GIRLFRIEND_USERNAME:
            return
        
        # Check if message contains Instagram reel URL
        message_text = getattr(message, 'text', '')
        reel_url = extract_instagram_reel_url(message_text)
        
        if reel_url:
            print(f"Found Instagram reel: {reel_url}")
            
            # Let your girlfriend know you're checking it out (optional)
            # await message.respond("Checking this out...👀")
            
            # Scrape the Instagram reel
            reel_content = scrape_instagram_reel(reel_url)
            
            if reel_content:
                # Analyze with Claude
                print("Analyzing with Claude...")
                claude_response = analyze_with_claude(reel_content, reel_url)
                print(f"Claude response: {claude_response}")
                
                # Send response
                await message.respond(claude_response)
            else:
                await message.respond("I couldn't load that reel properly, but I'll check it out later! 👍")
    except Exception as e:
        print(f"Error in handle_new_message: {e}")

# Main function
async def main():
    # Create Telegram client
    client = TelegramClient('reel_analyzer_session', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    
    # Connect to Telegram
    print("Connecting to Telegram...")
    await client.connect()
    
    # Ensure you're authorized
    if not await client.is_user_authorized():
        print(f"First-time login for {TELEGRAM_PHONE}")
        
        # Send code request
        await client.send_code_request(TELEGRAM_PHONE)
        try:
            # Sign in with code (will prompt in console)
            code = input('Enter the code you received: ')
            await client.sign_in(TELEGRAM_PHONE, code)
        except SessionPasswordNeededError:
            # 2FA is enabled
            await client.sign_in(password=TELEGRAM_PASSWORD)
    
    # Register event handler
    client.add_event_handler(handle_new_message, events.NewMessage)
    
    print("Successfully connected! Monitoring for Instagram reels...")
    print("Waiting for messages from Girlfriend...")
    #print(f"Waiting for messages from: {GIRLFRIEND_USERNAME}")
    
    # Keep client running
    await client.run_until_disconnected()

# Run the main function
if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")