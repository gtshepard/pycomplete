


class WordCache:

    def __init__(self):
        self.cache = set()
        self.build_cache()

    def build_cache(self):
        file_paths = ["/usr/share/dict/words", "one_hundred_most_common_words.txt"]
        n = len(file_paths)
        for i in range(n):
            with open(file_paths[i]) as input_dictionary:
                for line in input_dictionary:
                    words = line.strip().split(" ")
                    for word in words:
                        if word.isalpha():                
                            self.cache.add(word)

    def is_valid_word(self, s):
        return True if s in self.cache else False 
      
class Node:
    def __init__(self, char=''):
        self.children = [None] * 26
        # marks frequency at end
        self.end_of_word = 0
        self.char = char 

    def mark_as_leaf(self):
        self.end_of_word += 1 
    
    def unmark_as_leaf(self):
        self.end_of_word -= 1

class Trie:

    def __init__(self):
        self.root = Node()
        self.build_trie("one_hundred_most_common_words.txt")
    #ascii a char value is 141,
    # b is 142 
    # b - a = 1
    # if we index from 0 to 25 
    # b is in position 1 
    # thus in a trie node its stored
    # in children[1]
    def get_index(self, t):
        return ord(t) - ord('a')
    
    def insert(self, key):
        if not key:
            return 

        key = key.lower()
        curr_node = self.root

        # maybe make text area only take up 3/4 of page
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
            curr_node.mark_as_leaf()
        else:
            return False

    def build_trie(self, file_path):
        with open(file_path) as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split('\n')
                for word in words:
                    self.insert(word)

        #for word in words:
         #   self.insert(word)

    def print_trie(self):
        result = []
        self.dfs(self.root, '', result)
        print(result)

    def dfs(self, node, word, res, k=3):
        
        if node.end_of_word > 0:
            if len(res) < k:
                res.append(word)

        # For each level, go deep down, but DFS fashion 
        # add current char into our current word.
        if len(res) < k:
            for child in node.children:
                if child:
                    self.dfs(child, word + child.char, res, k)

    def build_k_words_with_same_prefix(self, key, k):
      
        key = key.lower()
        curr_node = self.root
        # find end of prefix in trie 
        n = len(key)
        for level in range(n):
            index = self.get_index(key[level])
            if not curr_node.children[index]:
                return False 
            curr_node = curr_node.children[index]

        source = curr_node
        same_prefix = []

        # build k words with specified prefix 
        self.dfs(source, key, same_prefix, k=k)
        return same_prefix

class AutoComplete:
    def __init__(self):
        self.word_cache = WordCache()
        self.trie = Trie()
        pass

    def record_word(self, word):
        if word in self.word_cache.cache:
            # have to adjust insert so size does not execeede 100
            self.trie.insert(word)
       

    def suggest_words(self, prefix, top_k):
        suggested_words = self.trie.build_k_words_with_same_prefix(prefix,k=top_k)
        print(suggested_words)
        return suggested_words

if __name__ == '__main__':

    words = ['hello', 'abc', 'baz', 'bar', 'barz', 'acorn', 'acorns']
    all_words = []
    a = AutoComplete()
    a.record_word("whale")
    a.suggest_words("wh", 5)
   # file_path = "one_hundred_most_common_words.txt"
    #t.build_trie(file_path)
    #t.build_k_words_with_same_prefix("wh",k=5)

    # how to add frequency to trie?
    # 1+ represents word end 
    # 0 represents no word
    # if try inserted, its mark is set to 1
    # if a word is searched for and found frequency value is + 1 
    
    # if we type a word and hit space, that is not in the trie, then the word 
    # is pushed into the trie
    # the issue here is users may type things that are not words
    # to eliminate this problem we will check the words against the word dictionary
    # and the 100 most common words dictionary to make sure to only insert real words
    # we sacrfice a bit of space, for effiecney and accuracy.
    # we keep the trie smaller by not adding uneeded content and accruate 
    # if we restict the size of the trie to 100, we will never run into search issues 
    # and it effectilvely operates in constant time 

    #1. prevent strings that are not real words being placed in trie 
    # this happens when user hits space when a word is misspelled.
    # we check the users input against a 2 word banks - 100 most common words
    # and dictionary 

'''
    with open("/usr/share/dict/words") as input_dictionary:
        for line in input_dictionary:
            words = line.strip().split(" ")
            for word in words:
                if word.isalpha():                
                    # all_words.append(word)
                    t.insert(word)
  '''
#  O(L + N*W) lookup O(L) time for prefix lookup. O(N*W) where N is the number of words that have the prefix abd W is
# the is the lenght of the longest word  
# 
# O(W * L * N) where L is the max word length (depth) and N is the number of words and W is the width of the tree
# however W is constant at 26, thus we have O(L * N) space
# compared to a series of maps its more efficient memory wise if we you had as hash map for each word
# 

