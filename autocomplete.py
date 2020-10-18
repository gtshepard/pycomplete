


class Node:
    def __init__(self, char=''):
        self.children = [None] * 26
        self.is_end_of_word = False
        self.char = char 

    def mark_as_leaf(self):
        self.is_end_of_word = True 
    
    def unmark_as_leaf(self):
        self.is_end_of_word = True 

class Trie:


    def __init__(self):
        self.root = Node()
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

        #mark as word end, happens whether we insert
        # letters or not 
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
        
        return True if curr_node and curr_node.is_end_of_word else False

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
        
        if node.is_end_of_word:
            if len(res) < k:
                res.append(word)

        # For each level, go deep down, but DFS fashion 
        # add current char into our current word.
        if len(res) < k:
            for child in node.children:
                if child:
                    self.dfs(child, word + child.char, res, k)

    def k_similar(self, key, k):
      
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
        print(same_prefix)

if __name__ == '__main__':
    t = Trie()
    words = ['hello', 'abc', 'baz', 'bar', 'barz', 'acorn', 'acorns']
    all_words = []

    file_path = "one_hundred_most_common_words.txt"
    t.build_trie(file_path)
    t.k_similar("wh",k=5)


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

