from classes import BDD, Table
import re
import mariadb
import sys

def commence_contient(nom):
    search_type_2 = int(input(f"Commence par {nom} ou Contient {nom}? (1/2)"))
    if search_type_2 == 1:
        req_like = f"{nom}%"
    elif search_type_2 == 2:
        req_like = f"%{nom}%"
    return req_like



create_database = ""
create_database = input("Do you want to create (or erase and create if it already exists) the database? ")
if re.match('(?i)yes|y|oui|o', create_database):
    import importBDD

def main():
    medicaments = BDD()
    medicaments.connect_BDD()

    cur = medicaments.cur
    conn = medicaments.conn

    # cur.execute("SHOW TABLES;")
    # chercher nom -> SELECT nom FROM CIS_bdpm WHERE nom LIKE '...%'
    # chercher pathologie
    # substance active

    saisie=False
    while not saisie:
        try:
            search_type = int(input("1) Chercher par le Nom\n2) Chercher par la Pathologie\n3) Chercher par la Substance active\nVotre choix (entrer le numero): "))
            saisie=True
        except Exception:
            print("Bad input.")

    if search_type == 1:
        nom = input("Entrez le nom du médicament : ")
        req_like = commence_contient(nom)

        req = f"SELECT nom FROM CIS_bdpm WHERE nom LIKE '{req_like}'"
        list_results = medicaments.execute_requete(req)
        for l in list_results:
            print(l)
            
    elif search_type == 2:
        pathologie = input("Entrez le nom de la pathologie : ")
        req = f"SELECT CIS_bdpm.nom, CIS_HAS_SMR_bdpm.SMR_libelle FROM CIS_bdpm INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis WHERE SMR_libelle LIKE '%{pathologie}%'"
        list_results = medicaments.execute_requete(req)
        for l in list_results:
            print(l)

    conn.close()