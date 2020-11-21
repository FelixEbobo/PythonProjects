from urllib.request import urlopen
from urllib.parse import urlparse
import re
import sys
LINK_REGEXP = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")

class LinkCollector:
    def __init__(self, url):
        self.url = '' + urlparse(url).netloc
        self.collected_links = {}
        self.visited_links = set()
    
    def collect_links(self, path='/'):
        full_url = 'http://' + self.url + path
        self.visited_links.add(full_url)
        page = str(urlopen(full_url).read())
        links = LINK_REGEXP.findall(page)
        links = {self.normalize_link(path, link
                ) for link in links}
        self.collected_links[full_url] = links
        for link in links:
            self.collected_links.setdefault(link, set())
        # print(links, self.visited_links,
                # self.collected_links, unvisited_links, sep='\n')

    def normalize_link(self, path='', link=''):
        template = re.compile('https?://')
        if re.match(template, link) is not None:
            return link
        if link.startswith('/'):
            return self.url + link
        else:
            return self.url + path.rpartition(
                    '/')[0] + '/' + link
        

if __name__ == "__main__":
    link = 'http://localhost:8000'
    collector = LinkCollector(link)
    collector.collect_links()
    for link, item in collector.collected_links.items():
        print(f"{link}: {item}")
