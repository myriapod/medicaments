from classes import BDD, Table, Interface, Search
import re
import mariadb
import sys
from pick import pick


user=input("Username mariadb: ")
pswd=input(f"Password {user} mariadb: ")

create_database = ""
create_database = input("Est-ce que vous voulez créer ou recréer la base de donnée? (Oui/Non) ")
if re.match('(?i)yes|y|oui|o', create_database):
    root_pswd=input("Password root mariadb: ")
    import importBDD

# setting up the database and mariaDB
medicaments = BDD(user, pswd)
medicaments.connect_BDD()
cur = medicaments.cur
conn = medicaments.conn

while True:
    interface = Interface()
    interface.menu()
    print(interface.option)
    
    # recherche par médicament
    if interface.search_type == 0:
        choix = input("Recherche par nom du médicament, précision nécéssaire: Contient ou Commence par ? ")
        if re.match("(?i)contient.*", choix):
            interface.search_type = 1
        elif re.match("(?i)commence.*", choix):
            interface.search_type = 2
        print('\033[1A', end='\x1b[2K')


    if interface.search_type in [1, 2]:
        nom = input("Entrez le nom du médicament : ")
        res = "contiennent" if interface.search_type == 1 else "commencent par"
        search = Search(nom=nom, search_type=interface.search_type)
        list_results = medicaments.execute_requete(search.request)
        additional_info = medicaments.execute_list_requetes(search.additional_info)

        interface.display(f'les médicaments qui {res} {nom}', list_results, additional_info)
        
        if not interface.continue_search():
            interface.search_type = 5
            
    elif interface.search_type == 3:
        pathologie = input("Entrez le nom de la pathologie : ")

        search = Search(pathologie=pathologie)
        list_results = medicaments.execute_requete(search.request)
        additional_info = medicaments.execute_list_requetes(search.additional_info)

        interface.display(f'la pathologie {pathologie}',list_results, additional_info)
        
        if not interface.continue_search():
            interface.search_type = 5

    elif interface.search_type == 4:
        SA = input("Entrez la substance active : ")

        search=Search(SA=SA)
        list_results = medicaments.execute_requete(search.request)
        additional_info = medicaments.execute_list_requetes(search.additional_info)

        interface.display(f'la substance active {SA}',list_results, additional_info)
        
        if not interface.continue_search():
            interface.search_type = 5

    if interface.search_type == 5:
        print("Fermeture.")
        break

conn.close()
