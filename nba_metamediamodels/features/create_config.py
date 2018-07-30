import configparser
config = configparser.ConfigParser()
site ='theringer.com'
config[site] = {}
ringer = config[site]
ringer['rooturl'] = 'https://www.theringer.com/'
ringer['link_name'] = "h2"
ringer['link_class'] = "c-entry-box--compact__title"
ringer['archivepath'] = "archives/nba/{year}/{month}"
ringer['author_name'] = "span"
ringer['author_class'] = "c-byline__item"
ringer['pubdate_name'] = "time"
ringer['pubdate_class'] = "c-byline__item"
ringer['body_name'] = "div"
ringer['body_class'] = "c-entry-content"
with open('html_config.ini', 'w') as configfile:
    config.write(configfile)