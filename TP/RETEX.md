# RETEX – Ce que j'ai appris avec ce TP

## Ce qui a bien marché

Au départ, j'étais un peu dépassée : on nous demandait de tout tester *avant même de coder*, et j'avais l'habitude de faire l'inverse. Mais finalement, cette méthode m'a vraiment aidée. En écrivant les tests en premier, j'ai d'abord dû **comprendre précisément ce que devait faire chaque fonction**, surtout avec les formats binaires (PointSet, Triangles). Ça m'a évité de coder n'importe quoi.

Les tests de sérialisation/désérialisation ont été les plus utiles : une fois qu'ils passaient, je savais que j'échangeais les bonnes données avec l'API. Et le mock du PointSetManager m'a sauvée — sans ça, j'aurais été bloquée en attendant d'avoir un vrai service externe.

J'ai aussi beaucoup apprécié `ruff` : même si les messages étaient parfois un peu stricts (notamment sur les docstrings !), ça m'a forcée à écrire du code propre. Et à la fin, voir « All checks passed! » était super satisfaisant.

## Ce que j'aurais fait différemment

Je me suis perdue pendant un moment avec l'algorithme de triangulation. J'ai cherché une version complète de Delaunay, mais c'était trop complexe à faire « from scratch ». J'aurais gagné du temps en **acceptant plus tôt** de faire une version simple (triangulation en éventail). Après tout, le but du TP n'était pas la géométrie, mais la qualité du test — et ça, je l'ai compris un peu tard.

Côté outils, j'ai galéré avec `make` et `pdoc` sous Windows. J'aurais dû tester l'environnement dès la première séance, au lieu de tout laisser pour la fin. Finalement j'ai contourné en utilisant directement `python -m pytest` et compagnie, mais j'ai perdu du temps bêtement.

## Mon plan vs la réalité

Mon plan de tests (`PLAN.md`) était assez complet sur le papier : j'avais bien identifié les 3 grandes catégories (sérialisation, triangulation, API). Mais dans les détails, j'avais sous-estimé certains trucs et sur-estimé d'autres.

**Ce qui a marché comme prévu :**
- Les tests de sérialisation/désérialisation : buffer tronqués, valeurs extrêmes (NaN, Inf), indices invalides → j'ai bien testé tout ça
- Les tests API avec mock : erreurs 404/503, méthodes non autorisées, validation des headers → nickel
- La séparation des tests de performance avec le marker `@pytest.mark.slow`

**Ce que j'ai dû adapter :**
- Dans mon plan, j'avais prévu de tester des "propriétés structurelles" comme l'aire non nulle des triangles ou la convexité. En vrai, avec ma triangulation en éventail basique, ces propriétés ne sont pas garanties. J'ai gardé les tests d'aires pour les points bien espacés, mais j'ai dû accepter que des triangles dégénérés puissent exister avec des points colinéaires.
- J'avais pas prévu autant de variantes de tests. Par exemple, j'ai fini par tester les points très proches (epsilon), les doublons, et plein de cas limites qui me sont venus en codant.

**Ce que j'ai ajouté en cours de route :**
- Des tests de déterminisme (même input → même output)
- Des tests pour vérifier que tous les points sont utilisés dans au moins un triangle
- Plus de tests API que prévu (IDs vides, très longs, caractères spéciaux)

Au final, je suis passée de ~15 tests prévus dans mon plan à 72 tests. C'est en implémentant que j'ai vu tous les cas foireux possibles.

## En résumé

Même si j'étais en retard à la séance 5, ce TP m'a montré l'intérêt d'une **démarche test-first**. Mes tests m'ont guidée, rassurée, et ont rendu le debug beaucoup plus rapide. À la fin, j'ai 98% de couverture avec tous les tests qui passent, une doc générée, et un `Makefile` qui marche.

Je retiens surtout que **les tests ne sont pas une corvée** : c'est ce qui fait qu'on peut refactoriser sans avoir peur de tout casser. Mon plan initial était utile pour structurer ma réflexion, mais c'est vraiment en codant que j'ai découvert la majorité des cas à tester. C'est ça aussi le test-first : on itère, on découvre, on améliore.

Et même sous Windows avec des outils relous, on y arrive en s'adaptant. Le truc le plus important que j'ai compris : écrire les tests avant force à vraiment réfléchir à ce que doit faire le code. Au début c'est bizarre, mais après ça devient naturel. 