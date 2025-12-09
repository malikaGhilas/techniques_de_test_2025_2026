# RETEX – Ce que j’ai appris avec ce TP

## Ce qui a bien marché

Au départ, j’étais un peu dépassée : on nous demandait de tout tester *avant même de coder*, et j’avais l’habitude de faire l’inverse. Mais finalement, cette méthode m’a vraiment aidée. En écrivant les tests en premier, j’ai d’abord dû **comprendre précisément ce que devait faire chaque fonction**, surtout avec les formats binaires (PointSet, Triangles). Ça m’a évité de coder n’importe quoi.

Les tests de sérialisation/désérialisation ont été les plus utiles : une fois qu’ils passaient, je savais que j’échangeais les bonnes données avec l’API. Et le mock du PointSetManager m’a sauvée — sans ça, j’aurais été bloquée en attendant d’avoir un vrai service externe.

J’ai aussi beaucoup apprécié `ruff` : même si les messages étaient parfois un peu stricts (notamment sur les docstrings !), ça m’a forcée à écrire du code propre. Et à la fin, voir « All checks passed! » était super satisfaisant.

## Ce que j’aurais fait différemment

Je me suis perdue pendant un moment avec l’algorithme de triangulation. J’ai cherché une version complète de Delaunay, mais c’était trop complexe à faire « from scratch ». J’aurais gagné du temps en **acceptant plus tôt** de faire une version simple (triangulation en éventail). Après tout, le but du TP n’était pas la géométrie, mais la qualité du test — et ça, je l’ai compris un peu tard.

Côté outils, j’ai galéré avec `make` et `pdoc` sous Windows. J’aurais dû tester l’environnement dès la première séance, au lieu de tout laisser pour la fin. Un conteneur Docker ou WSL m’aurait probablement évité ces problèmes.

## Mon plan vs la réalité

Mon plan de tests (`PLAN.md`) était ambitieux : j’avais prévu de valider des propriétés géométriques fortes (aires non nulles, convexité, etc.). Mais une fois face à l’implémentation, j’ai dû **simplifier** : mon algorithme ne garantissait pas ces propriétés, donc les tests seraient restés rouges. J’ai donc recentré mes tests sur ce qui comptait vraiment :
- le bon format binaire en entrée/sortie,
- la gestion des cas limites (moins de 3 points),
- la robustesse de l’API (même avec des données bizarres).

C’est un bon rappel : un test pertinent vaut mieux qu’un test « parfait » qui ne correspond pas à l’implémentation.

## En résumé

Même si j’étais en retard à la séance 5, ce TP m’a montré la puissance d’une **démarche test-first bien appliquée**. Mes tests m’ont guidée, rassurée, et ont rendu le debug beaucoup plus rapide. À la fin, avoir 89 % de couverture, une doc générée, et un `Makefile` qui fonctionne, c’est une vraie fierté.

Je retiens surtout que **les tests ne sont pas une corvée** : ce sont la base d’un code fiable. Et même sous Windows, avec des outils capricieux, on arrive au bout avec un peu de persévérance ! 