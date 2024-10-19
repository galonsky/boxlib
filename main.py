import csv
from collections import defaultdict

import requests
import json
from typing import Generator

from rss_parser import RSSParser


def get_watchlist(filename: str) -> Generator[str, None, None]:
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row["Name"]


def get_library_results(title: str):
    response = requests.get(f"https://catalog.minlib.net/Search/Results?join=AND&bool0[]=AND&lookfor0[]={title}&type0[]=Title&filter[]=format_category%3A%22Movies%22&filter[]=availability_toggle%3A%22global%22&filter[]=format%3A%22Blu-ray%22&sort=relevance&view=rss&searchSource=local")
    rss = RSSParser.parse(response.text)
    for item in rss.channel.items[:5]:
        yield {
            "title": item.title.content,
            "url": item.guid.content,
            "description": item.description.content,
        }


if __name__ == '__main__':
    watchlist = list(get_watchlist("watchlist.csv"))
    results = defaultdict(list)
    for title in watchlist:
        for result in get_library_results(title):
            results[title].append(result)
    print(json.dumps(results))
