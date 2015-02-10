# -*- coding: utf-8 -*-
"""
Created on Sun Dec 2014

@author: GRUPO 3
"""

# TRABALHO DE GRUPO
# GRUPO 3

from Bio import SeqIO
import criar_tabela, Blastp_teste, aceder_ncbi, Phylogeny, P_uniprot, validar_tabela

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
            try: 
                 f = open("Anotacoes.txt",'w')
                 f.write("\n##########Anotações#########\n\n\n")
                 anotacoes_type(record,f)
                 f.close()
                 print "File created\n"
            except:
                print "Get genome file first.\n"
        elif n == '3':
            try: 
                l_locus = anotacao_locus_tag(record)
                l_geneID = anotacao_geneID(record)
                l_proteinas = anotacao_proteina(record)
                l_local = anotacao_local(record)
                l_produto = anotacao_produto(record)
                criar_tabela.tabela_info(l_locus,l_geneID,l_local,l_proteinas,l_produto)
                print "Table created\n" 
            except:
                print "Get genome file first.\n"
        elif n == '4':
            try: 
                locus = str(raw_input("Gene locus_tag: "))
                #locus = "NGO0525"
                a = Blastp_teste.get_locustag(record,locus)
                gi = a[0]
                Blastp_teste.blast(gi)
            except:
                print "Get genome file first.\n"
        elif n == '5':
            try:
                Blastp_teste.analise(gi)
            except:
                print "Necessário fazer blast antes da análise.\n"
        elif n == '6':
            x = str(raw_input("Protein acession: "))
            listapro = []
            listapro.append(x)
            #x=YP_207711.1
            listaIDs = P_uniprot.uniprot_ID(listapro)
            print listaIDs
            print "\n"
        elif n == '7':
            #Q5F938
            y = str(raw_input("Uniprot ID: "))
            listay = []
            listay.append(y)
            P_uniprot.uniprot_Info(listay)
        elif n == '8':
            z = str(raw_input("Uniprot ID: "))
            listaz = []
            listaz.append(z)
            P_uniprot.uniprot_xml(listaz)
        elif n == '9':
            fic = str(raw_input("Nome ficheiro (.phy): "))
            #exemplo de ficheiro = "alinhamentos.phy" - encontra-se ja na pasta
            #Cria ficheiro com os alinhamentos multiplos
            Phylogeny.alignments(fic + ".phy")
            print "Ficheiro Multiple_alignments.fasta criado.\n"
        elif n == '10':
            fics = str(raw_input("Nome ficheiro (.dnd): "))
            #exemplo: fics = "filogenia.dnd" - encontra-se ja na pasta
            Phylogeny.phylogeny(fics + ".dnd")
            print "\n"
        elif n == '0': 
            n = False
        else:
            print "Operacao Inexistente"
                                             
     
if __name__ == "__main__":
    
    menu_inicial()
    
    #valida com a informaçao da tabela, meramente para ter uma ideia se o que foi
    #retirado do ncbi está correto ou não
    #validar_tabela.valida(record)
    
    
    