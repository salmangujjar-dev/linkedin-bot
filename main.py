import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from linkedin_bot import LinkedInBot
from urllib.parse import urlparse
from typing import List

load_dotenv()

app = FastAPI(
    title="LinkedIn Bot API",
    description="An API for automating LinkedIn interactions",
    version="1.0.0"
)

class LinkedInMessage(BaseModel):
    urls: List[str] = Field(..., description="List of LinkedIn profile URLs to send invites to")
    messages: List[str] = Field(..., description="List of personalized messages for each invite")
    
    @field_validator('urls', 'messages')
    def check_length(cls, v):
        if len(v) == 0:
            raise ValueError('List must not be empty')
        return v
    
    @field_validator('urls')
    def validate_urls(cls, urls):
        for url in urls:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError(f'Invalid URL: {url}')
        return urls
    
    @field_validator('messages')
    def check_length_match(cls, v, values):
        if 'urls' in values.data and len(v) != len(values.data['urls']):
            raise ValueError('The number of messages must match the number of URLs')
        return v


@app.post("/linkedin/send_invites", 
          response_model=dict,
          summary="Send LinkedIn invites",
          description="Sends connection invites to specified LinkedIn profiles with personalized messages")
async def send_invites(message_data: LinkedInMessage):
    """
    Send LinkedIn invites to multiple profiles.

    - **urls**: List of LinkedIn profile URLs to send invites to
    - **messages**: Corresponding list of personalized messages for each invite

    Returns:
        A dictionary with status and message indicating success or failure
    """
    
    bot = LinkedInBot()
    
    session_key = os.getenv('LINKEDIN_EMAIL')
    session_password = os.getenv('LINKEDIN_PASSWORD')
    
    if not session_key or not session_password:
        raise HTTPException(status_code=500, detail="LinkedIn credentials not found in environment variables.")
    
    try:
        await bot.run(session_key, session_password, message_data.urls, message_data.messages)
        return {"status": "success", "message": "Messages sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=4)