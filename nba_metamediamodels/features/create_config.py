import configparser
config = configparser.ConfigParser()
site ='theringer.com'
config[site] = {}
ringer = config[site]
ringer['rooturl'] = 'https://www.theringer.com/'
ringer['link_name'] = "h2"
ringer['link_class'] = "c-entry-box--compact__title"
ringer['archivepath'] = "archives/nba/{archive_start_year}/{archive_start_month}"
ringer['archive_start_month'] = "3"
ringer['archive_start_year'] = "2016"
ringer['author_name'] = "span"
ringer['author_class'] = "c-byline__item"
ringer['pubdate_name'] = "time"
ringer['pubdate_class'] = "c-byline__item"
ringer['body_name'] = "div"
ringer['body_class'] = "c-entry-content"
with open('html_config.ini', 'w') as configfile:
    config.write(configfile)