# XNXX-DL

This project is a web scraper and video downloader that scrapes a given webpage for all URLs that match a specific path, saves them to a text file, downloads the videos using `youtube-dl`, and then organizes the downloaded `.mp4` files into a subdirectory named after a specific part of the URL.

## Features

- Scrapes a webpage for URLs matching a specified path.
- Saves the URLs to a text file.
- Downloads videos from the URLs using `youtube-dl`.
- Moves the downloaded `.mp4` files to a subdirectory named after a segment in the base URL.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `argparse` library (standard with Python 3.x)
- `shutil` library (standard with Python 3.x)
- `os` library (standard with Python 3.x)
- `youtube-dl`

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/thisisawesome1994/xnxx-dl.git
    cd xnxx-dl
    ```

2. Install the required Python libraries:
    ```sh
    pip install requests beautifulsoup4 youtube-dl
    ```

3. Make sure `youtube-dl.exe` is in your PATH or in the same directory as the script.

## Usage

Run the script with the base URL, output file, and filter path. For example:

```sh
python app.py --to_download_file to_download_file.txt --filter_path /video
```
## Arguments
base_url: The base URL of the webpage to scrape.
--output: The output file path (default: urls.txt).
--filter_path: The path to filter URLs (default: /video).
Example
For the following command:
```
python app.py https://www.xnxx.com/search/* --output urls.txt --filter_path /video
```
The script scrapes https://www.xnxx.com/search/query for all URLs that start with https://www.xnxx.com/video*
Saves the filtered URLs to urls.txt.
Downloads the videos from the URLs listed in urls.txt using youtube-dl.exe.
Removes urls.txt after a successful download.
Moves all .mp4 files to a subdirectory named query.

## Project Structure
```
web-scraper-and-video-downloader/
│
├── app.py                  # Main script source (redundant)
└── README.md               # Project documentation
```

Contributing
Contributions are welcome! Please fork the repository and use a feature branch. Pull requests are warmly welcome.

