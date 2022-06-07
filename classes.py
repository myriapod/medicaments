import sys
import re
import mariadb
from pick import pick


class BDD():
    def __init__(self, user, password, root_password=None):
        self.user = user
        self.password = password
        self.root_password = root_password
        self.cur = None
        self.conn = None
    
    def create_bdd(self):
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user="root",
                password=self.root_password,
                host="127.0.0.1",
                port=3306
            )
            print("Connected to mariaDB")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        cur = conn.cursor()

        # Create the database and add privileges to the user you want
        cur.execute("DROP DATABASE IF EXISTS medicaments")
        cur.execute("CREATE DATABASE IF NOT EXISTS medicaments")
        cur.execute(f"GRANT ALL PRIVILEGES ON medicaments.* TO '{self.user}'@'localhost'")
        cur.execute("FLUSH PRIVILEGES")

        conn.close()
        
        
    def connect_BDD(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host="127.0.0.1",
                port=3306,
                database="medicaments"
                )
            # print("Connected to medicaments")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()
        

    def execute_requete(self, req, nom=True):
        list_results = []
        self.cur.execute(req)
        if results := self.cur.fetchall():
            list_results.extend(r[0] for r in results)
        else:
            print("Aucun résultat trouvé.")
            
        #if nom:
        #    for n in range(len(list_results)): # on récupère que le nom du médicament
        #        list_results[n] = list_results[n].split(", ", 1)[0]
                
        return list_results
    
    def execute_list_requetes(self, list_req):
        return [self.execute_requete(req, nom=False) for req in list_req]



