# Feu vert

Ceci est notre projet pour le cours de développement informatique 2.

## Spécifications des tests unitaires

Les spécifications ci-dessous décrivent précisément les 7 tests unitaires.
Chaque test possède exactement 2 spécifications :

1. Les données d'entrée et leurs types attendus.
2. Le résultat attendu, y compris la réaction en cas de valeur invalide.

| Test unitaire | N° | Données d'entrée et types attendus | Données acceptées | Données refusées et réaction attendue |
|---|---:|---|---|---|
| `test_add_three_answers_with_one_correct_answer` | 1 | `question_id` : `int` ; `answers` : `list` de 3 tuples `(str, bool)` ; `explanation` : `str` | Une question existante, trois propositions textuelles et exactement un `True` | Une liste vide, une liste de taille différente de 3 ou des éléments qui ne sont pas des tuples `(str, bool)` doivent être refusés par `DatabaseError` ; ce cas est couvert par les tests de rejet ci-dessous. |
| `test_add_three_answers_with_one_correct_answer` | 2 | Les trois propositions doivent être liées à la même question ; une seule proposition porte `is_correct=True` | 3 réponses sont insérées ; la réponse correcte est `Proposition B` et son explication est enregistrée | Si aucune proposition ou plusieurs propositions sont correctes, l'insertion doit être refusée par `DatabaseError` et aucune réponse ne doit rester en base. |
| `test_reject_answers_when_the_number_of_propositions_is_invalid` | 1 | `question_id` : `int` ; `answers` : `list` de 2 tuples `(str, bool)` au lieu de 3 | Aucune donnée ne doit être insérée lorsque le nombre de propositions est incorrect | La méthode doit lever `DatabaseError` et la liste retournée par `get_answers_by_question` doit être vide. |
| `test_reject_answers_when_the_number_of_propositions_is_invalid` | 2 | La liste contient des propositions textuelles valides, mais sa longueur vaut `2` | Le type des éléments est correct, mais la règle métier n'est pas respectée | Une liste de longueur différente de `3` doit être rejetée ; la transaction doit être annulée, sans insertion partielle. |
| `test_reject_answers_when_there_is_not_exactly_one_correct_answer` | 1 | `answers` : `list` de 3 tuples `(str, bool)` ; deux tuples ont la valeur `True` | La structure de la liste est correcte, mais le nombre de bonnes réponses ne l'est pas | La méthode doit lever `DatabaseError`, car il doit y avoir exactement une bonne réponse. |
| `test_reject_answers_when_there_is_not_exactly_one_correct_answer` | 2 | Les textes sont des `str` et les indicateurs sont des `bool` ; aucune insertion préalable n'existe | La base doit rester vide pour cette question après l'échec | Toute liste comportant `0` ou plus de `1` valeur `True` doit être refusée et ne doit laisser aucune donnée partielle. |
| `test_edit_and_delete_answer` | 1 | `question_id` : `int` ; texte et explication : `str` ; `answer_id` : `int` | Le texte peut devenir `Nouvelle proposition` et l'explication `Nouvelle explication` | Un identifiant de réponse inexistant doit lever `DatabaseError` lors d'une modification ; ce cas n'est pas encore couvert par ce test. |
| `test_edit_and_delete_answer` | 2 | `answer_id` : `int` correspondant à une réponse existante | La réponse est supprimée et la recherche renvoie une liste vide | Un identifiant inexistant doit lever `DatabaseError` et ne doit supprimer aucune autre réponse ; ce cas n'est pas encore couvert par ce test. |
| `test_add_find_and_remove_subject` | 1 | `subject_name` : `str` non vide ; `subject_id` retourné : `int` | Le sujet ajouté est retrouvé par son nom et apparaît dans la liste `(id, nom)` | Un nom vide ou d'un autre type n'est pas validé par le test actuel ; une validation de type doit être ajoutée si cette règle est exigée. |
| `test_add_find_and_remove_subject` | 2 | `subject_id` : `int` correspondant au sujet créé | Après suppression, `get_subject_id` retourne `-1` | Un identifiant inexistant doit lever `DatabaseError` lors de la suppression ; ce cas n'est pas encore couvert par ce test. |
| `test_edit_subject` | 1 | Ancien et nouveau noms : `str` ; identifiant : `int` existant | Le nom est modifié et le même identifiant est conservé | Un nouveau nom d'un autre type n'est pas validé par le test actuel ; une validation de type doit être ajoutée si cette règle est exigée. |
| `test_edit_subject` | 2 | Recherche avec l'ancien puis le nouveau nom, tous deux de type `str` | L'ancien nom renvoie `-1` et le nouveau nom renvoie le même `subject_id` | La modification ne doit pas créer un deuxième sujet ni changer l'identifiant. |
| `test_reject_edit_of_unknown_subject` | 1 | `subject_id=-1` : `int` représentant un identifiant inexistant ; nouveau nom : `str` | Aucun sujet ne doit être modifié | La méthode doit lever `DatabaseError`, car le sujet demandé n'existe pas. |
| `test_reject_edit_of_unknown_subject` | 2 | L'identifiant est bien de type `int`, mais sa valeur ne correspond à aucune ligne | La transaction doit être annulée et la base doit rester inchangée | Un identifiant inexistant ne doit pas être accepté silencieusement ni créer un sujet. |

### Règles générales

- Les identifiants `question_id`, `answer_id`, `subject_id` sont des `int`.
- Les noms, textes et explications sont des `str`.
- `answers` est une `list` composée de tuples `(str, bool)`.
- Une `DatabaseError` indique qu'une opération en base est refusée ou qu'un
  identifiant n'existe pas.
- Les tests utilisent des données temporaires et les suppriment à la fin afin
  de ne pas modifier les données permanentes de l'application.
- Les réactions indiquées comme « pas encore couvertes » sont des exigences
  documentées, mais elles nécessitent encore un test dédié pour être vérifiées
  automatiquement.

Pour exécuter les tests :

```bash
python -m unittest discover -s classes/test -p "test_*.py"
```
