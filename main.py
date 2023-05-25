import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL to process")
args = parser.parse_args()

url = args.URL
print(url)

# Revisit this
url_pattern = re.compile(
    r'^(https?|ftp)://'  # Protocol (http, https, ftp)
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Domain
    r'(?:/?|[/?]\S+)$', re.IGNORECASE  # Ignore case
)

if url_pattern.match(url):
    print("Valid URL")
else:
    print("Invalid URL")

if __name__ == "__main__":
    print("hello")