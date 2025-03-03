import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load URLs from a file
with open("urls.txt", "r", encoding="utf-8") as file:
    urls = [line.strip() for line in file.readlines()[:500]]  # First 500 URLs

data = []

# Headers to avoid blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Debug: Check if URLs are loaded
print(f"Loaded {len(urls)} URLs.")

for url in urls:
    try:
        print(f"Scraping: {url}")  # Debugging Output

        # Fetch the webpage
        response = requests.get(url, headers=headers)

        # Check for successful response
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract Title
            title = soup.find("h1").text.strip() if soup.find("h1") else "No Title"

            # Extract Author
            author_meta = soup.find("meta", {"name": "author"})
            author = author_meta["content"].strip() if author_meta else "Unknown"

            # Extract Reading Time
            reading_time_meta = soup.find("meta", {"name": "twitter:data1"})
            reading_time = reading_time_meta["content"].strip() if reading_time_meta else "Unknown"

            # Extract Claps
            claps_btn = soup.find("button", {"data-testid": "clapCount"})
            claps = claps_btn.text.strip() if claps_btn else "0"

            # Store the extracted data
            data.append([title, author, reading_time, claps, url])

        else:
            print(f"Failed to fetch {url} - Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Save data to CSV
df = pd.DataFrame(data, columns=["Title", "Author", "Reading Time", "Claps", "URL"])
df.to_csv("medium_articles.csv", index=False, encoding="utf-8")

print("Scraping completed! Data saved in 'medium_articles.csv'.")
