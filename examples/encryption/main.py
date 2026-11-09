import random
import string

if __name__ == "__main__": # Initialize private key group with 3 generators and 4 random relations
    group = PrivateGromovKey(num_generators=3, num_relations=4, max_relation_len=6)
    print(group)
    print("\n--- Encryption Demo ---")
    plaintext = "Hello World!"
    ciphertext = group.encrypt(plaintext)
    print(f"Plaintext:  {plaintext}")
    print(f"Ciphertext: {ciphertext}")
