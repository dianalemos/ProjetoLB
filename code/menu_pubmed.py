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
    Entrez.email = "pg27658@alunos.uminho.pt"
    handle = Entrez.esearch(db = "pubmed", term = "Neisseria gonorrhoeae", retmax = 400) # 400 do total existentes
    record = Entrez.read(handle)
    idlist = record["IdList"]
    
    return idlist


def obterRegistos(idlist, filename):
    # Para obter os registos Medline correspondentes e extraír a informação
    handle = Entrez.efetch(db = "pubmed", id = idlist, rettype = "medline", retmode = "text")
    records = Medline.parse(handle)
    f = open(filename, "w")
    # para guardar os registos é necessário convertê-los numa lista
    records = list(records)
    
    # Percorrer os registos para imprimir alguma informação sobre cada um deles
    for record in records:
        #print "TITLE: ", record.get("TI", "?")
        f.write("TITLE: %s\n" % str(record.get("TI", "?")))
        #print "AUTHORS: ", record.get("AU", "?")
        f.write("AUTHORS: %s\n" % str(record.get("AU", "?")))
        #print "SOURCE: ", record.get("SO", "?")
        f.write("SOURCE: %s\n\n\n" % str(record.get("SO", "?")))

    f.close()
    return records
    
    
def download2():
    # Fazer o download dos ID's de 400 artigos do PubMed
    print ""
    handle = Entrez.esearch(db = "pubmed", term = "Resistant Neisseria gonorrhoeae", retmax = 400) # 400 do total existentes
    record = Entrez.read(handle)
    idlist2 = record["IdList"]
    #print(idlist)
    
    return idlist2
    
def procuraTitulo(records):
    # Procura de artigos por introdução do título
    search_title = raw_input("Qual o artigo que procura: ")
        
    for record in records:
        if not "TI" in record:
            continue
        if search_title in record["TI"]:
            print ""
            print ("%s encontrado: %s\n" % (search_title, record["SO"])) # será apresentada a fonte do artigo introduzido        
        
        
def procuraAutor(records):
    # Procura de artigos por introdução do autor
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



def menu_artigos():
    n = True    
    while n:
        print "++++++++ PESQUISA DE ARTIGOS +++++++++"
        print "++++++++++++++++++++++++++++++++++++++\n"
        print "   1 - Todos artigos da Neisseria gonorrhoeae"
        print "   2 - Procurar artigo por título"
        print "   3 - Procurar artigo por autor"
        print "   4 - Procurar abstract"
        print "   5 - Todos artigos sobre resistência"
        print "   0 - Exit" 
        print "+++++++++++++++++++++++++++++++++++++++\n"
        lista = download()
        n = raw_input("Insira a opcao desejada: ")
        if n == '1':
            registos = obterRegistos(lista,"Artigos_Neisseria_gonorrhoeae.txt")
            print "Ficheiro \"Artigos_Neisseria_gonorrhoeae.txt\" criado.\n"   
        if n == '2':
            registos = obterRegistos(lista,"Artigos_Neisseria_gonorrhoeae.txt")
            procuraTitulo(registos)
        if n == '3':
            registos = obterRegistos(lista,"Artigos_Neisseria_gonorrhoeae.txt")
            procuraAutor(registos)   
        if n == '4':
            registos = obterRegistos(lista,"Artigos_Neisseria_gonorrhoeae.txt")
            abstract(registos)
        if n == '5':
            lista2 = download2()
            registos2 = obterRegistos(lista2, "Artigos_Resistant_Neisseria_gonorrhoeae.txt")
            print "\"Artigos_Resistant_Neisseria_gonorrhoeae.txt\" criado.\n" 
            
if __name__ == '__main__':
    menu_artigos()
    
    
    
