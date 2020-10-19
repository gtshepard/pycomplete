class BkNode:
    def __init__(self, word):
        self.word = word
        self.children = {}

class BkTree:
    def __init__(self):
        self.root = BkNode()
        self.tolerance = 2
        self.max_words = 100
        self.max_word_len = 15

    def edit_distance(self, s1, s2):
        print(s1, s2)
        n, m = len(s1), len(s2)
        dp = [[-1 for _ in range(m + 1)] for _ in range(n + 1)]

        # if s2 empty, we can remove all characters of s1
        # to make it empty
        for i in range(n + 1):
            dp[i][0] = i

        # if s1 is empty, we hae to insert all chars of s2
        for j in range(m + 1):
            dp[0][j] = j

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # delete, insert, replace
                    dp[i][j] = 1 + min(dp[i - 1][j], min(dp[i][j - 1], dp[i - 1][j]))

        return dp[n][m]

    def insert(self, root, word):
        new_node = BkNode(word)
        if not root:
            self.root = new_node
            return 

        edit_dist = self.edit_distance(root.word. new_node.word)
    
        while         


       # while edit_dist in curr.children:
           # curr = curr.children[edit_dist]
          #  edit_dist = self.edit_distance(curr.word, word)
      #  curr.children[edit_dist] = new_node
       # new_node
        

        if self.tree[]

        root.children[edit_dist]
            

if __name__ == '__main__':
    bk = BkTree()
    w1, w2 = "help", "shell"
    print("edit: ", bk.edit_distance(w1, w2))
 