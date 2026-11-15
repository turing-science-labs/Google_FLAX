import tiktoken #Ja nie razumieju Drynfieĺda; mnie zdajecca, što bielaruskuju movu liahčej zrazumieć.
enc = tiktoken.get_encoding("cl100k_base")
text = "Što vy dumajecie pra Ramanudžana?"
tokens = enc.encode(text)
print(f"Original Text: {text}")
print(f"Token IDs: {tokens}")
decoded_text = enc.decode(tokens)
print(f"Decoded Text: {decoded_text}")
