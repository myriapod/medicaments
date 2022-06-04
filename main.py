from classes import BDD, Table, Interface
import re
import mariadb
import sys
from pick import pick


create_database = ""
# create_database = input("Do you want to create (or erase and create if it already exists) the database? ")
if re.match('(?i)yes|y|oui|o', create_database):
    import importBDD

# setting up the database and mariaDB
medicaments = BDD()
medicaments.connect_BDD()
cur = medicaments.cur
conn = medicaments.conn


interface = Interface()
interface.menu()

# recherche par médicament
if interface.search_type == 0:
    choix = input("Recherche par nom du médicament, précision nécéssaire: Contient ou Commence par ? ")
    if re.match("(?i)contient.*", choix):
        interface.search_type = 1
    elif re.match("(?i)commence.*", choix):
        interface.search_type = 2

if interface.search_type in [1,2]:
    print(" > Recherche par nom du médicament")
    nom = input("Entrez le nom du médicament : ")
    if interface.search_type == 1:
        res = "contiennent"
        req_like = f"%{nom}%"
    else:
        res = "commencent par"
        req_like = f"{nom}%"

    req = f"SELECT nom FROM CIS_bdpm WHERE nom LIKE '{req_like}' GROUP BY CIS_bdpm.nom ASC"
    list_results = medicaments.execute_requete(req)
    interface.display(f'les médicaments qui {res} {nom}',list_results)

# recherche par pathologie
elif interface.search_type == 3:
    print(" > Recherche par nom de la pathologie")
    pathologie = input("Entrez le nom de la pathologie : ")
    req = f"SELECT CIS_bdpm.nom, CIS_HAS_SMR_bdpm.SMR_libelle FROM CIS_bdpm INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis WHERE SMR_libelle LIKE '%{pathologie}%' GROUP BY CIS_bdpm.nom ASC"
    list_results = medicaments.execute_requete(req)
    interface.display(f'la pathologie {pathologie}',list_results)

# recherche par substance active
elif interface.search_type == 4:
    print(" > Recherche par nom de la substance active")
    SA = input("Entrez la substance active : ")
    req = f'''SELECT CIS_bdpm.nom 
                FROM CIS_bdpm INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{SA}%'
                GROUP BY CIS_bdpm.nom ASC
                '''
    list_results = medicaments.execute_requete(req)
    interface.display(f'la substance active {SA}',list_results)
    
# quitter
elif interface.search_type == 5:
    print("Fermeture.")

conn.close()