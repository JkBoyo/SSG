from main import extract_title
import unittest
class TestMainFuncs(unittest.TestCase):
    def test_extract_title(self):
        titled_strings = [
            "# This is the title\n\nThis is a paragraph\n\n## This is a second heading\n\n!. for an\n2. ordered list",
            "## This is an out of order title\n\n# title\n\nbut it should still work."
        ]
        result_titles = [
            "This is the title", "title"
        ]
        self.assertEqual([extract_title(string) for string in titled_strings], result_titles)

    def test_title_exception(self):
        markdown_without_titles = "## subtitle\n\nparagraph\n\n1. first el\n\n2. second el"
        with self.assertRaises(Exception, msg= "No Title in markdown."):
            extract_title(markdown_without_titles)