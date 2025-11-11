import unittest
from trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
    
    def test_insert_and_search(self):
        self.trie.insert("cat")
        self.assertTrue(self.trie.search("cat"))
        self.assertFalse(self.trie.search("dog"))
    
    def test_starts_with(self):
        self.trie.insert("cat")
        self.assertTrue(self.trie.starts_with("ca"))
        self.assertFalse(self.trie.starts_with("do"))
