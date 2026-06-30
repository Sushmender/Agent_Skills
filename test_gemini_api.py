import os
import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import errors

async def test_api():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return

    print("Testing Gemini API...")
    
    # Initialize the client
    client = genai.Client(api_key=api_key)
    
    try:
        # We use a simple prompt to minimize token usage
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents='Respond with a single word: Hello'
        )
        print("SUCCESS! The API is up and running.")
        print(f"Response: {response.text}")
        
    except errors.ClientError as e:
        if e.code == 429:
            print(f"\nRATE LIMIT (429): Resource Exhausted.")
            print("You have hit the Gemini API quota limit (typically 15 RPM on the free tier).")
            print("Please wait about 60 seconds before running the app again.")
        else:
            print(f"\nAPI Error: {e.code} - {e.message}")
            
    except Exception as e:
        print(f"\nUnknown Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
