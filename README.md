# Ressources SSD

Une porte d’entrée pour les enseignants du supérieur en statistique et science des données : des supports à adapter, des activités et des données pour les cours.

[Consulter le site](https://aureliennicosiaulaval.github.io/site_ressources_SSD/)

## Contenu

- Accueil : quatre entrées par besoin pédagogique.
- Catalogue : recherche textuelle, filtres et liens partageables.
- Parcours : préparer un support, une activité, choisir des données et diffuser un cours.
- Fiches : modèles Quarto, site de cours, tutoriels learnr, UlavalSSD et GitHub.
- Téléchargements : gabarit de site et fiche de préparation d’activité.

Les adresses des pages historiques sont conservées. Les fiches distinguent les prérequis de consultation, d’adaptation et d’hébergement.

## Développement

Prérequis : Quarto 1.9.38 et Python 3. Les exemples R du site sont affichés sans exécution lors de sa construction. Node.js sert uniquement à vérifier la syntaxe du script du catalogue.

```bash
git clone git@github.com:AurelienNicosiaULaval/site_ressources_SSD.git
cd site_ressources_SSD
quarto preview
```

Pour produire et vérifier le site :

```bash
quarto render
python3 scripts/check_site.py
node --check assets/catalogue.js
```

Le rendu se trouve dans `docs/`. La compilation génère le catalogue et l’archive téléchargeable avec `scripts/prepare.py`. Le fragment `_includes/catalogue.html` est versionné pour permettre à Quarto de résoudre les inclusions dès l’inventaire initial.

## Ajouter une ressource

1. Ajouter sa fiche ou une section dans une fiche existante.
2. Ajouter une entrée à `assets/ressources.json` : identifiant, catégorie, titre, description, prérequis, lien et mots-clés.
3. Lancer `python3 scripts/prepare.py`, puis `quarto render`.
4. Exécuter la vérification des liens et tester la recherche dans le navigateur.

Catégories : `supports`, `activites`, `donnees`, `diffusion`. Les accents ne sont pas nécessaires dans la recherche. Les paramètres `besoin` et `recherche` conservent la sélection dans l’URL. Sans JavaScript, toutes les ressources restent visibles.

Ne pas modifier directement les pages dans `docs/` ni le fragment de catalogue généré.

## Publication

Le workflow GitHub Actions rend et vérifie le site. Les branches de refonte et les demandes de fusion produisent un artefact de prévisualisation. Seule la branche `main` déclenche le déploiement sur GitHub Pages.

Le dépôt doit utiliser « GitHub Actions » dans les paramètres Pages. Les fichiers générés restent aussi versionnés dans `docs/` pour faciliter la consultation du rendu.

## Réutilisation et contribution

Vérifier les licences et les conditions d’accès dans chaque dépôt source. Le catalogue ne remplace pas ces conditions.

[Proposer une ressource ou signaler un problème](https://github.com/AurelienNicosiaULaval/site_ressources_SSD/issues) · [Contacter Aurélien Nicosia](mailto:aurelien.nicosia@mat.ulaval.ca)

Merci à Anne-Sophie Charest pour sa contribution à la création des ressources.
