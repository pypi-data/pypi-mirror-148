import unittest
import os
import spacy
from urllib.request import urlopen

class CompVisTestCase(unittest.TestCase):
    
    def test_manual_rps_presence(self):
        manual_game_script = 'manual_rps.py'
        self.assertIn(manual_game_script, os.listdir('.'), 'There is no manual_rps.py file in your project folder. If it is there, make sure it is named correctly, and that it is in the main folder')

    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 1500, 'The README.md file should be at least 1500 characters long')
        nlp = spacy.load("en_core_web_md")
        documentation = urlopen("https://aicore-files.s3.amazonaws.com/documentation.md")
        tdata = str(documentation.read(), 'utf-8')
        doc_1 = nlp(readme)
        doc_2 = nlp(tdata)
        self.assertLessEqual(doc_1.similarity(doc_2), 0.975, 'The README.md file is almost identical to the one provided in the template')


if __name__ == '__main__':

    unittest.main(verbosity=2)
    