import random
import string

class PrivateGromovKey:
    def __init__(self, num_generators: int, num_relations: int, max_relation_len: int = 5):
        """ Represents a group with N generators and M randomly chosen relations (Private Gromov Key),
        along with a random permutation mapping of the 26 alphabet characters. """
        self.N = num_generators
        self.M = num_relations
        self.max_len = max_relation_len # Generators: ['x1', 'x2', ..., 'xN']
        self.generators = [f"x{i}" for i in range(1, self.N + 1)] # Inverses: ['x1^-1', 'x2^-1', ..., 'xN^-1']
        self.inverses = [f"{g}^-1" for g in self.generators] # All available symbols we can choose from when building a word
        self.symbols = self.generators + self.inverses # Generate M unique, simplified relations
        self.relations = self._generate_relations()

        # Permutation mapping of the 26 letters (a-z)
        self.alphabet = list(string.ascii_lowercase)
        self.permitted_alphabet = list(string.ascii_lowercase)
        random.shuffle(self.permitted_alphabet)
        self.permutation_map = dict(zip(self.alphabet, self.permitted_alphabet))

    def simplify_word(self, word_list: list) -> list:
        """ Simplifies a word by removing adjacent inverses (e.g. 'x1' followed immediately by 'x1^-1' gets canceled). """ 
        stack = []
        for symbol in word_list:
            if stack:
                top = stack[-1] # A symbol and its inverse cancel each other out
                is_inverse_of_top = (symbol.endswith("^-1") and symbol[:-3] == top) or \
                                    (top.endswith("^-1") and top[:-3] == symbol)
                if is_inverse_of_top:
                    stack.pop()
                    continue
            stack.append(symbol)
        return stack

    def _generate_relations(self) -> list:
        relations_set = set()
        relations_list = []
        while len(relations_list) < self.M:
            length = random.randint(2, self.max_len) # Randomly pick symbols to construct a raw word
            raw_word = [random.choice(self.symbols) for _ in range(length)] # Cancel out trivial adjacent inverses
            simplified = self.simplify_word(raw_word) # Represent as a tuple to store in set for uniqueness tracking
            word_tuple = tuple(simplified)
            if simplified and word_tuple not in relations_set:
                relations_set.add(word_tuple)
                relations_list.append(simplified)
        return relations_list

    def encrypt(self, text: str) -> str:
        """ Scrambles a text string using the private alphabet permutation map. """
        encrypted_chars = []
        for char in text:
            if char.lower() in self.permutation_map:
                # Get the cipher character matching original case
                cipher_char = self.permutation_map[char.lower()]
                encrypted_chars.append(cipher_char.upper() if char.isupper() else cipher_char)
            else:
                encrypted_chars.append(char)
        return "".join(encrypted_chars)

    def __str__(self) -> str:
        gens_str = ", ".join(self.generators)
        rels_str = ", ".join(["*".join(rel) for rel in self.relations])
        perm_sample = "".join([self.permutation_map[c] for c in string.ascii_lowercase])
        return f"Private Gromov Key Group G = < {gens_str} | {rels_str} >\n" \
               f"Alphabet Permutation (a-z): {perm_sample}"

if __name__ == "__main__": # Initialize private key group with 3 generators and 4 random relations
    group = PrivateGromovKey(num_generators=3, num_relations=4, max_relation_len=6)
    print(group)
    print("\n--- Encryption Demo ---")
    plaintext = "Hello World!"
    ciphertext = group.encrypt(plaintext)
    print(f"Plaintext:  {plaintext}")
    print(f"Ciphertext: {ciphertext}")
