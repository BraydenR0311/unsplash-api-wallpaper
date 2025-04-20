# unsplash-api-wallpaper

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Python wrapper around [Unsplash](https://unsplash.com) for convenient image downloading.

## Goal
Unsplash has some of the best photos, which would be great wallpapers. I wanted to build my own way of fetching random pictures through the API. In this way, the user can set up systemd services/timers to fetch images every so often.

## Setup
Currenly, I'm running [dwm](https://dwm.suckless.org/) for my window manager (along with other [suckless](https://suckless.org) tools like [st](https://st.suckless.org), [slstatus](https://tools.suckless.org/slstatus/), and [dmenu](https://tools.suckless.org/dmenu/)).

## Usage
The program is exposed as a command-line tool.
```
pip install -e .
python -m unsplash_api_wallpaper.cli orangutans 3 # Pull 3 random images of orangutans.
```

If no args are specified to the cli, it will parse search_terms.txt, a newline separated file of search terms, and randomly chose one. I have some terms in there that I want as wallpapers.

I have a shell script, turned into a systemd service, that chooses a random image from a chosen directory of images.
```
#!/usr/bin/bash

# Wallpaper directory
WALLPAPER_DIR=~/Documents/wallpapers/
IMG=$(find $WALLPAPER_DIR -type f | shuf -n 1)

# Use random background image
feh --bg-fill ${IMG}

```

A systemd timer will then start this every so often.
```
[Unit]
Description=Create random background periodically.
After=graphical.target

[Timer]
OnBootSec=30min
OnUnitActiveSec=30min
Unit=random-background.service

[Install]
WantedBy=default.target
```

## TODO
- Implement deletion of old files once max cache size is exceeded.
- Store image data in a csv (location, author, image properties, etc.)
- Add entry point in pyproject.toml so script can be called like ```unsplash-rand -s foo -n 42```

## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         unsplash_api_wrapper and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── unsplash_api_wallpaper   <- Source code for use in this project.
```

--------

