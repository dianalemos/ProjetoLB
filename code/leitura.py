# -*- coding: utf-8 -*-
"""
Created on Sun Dec 2014

@author: GRUPO 3
"""

# TRABALHO DE GRUPO
# GRUPO 3

from Bio import SeqIO
import criar_tabela, Blastp_teste, aceder_ncbi, Phylogeny
import urllib
from Bio import SwissProt
from Bio import ExPASy
import os.path
from Bio.SeqIO import UniprotIO
import urllib2



def anotacoes_geral(filename,f):
    print ""
    print "Verificacao das anotacoes correspondentes a zona do genoma: "
    f.write("#######ANOTAÇÕES GERAIS#######\n\n\n")
    print ""
    records = SeqIO.parse(filename, "genbank")
    for seq_record in records:
        print "ID: %s" % seq_record.id
        f.write("ID: %s\n" % seq_record.id)
        print "Name: %s" % seq_record.name
        f.write("Name: %s\n" % seq_record.name)
        print "Description: %s" % seq_record.description
        f.write("Description: %s\n" % seq_record.description)
        print "Sequence length: %i" % len(seq_record)
        f.write("Sequence length: %i\n" % len(seq_record))
        print "Number of features: %i" % len(seq_record.features)  
        f.write("Number of features: %i\n" % len(seq_record.features))  
        print "Organism %s" % seq_record.annotations["organism"]
        f.write("Organism: %s\n" % seq_record.annotations["organism"]) 
        print "Accessions zone: %s" % seq_record.annotations["accessions"]
        f.write("Accessions zone: %s\n" % seq_record.annotations["accessions"]) 
        print ""
        
#Escreve num ficheiro as informações para cada tipo gene e CDS
def anotacoes_type(record,f):
    features = record.features
    genes_id = []
    for aux in features:
            if aux.type=='CDS':
                f.write("Tipo: %s\n" % aux.type)
                f.write("Localização: %s\n" % aux.location)
                f.write("Proteina codificada: %s\n" % aux.qualifiers['protein_id'])
                genes_id.append(aux.qualifiers['db_xref'])
                f.write("Gene ID: %s\n" % aux.qualifiers['db_xref'])
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                if "product" in aux.qualifiers: f.write("Produto: %s\n" % aux.qualifiers['product'])
                else: f.write("Nao tem produto\n")
                f.write("\n")
            elif aux.type=='gene':
                f.write("Tipo: %s\n" % aux.type)
                f.write("Localização: %s\n" % aux.location)
                if "db_xref" in aux.qualifiers: f.write("Gene ID: %s\n" % aux.qualifiers['db_xref'])
                else: f.write("Não tem Gene ID\n")
                f.write("Locus_tag: %s\n" % aux.qualifiers['locus_tag'])
                f.write("\n")
                

###Anotaçoes individuais###
#Devolve lista com todos os locus_tag
def anotacao_locus_tag(record):
    f = record.features
    locus = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "locus_tag" in x.qualifiers:
                locus.append(x.qualifiers["locus_tag"][0])
            else: locus.append("NA")
    return locus

#Devolve lista com todos os GENE ID
def anotacao_geneID(record):
    f = record.features
    id = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "db_xref" in x.qualifiers:
                id.append(x.qualifiers["db_xref"][1:])
            else: id.append("NA")
    return id

#Devolve lista com todas as localizações
def anotacao_local(record):
    f = record.features
    id = []
    for i in f:
        if i.type == "CDS":
            id.append(i.location)
    return id
    
#Devolve lista com todas as proteinas codificadas
def anotacao_proteina(record):
    f = record.features
    id = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "protein_id" in x.qualifiers:
                id.append(x.qualifiers["protein_id"][0])
            else: id.append("NA")
    return id

#Devolve lista com os produtos
def anotacao_produto(record):
    f = record.features
    id = []
    for i in range(len(f)):
        x = f[i]
        if x.type == "CDS": 
            if "product" in x.qualifiers:
                id.append(x.qualifiers["product"])
            else: id.append("NA")
    return id
    
    
