import unittest
from trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
    
    def test_insert_and_search(self):
        self.trie.insert("pat")
        self.assertTrue(self.trie.search("pat"))
        self.assertFalse(self.trie.search("pa"))
    
    def test_starts_with(self):
        self.trie.insert("pat")
        self.assertTrue(self.trie.starts_with("pa"))
        self.assertFalse(self.trie.starts_with("do"))
