class Node:
    def __init__(self, char=''):
        self.children = [None] * 28
        # marks frequency at end
        self.end_of_word = 0
        self.char = char 

    def mark_as_leaf(self):
        self.end_of_word += 1 
    
    def unmark_as_leaf(self):
        self.end_of_word -= 1
    def unmark_as_leaf_to_delete(self):
        self.end_of_word = 0

from heapq import *
class TopkTrie:

    def __init__(self, file_path=None):
        self.number_of_words = 0
        self.capacity = 1001
        self.word_freq = {}
        self.root = Node()
        if file_path:
            self.build_trie(file_path)
    
    # convert char to index 0 to 27
    def get_index(self, t):
        
        if t == r"""'""":
            return 26

        if t == "-":
            return 27

        return ord(t) - ord('a')
    
    def insert(self, key):

        if not key:
            return 

        # prune least frequent element if cacapicty exceeded
        if self.number_of_words >= self.capacity:
            self.lfu_prune()

        key = key.lower()
        curr_node = self.root
        self.word_freq[key] = self.word_freq.get(key, 0) + 1
       
        for level in range(len(key)):
            # get the index for the levelth char 
            # of the word to insert
            index = self.get_index(key[level])
            
            # if char does not exist
            if not curr_node.children[index]:
                # insert char at current level 
                curr_node.children[index] = Node(key[level])

            curr_node = curr_node.children[index]

        # mark as word end by incrementing frequncy
        curr_node.mark_as_leaf()
        self.number_of_words += 1

    def search(self, key):
        if not key:
            return False
        
        key = key.lower()
        curr_node = self.root
        n = len(key)
        for level in range(n):
            index = self.get_index(key[level])
            if not curr_node.children[index]:
                return False 
            curr_node = curr_node.children[index]
        
        if curr_node and curr_node.end_of_word > 0:
            self.word_freq[key] += 1
            curr_node.mark_as_leaf()
            return True 
        else:
            return False

    def build_trie(self, file_path):
        with open(file_path) as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split('\n')
                for word in words:
                    self.insert(word)


    def delete(self, key):
        if not self.root or not key:
            print("Empty Trie")
            return 
        self.delete_helper(key, self.root, len(key),0)
        self.number_of_words -= 1

    # recursively delete word from trie
    def delete_helper(self, key, curr, length, level): 
        did_delete = False 
        n = len(key)
        
        if not curr:
            return did_delete

        if level is length:
            if self.is_childless(curr):
                curr = None
                did_delete = True
            else:
                curr.unmark_as_leaf_to_delete()
                did_delete = False 
        else:
            child_node = curr.children[self.get_index(key[level])]
            child_deleted = self.delete_helper(key, child_node, length, level + 1)
            if child_deleted:
                current_node.children[self.get_index(key[level])] = None

                if current_node.is_end_word > 0:
                    did_delete = False 

                elif not self.is_childless(curr):
                    did_delete = False 
                else:
                    curr = None 
                    did_delete = True
            else:
                did_delete = False 

        return did_delete

    def is_childless(self, node):
            n = len(node.children)
            for i in range(n):
                if not node.children[i]:
                    return False 
            return True 

    def print_trie(self):
        result = []
        self.construct_words(self.root, '', result)
        print(result)
    
    # trie is a tree where each node has 26 chidren 
    # thus we can use DFS to travese trie and long the way rebuild words
    def construct_words(self, node, word, res):
        if node.end_of_word > 0:
            res.append((node.end_of_word, word))

        for child in node.children:
            if child:
                self.construct_words(child, word + child.char, res)
    
    def get_end_of_prefix(self, prefix):
        key = prefix.lower()
        curr_node = self.root
        # find end of prefix in trie 
        n = len(key)
        for level in range(n):
            index = self.get_index(key[level])
            if not curr_node.children[index]:
                return False 
            curr_node = curr_node.children[index]
        
        return curr_node
        
    # get least frequently used word
    def get_lfu(self):
        least_freq = (float('inf'), None)
        for word, f in self.word_freq.items():
            if f < least_freq[0]:
                least_freq = (f, word)
        return least_freq[1]

    def lfu_prune(self):
        key = self.get_lfu()
        del self.word_freq[key]
        self.delete(key)


