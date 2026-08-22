import unittest

from classes.database_manager import DatabaseError
from classes.subject import Subject


class TestSubject(unittest.TestCase):
    def setUp(self):
        # Le nom réservé évite de modifier un sujet utilisé par l'application.
        self.subject = Subject()
        self.subject_name = "__test_subject_unit__"

    def tearDown(self):
        # Le nettoyage est exécuté même si une assertion échoue.
        subject_id = self.subject.get_subject_id(self.subject_name)
        if subject_id != -1:
            self.subject.remove_subject(subject_id)
        self.subject.close()

    def test_add_find_and_remove_subject(self):
        # Un sujet ajouté doit être trouvable par son nom et dans le listing.
        print("Test ajout, recherche et suppression d'un sujet")
        self.subject.add_subject(self.subject_name)

        subject_id = self.subject.get_subject_id(self.subject_name)
        subjects = self.subject.get_subjects()
        print(f"Sujet trouvé : id={subject_id}, total de sujets={len(subjects)}")

        self.assertNotEqual(subject_id, -1)
        self.assertIn((subject_id, self.subject_name), subjects)

        self.subject.remove_subject(subject_id)
        self.assertEqual(self.subject.get_subject_id(self.subject_name), -1)
        print("Résultat : sujet supprimé")

    def test_edit_subject(self):
        # La modification doit conserver l'identifiant tout en changeant le nom.
        print("Test modification d'un sujet")
        new_name = "__test_subject_unit_updated__"
        self.subject.add_subject(self.subject_name)
        subject_id = self.subject.get_subject_id(self.subject_name)

        self.subject.edit_subject(subject_id, new_name)

        self.assertEqual(self.subject.get_subject_id(self.subject_name), -1)
        self.assertEqual(self.subject.get_subject_id(new_name), subject_id)
        print(f"Résultat : sujet id={subject_id} renommé en '{new_name}'")
        self.subject_name = new_name

    def test_reject_edit_of_unknown_subject(self):
        # Modifier un identifiant absent doit signaler l'erreur métier prévue.
        print("Test refus de modification d'un sujet inexistant")
        with self.assertRaises(DatabaseError):
            self.subject.edit_subject(-1, "Sujet inexistant")
        print("Résultat : erreur DatabaseError détectée")


if __name__ == "__main__":
    unittest.main()
