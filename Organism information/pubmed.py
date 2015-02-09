# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 13:12:40 2014

@author: Grupo 3
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
    handle = Entrez.esearch(db = "pubmed", term = "Neisseria gonorrhoeae", retmax = 400) # 400 do total existentes
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
    
    
def download2():
    # Fazer o download dos ID's de 400 artigos do PubMed
    print ""
    handle = Entrez.esearch(db = "pubmed", term = "Resistant Neisseria gonorrhoeae", retmax = 400) # 400 do total existentes
    record = Entrez.read(handle)
    idlist2 = record["IdList"]
    #print(idlist)
    
    return idlist2


def obterRegistos2(idlist2):
    # Para obter os registos Medline correspondentes e extraír a informação
    handle = Entrez.efetch(db = "pubmed", id = idlist2, rettype = "medline", retmode = "text")
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
    # Procura de artigos por introdução do título
    search_title = raw_input("Qual o artigo que procura: ")
        
    for record in records:
        if not "TI" in record:
            continue
        if search_title in record["TI"]:
            print ""
            print ("%s encontrado: %s" % (search_title, record["SO"])) # será apresentada a fonte do artigo introduzido
            print ""
        
        
        
def procuraAutor(records):
    # Procura de artigos por introdução do título
    search_author = raw_input("Qual o autor que procura: ")
        
    for record in records:
        if not "AU" in record:
            continue
        if search_author in record["AU"]:
            print ""
            print ("Autor %s encontrado: %s" % (search_author, record["SO"])) # será apresentada a fonte do artigo introduzido
            print ""
            

def abstract(records):
    # Procura dos abstract dos artigos publicado no último ano
    Entrez.email = "history.user@example.com"
    search_results = Entrez.read(Entrez.esearch(db="pubmed", term="Neisseria gonorrhoeae", 
                                                reldate=365, datetype="pdat", 
                                                usehistory="y"))

    #contagem do nº de resultados obtidos
    count = int(search_results["Count"])
    print("Found %i results" % count)
    
    # download de 10 registos de cada vez para um ficheiro de texto
    batch_size = 10
    out_handle = open("recent_Neisseria_gonorrhoeae.txt", "w")
    for start in range(0,count,batch_size):
        end = min(count, start+batch_size)
        print("Going to download record %i to %i" % (start+1, end))
        fetch_handle = Entrez.efetch(db="pubmed", 
                                     rettype="medline", retmode="text", 
                                     retstart=start, retmax=batch_size, 
                                     webenv=search_results["WebEnv"], query_key=search_results["QueryKey"])
    
        data = fetch_handle.read()
        fetch_handle.close()
        out_handle.write(data)
        
    out_handle.close()
    
    return data



def teste():
    # Obter todos os artigos que contenham o termo Neisseria Gonorrhoeae
    lista = download()
    registos = obterRegistos(lista)
    procuraTitulo(registos)
#    procuraAutor(registos)
#    abstract(registos)

    # Obter todos os artigos que contenham o termo Resistant Neisseria Gonorrhoeae
#    lista2 = download2()
#    registos2 = obterRegistos2(lista2)
    

        

if __name__ == '__main__':
    teste()
    
    
    
