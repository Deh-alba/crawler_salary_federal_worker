import scrapy
from selenium import webdriver
import pandas
from urllib.parse import urljoin

class salary_spider(scrapy.Spider):
    name = "salary"
    siape = dict()

    # exemple
    # start_urls = ['https://www.portaldatransparencia.gov.br/servidores/Servidor-DetalhaServidor.asp?IdServidor=1001717']
    # https://www.portaldatransparencia.gov.br/servidores/Servidor-ListaServidores.asp?bogus=1&Pagina=1&TextoPesquisa=andre


    def start_requests(self):

        urls = list()
        arq = pandas.read_csv("servidores_ativos_ufpel.csv")
        servidore = arq["nome"]
        siapeUtil = arq["siape"]

        while servidore.count()!=0:
            
            base = "https://www.portaldatransparencia.gov.br/servidores/Servidor-ListaServidores.asp?bogus=1&Pagina=1&TextoPesquisa="
            
            name = servidore.head(1).to_string().split("    ")
            name = name[len(name)-1]
            self.siape[name] = siapeUtil.head(1).to_string().split("    ") [1]         
            
            urls.append(base+name.replace(' ', '%20'))
            
            servidore.drop(servidore.head(1).index, inplace=True)
            
            
            siapeUtil.drop(siapeUtil.head(1).index, inplace=True)
            
        

        for url in urls:
            #print(url)

            yield scrapy.Request(url=url, callback=self.parse)
