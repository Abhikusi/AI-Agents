import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI

# Initialize and constants
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if api_key and api_key.startswith('sk-proj-') and len(api_key) > 10:
    print("API kyes looks good so far.")
else:
    print("There might be a problem with the API key. Please check it.")

MODEL = "gpt-4o-mini"
openai = OpenAI()

# A call to represent a Webpage
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

class Website:
    """
    Represents a website and provides methods to extract its title, main text content, and links.
    Returns a formatted string containing the webpage's title and main text content.
    """

    def __init__(self, url):
        self.url = url
        response = requests.get(url, headers=headers)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser') # Parse the HTML content
        self.title = soup.title.string if soup.title else "No Title"
        if soup.body:
            for irrelevant in soup.body(['script', 'style', 'img', 'input']):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator='\n', strip=True)
        else:
            self.text = "No text content found"
        links = [link.get('href') for link in soup.find_all('a', href=True)]
        self.links = [link for link in links if link]

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"
    

website = Website("https://www.cnn.com")
# print(website.get_contents())

# With help of OpenAI API GTP-4o-mini model, we can figure out which links are relevant to the business brochure project.

link_system_prompt = "You are provided with a list of links found on a webpage. \
                     You are able to decide which of the links would be most relevant to include in a brochure about the company. \
                     such as links to an About page, or a Conpany page. \n"
link_system_prompt += "You should reponse in JSON as i the example:"
link_system_prompt += """
{
    "links": [
        {"type": "about page", "url": "https://full.url/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"},
    ]
}
"""

# print(link_system_prompt)

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with full https URL in JSON format. \
                   Do not include Terms of Service, Privacy, email links. \n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

# print(get_links_user_prompt(website))

def get_links(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return json.loads(result)

huggingface = Website("https://huggingface.co")
huggingface.links

get_links("https://huggingface.co")


# Make Brochure!

def get_all_details(url):
    result = "Landing Page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print(f"Links found: {links}")
    for link in links["links"]:
        if "url" in link:
            result += f"Link Type: {link.get('type', 'unknown')}\n"
            result += f"Link URL: {link['url']}\n"
            result += Website(link['url']).get_contents()
    return result

# print(get_all_details("https://huggingface.co"))

system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    user_prompt += get_all_details(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

def create_brochure(company_name, url):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ]
    )
    return response.choices[0].message.content

# print(create_brochure("Hugging Face", "https://huggingface.co"))

# More improvements to the Brochure, this will steam the result rather than giving it in single short

def stream_brochure(company_name, url):
    stream = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt },
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
        ], 
        stream=True
    )

    response = ""
    display_handle = display(Markdown(""), display_id=True)
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        response = response.replace("```","").replace("markdown", "")
        update_display(Markdown(response), display_id=display_handle.display_id)

print(stream_brochure("HuggingFace", "https://huggingface.co"))