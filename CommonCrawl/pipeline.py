import requests
import warcio.archiveiterator
import gzip
from io import BytesIO
import trafilatura
import os

# -------------------------
# Download WARC file (full file)
# -------------------------
def download_warc(warc_url, local_path):
    if os.path.exists(local_path):
        print(f"{local_path} already exists, skipping download")
        return
    print(f"Downloading {warc_url} ...")
    r = requests.get(warc_url, stream=True)
    r.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    print("Download complete!")

# -------------------------
# Extract clean text from WARC file
# -------------------------
def extract_warc_to_text(local_warc_path, out_dir="wikipedia_corpus", max_pages=None):
    os.makedirs(out_dir, exist_ok=True)
    count = 0

    with gzip.open(local_warc_path, 'rb') as f:
        for record in warcio.archiveiterator.ArchiveIterator(f):
            if record.rec_type != "response":
                continue

            try:
                html = record.content_stream().read().decode("utf-8", errors="ignore")
                text = trafilatura.extract(html)
                if not text:
                    continue

                # Save each page
                filename = os.path.join(out_dir, f"page_{count}.txt")
                with open(filename, "w", encoding="utf-8") as out_f:
                    out_f.write(text)

                count += 1
                print(f"Saved page {count}")

                if max_pages and count >= max_pages:
                    break

            except Exception as e:
                print(f"Skipping record due to error: {e}")
                continue

    print(f"Done! Extracted {count} pages into {out_dir}")

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    # Example: one Wikipedia-heavy WARC from CC-MAIN-2025-38
    warc_url = "https://data.commoncrawl.org/crawl-data/CC-MAIN-2025-38/segments/1757047532641.17/warc/CC-MAIN-20250905112101-20250905142101-00000.warc.gz"
    local_warc_path = "CC-MAIN-2025-38-wikipedia.warc.gz"

    download_warc(warc_url, local_warc_path)
    extract_warc_to_text(local_warc_path, max_pages=1)  # max_pages just for testing
