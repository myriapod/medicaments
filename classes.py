import sys
import re
import mariadb


class BDD():
    def __init__(self, user="myri", password="myri"):
        self.user = user
        self.password = password
        self.cur = None
        self.conn = None
    
    def create_bdd(self):
        # Connect to MariaDB Platform
        try:
            conn = mariadb.connect(
                user="root",
                password="123456",
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
            print("Connected to medicaments")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.cur = self.conn.cursor()
        

    def execute_requete(self, req):
        list_results = []
        self.cur.execute(req)
        if results := self.cur.fetchall():
            for r in results:
                list_results.append(r[0])
        else:
            print("Aucun résultat trouvé.")
        return list_results



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