######UNIPROT######

#Vai buscar os ids das proteinas ao Uniprot - parte do codigo baseado no codigo do grupo 5
def uniprot_ID(proteins):
    listaIDs = []
    for i in range(len(proteins)):
        handler = urllib.urlopen("http://www.uniprot.org/uniprot/?query="+proteins[i]+"&sort=score")        
        data = str(handler.read())
        try:
            start = data.index('<tbody>')
        except ValueError:
            start = len(data)
        
        if start != len(data):
            ids = data[start+15:start+21]
            listaIDs.append(ids)
    return listaIDs

def uniprot_xml(ids):
    for i in range(len(ids)):
        url = 'http://www.uniprot.org/uniprot/' + ids[i] + '.xml' 
        data = urllib2.urlopen(url).read()
        records = UniprotIO.UniprotIterator(data)
        for i in records:
            print i.annotations
            print ""

#Devolve lista das proteinas reviewed e lista das unreviewed
def uniprot_Info(ids):
    l_unrev, l_rev = [], []
    tag = 'reviewed'
    s, e = '>', '<'
    for i in range(len(ids)):
        url = 'http://www.uniprot.org/uniprot/' + ids[i] + '.rdf' 
        data = urllib2.urlopen(url).read()
        try: 
            start = data.index(tag)
            start = start + data[start:].index(s) + 1
            end = start + data[start:].index(e)
            value = data[start:end].lower()
            value = data[start:end]
            if value == 'false':
                print "%s - unreviewed protein\n" % ids[i]
                l_unrev.append(ids[i])
            else:
                print "%s - reviewed protein\n" % ids[i]
                l_rev.append(ids[i])
        except ValueError:
            l_unrev.append('NA')
            l_rev.append('NA')
    
    return l_unrev,l_rev
              
              
              
##############################################################################
###VALIDA INFORMAÇAO TABELA### Codigo grupo 5
# verify if information in the feature is the same as the one present in the line
def verify(line, feature, ltstart, ltend):
    check = False
    #print "LINE %s" % line
    start, end, strand = feature.location.start + 1, feature.location.end, feature.location.strand
    #print "START %s" % start
    #As zonas de start e end nao correspondem as da tabela
    if start == int(line[2]) and end == int(line[3]) and strand == int(line[4] + '1'):
        check = True
    return check

def valida(record):
    ltstart, ltend = "NGO0487", "NGO0727"
    # open log file to record validation
    with open('validacao.log', 'w') as f:
    
        # open comparison table
        with open('ProteinTable864_169534.tsv') as table:
            for line in table:
                if line[0] != '#':
                    line = line[:-1].split('\t')
                    
                    # if current locus_tag is between target locus_tag's
                    if line[7] >= ltstart and line[7] <= ltend:
                        ngos = []
        
                    
                        # fetch features with identical locus_tag
                        for feature in record.features:
                            if feature.type == 'gene' or feature.type == 'CDS':
                                if feature.qualifiers['locus_tag'][0] == line[7]:
                                    ngos.append(feature)
                                
                        
                        # compare if information in each feature is the same as the one present in the comparison table and write to file
                        for ngo in ngos:
                            if verify(line, ngo, ltstart, ltend):
                                f.write('Check! ' + line[7] + ' ' + str(ngo.qualifiers['locus_tag'][0]) + ' ' + str(ngo.type) + ' ' + str(ngo.location) +'\n')
                            else:
                                f.write('Not check...\n' + str(ngo) + str(line) + '\n')
                                                
##############################################################################
                                                
##############MENU####################
            
