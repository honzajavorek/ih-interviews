import os
from datetime import datetime

import pytz
from algoliasearch.search_client import SearchClient
from feedgen.feed import FeedGenerator


if __name__ == '__main__':
    client = SearchClient.create(os.environ['APP_ID'], os.environ['API_KEY'])
    index = client.init_index('interviews_publishedAt_desc')
    articles = index.search('')['hits']

    fg = FeedGenerator()
    fg.title('IH Interviews')
    fg.id('ih-interviews-20201123-205642')
    pubs = []
    for article in articles:
        pub = datetime.fromtimestamp(article['publishedAt'] / 1000).replace(tzinfo=pytz.timezone('UTC'))
        pubs.append(pub)
        fe = fg.add_entry()
        fe.id(article['interviewId'])
        fe.published(pub)
        fe.pubDate(pub)
        fe.updated(pub)
        fe.title(article['title'])
        fe.link(href=f"https://www.indiehackers.com/interview/{article['interviewId']}")
    fg.updated(max(pubs))
    print(fg.atom_str(pretty=True).decode())
