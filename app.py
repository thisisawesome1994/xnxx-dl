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
    try:
        subprocess.run(['youtube-dl', '-a', file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"youtube-dl failed with error: {e}")
        return False
    return True

def move_mp4_files(subdirectory):
    # Create subdirectory if it does not exist
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)
    
    # Move all .mp4 files to the subdirectory
    for file in os.listdir('.'):
        if file.endswith('.mp4'):
            shutil.move(file, os.path.join(subdirectory, file))

def save_downloaded_url(url, file_path):
    with open(file_path, 'a') as file:
        file.write(url + '\n')

def read_downloaded_urls(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def get_subdirectory_from_url(base_url):
    parsed_url = urlparse(base_url)
    path_parts = parsed_url.path.split('/')
    if 'search' in path_parts:
        search_index = path_parts.index('search')
        if (search_index + 1) < len(path_parts):
            return path_parts[search_index + 1]
    return 'video'

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Scrape a webpage for all URLs and save them to a file.')
    parser.add_argument('--to_download_file', type=str, default='to_download.txt', help='The file containing URLs to start the scrape from (default: to_download.txt)')
    parser.add_argument('--output', type=str, default='urls.txt', help='The output file path (default: urls.txt)')
    parser.add_argument('--filter_path', type=str, default='/video', help='The path to filter URLs (default: /video)')
    parser.add_argument('--downloaded_file', type=str, default='downloaded.dat', help='The file to save downloaded URLs (default: downloaded.dat)')
    args = parser.parse_args()

    # Read URLs to download from file
    with open(args.to_download_file, 'r') as file:
        base_urls = [line.strip() for line in file]

    # Read previously downloaded URLs
    downloaded_urls = read_downloaded_urls(args.downloaded_file)

    for base_url in base_urls:
        # Scrape URLs and filter out already downloaded ones
        filtered_urls = scrape_urls(base_url, args.filter_path)
        new_urls = [url for url in filtered_urls if url not in downloaded_urls]

        for url in new_urls:
            if url in downloaded_urls:
                print(f"Skipping already downloaded URL: {url}")
                continue

            # Save the single URL to a temporary file
            temp_output_file = 'temp_urls.txt'
            save_urls_to_file([url], temp_output_file)

            # Run youtube-dl with the temporary file
            success = run_youtube_dl(temp_output_file)

            if success:
                # Remove the temporary file after successful download
                os.remove(temp_output_file)

                # Save the successfully downloaded URL to the downloaded_file
                save_downloaded_url(url, args.downloaded_file)

                # Add the URL to the set of downloaded URLs to avoid re-downloading in the same run
                downloaded_urls.add(url)

                # Determine the subdirectory name based on the base URL
                subdirectory = get_subdirectory_from_url(base_url)

                # Move the .mp4 files to the determined subdirectory
                move_mp4_files(subdirectory)
            else:
                print(f"Skipping URL {url} due to download error.")
        if not new_urls:
            print(f"No new URLs to download from {base_url}.")

if __name__ == '__main__':
    main()
