from classes import Table, BDD

print("Importing database...")

# we delete all of the previous database and tables when we launch this program

# Creating the bdd
user=input("Username mariadb: ")
pswd=input(f"Password {user} mariadb: ")
root_pswd=input("Password root mariadb ")
medicaments = BDD(user, pswd, root_pswd)
medicaments.create_bdd()


# >>>>>>>>> CIS_bdpm.txt
bdpm_fields_list = ['code_cis', 'nom', 'forme', 'voie', 'statut_admin_AMM', 'type_procedure_AMM', 'etat', 'date_AMM', 'statutBdm', 'EU_auth', 'titulaire', 'surveillance']
bdpm_fields = '''code_cis INT UNIQUE PRIMARY KEY,
                nom TEXT,
                forme TEXT,
                voie TEXT,
                statut_admin_AMM TEXT,
                type_procedure_AMM TEXT,
                etat TEXT,
                date_AMM DATE,
                statutBdm TEXT,
                EU_auth TEXT,
                titulaire TEXT,
                surveillance TEXT '''

CIS_bdpm = Table("CIS_bdpm", bdpm_fields_list, bdpm_fields)
CIS_bdpm.create_table()
CIS_bdpm.fill_table()

# print(" >>>>>>>>> CIS_bdpm")



# >>>>>>>>> CIS_CIP_bdpm.txt
CIP_bdpm_fields_list = ['code_cis', 'code_CIP7', 'libelle', 'statut_pres', 'etat_AMM', 'date_commercialisation', 'code_CIP13', 'collectivite_agree', 'remboursement', 'prix_euro', 'indications']
CIP_bdpm_fields = '''code_cis INT UNIQUE,
                    code_CIP7 INT CHECK (CHAR_LENGTH(code_CIP7) = 7),
                    libelle TEXT,
                    statut_pres TEXT,
                    etat_AMM TEXT,
                    date_commercialisation DATE,
                    code_CIP13 BIGINT CHECK (CHAR_LENGTH(code_CIP13) = 13),
                    collectivite_agree TEXT,
                    remboursement TEXT,
                    prix_euro TEXT,
                    indications LONGTEXT,
                    FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis)'''
CIP_bdpm = Table("CIS_CIP_bdpm", CIP_bdpm_fields_list, CIP_bdpm_fields)
CIP_bdpm.create_table()
CIP_bdpm.fill_table()

# print(" >>>>>>>>> CIP_bdpm")



# >>>>>>>>> CIS_COMPO_bdpm.txt
COMPO_bdpm_fields_list = ['code_cis', 'designation', 'code_substance', 'nom_substance', 'dosage', 'ref_dosage', 'nature_compo', 'numero_SA_ST']
COMPO_bdpm_fields = '''code_cis INT UNIQUE,
                    designation TEXT,
                    code_substance INT, 
                    nom_substance TEXT,
                    dosage TEXT,
                    ref_dosage TEXT,
                    nature_compo TEXT,
                    numero_SA_ST INT,
                    FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis)
                    '''
COMPO_bdpm = Table("CIS_COMPO_bdpm", COMPO_bdpm_fields_list, COMPO_bdpm_fields)
COMPO_bdpm.create_table()
COMPO_bdpm.fill_table()

# print(" >>>>>>>>> COMPO_bdpm")



# >>>>>>>>> HAS_LiensPageCT_bdpm.txt
HAS_Liens_bdpm_fields_list = ['HAS_code', 'link_CT']
HAS_Liens_bdpm_bdpm_fields = '''HAS_code varchar(8) UNIQUE PRIMARY KEY,
                    link_CT TEXT
                    '''
HAS_Liens_bdpm = Table("HAS_LiensPageCT_bdpm", HAS_Liens_bdpm_fields_list, HAS_Liens_bdpm_bdpm_fields)
HAS_Liens_bdpm.create_table()
HAS_Liens_bdpm.fill_table()

# print(" >>>>>>>>> HAS_links_bdpm")