class Table():
    def __init__(self, name, fields_list, fields, user="myri", password="myri"):
        self.user = user
        self.password = password
        self.name = name
        self.fields = fields
        self.fields_list = fields_list
        ###
        with open(f'database/{self.name}.txt', 'r', encoding='iso-8859-15') as f:
            self.data = f.read().split('\n')
            self.data.pop(-1)
        ###
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host="127.0.0.1",
                port=3306,
                database="medicaments"
                )
            # print("Connected to mariaDB")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()
        
        
    def create_table(self):
        try:
            self.cur.execute(f'''DROP TABLE IF EXISTS {self.name}''')
            self.cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.name} ({self.fields})''')
        except mariadb.IntegrityError:
            print("Integrity error")
        
    def fill_table(self):
        for line in self.data:
            err = False
            values=[]
            values=line.split('\t')

            # fix specific things
            if self.name == 'CIS_COMPO_bdpm' and values[0]=="68285029":
                values.remove("")
                values.remove("")
                values.remove("")
            elif self.name == 'CIS_GENER_bdpm' and values[3] in ["67215259", "69616681"]:
                values.remove("")
                values.remove("")
            elif self.name == "CIS_CIP_bdpm": # get rid of the bad columns that are annoying
                values.pop(10)
                values.pop(10)
                values.pop(10)
            elif self.name == "CIS_InfoImportantes_20220602145935_bdpm" and not re.match("6.*", values[0]):
                err = True


            if not err:
                fields_ok = []
                values_ok = []
                for v in range(len(values)):
                    if values[v]!="":
                        if re.match(".*'.*", values[v]): # deal with a '
                            new = values[v].replace("\'", "\\'")
                            values[v] = new
                        fields_ok.append(self.fields_list[v]) # get the list of fields that aren't empty
                        values_ok.append(values[v])

                # reset
                fields_req=""
                values_req=""

                fields_req = "".join(f'{fields_ok[f]}, ' for f in range(len(fields_ok)-1)) # turn the fields into a string to put in the sql request
                fields_req += fields_ok[-1]

                numbers = []

                # turn the values into a string to put in the sql request
                for v in range(len(values_ok)-1):
                    if re.match("(code|prix|numero|id).*", fields_ok[v]): # if it's a code it's an INT
                        values_req+=f"{values_ok[v]}, "
                        numbers.append(values_ok[v])

                    elif re.match("date.*", fields_ok[v]): # understand the dates correctly
                        if re.match(".*/.*", values_ok[v]):
                            values_req+=f"STR_TO_DATE('{values_ok[v]}', '%d/%m/%Y'), "
                        elif re.match(".*\-.*", values_ok[v]):
                            values_req+=f"STR_TO_DATE('{values_ok[v]}', '%Y-%m-%d'), "
                        else:
                            values_req+=f"'{values_ok[v]}', "
                    else:
                        values_req+=f"'{values_ok[v]}', "

                # deal with the last value of the string
                if values_ok[-1] in numbers:
                    values_req+=f"{values_ok[-1]}"
                else:
                    values_req+=f"'{values_ok[-1]}'"

                # print(fields_req)
                # print(values_req)

                req=f'''INSERT INTO {self.name} ({fields_req})
                        VALUES ({values_req})'''

                try:
                    self.cur.execute(req)
                except (mariadb.IntegrityError): # skip the lines we've already added
                    pass


        self.conn.commit()
        self.conn.close()


class Interface():
    def __init__(self):
        self.search_type = None
        self.search_method = None
        self.option = None
        
        
    def menu(self):
        title = 'Menu de recherche (appuyez sur ESPACE pour séléctionner, ENTREE pour choisir)'
        options = ['1) Chercher par le Nom:', '  a- contient', '  b- commence par', '2) Chercher par la Pathologie', '3) Chercher par la Substance active', '4) Quitter']
        option, index = pick(options, title)
        self.option = option
        self.search_type = index
        
    def continue_search(self):
        choix = input("Faire une autre recherche? (Oui/Non) ")
        if re.match('y|yes|o|oui', choix, flags=re.I):
            return True

    def display(self, recherche, list_results, additional_info):
        print(f"\nRESULTATS POUR {recherche}")
        print(" "*10+"_"*50+" "*10)
        
        for r in range(len(list_results)):
            add_info=""
            print(list_results[r])
            try:
                if additional_info[0][r] is not None:
                    add_info+=f"  forme: {additional_info[0][r]}"
                if additional_info[1][r] is not None:
                    add_info += f"  voie: {additional_info[1][r]}"
                if additional_info[2][r] is not None:
                    add_info += f"  remboursement: {additional_info[2][r]}"
                if additional_info[3][r] is not None:
                    add_info += f"  prix: {additional_info[3][r]} €"
            except IndexError:
                pass
            print(f"{add_info}\n")
        
    def old_display(self, recherche, list_results, additional_info):
        print(f"\nRESULTATS POUR {recherche}")
        
        ligne=150
        print("_"*ligne+"\n|"+" "*(ligne-2)+" |")
        for l in range(len(list_results)):
            longueur=len(list_results[l])
            to_fill = ligne-longueur-3
            print(f"|  {list_results[l]}" + " "*to_fill + "|")
            for info in additional_info:
                print(f"|  {info[l]}" + " "*to_fill + "|")
        print("|"+"_"*(ligne-1)+"|\n")


class Search():
    def __init__(self, nom=None, search_type=None, pathologie=None, SA=None):
        self.nom = nom
        self.search_type = search_type
        self.pathologie = pathologie
        self.SA = SA
        
        
        if self.nom is not None:
            self.req_like = f"%{self.nom}%" if self.search_type == 1 else f"{self.nom}%"
            self.request = f'''SELECT nom 
                    FROM CIS_bdpm 
                    WHERE nom LIKE '{self.req_like}' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.forme = f'''SELECT CIS_bdpm.forme
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    WHERE CIS_bdpm.nom LIKE '{self.req_like}' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.voie = f'''SELECT CIS_bdpm.voie
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    WHERE CIS_bdpm.nom LIKE '{self.req_like}' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.remboursement = f'''SELECT CIS_CIP_bdpm.remboursement 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    WHERE CIS_bdpm.nom LIKE '{self.req_like}' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.prix = f'''SELECT CIS_CIP_bdpm.prix_euro 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    WHERE CIS_bdpm.nom LIKE '{self.req_like}' 
                    GROUP BY CIS_bdpm.nom ASC'''
        
        elif self.pathologie is not None:
            self.request = f'''SELECT CIS_bdpm.nom, CIS_HAS_SMR_bdpm.SMR_libelle 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis 
                    WHERE SMR_libelle LIKE '%{self.pathologie}%' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.forme = f'''SELECT CIS_bdpm.forme
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis 
                    WHERE SMR_libelle LIKE '%{self.pathologie}%' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.voie = f'''SELECT CIS_bdpm.voie
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis 
                    WHERE SMR_libelle LIKE '%{self.pathologie}%' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.remboursement = f'''SELECT CIS_CIP_bdpm.remboursement 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis 
                    WHERE SMR_libelle LIKE '%{self.pathologie}%' 
                    GROUP BY CIS_bdpm.nom ASC'''
            self.prix = f'''SELECT CIS_CIP_bdpm.prix_euro 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_HAS_SMR_bdpm on CIS_bdpm.code_cis=CIS_HAS_SMR_bdpm.code_cis 
                    WHERE SMR_libelle LIKE '%{self.pathologie}%' 
                    GROUP BY CIS_bdpm.nom ASC'''
                
        elif self.SA is not None:
            self.request = f'''SELECT CIS_bdpm.nom 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                    WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{self.SA}%'
                    GROUP BY CIS_bdpm.nom ASC
                    '''
            self.forme = f'''SELECT CIS_bdpm.forme
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                    WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{self.SA}%'
                    GROUP BY CIS_bdpm.nom ASC'''
            self.voie = f'''SELECT CIS_bdpm.voie
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                    WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{self.SA}%'
                    GROUP BY CIS_bdpm.nom ASC'''
            self.remboursement = f'''SELECT CIS_CIP_bdpm.remboursement 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                    WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{self.SA}%'
                    GROUP BY CIS_bdpm.nom ASC'''
            self.prix = f'''SELECT CIS_CIP_bdpm.prix_euro 
                    FROM CIS_bdpm 
                    INNER JOIN CIS_CIP_bdpm ON CIS_bdpm.code_cis=CIS_CIP_bdpm.code_cis
                    INNER JOIN CIS_COMPO_bdpm ON CIS_bdpm.code_cis=CIS_COMPO_bdpm.code_cis
                    WHERE CIS_COMPO_bdpm.nom_substance LIKE '%{self.SA}%'
                    GROUP BY CIS_bdpm.nom ASC'''
                    
        self.additional_info = [self.forme, self.voie, self.remboursement, self.prix]