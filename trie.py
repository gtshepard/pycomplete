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

    def build_trie(self, words):
        for word in words:
            self.insert(word)

    def print_trie(self):
        result = []
        self.dfs(self.root, '', result)
        print(result)

    def dfs(self, node, word, res):
        
        if node.is_end_of_word:
            res.append(word)
    
        # For each level, go deep down, but DFS fashion 
        # add current char into our current word.
        for child in node.children:
            if child:
                idx = self.get_index(child.char)
                self.dfs(node.children[idx], word + child.char, res)
    
    def same_prefixes(self, key):
        key = key.lower()
        curr_node = self.root
        n = len(key)
        for level in range(n):
            index = self.get_index(key[level])
            if not curr_node.children[index]:
                return False 
            curr_node = curr_node.children[index]

        source = curr_node
        same_prefix = []
        self.dfs(source, key, same_prefix)
        print(same_prefix)

if __name__ == '__main__':
    t = Trie()
    words = ['hello', 'abc', 'baz', 'bar', 'barz', 'acorn', 'acorns']
    t.build_trie(words)
   # t.print_trie()
    t.same_prefixes("a")

