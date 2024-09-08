import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", "bold", "https://www.examplewebsite.com")
        node2 = TextNode("This is a text node", "bold", "https://www.examplewebsite.com")
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", "https://www.examplewebsite.com")
        node2 = TextNode("This is a text node", "https://www.examplewebsite.com")
        self.assertEqual(node, node2)

    def test_eq5(self):
        node = TextNode("This is a text node", "bold", "https://www.examplewebsite.com")
        node2 = TextNode("This is not a text node", "bold", "https://www.examplewebsite.com")
        self.assertNotEqual(node, node2) 

if __name__ == "__main__":
    unittest.main()