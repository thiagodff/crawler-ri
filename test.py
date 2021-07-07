import time
from multiprocessing import Process
from urllib.parse import urlparse

from crawler.page_fetcher import PageFetcher
from crawler.scheduler import Scheduler

inicio = time.time()  # inicio do tempo execução
sites = ('http://www.uol.com.br', 'http://www.uai.com.br', 'http://www.terra.com.br', 'http://www.bbc.com',
         'http://www.g1.globo.com', 'http://www.tecmundo.com.br', 'http://www.olhardigital.com.br',
         'http://www.estadao.com.br', 'http://www.em.com.br', 'http://pt.stackoverflow.com')
depth_limit = 3  # limite de profundidade
page_limit = 30  # limite das páginas

sites_parsed = [urlparse(site) for site in sites]
escalonador = Scheduler('amarelaoBot', page_limit, depth_limit, sites_parsed)
# Scheduler(self, str_usr_agent, int_page_limit, int_depth_limit, arr_urls_seeds):

# instanciando o array de page fetcher
page_fetchers = [PageFetcher(escalonador) for _ in range(5)]

# inicializando cada um dos processos
processos = []
for fetcher in page_fetchers:
    p = Process(target=fetcher.run())
    p.start()
    processos.append(p)

# Finalizando os processos
for processo in processos:
    processo.join()
