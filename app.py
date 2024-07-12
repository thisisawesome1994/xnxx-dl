import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import subprocess
import os
import shutil

def scrape_urls(base_url, filter_path):
    # Send a request to the webpage
    response = requests.get(base_url)
    response.raise_for_status()  # Check that the request was successful

    # Parse the webpage content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlink tags
    links = soup.find_all('a', href=True)

    # Parse the base URL to get the main domain
    parsed_base_url = urlparse(base_url)
    main_domain = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}"

    # Filter and collect URLs
    filtered_urls = []
    for link in links:
        href = link['href']
        # Join the relative URLs with the base URL
        full_url = urljoin(base_url, href)
        # Filter URLs that start with the main domain and specific path
        if full_url.startswith(main_domain + filter_path):
            filtered_urls.append(full_url)

    return filtered_urls

def save_urls_to_file(urls, file_path):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(url + '\n')

def run_youtube_dl(file_path):
    subprocess.run(['youtube-dl.exe', '-a', file_path], check=True)

def move_mp4_files(subdirectory):
    # Create subdirectory if it does not exist
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)
    
    # Move all .mp4 files to the subdirectory
    for file in os.listdir('.'):
        if file.endswith('.mp4'):
            shutil.move(file, os.path.join(subdirectory, file))

def get_subdirectory_from_url(base_url):
    parsed_url = urlparse(base_url)
    path_parts = parsed_url.path.split('/')
    if 'search' in path_parts:
        search_index = path_parts.index('search')
        if search_index + 1 < len(path_parts):
            return path_parts[search_index + 1]
    return 'video'

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Scrape a webpage for all URLs and save them to a file.')
    parser.add_argument('base_url', type=str, help='The base URL of the webpage to scrape')
    parser.add_argument('--output', type=str, default='urls.txt', help='The output file path (default: urls.txt)')
    parser.add_argument('--filter_path', type=str, default='/video', help='The path to filter URLs (default: /video)')
    args = parser.parse_args()

    # Scrape URLs and save to file
    filtered_urls = scrape_urls(args.base_url, args.filter_path)
    save_urls_to_file(filtered_urls, args.output)

    # Run youtube-dl with the output file
    run_youtube_dl(args.output)

    # Remove the output file after successful download
    os.remove(args.output)

    # Determine the subdirectory name based on the base URL
    subdirectory = get_subdirectory_from_url(args.base_url)

    # Move all .mp4 files to the determined subdirectory
    move_mp4_files(subdirectory)

if __name__ == '__main__':
    main()
