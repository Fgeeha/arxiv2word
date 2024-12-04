# arxiv2word

## Description

The project is designed to easily receive word files of articles from arxiv.org

Uses Python (icecream + aiofiles + aiohttp + beautifulsoup4 + requests) + Poetry + makefile + Docker + Pandoc

## Using

First download the project and then write to launch it:

If you have a make on PC

```bash
make build
make run
```

if you don't have make on PC

```bash
docker build -t arxiv-downloader
docker run -it --rm -v $(pwd)/output:/app/output arxiv-downloader
```
