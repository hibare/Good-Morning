import logging
from decouple import config, Csv
from apscheduler.schedulers.blocking import BlockingScheduler
from google_news import GoogleNews
from open_weather import OpenWeatherAPI
from slack_notification import send_notification

# Configure and create a logger
logging.basicConfig(format='%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] [%(levelname)s] %(name)s: %(message)s') 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

# Create a blocking scheduler
sched = BlockingScheduler(timezone=config('TIMEZONE'))

def run():
    logger.info("Starting program")


    # Process News

    news_interested_topics = config('NEWS_INTERESTED_TOPICS', cast=Csv())
    
    news = GoogleNews()

    for news_topic in news_interested_topics:
        n_result = news.by_topic(news_topic)

        if n_result.get("status"):
            text = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":newspaper: Daily News dose on topic `%s`." % (n_result.get("topic"))
                        }
                    }
                ]
            }

            for _ in n_result.get("news"):
                text["blocks"].append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*<%s|%s>*\n" % (_.get("link"), _.get("title"))
                    }
                })
            
            send_notification(text)

    news_location = config('NEWS_LOCATION')
    n_result = news.by_location()

    if n_result.get("status"):
        text = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":newspaper: Daily News dose from `%s`." % (n_result.get("country"))
                    }
                }
            ]
        }

        for _ in n_result.get("news"):
            text["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<%s|%s>*\n" % (_.get("link"), _.get("title"))
                }
            })
        
        send_notification(text)
    else:
        logger.exception("Failed to fetch news")

            
    # Process Weather
    weather_cities = config('WEATHER_CITIES', cast=Csv())
    weather_countries = config('WEATHER_COUNTRIES', cast=Csv())

    weather = OpenWeatherAPI()

    for i in range(len(weather_cities)):
        city = weather_cities[i]
        country = weather_countries[i]

        w_result = weather.one_call(city, country)

        if w_result.get("status"):
            text = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": ":sunflower: *Weather*"
                        }
                    }
                ]
            }
            text["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*%s, %s*\n\nCurrent: :thermometer: %s C  :wind_chime: %s m/s `%s`" % (city, country, w_result.get("weather").get("current").get("temp"), w_result.get("weather").get("current").get("wind_speed"), w_result.get("weather").get("current").get("description"))
                }
		    })
            
            hourly = list()

            for _ in w_result.get("weather").get("hourly"):
                hourly.append("%s :thermometer: %s C :wind_chime: %s m/s `%s`" % (_.get("hour"), _.get("temp"), _.get("wind_speed"), _.get("description")))

            text["blocks"].append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Forecast:\n%s" % ("\n".join(hourly))
                }
		    })

            send_notification(text)

        else:
            logger.error("Weather extraction failed for city=%s, country=%s, result=%s", city, country, w_result)
        


if __name__ == "__main__":
    sched.add_job(run, trigger='cron', hour='6', minute='0', id="get_things", replace_existing=True)
    logger.info("Job scheduled")
    
    sched.start()
    