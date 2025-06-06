# Gabarit de site web Quarto

Ce dossier contient un **template minimal** pour créer un site web Quarto inspiré du projet *Ressources SSD*.

## Utilisation rapide

1. Installez [Quarto](https://quarto.org).
2. Dans un terminal, exécutez :
   ```bash
   quarto use template <chemin-vers-ce-repertoire>
   ```
3. Personnalisez les fichiers `index.qmd`, `about.qmd` et `styles.css` selon vos besoins.
4. Lancez l'aperçu du site :
   ```bash
   quarto preview
   ```
5. Une fois satisfait·e, publiez sur GitHub Pages ou toute autre plateforme.

## Contenu du template

- `template.yaml` : métadonnées du modèle.
- `skeleton/` : fichiers du projet à copier lors de la création.
  - `_quarto.yml` définit la configuration du site.
  - `index.qmd` page d'accueil.
  - `about.qmd` page d'exemple.
  - `styles.css` feuille de style simple.
