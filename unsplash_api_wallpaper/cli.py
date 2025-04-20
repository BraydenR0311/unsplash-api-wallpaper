import argparse

from unsplash_api_wallpaper.config import IMAGE_DIR
from unsplash_api_wallpaper.unsplash_api import UnsplashApi, download_to_jpg

parser = argparse.ArgumentParser("Unsplash API")
parser.add_argument(
    "-s",
    "--search",
    nargs="?",
    type=str,
    default="",
    help="Search query for desired image.",
)
parser.add_argument(
    "-n",
    "--number",
    nargs="?",
    type=int,
    default=1,
    help="Number of images to download.",
)

args = parser.parse_args()

if __name__ == "__main__":
    unsplash = UnsplashApi()

    data = unsplash.rand(args.search, args.number)
    _ = download_to_jpg(data, IMAGE_DIR)
    print(
        f"Current size of cache: "
        f"{len([f for f in IMAGE_DIR.iterdir() if f.is_file()])} files."
    )
