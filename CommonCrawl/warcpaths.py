import gzip

with gzip.open("CommonCrawl/warc.paths.gz", "rt") as f:
    warc_urls = [line.strip() for line in f]

print(f"Found {len(warc_urls)} WARC files")
print(warc_urls[:10])  # peek at first 10
