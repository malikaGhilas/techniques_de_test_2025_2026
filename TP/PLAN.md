# Plan de Tests Triangulator

## 1. Sérialisation / Désérialisation

### Sérialisation d’un PointSet valide

**Pourquoi :** Vérifier le respect du format binaire attendu (interopérabilité).
**Comment :** Créer un PointSet, le sérialiser, puis vérifier la taille, les offsets et les valeurs avec `struct.unpack`.

### Désérialisation d’un PointSet valide

**Pourquoi :** Garantir la réversibilité et la fidélité des données reçues.
**Comment :** Construire un buffer binaire, désérialiser, et comparer les coordonnées avec `pytest.approx`.

### PointSet vide / 1 point / 2 points

**Pourquoi :** Tester les cas limites non-triangulables.
**Comment :** Vérifier que la sérialisation reste correcte et que la triangulation échoue proprement (erreur claire ou 0 triangle).

### Valeurs extrêmes et corrompues

**Pourquoi :** Assurer la robustesse face à des floats extrêmes ou à des buffers invalides.
**Comment :** Tester des valeurs très grandes/petites, NaN/Inf, et des buffers tronqués ou incohérents → attendre une exception explicite.

### Sérialisation/Désérialisation des Triangles

**Pourquoi :** Valider le format binaire complet (points + indices).
**Comment :** Vérifier la structure (compte, taille, indices), la cohérence, et la réversibilité.

### Indices invalides (hors limites / négatifs)

**Pourquoi :** Prévenir les incohérences dans les données de sortie.
**Comment :** Injecter des indices erronés et attendre une erreur de validation.

---

## 2. Algorithme de Triangulation

### Cas simples (3, 4, 5 points)

**Pourquoi :** Vérifier la validité géométrique de la triangulation de base.
**Comment :** Vérifier le nombre de triangles, la cohérence des indices et la non-dégénérescence.

### Point intérieur

**Pourquoi :** Tester la triangulation avec des points non convexes.
**Comment :** Vérifier la couverture complète et la connexité.

### Points aléatoires

**Pourquoi :** Évaluer la robustesse sur des données variées.
**Comment :** Générer aléatoirement plusieurs jeux de points et vérifier propriétés topologiques (tous les points utilisés, pas de triangles dégénérés).

### Cas dégénérés (colinéaires, doublons, quasi-alignés)

**Pourquoi :** Tester les limites numériques et géométriques.
**Comment :** Vérifier qu’une erreur claire est levée ou que 0 triangle est retourné, selon le choix de conception.

### Propriétés structurelles

**Pourquoi :** Garantir intégrité et stabilité.
**Comment :** Vérifier que tous les points d’entrée sont conservés, qu’aucun triangle n’a une aire nulle, et que les résultats sont déterministes.

---

## 3. API HTTP

### POST /triangulate — Cas nominal

**Pourquoi :** Vérifier le fonctionnement complet (intégration avec PointSetManager).
**Comment :** Mocker la réponse du PointSetManager et vérifier le format binaire du résultat.

### POST /triangulate — Erreurs de requête

**Pourquoi :** Gérer les entrées invalides proprement.
**Comment :** Tester JSON malformés, types incorrects → attendre 400 Bad Request.

### Erreurs du PointSetManager (404, 500, indisponible)

**Pourquoi :** Tester la résilience et la propagation d’erreurs.
**Comment :** Mocker différents codes d’erreur et vérifier les réponses (404, 502, 503).

### Données corrompues ou non-triangulables

**Pourquoi :** Gérer les données invalides reçues.
**Comment :** Simuler un buffer invalide ou <3 points → 422 ou 400 selon le cas.

### Points colinéaires

**Pourquoi :** Cas géométrique non-valide à signaler au client.
**Comment :** Mocker un PointSet aligné → 400 Bad Request.

### Validation des en-têtes HTTP

**Pourquoi :** Respect du protocole et du contrat OpenAPI.
**Comment :** Vérifier `Content-Type`, `Content-Length`, et les headers sur toutes les réponses.

### Méthodes non autorisées et routes inconnues

**Pourquoi :** Sécuriser l’API.
**Comment :** Tester GET/PUT/DELETE → 405 Method Not Allowed ; routes inexistantes → 404.
