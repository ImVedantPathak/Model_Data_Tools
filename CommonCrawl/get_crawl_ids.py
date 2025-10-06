import requests

# List all available crawls
collinfo = requests.get("https://index.commoncrawl.org/collinfo.json").json()
with open("available.txt",'w') as f:
    for crawl in collinfo:
        f.write(crawl['id']+"\n")

print("Saved all crawl IDs")