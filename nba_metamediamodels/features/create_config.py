# this file creates a config file called:
CONFIG_FILENAME = 'html_config.ini'
print(f'This script will output a config file called: {CONFIG_FILENAME}')

# the config file will contain an "entry" (config._sections[entry])
# for each site that we'd like to scrape data from

# we'll use configparser, which is in the standard lib:
# https://docs.python.org/3/library/configparser.html
import configparser

# note - there are many ways to write a config file, but I did it this way, because it was the first thing I found.

# instantiate the config object
config = configparser.ConfigParser()

# make one section of the config file (the ringer)
site ='theringer.com'
print(f'making config for {site} ...')

# so that we don't have to build the whole dictionary all at once, we'll assign the first section of the file,
# denoted by "config[site]" to be an empty dict.
# note however, that the config file will NOT look like a dictionary (no curly brackets)
# in configparser, the dictionary is represented by line-separated `KEY = VALUE` pairs
# look at the pictures in the documentation to see more
config[site] = {}

# if we were to do `config.write(CONFIG_FILENAME)` right now, it'd look like this:
# ```
# [theringer.com]
#
# ```

# just so that we don't have to keep repeating congif[site][KEY] for every entry,
# we'll reassign this object to a shorter and more descriptive variable, "ringer"
ringer = config[site]
ringer['rooturl'] = 'https://www.theringer.com/'
ringer['link_name'] = "h2"
ringer['link_class'] = "c-entry-box--compact__title"
ringer['archive_path_example'] = "archives/nba/{archive_start_year}/{archive_start_month}"
ringer['archive_path_prefix'] = "archives/nba/"
ringer['archive_start_month'] = "3"
ringer['archive_start_year'] = "2016"
ringer['author_name'] = "span"
ringer['author_class'] = "c-byline__item"
ringer['pubdate_name'] = "time"
ringer['pubdate_class'] = "c-byline__item"
ringer['body_name'] = "div"
ringer['body_class'] = "c-entry-content"

# this syntax is unique to configparser, where you can see the dict entries for any "section"
# in this case, a "section" is defined as any top-level dict
# so far, we only have config['theringer.com'] (defined in line 26), so there's only 1 section
# but in the future, if we also define config['grantland.com'], then the file would look like this:
# ```
# [theringer.com]
# ...
# entries
# ...
#
#
# [grantland.com]
# ...
# entries
# ...
#
#
# ```


# let's print out what we've done for this first section, just as a sanity check
print(config._sections[site])

# and finally write the file to its .ini location
# note, we're using 'w' ~ 'Write', versus using 'r' for 'Read'
# also note the use of the WITH statement, so as to immediately close the file after we write to it
with open(CONFIG_FILENAME, 'w') as configfile:
    config.write(configfile)