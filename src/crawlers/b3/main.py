import os
import re
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest

class B3Spider(scrapy.Spider):

    name = "b3_spider"

    def start_requests(self):

        # URL to POST request
        url_base = 'http://bvmf.bmfbovespa.com.br/cias-listadas/empresas-listadas/BuscaEmpresaListada.aspx?idioma=pt-br'

        params = dict()

        params['opcao'] = '0'
        params['indiceAba'] = '0'
        params['idioma'] = 'pt-br'
        params['__EVENTTARGET'] = 'ctl00:contentPlaceHolderConteudo:BuscaNomeEmpresa1:btnTodas'

        yield FormRequest(url=url_base,
                          callback=self.parse_front,
                          method='POST',
                          formdata=params,
                          dont_filter=True,
                          headers={'Content-Type': 'application/x-www-form-urlencoded',
                                   'charset':'UTF-8',
                                   'Origin':'http://bvmf.bmfbovespa.com.br'})

    def parse_front(self, response):

        main_url_base = 'http://bvmf.bmfbovespa.com.br/pt-br/mercados/acoes/empresas/ExecutaAcaoConsultaInfoEmp.asp?'

        # Lista que armazena as companhias
        companies = list()

        companies_rows = response.css('tbody tr')

        for company_row in companies_rows:

            razao_social = company_row.css('td:nth-of-type(1) > a ::text')
            main_url = company_row.css('td:nth-of-type(1) > a ::attr(href)')
            nome_pregao = company_row.css('td:nth-of-type(2) > a ::text')
            segmento = company_row.css('td:nth-of-type(3)::text')

            # Segmento não informado: NDA
            if segmento.extract()[0].strip():
                seg = segmento.extract()[0].strip()
            else:
                seg = 'NDA'

            company_data = dict()

            company_data['razao_social'] = razao_social.extract()[0]
            company_data['main_url'] = main_url_base + 'CodCVM=' + str(main_url.extract()[0]).replace('ResumoEmpresaPrincipal.aspx?codigoCvm=', '')
            company_data['main_url'] = company_data['main_url'] + '&AnoDoc=2021'
            company_data['nome_pregao'] = nome_pregao.extract()[0]
            company_data['segmento'] = seg

            companies.append(company_data)

        # Follow the links to the next parser
        for data in companies:
            yield response.follow(url=data['main_url'],
                                  cb_kwargs=dict(metadata=data),
                                  callback=self.parse_pages)

    def parse_pages(self, response, metadata):

        # Códigos de Negociação (Lista)
        info_row_tickers = response.css('div#accordionDados > table tr:nth-of-type(2)')
        tickers = info_row_tickers.css('td:nth-of-type(2) > a.LinkCodNeg ::text').extract()

        # Classificação Setorial (Strings)
        info_row_setor = response.css('div#accordionDados > table tr:nth-of-type(5)')
        setor = info_row_setor.css('td:nth-of-type(2) ::text').extract()[0]
        divisao_setorial = str(setor).split('/')

        # Save all the data collected
        results_dict = dict()

        results_dict['razao_social'] = metadata['razao_social']
        results_dict['nome_pregao'] = metadata['nome_pregao']
        results_dict['segmento'] = metadata['segmento']
        results_dict['tickers'] = tickers
        results_dict['setor_economico'] = str(divisao_setorial[0]).strip()
        results_dict['subsetor'] = str(divisao_setorial[1]).strip()
        results_dict['segmento_setorial'] = str(divisao_setorial[2]).strip()
        results_dict['url_dados'] = response.url

        results_list.append(results_dict)


if __name__ == '__main__':

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    filename = 'b3'

    # List to save the data collected
    results_list = list()

    # Initiate a CrawlerProcess
    process = CrawlerProcess()

    # Tell the process which spider to use
    process.crawl(B3Spider)

    # Start the crawling process
    process.start()

    # Save the list of dicts
    # with open(os.path.join(THIS_DIR + '/data/results-{}.json'.format(filename)), 'w', encoding='utf8') as f:
    #     json.dump(results_list, f, ensure_ascii=False)