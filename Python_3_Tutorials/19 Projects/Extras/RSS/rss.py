#!/usr/bin/python3
__author__ = "Santhosh Baswa"

from xml.dom.minidom import parse
from urllib.request import urlopen
from html.parser import HTMLParser

DEFAULT_NAMESPACES = (
    None, # RSS 09.1, 0.92, 0.93, 0.94, 2.0
    'http://purl.org/rss/1.0/', # RSS 1.0
    'http://my.netscape.com/rdf/simple/0.9/', # RSS 0.90
    'http://www.w3.org/2005/Atom', # ATOM
    'http://purl.org/dc/elements/1.1/' # dublin core namespace
)

class HTMLDataOnly(HTMLParser):
    ''' only gets data (text) from HTML -- no tags! '''
    def handle_data(self, data):
        self._data = ' '.join([self._data, data]) if hasattr(self, 'data') else data
    def get_data(self):
        return self._data

class RSS:
    def __init__(self, url):
        self.feed = parse(urlopen(url))

        # rss or atom?
        for t in ('item', 'entry'):
            self.node = self.getElementsByTagName(self.feed, t)
            if self.node: break

        self.feedTitle = self.textOf(self.first(self.feed, 'title'))
        self.feedDescription = self.textOf(self.first(self.feed, 'description'))
        self.feedURL = url
        self._index = 0;

    def next_index(self, i = None):
        print("next_index", self._index)
        if i is None: self._index += 1
        elif i < 0: self._index = None
        else: self._index = i
        if self._index >= len(self.node): self._index = None 
        return self._index

    def title(self, n = None):
        return self.textOfNode('title', n).strip()

    # atom uses an href attribute for the link
    def link(self, n = None):
        if n is None: n = self.node[self._index]
        l = self.textOfNode('link', n).strip()
        return l if l else self.attrOf(n, 'link', 'href').strip()

    def description(self, n = None):
        htmldata = HTMLDataOnly()
        for t in ('description', 'summary'):
            text = self.textOfNode(t, n)
            if text:
                htmldata.feed(text)
                return htmldata.get_data().strip()
        return ''

    def date(self):
        for t in ('date', 'pubDate'):
            s = self.textOfNode(t)
            if s: return s

    def getElementsByTagName(self, node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
        for namespace in possibleNamespaces:
            children = node.getElementsByTagNameNS(namespace, tagName)
            if len(children): return children
        return []

    def first(self, node, tagName, possibleNamespaces=DEFAULT_NAMESPACES):
        children = self.getElementsByTagName(node, tagName, possibleNamespaces)
        return children[0] if len(children) else None

    def attrOf(self, node, element, attr):
        n = self.first(node, element)
        return n.getAttribute(attr) if n else ''

    def textOf(self, node):
        return ''.join([child.data for child in node.childNodes]) if node else ''

    def textOfNode(self, tagName, n = None):
        if n is None: n = self.node[self._index]
        return self.textOf(self.first(n, tagName))

    def record(self, n):
        return {
            'title': self.title(n),
            'link': self.link(n),
            'description': self.description(n),
            'index': self.node.index(n)
        }

    def records(self):
        for n in self.node:
            yield self.record(n)

def main():
    for url in (
        'http://feeds.nytimes.com/nyt/rss/Books',
        'http://billweinman.wordpress.com/feed/',
        'http://perlhacks.com/atom.xml'
    ): 
        rss = RSS(url)
        for r in rss.records():
            print("node {} of {}".format(r['index'] + 1, len(rss.node)))
            print(r['title'])
            print(r['link'])
            print(r['description'])

if __name__ == "__main__": main()
