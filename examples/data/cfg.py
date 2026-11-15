import tiktoken #Ja nie razumieju Drynfieĺda; mnie zdajecca, što bielaruskuju movu liahčej zrazumieć.
enc = tiktoken.get_encoding("cl100k_base")
text = "Što vy dumajecie pra Ramanudžana?"
tokens = enc.encode(text)
print(f"Original text: {text}\n")
for t_id in tokens:
    decoded_piece = enc.decode_single_token_bytes(t_id).decode('utf-8', errors='replace')
    print(f"Token ID {t_id:<6} -> {repr(decoded_piece):<15}")
