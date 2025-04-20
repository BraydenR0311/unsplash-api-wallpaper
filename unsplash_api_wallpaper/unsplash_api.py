import os
from pathlib import Path
import random

from dotenv import load_dotenv
from PIL import Image
import requests

from unsplash_api_wallpaper.config import IMAGE_DIR, SEARCH_TERM_FILE
from unsplash_api_wallpaper.query import Query

# Load api key into environment.
load_dotenv()


class UnsplashApi:
    """Simple wrapper around the Unsplash image website api."""

    def __init__(self, root="https://api.unsplash.com/"):
        # Ensure root url ends with a slash.
        if not root.endswith("/"):
            root = root + "/"
        self.root = root
        self.access_key = os.environ["UNSPLASH_ACCESS_KEY"]
        # default query for image request.
        self.query = Query(
            {"client_id": self.access_key, "orientation": "landscape"}
        )

        # Parse newline separated file for search terms.
        with open(SEARCH_TERM_FILE, "r", encoding="utf8") as f:
            self.random_searches = [
                line.strip().lower() for line in f.readlines()
            ]

    def rand(self, search_str: str = "", n: int = 1) -> list:
        """Pull n random images with the given search string.

        If no search_str is specified, choose randomly from SEARCH_TERM_FILE.
        """
        if not search_str:
            search_str = random.choice(self.random_searches)
            print(f"No search term specified. Using '{search_str}'.")
        endpoint = "photos/random/"
        response = requests.get(
            self.root
            + endpoint
            + self.query({"query": search_str, "count": str(n)})
        )
        response.raise_for_status()
        return response.json()


def download_to_jpg(data: list, dirpath: str | os.PathLike) -> list:
    """Unplash data is a list of dicts where each item is data for a single
    image. Attempt to download an image from the website and save to a directory."""
    if type(data) is not list:
        raise TypeError("Data must be a list.")

    dirpath = Path(dirpath)
    if not dirpath.is_dir():
        FileNotFoundError("Either doesn't exist or isn't a directory.")

    saved_images = []
    for img in data:
        # Proper filename.
        filename = img["slug"] + ".jpg"
        # URL for one of the image types.
        url = img["urls"]["raw"]

        # Attempt to download image.
        print(f"Downloading: {url}.")
        response = requests.get(url)
        # Raise error if unsuccessful for any reason.
        response.raise_for_status()
        # Get bytes data if successful.
        raw = response.content

        # Add filename to the directory path.
        filepath = dirpath.resolve() / filename

        # Write save to disk.
        print(f"Saving to {filepath}.")
        with open(filepath, "wb") as f:
            f.write(raw)
        # Keep track of filepaths.
        saved_images.append(filepath)

    print(f"Downloaded {len(saved_images)} images.")

    return saved_images


if __name__ == "__main__":
    unsplash = UnsplashApi()
    data = unsplash.rand("Golden Colorado", 3)
    image_paths = download_to_jpg(data, IMAGE_DIR)

    pil_imgs = [Image.open(img) for img in image_paths]