# >>>>>>>>> CIS_HAS_SMR_bdpm.txt
HAS_SMR_bdpm_fields_list = ['code_cis', 'HAS_code', 'motif_eval', 'date_avis', 'SMR_value', 'SMR_libelle']
HAS_SMR_bdpm_fields = '''code_cis INT UNIQUE,
                    HAS_code varchar(8),
                    motif_eval TEXT, 
                    date_avis DATE,
                    SMR_value TEXT,
                    SMR_libelle LONGTEXT,
                    FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis),
                    FOREIGN KEY (HAS_code) REFERENCES HAS_LiensPageCT_bdpm(HAS_code)
                    '''
HAS_SMR_bdpm = Table("CIS_HAS_SMR_bdpm", HAS_SMR_bdpm_fields_list, HAS_SMR_bdpm_fields)
HAS_SMR_bdpm.create_table()
HAS_SMR_bdpm.fill_table()

# print(" >>>>>>>>> HAS_SMR_bdpm")



# >>>>>>>>> CIS_HAS_ASMR_bdpm.txt
HAS_ASMR_bdpm_fields_list = ['code_cis', 'HAS_code', 'motif_eval', 'date_avis', 'ASMR_value', 'ASMR_libelle']
HAS_ASMR_bdpm_fields = '''code_cis INT UNIQUE,
                    HAS_code varchar(8),
                    motif_eval TEXT, 
                    date_avis TEXT,
                    ASMR_value TEXT,
                    ASMR_libelle TEXT,
                    FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis),
                    FOREIGN KEY (HAS_code) REFERENCES HAS_LiensPageCT_bdpm(HAS_code)
                    '''
HAS_ASMR_bdpm = Table("CIS_HAS_ASMR_bdpm", HAS_ASMR_bdpm_fields_list, HAS_ASMR_bdpm_fields)
HAS_ASMR_bdpm.create_table()
HAS_ASMR_bdpm.fill_table()

# print(" >>>>>>>>> HAS_ASMR_bdpm")



# >>>>>>>>> CIS_GENER_bdpm.txt
GENER_bdpm_fields_list = ['id_gener', 'gener_libelle', 'code_cis', 'numero_type', 'numero_tri']
GENER_ASMR_bdpm_fields = '''id_gener INT,
                    gener_libelle TEXT,
                    code_cis INT UNIQUE,
                    numero_type INT,
                    numero_tri INT,
                    FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis)
                    '''
GENER_bdpm = Table("CIS_GENER_bdpm", GENER_bdpm_fields_list, GENER_ASMR_bdpm_fields)
GENER_bdpm.create_table()
GENER_bdpm.fill_table()

# print(" >>>>>>>>> GENER_bdpm")



# >>>>>>>>> CIS_CPD_bdpm.txt - foreign key error when creating the table
CPD_bdpm_fields_list = ['code_cis', 'condition']
CPD_bdpm_fields = '''code_cis INT UNIQUE,
                condition LONGTEXT,
                FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis)
                '''
CPD_bdpm = Table("CIS_CPD_bdpm", CPD_bdpm_fields_list, CPD_bdpm_fields)
try:
    CPD_bdpm.create_table()
    CPD_bdpm.fill_table()
    # print(" >>>>>>>>> CPD_bdpm")
except Exception:
    print("Failed CPD_bdpm, moving on")




# >>>>>>>>> CIS_InfoImportantes_20220602145935_bdpm.txt
INFO_bdpm_fields_list = ['code_cis', 'date_debut_info', 'date_fin_info', 'info']
INFO_bdpm_fields = '''code_cis INT UNIQUE,
                date_debut_info DATE,
                date_fin_info DATE,
                info TEXT,
                FOREIGN KEY (code_cis) REFERENCES CIS_bdpm(code_cis)
                '''
INFO_bdpm = Table("CIS_InfoImportantes_20220602145935_bdpm", INFO_bdpm_fields_list, INFO_bdpm_fields)
INFO_bdpm.create_table()
INFO_bdpm.fill_table()

# print(" >>>>>>>>> INFO_bdpm")


print("Database imported.")
