__version__ = '0.0.6'

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
import subprocess
import os
import shutil

def scrape_urls(base_url, filter_path):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    parsed_base_url = urlparse(base_url)
    main_domain = f"{parsed_base_url.scheme}://{parsed_base_url.netloc}"
    filtered_urls = [urljoin(base_url, link['href']) for link in links if urljoin(base_url, link['href']).startswith(main_domain + filter_path)]
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
    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)
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
    parser = argparse.ArgumentParser(description='Scrape a webpage for all URLs and save them to a file.')
    parser.add_argument('--to_download_file', type=str, default='to_download.txt', help='The file containing URLs to start the scrape from (default: to_download.txt)')
    parser.add_argument('--output', type=str, default='urls.txt', help='The output file path (default: urls.txt)')
    parser.add_argument('--filter_path', type=str, default='/video', help='The path to filter URLs (default: /video)')
    parser.add_argument('--downloaded_file', type=str, default='downloaded.dat', help='The file to save downloaded URLs (default: downloaded.dat)')
    args = parser.parse_args()

    with open(args.to_download_file, 'r') as file:
        base_urls = [line.strip() for line in file]

    downloaded_urls = read_downloaded_urls(args.downloaded_file)

    for base_url in base_urls:
        filtered_urls = scrape_urls(base_url, args.filter_path)
        new_urls = [url for url in filtered_urls if url not in downloaded_urls]

        for url in new_urls:
            if url in downloaded_urls:
                print(f"Skipping already downloaded URL: {url}")
                continue

            temp_output_file = 'temp_urls.txt'
            save_urls_to_file([url], temp_output_file)

            success = run_youtube_dl(temp_output_file)

            if success:
                os.remove(temp_output_file)
                save_downloaded_url(url, args.downloaded_file)
                downloaded_urls.add(url)
                subdirectory = get_subdirectory_from_url(base_url)
                move_mp4_files(subdirectory)
            else:
                print(f"Skipping URL {url} due to download error.")
        if not new_urls:
            print(f"No new URLs to download from {base_url}.")

if __name__ == '__main__':
    main()
