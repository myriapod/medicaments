from classes import BDD, Table
import re
import mariadb
import sys

def commence_contient(nom):
    res=""
    search_type_2 = int(input(f"Commence par {nom} ou Contient {nom}? (1/2)"))
    if search_type_2 == 1:
        req_like = f"{nom}%"
        res="commence par"
    elif search_type_2 == 2:
        req_like = f"%{nom}%"
        res="contient"
    return req_like, res

def display(recherche,list_results):
    print(f"\nRESULTATS POUR {recherche}")
    
    ligne=150
    print("_"*ligne+"\n|"+" "*(ligne-2)+" |")
    for l in list_results:
        longueur=len(l)
        to_fill = ligne-longueur-3
        print(f"|  {l}" + " "*to_fill + "|")
    print("|"+"_"*(ligne-1)+"|\n")


create_database = ""
# create_database = input("Do you want to create (or erase and create if it already exists) the database? ")
if re.match('(?i)yes|y|oui|o', create_database):
    import importBDD

# setting up the database and mariaDB
medicaments = BDD()
medicaments.connect_BDD()
cur = medicaments.cur
conn = medicaments.conn


# loop for the menu
while True:
    # vérification de la saisie
    saisie=False
    while not saisie:
        try:
            search_type = int(input("1) Chercher par le Nom\n2) Chercher par la Pathologie\n3) Chercher par la Substance active\n4) Quitter\n>>>>> Votre choix (entrer le numero): "))
            saisie=True
        except Exception:
            print("Bad input.")

    # recherche par médicament
    if search_type == 1:
        nom = input("Entrez le nom du médicament : ")
        req_like, res = commence_contient(nom)

        req = f"SELECT nom FROM CIS_bdpm WHERE nom LIKE '{req_like}' GROUP BY CIS_bdpm.nom ASC"
        list_results = medicaments.execute_requete(req)
        display(f'les médicaments qui {res} {nom}',list_results)
    
    # recherche par pathologie
    elif search_type == 2:
        pathologie = input("Entrez le nom de la pathologie : ")
        req = f"SELECT CIS_bdpm.nom, CIS_HAS_SMR_bdpm.SMR_libelle FROM CIS_bdpm INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis WHERE SMR_libelle LIKE '%{pathologie}%' GROUP BY CIS_bdpm.nom ASC"
        list_results = medicaments.execute_requete(req)
        display(f'la pathologie {pathologie}',list_results)
    
    # recherche par substance active
    elif search_type == 3:
        SA = input("Entrez la substance active : ")
        req = f'''SELECT CIS_bdpm.nom 
                    FROM CIS_bdpm INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                    WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{SA}%'
                    GROUP BY CIS_bdpm.nom ASC
                    '''
        list_results = medicaments.execute_requete(req)
        display(f'la substance active {SA}',list_results)
        
    # quitter
    elif search_type == 4:
        print("Fermeture.")
        break

conn.close()