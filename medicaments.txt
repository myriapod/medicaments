telecharger tous les fichiers csv sur : https://base-donnees-publique.medicaments.gouv.fr/telechargement.php

Faire une bdd sur mariadb en suivant le schéma: https://base-donnees-publique.medicaments.gouv.fr/docs/Contenu_et_format_des_fichiers_telechargeables_dans_la_BDM_v1.pdf
(il faut creer la bdd et les tables puis charger les fichiers CSV)


!! Ne pas oublier les contraintes, clées primaires et secondaires

(verifier si je peux bien ne pas ajouter dans CIS_COMPO_bdpm une ligne avec un COD CIS qui n'est pas dans CIS_bdpm)



-------------- INTERFACE PYTHON

proposer une interface ligne de commande un peu equivalente a : https://base-donnees-publique.medicaments.gouv.fr/index.php

l'utilisateur peut chercher un medicament  avec:

- son nom
- pathologie
- substance actives


On peut donner quelques informations supplémentaires sur les médicaments a l'utilisateur (Jointure)




