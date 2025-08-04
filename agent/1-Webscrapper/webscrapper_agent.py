import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# Load environment variables in a file called .env
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# check they key
if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

# Initialize OpenAI client
openai = OpenAI()

# Initial connect test to OpenAI API
message = "Hello, OpenAI! This is a test message to check the connection."
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": message}]
    )
print("OpenAI API connection test successful:", response.choices[0].message.content)

# Start web scraping

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
} # Set a browser-like User-Agent to avoid blocking when making web requests


class WebsiteScraper:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url, headers=header)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

book = WebsiteScraper("http://books.toscrape.com/")  # Example URL for scraping
# print(f"Title: {book.title}")
# print(f"Text snippet: {book.text[:500]}...")  # Print first 500 characters of the text


## Types of prompts

# Models like GPT4o have been trained to receive instructions in a particular way.

# They expect to receive:

# **A system prompt** that tells them what task they are performing and what tone they should use

# **A user prompt** -- the conversation starter that they should reply to

# Define system prompt 

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."

# Fuction for user prompt
def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += f"\nThe contents of this website is as follows; \
                   please provide a short summary of this website in markdown. \
                   If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

# print(user_prompt_for(book))

def message_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# Now, we call the OpenAI API to get a response based on the message we created

def summarize(url):
    website = WebsiteScraper(url)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_for(website)
    )
    return response.choices[0].message.content

# result = summarize("https://www.bbc.com/news")
# print("Summary of the news today:", result)

# News and information sites (public pages):
# https://www.bbc.com/news
# https://www.nytimes.com/section/technology
# https://www.cnn.com/world
# https://www.reuters.com/business/
# https://www.npr.org/sections/news/

# Open data and documentation:
# https://docs.python.org/3/
# https://pypi.org/
# https://en.wikipedia.org/wiki/Web_scraping

# Blogs and tech:
# https://blog.python.org/
# https://techcrunch.com/

if __name__ == "__main__":
    result = summarize("https://techcrunch.com/")
    print("Summary of the news today:", result)