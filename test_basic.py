import unittest
import subprocess
import re
from os import environ

class MoveRatingTestBasic(unittest.TestCase):
    def setUp(self):
        if environ.get('OMDB_API_KEY') is None or len(environ.get('OMDB_API_KEY')) < 1:
            raise Exception("The OMDB_API_KEY environment variable is not set. Unable to run tests without it")

    def test_existing_movie(self):
        p = self._movie_rating_cmd("--title 'Guardians of the Galaxy'")
        rating = p.stdout.rstrip()
        self.assertTrue(re.match(r'^\d\d%$', rating), "Existing movie has a rating ({})".format(p.stdout))

    def test_existing_movie_bad_year(self):
        p = self._movie_rating_cmd("--title 'Guardians of the Galaxy' --year 1999")
        self.assertNotEqual(p.returncode, 0, "Non-zero return code")
        self.assertTrue(p.stdout == "", "Bad Year ({}) doesn't have a rating")
        error = p.stderr.rstrip()
        self.assertEqual("We're sorry, but a movie by that name (Guardians of the Galaxy) in that year (1999) was not found", error, "Correct error for bad year")

    def test_typo_movie(self):
        p = self._movie_rating_cmd("--title 'Napolean Dynamite'")
        self.assertNotEqual(p.returncode, 0, "Non-zero return code")
        self.assertTrue(p.stdout == "", "Typo ({}) doesn't have a rating")
        error = p.stderr.rstrip()
        self.assertEqual("We're sorry, but a movie by that name (Napolean Dynamite) was not found", error, "Correct error for typo movie")

    def test_missing_title(self):
        p = self._movie_rating_cmd("")
        self.assertNotEqual(p.returncode, 0, "Non-zero return code")
        self.assertTrue('arguments are required: --title' in p.stderr, "Correct error for missing title")

    def test_invalid_year(self):
        p = self._movie_rating_cmd("--title Foo --year 200a")
        self.assertNotEqual(p.returncode, 0, "Non-zero return code")
        self.assertTrue('--year: invalid int value' in p.stderr, "Correct error for invalid year")

    def test_invalid_api_key(self):
        p = subprocess.run("/usr/src/app/movie_rating.py --api-key foo --title foo", shell=True, capture_output=True, text=True)
        self.assertNotEqual(p.returncode, 0, "Non-zero return code")
        self.assertTrue("API Key was not valid" in p.stderr, "Correct error for invalid api-key")


    def _movie_rating_cmd(self, args):
        p = subprocess.run("/usr/src/app/movie_rating.py {}".format(args), shell=True, capture_output=True, text=True)
        return p

if __name__ == '__main__':
    unittest.main()
