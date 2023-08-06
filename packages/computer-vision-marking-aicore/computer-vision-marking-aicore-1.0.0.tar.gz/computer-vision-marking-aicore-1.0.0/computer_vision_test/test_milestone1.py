import unittest
import os
import spacy
import pkgutil

class CompVisTestCase(unittest.TestCase):
    
    def test_diff(self):
        solution_path = 'hangman/hangman_solution.py'
        template_path = 'hangman/hangman_Template.py'
        with open(solution_path, 'r') as f:
            solution = f.read()
        with open(template_path, 'r') as f:
            template = f.read()
        self.assertNotEqual(solution, template, 'The hangman_solution.py file is identical to the hangman_Template.py file')
    
    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 500, 'The README.md file should be at least 500 characters long')
        nlp = spacy.load("en_core_web_md")
        tdata = str(pkgutil.get_data(__name__, "documentation.md"))
        doc_1 = nlp(readme)
        doc_2 = nlp(tdata)
        self.assertLessEqual(doc_1.similarity(doc_2), 0.975, 'The README.md file is almost identical to the one provided in the template')


if __name__ == '__main__':

    unittest.main(verbosity=2)
    