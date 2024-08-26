# LinkedIn Bot

This project is a FastAPI-based application that automates LinkedIn interactions, including sending connection requests and messages.

## Features

- Send connection requests to multiple LinkedIn profiles
- Add personalized notes to connection requests
- Send messages to existing connections
- Handle LinkedIn security challenges automatically
- RESTful API endpoint for easy integration

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- A LinkedIn account
- Azure OpenAI API access (for CAPTCHA solving)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/salmangujjar-dev/linkedin-bot.git
   cd linkedin-automation-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   LINKEDIN_EMAIL=your_linkedin_email
   LINKEDIN_PASSWORD=your_linkedin_password
   AZURE_OPENAI_DEPLOYMENT=your_azure_openai_deployment
   ```

## Usage

1. Start the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. To send connection requests, make a POST request to `/linkedin/send_invites` with the following JSON body:
   ```json
   {
     "urls": ["https://www.linkedin.com/in/profile1", "https://www.linkedin.com/in/profile2"],
     "messages": ["Hello, I'd like to connect!", "Hi there, let's connect!"]
   }
   ```

## API Endpoints

- `POST /linkedin/send_invites`: Send connection requests to specified LinkedIn profiles

## Project Structure

- `main.py`: FastAPI application and API endpoint definitions
- `linkedin_bot.py`: Main bot logic for LinkedIn interactions
- `linkedin_actions.py`: Specific LinkedIn actions (login, connect, message, etc.)
- `security_check.py`: Handles LinkedIn security challenges
- `selenium_utils.py`: Utility functions for Selenium setup
- `llm_utils.py`: Utility functions for language model setup

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with LinkedIn's terms of service.

## License

[MIT License](LICENSE)