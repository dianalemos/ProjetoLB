# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 13:12:40 2014

@author: SONY
"""

# GRUPO 3
# TAREFA ANÁLISE DE LITERATURA

from Bio import Entrez
from Bio import Medline


def procuraArtigos():
    # Procurar no PubMed todos os artigos que contêm informações acerca da Neisseria gonorrhoeae
    Entrez.email = "pg27658@alunos.uminho.pt"      # Dizer sempre ao NCBI quem somos
    handle = Entrez.egquery(term = "Neisseria gonorrhoeae")
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"] == "pubmed":
            print "Numero de artigos no PubMed: ", (row["Count"])
            
    return record
    
                
def download():
    # Fazer o download dos ID's de 400 artigos do PubMed
    print ""
    handle = Entrez.esearch(db = "pubmed", term = "Neisseria gonorrhoeae", retmax = 400) # dos 11110 existentes, vão ser apresentados 400
    record = Entrez.read(handle)
    idlist = record["IdList"]
    #print(idlist)
    
    return idlist


def obterRegistos(idlist):
    # Para obter os registos Medline correspondentes e extraír a informação
    handle = Entrez.efetch(db = "pubmed", id = idlist, rettype = "medline", retmode = "text")
    records = Medline.parse(handle)
    
    # para guardar os registos é necessário convertê-los numa lista
    records = list(records)
    
    # Percorrer os registos para imprimir alguma informação sobre cada um deles
    for record in records:
        print "TITLE: ", record.get("TI", "?")
        print "AUTHORS: ", record.get("AU", "?")
        print "SOURCE: ", record.get("SO", "?")
        print ""
        
    return records
        
    
def procuraTitulo(records):
    search_title = raw_input("Qual o artigo que procura: ")
        
    for record in records:
        if not "TI" in record:
            continue
        if search_title in record["TI"]:
            print ("%s encontrado: %s" % (search_title, record["SO"]))
            print ""
        
        
        
def procuraAutor(records):
    search_author = raw_input("Qual o autor que procura: ")
        
    for record in records:
        if not "AU" in record:
            continue
        if search_author in record["AU"]:
            print ("Autor %s encontrado: %s" % (search_author, record["SO"]))
            print ""



def teste():
    lista = download()
    registos = obterRegistos(lista)
    procuraTitulo(registos)
    procuraAutor(registos)




        

if __name__ == '__main__':
    teste()
    
    
# Ler paper da anotação do genoma
