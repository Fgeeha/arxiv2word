# arxiv2word

## Description

The project is designed to easily receive word files of articles from arxiv.org

Uses [Python](https://www.python.org/) (icecream + aiofiles + aiohttp + beautifulsoup4 + requests) + [Poetry](https://python-poetry.org/docs/) + [makefile](https://www.gnu.org/software/make/) + [Docker](https://www.docker.com/) + [Pandoc](https://pandoc.org/installing.html)

## Using (docker)

First download the project and then write to launch it:

If you have a make on PC

```bash
make build
make run
```

if you don't have make on PC (linux or macos)

```bash
docker build -t arxiv-downloader .
docker run -it --rm -v $(pwd)/output:/app/output arxiv-downloader
```

if you don't have make on PC (Windows)

```bash
docker build -t arxiv-downloader .
docker run -it --rm -v $(cd)/output:/app/output arxiv-downloader
```

## Using (without docker)

You need to put [Pandoc](https://pandoc.org/installing.html) and [Poetry](https://python-poetry.org/docs/) on your device

Linux:

```bash
poetry install
poetry run python3 main.py
```

Windows:

```bash
poetry install
poetry run py .\main.py
```
