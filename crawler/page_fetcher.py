from bs4 import BeautifulSoup
from threading import Thread
import requests
from urllib.parse import urlparse, urljoin, ParseResult

from crawler.scheduler import Scheduler


class PageFetcher(Thread):
    USER_AGENT = 'bot_rachadores'

    def __init__(self, obj_scheduler: Scheduler):
        super().__init__()
        self.obj_scheduler = obj_scheduler

    def request_url(self, obj_url: ParseResult):
        """
            Faz a requisição e retorna o conteúdo em binário da URL passada como parametro

            obj_url: Instancia da classe ParseResult com a URL a ser requisitada.
        """
        response = requests.get(url=obj_url.geturl(), headers={'User-Agent': PageFetcher.USER_AGENT})
        return response.content if 'text/html' in response.headers['Content-Type'] else None

    def discover_links(self, obj_url: ParseResult, depth: int, bin_str_content):
        """
        Retorna os links do conteúdo bin_str_content da página já requisitada obj_url
        """
        soup = BeautifulSoup(bin_str_content, features="lxml")
        new_url, new_depth = None, None
        for link in soup.select('a'):
            try:
                aux_url = urlparse(link['href'])
            except KeyError:
                break
            else:
                if aux_url.hostname is None:
                    new_url = urlparse(obj_url.scheme + '://' +
                                       obj_url.hostname + '/' + aux_url.path)
                else:
                    new_url = aux_url
                new_depth = 0 if obj_url.hostname != new_url.hostname else depth + 1
        yield new_url, new_depth

    def crawl_new_url(self) -> None:
        """
            Coleta uma nova URL, obtendo-a do escalonador
        """
        url, depth = self.obj_scheduler.get_next_url()
        if url is not None:
            response = self.request_url(url)
            if response is not None:
                for url, depth in self.discover_links(url, depth, response):
                    print(f'URL: {url.geturl()}')

    def run(self):
        """
            Executa coleta enquanto houver páginas a serem coletadas
        """
        while not self.obj_scheduler.has_finished_crawl():
            self.crawl_new_url()
