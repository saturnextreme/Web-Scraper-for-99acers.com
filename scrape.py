from scraper.PropertyCrawler import PropertyCrawler

state = ['Bengaluru', 'Pune', 'Delhi', 'Mumbai', 'Lucknow', 'Agra', 'Ahmedabad', 'Kolkata', 'Jaipur', 'Chennai']

for s in state:
    with PropertyCrawler() as bot:
        bot.page()
        bot.changeLocation(state=s)
        data = bot.checkData(city_=s)
