import argparse

parser = argparse.ArgumentParser()
parser.add_argument("URL", help="URL to process")
args = parser.parse_args()

url = args.URL
print(url)


if __name__ == "__main__":
    print("hello")