import asyncio
import os
import re
import subprocess
from typing import Optional
from urllib.parse import urljoin

import aiohttp
import requests
from aiofiles import open as aio_open
from bs4 import BeautifulSoup
from icecream import ic
from requests.exceptions import (
    RequestException,
    Timeout,
)


# Directory for saving output files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


# Function for extracting the article ID from the link
def extract_arxiv_id(url: str) -> Optional[str]:
    pattern = r"(?:arxiv\.org(?:/pdf|/abs)/|ar5iv\.labs\.arxiv\.org/html/)(\d+\.\d+)"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


async def clean_images_from_folder(folder_path: str = OUTPUT_DIR) -> None:
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        ic(f"Folder not found: {folder_path}")
        return

    for file in files:
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path) and any(
            file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS
        ):
            try:
                os.remove(file_path)
                ic(f"The file was deleted: {file}")
            except Exception as e:
                ic(f"Error deleting a file {file}: {e}")

        elif os.path.isdir(file_path):
            await clean_images_from_folder(file_path)


# Asynchronous function for downloading images
async def download_image(
    session: aiohttp.ClientSession,
    url: str,
    output_dir: str,
) -> None:
    try:
        if url.startswith("data:image"):
            ic(f"Skipping the image (base64): {url}")
            return
        img_data = await session.get(url)
        img_data.raise_for_status()  # Проверка на успешный запрос
        img_name = os.path.join(output_dir, os.path.basename(url))
        if not os.path.exists(img_name):
            async with aio_open(img_name, "wb") as img_file:
                await img_file.write(await img_data.read())
            ic(f"The image has been downloaded: {img_name}")
    except Exception as e:
        ic(f"Error downloading the image {url}: {e}")


# Asynchronous function for downloading all images from an HTML page
async def download_images(
    html_content: str,
    output_dir: str,
    base_url: str = "https://ar5iv.labs.arxiv.org",
) -> None:
    soup = BeautifulSoup(html_content, "html.parser")
    image_urls = [
        urljoin(base_url, img["src"]) for img in soup.find_all("img", src=True)
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, img_url, output_dir) for img_url in image_urls]
        await asyncio.gather(*tasks)


# A function for correcting paths to images in HTML
def fix_image_paths_in_html(html_content: str, output_dir: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")

    # Replacing all relative paths with local paths
    for img in soup.find_all("img", src=True):
        img_path = img["src"]

        # If the path is relative, replace it with the path available inside the container
        if img_path.startswith("/html") or img_path.startswith("/assets"):
            img["src"] = os.path.join(output_dir, os.path.basename(img_path))

    # We return the corrected HTML as a string
    return str(soup)


# Function for converting HTML to Word
def convert_html_to_word(html_filename: str) -> None:
    output_filename = html_filename.replace(".html", ".docx")
    command = ["pandoc", html_filename, "-o", output_filename]
    try:
        subprocess.run(command, check=True)
        ic(f"The file has been successfully converted: {output_filename}")
    except subprocess.CalledProcessError as e:
        ic(f"Conversion error: {e}")
    except FileNotFoundError:
        ic("Error: Pandoc is not installed. Install Pandoc to continue.")


# Function for downloading HTML pages and processing
async def download_arxiv_html(arxiv_id: str) -> Optional[str]:
    url = f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        html_filename = os.path.join(OUTPUT_DIR, f"{arxiv_id}.html")
        html_content = response.text

        # Downloading images asynchronously
        await download_images(html_content, OUTPUT_DIR)

        # Correcting paths to images in HTML
        fixed_html_content = fix_image_paths_in_html(html_content, OUTPUT_DIR)

        # Saving the corrected HTML file
        with open(html_filename, "w", encoding="utf-8") as file:
            file.write(fixed_html_content)
        ic(f"The HTML file is saved as {html_filename}")
        return html_filename

    except Timeout:
        ic(f"Error: The timeout for connecting to the {url} has expired.")
    except RequestException as e:
        ic(f"Error when downloading an article from {url}: {e}")
    except Exception as e:
        ic(f"Unknown error: {e}")

    return None


# Главная функция программы
async def main() -> None:
    url = input(
        "Enter the link to the article (for example, https://arxiv.org/abs/2403.01915 ): ",
    ).strip()

    # Extracting the arxiv ID from the URL
    arxiv_id = extract_arxiv_id(url)

    if arxiv_id:
        # Uploading an HTML article
        html_filename = await download_arxiv_html(arxiv_id)
        if html_filename:
            # Converting HTML to Word
            convert_html_to_word(html_filename)
            # Clearing the folder
            await clean_images_from_folder(OUTPUT_DIR)
    else:
        ic(f"Couldn't identify the id - {url}")


# Launching the program
if __name__ == "__main__":
    ic.disable()
    asyncio.run(main())
