# Crawler - Recuperação de Informação

## Descrição
Este é um coletor genérico desenvolvido em Python sobre perspectiva orientada à objeto. Seu propósito é fazer buscas na web e armazenar as páginas encontradas dado determinado número de URL's, um limite máximo de exploração por URL e uma quantidade finita de páginas a serem buscadas.

O projeto possui 3 principais arquivos: `domain.py`, `scheduler.py` e `page_fetcher.py`. Cada método desenvolvido foi submetido a testes disponíveis em `scheduler_test.py` e `page_fetcher_test.py`. Todos os arquivos supra citados encontram-se na pasta `./crawler`. Além disso, para melhor apurar os testes e resultados, existem os arquivos jupyter `Coding Dojo - Crawler.ipynb` e `relatorio.ipynb`.

Cabe ressaltar que este coletor foi consolidado sobre o propósito de apenas baixar páginas públicas e a politica de solicitação aos servidores segue as diretrizes de arquivos `robots.txt` estabelecido pelo Google, que pode ser consultada no [link](https://developers.google.com/search/docs/advanced/robots/create-robots-txt?hl=pt-br).

## User Agent:

`amarelaoBot`

## Desenvolvido por:

- [Cristhian Minoves](https://github.com/CMinoves)
- [Pierre Vieira](https://github.com/PierreVieira)
- [Thiago Dornelles](https://github.com/thiagodff)
- [Vinícius Silva](https://github.com/vnszero)

## Sobre orientação do professor:

- [Daniel Hasan](https://github.com/daniel-hasan)

## Objetivo:

> O propósito da coleta é recolher páginas dos links escolhidos.
> As coletas foram feitas na data: 12/07/21.