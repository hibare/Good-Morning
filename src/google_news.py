import logging
import requests
import xml
from bs4 import BeautifulSoup

# Configure and create a logger
logging.basicConfig(format='%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] [%(levelname)s] %(name)s: %(message)s') 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

class GoogleNews:

    def __init__(self):
        self.VALID_TOPICS = [
            "WORLD",
            "NATION",
            "BUSINESS",
            "TECHNOLOGY",
            "ENTERTAINMENT",
            "SPORTS",
            "SCIENCE",
            "HEALTH"
        ]

    def by_topic(self, topic="WORLD"):
        result = dict(
            type="topic",
            topic=topic,
            status=False,
            error=None,
            news=list()
        )

        if topic in self.VALID_TOPICS:

            try:
                url = "https://news.google.com/news/rss/headlines/section/topic/{0}".format(topic)
                response = requests.get(url, timeout=60)
                content = response.text

                bs = BeautifulSoup(content, "xml")
                news_list = bs.findAll("item")

                news = list()

                for _ in news_list:
                    news.append(dict(
                        title=_.title.text,
                        link=_.link.text,
                        published=_.pubDate.text
                    ))

                result.update(
                    status=True,
                    news=news[:40]
                )

            except Exception:
                logger.exception("Exception in request")
                result.update(
                    error="Exception in request"
                )

        else:
            result.update(
                error="Invalid topic"
            )

        return result

    def by_location(self, location="IN"):
        result = dict(
            type="location",
            country=location,
            status=False,
            error=None,
            news=list()
        )

        try:
            url = "https://news.google.com/rss?hl=en-{0}&gl={0}&ceid={0}:en".format(location)
            response = requests.get(url, timeout=60)
            content = response.text

            bs = BeautifulSoup(content, "xml")
            news_list = bs.findAll("item")

            news = list()

            for _ in news_list:
                news.append(dict(
                    title=_.title.text,
                    link=_.link.text,
                    published=_.pubDate.text
                ))

            result.update(
                status=True,
                news=news[:40]
            )

        except Exception:
            logger.exception("Exception in request")
            result.update(
                error="Exception in request"
            )

        return result

