import requests
import warcio.archiveiterator
import gzip
from io import BytesIO

# query index for urls
def query_cc_index(domain, index="CC-MAIN-2025-38"):
    url = f"https://index.commoncrawl.org/{index}-index?url={domain}/*&output=json"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Index request failed: {r.status_code}")
    return [line for line in r.text.splitlines()]

# fetch and parse the warc record
def fetch_warc_record(record_json):
    import json
    record = json.loads(record_json)
    offset, length = int(record['offset']), int(record['length'])
    warc_url = record['filename']
    base_url = "https://data.commoncrawl.org/"

    headers = {"Range": f"bytes={offset}-{offset+length-1}"}
    r = requests.get(base_url + warc_url, headers=headers, stream=True)

    if r.status_code != 206:  # 206 = partial content
        raise Exception(f"WARC fetch failed: {r.status_code}")

    buf = BytesIO(r.content)
    with gzip.GzipFile(fileobj=buf) as f:
        for record in warcio.archiveiterator.ArchiveIterator(f):
            if record.rec_type == "response":
                payload = record.content_stream().read()
                return payload.decode("utf-8", errors="ignore")


# # Example usage
# if __name__ == "__main__":
#     # Find all records for a domain
#     results = query_cc_index("wikipedia.org")
#     print(f"Found {len(results)} results")

#     if results:
#         html = fetch_warc_record(results[0])
#         print("Fetched HTML snippet:\n", html[:1000])
