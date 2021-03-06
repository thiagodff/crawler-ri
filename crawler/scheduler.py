from time import sleep
from urllib import robotparser
from urllib.parse import ParseResult, urlparse
from util.threads import synchronized
from collections import OrderedDict
from .domain import Domain


class Scheduler:
    # tempo (em segundos) entre as requisições
    TIME_LIMIT_BETWEEN_REQUESTS = 20

    def __init__(self, str_usr_agent, int_page_limit, int_depth_limit, arr_urls_seeds):
        """
            Inicializa o escalonador. Atributos:
                - `str_usr_agent`: Nome do `User agent`. Usualmente, é o nome do navegador, em nosso caso,  será o nome do coletor (usualmente, terminado em `bot`)
                - `int_page_limit`: Número de páginas a serem coletadas
                - `int_depth_limit`: Profundidade máxima a ser coletada
                - `int_page_count`: Quantidade de página já coletada
                - `dic_url_per_domain`: Fila de URLs por domínio (explicado anteriormente)
                - `set_discovered_urls`: Conjunto de URLs descobertas, ou seja, que foi extraída em algum HTML e já adicionadas na fila - mesmo se já ela foi retirada da fila. A URL armazenada deve ser uma string.
                - `dic_robots_per_domain`: Dicionário armazenando, para cada domínio, o objeto representando as regras obtidas no `robots.txt`
        """
        self.str_usr_agent = str_usr_agent
        self.int_page_limit = int_page_limit
        self.int_depth_limit = int_depth_limit
        self.int_page_count = 0

        self.dic_url_per_domain = OrderedDict()
        self.set_discovered_urls = set()
        self.dic_robots_per_domain = {}

        for url in arr_urls_seeds:
            self.add_new_page(url, 1)

    @synchronized
    def count_fetched_page(self):
        """
            Contabiliza o número de paginas já coletadas
        """
        self.int_page_count += 1

    def has_finished_crawl(self):
        """
            Verifica se finalizou a coleta
        """
        return self.int_page_count > self.int_page_limit

    @synchronized
    def can_add_page(self, obj_url: ParseResult, depth: int) -> bool:
        """
            Retorna verdadeiro caso  profundidade for menor que a maxima
            e a url não foi descoberta ainda
        """
        domain = Domain(obj_url.hostname, Scheduler.TIME_LIMIT_BETWEEN_REQUESTS)
        try:
            value = self.dic_url_per_domain[domain]
        except KeyError:
            pass
        else:
            if (obj_url, depth) in value:
                return False
        return self.int_depth_limit > depth

    @synchronized
    def add_new_page(self, obj_url: ParseResult, depth: int) -> bool:
        """
            Adiciona uma nova página
            obj_url: Objeto da classe ParseResult com a URL a ser adicionada
            depth: Profundidade na qual foi coletada essa URL
        """
        # https://docs.python.org/3/library/urllib.parse.html
        if not self.can_add_page(obj_url, depth):
            return False
        domain = Domain(obj_url.hostname, Scheduler.TIME_LIMIT_BETWEEN_REQUESTS)
        if not (domain in self.dic_url_per_domain):  # Se não existir ainda o domínio no dicionário
            self.dic_url_per_domain[domain] = [(obj_url, depth)]  # Cria uma nova lista para aquele domíno
        else:
            self.dic_url_per_domain[domain].append((obj_url, depth))  # Adiciona na lista existente do domínio
        self.set_discovered_urls.add(obj_url.geturl())
        return True

    @synchronized
    def get_next_url(self) -> tuple:
        """
        Obtém uma nova URL por meio da fila. Essa URL é removida da fila.
        Logo após, caso o servidor não tenha mais URLs, o mesmo também é removido.
        """
        for domain in self.dic_url_per_domain.keys():
            if domain.is_accessible():
                # Não extraia self.dic_url_per_domain[domain] para uma variável, pois essas modificações devem ser
                # feitas por referência
                if len(self.dic_url_per_domain[domain]) > 0:
                    self.__acess_domain(domain)
                    return self.dic_url_per_domain[domain].pop(0)
        sleep(Scheduler.TIME_LIMIT_BETWEEN_REQUESTS)
        return None, None

    def __acess_domain(self, domain):
        value = self.dic_url_per_domain[domain]
        domain.accessed_now()
        self.dic_url_per_domain[domain] = value

    def can_fetch_page(self, obj_url) -> bool:
        """
        Verifica, por meio do robots.txt se uma determinada URL pode ser coletada
        """
        url = obj_url.geturl()
        url_p = urlparse(url)
        if not (url_p.netloc in self.dic_robots_per_domain.keys()):
            rp = robotparser.RobotFileParser()
            rp.set_url(url)
            rp.read()
            self.dic_robots_per_domain[url_p.netloc] = rp.can_fetch("*", url)
        return self.dic_robots_per_domain[url_p.netloc]
