# Line-Bot
You can read Dcard’s popular articles, daily stock prices and popular movies


## A brief introduction to job content
- Connecting with Heroku using Line Developers
- Use Selenium and Chromedriver to crawl data
- Use Git to push programs to Heroku


## A brief introduction to main module
### app

- Listen for all Post Requests from /callback
- Process messages

### crawler
- There is a class called crawler
- The methods of this class include crawling Dcard articles, movie types, and stock information

### getForum
- Get Dcard forum list
- Save data into csv file

### getMovie
- Get a list of movie genres
- Save data into csv file