def menu_inicial():
    n = True    
    while n:
        print "++++++++ PROJETO DE LABORATORIOS DE BIOINFORMATICA +++++++++"
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        print "   1 - Get genome file"
        print "   2 - Global Annotations genome" 
        print "   3 - Get genes table"
        print "   4 - Blast"
        print "   5 - Blast analysis"
        print "   6 - Get Uniprot ID"
        print "   7 - Get Uniprot info"
        print "   8 - Get Uniprot xml"
        print "   9 - Multiple Alignments"
        print "   10 - Phylogeny"
        print "   0 - Exit" 
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        n = raw_input("Insira a opcao desejada: ")
        if n == '1':
            filename = "zone_teste.gb"
            record = aceder_ncbi.zona_genoma(filename)
            print "%s Created\n" % filename
        elif n == '2':
             f = open("Anotacoes.txt",'w')
             f.write("\n##########Anotações#########\n\n\n")
             anotacoes_type(record,f)
             f.close()
             print "File created\n"
        elif n == '3':
            l_locus = anotacao_locus_tag(record)
            l_geneID = anotacao_geneID(record)
            l_proteinas = anotacao_proteina(record)
            l_local = anotacao_local(record)
            l_produto = anotacao_produto(record)
            criar_tabela.tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto)
            print "Table created\n" 
        elif n == '4':
            locus = str(raw_input("Gene locus_tag: "))
            #locus = "NGO0525"
            a = Blastp_teste.get_locustag(record,locus)
            gi = a[0]
            Blastp_teste.blast(gi)
        elif n == '5':
            Blastp_teste.analise(gi)
        elif n == '6':
            x = str(raw_input("Protein acession: "))
            listapro = []
            listapro.append(x)
            #x=YP_207711.1
            listaIDs = uniprot_ID(listapro)
            print listaIDs
            print "\n"
        elif n == '7':
            #Q5F938
            y = str(raw_input("Uniprot ID: "))
            listay = []
            listay.append(y)
            uniprot_Info(listay)
        elif n == '8':
            z = str(raw_input("Uniprot ID: "))
            listaz = []
            listaz.append(z)
            uniprot_xml(listaz)
        elif n == '9':
            fic = str(raw_input("Nome ficheiro: "))
            #fic = "alinhamentos.phy"
            Phylogeny.alignments(fic + ".phy")
            print "\n"
        elif n == '10':
            fics = str(raw_input("Nome ficheiro: "))
            #fics = "filogenia.dnd"
            Phylogeny.phylogeny(fics + ".dnd")
            print "\n"
        elif n == '0': 
            n = False
        else:
            print "Operacao Inexistente"
                                             
     
if __name__ == "__main__":
    #Ficheiro correspondente a zona do genoma em estudo - 468401 a 727400
    #filename = "zone.gb"
    #record = SeqIO.read(filename, "genbank") 
    # aceder ao NCBI e guarda o ficheiro correspondente a zona do genoma
    #record_zona = aceder_ncbi.zona_genoma(filename)

    #Abre ficheiro onde vao ser escritas algumas anotaçoes
    #f = open("Anotacoes.txt",'w')
    menu_inicial()
    # verificar as anotacoes gerais correspondentes a zona definida
    #anotacoes_geral(filename,f)
    
    #f.write("\n##########Anotações#########\n\n\n")
    # verificar as features correspondentes a zona definida
    
    #anotacoes_type(record,f)
    #menu(record,filename,f,f2)
#    #devolve locus_tag de cada gene    
#    l_locus = anotacao_locus_tag(record)
#    l_geneID = anotacao_geneID(record)
#    l_local = anotacao_local(record)
#    l_proteinas = anotacao_proteina(record)
#    l_produto = anotacao_produto(record)
#    
    #listaIDs = uniprot_ID(l_proteinas)
    #listaIDs = ['Q5F7R2','Q5F9B1','Q5F9B0','Q5F9A9','Q5F9A8']
    #l_unrev, l_rev = uniprot_Info(listaIDs)
    #Cria tabela informaçao      
    #criar_tabela.tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto)
    #f.close() 
    
    #valida com a informaçao da tabela
    #valida(record)
    
    
    