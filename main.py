from classes import Table, BDD

# Creating the bdd if needed
medicaments = BDD("myri")
medicaments.create_bdd()

# CIS_bdpm.txt
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
                        
# CIS_bdpm = Table("CIS_bdpm", bdpm_fields_list, bdpm_fields)
# CIS_bdpm.create_table()
# CIS_bdpm.fill_table()

    
    
# CIS_CPD_bdpm.txt
CPD_bdpm_fields_list = []



# CIS_GENER_bdpm.txt
# CIS_InfoImportantes_20220602145935_bdpm.txt
# CIS_HAS_SMR_bdpm.txt
# HAS_LiensPageCT_bdpm.txt
# CIS_HAS_ASMR_bdpm.txt
# CIS_CIP_bdpm.txt
# CIS_COMPO_bdpm.txt

