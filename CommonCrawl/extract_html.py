import requests
import trafilatura

def extract_clean_text(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {url}: {response.status_code}")
    html = response.text

    text = trafilatura.extract(html, include_comments=False, include_tables=False)
    return text

# # Example usage
# if __name__ == "__main__":
#     url = "https://en.wikipedia.org/wiki/Alan_Turing"
#     clean_text = extract_clean_text(url)

#     if clean_text:
#         print(clean_text[:1000])  # Print first 1000 chars
#     else:
#         print("No text extracted.")
