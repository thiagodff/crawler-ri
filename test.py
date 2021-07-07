import time
from multiprocessing import Process
from urllib.parse import urlparse

from crawler.page_fetcher import PageFetcher
from crawler.scheduler import Scheduler


def test():
    inicio = time.time()  # inicio do tempo execução
    sites = ('https://www.uol.com.br', 'https://www.uai.com.br', 'https://www.terra.com.br', 'https://www.bbc.com',
             'https://www.g1.globo.com', 'https://www.tecmundo.com.br', 'https://www.olhardigital.com.br',
             'https://www.estadao.com.br', 'https://www.em.com.br')
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
    fim = time.time()
    print(f'Tempo gasto: {fim - inicio}')


if __name__ == '__main__':
    test()
