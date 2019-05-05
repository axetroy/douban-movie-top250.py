from scrapy.cmdline import execute

# execute(['scrapy', 'crawl', 'greasyfork', '-s', 'JOBDIR=crawls/greasyfork'])
execute(['scrapy', 'crawl', 'douban_movie'])
