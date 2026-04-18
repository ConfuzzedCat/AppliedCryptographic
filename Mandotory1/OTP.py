def encrypt(plaintext, key):
    if len(plaintext) > len(key):
        cur_pos = 0
        while len(plaintext) > len(key):
            key += key[cur_pos]
            cur_pos = (cur_pos + 1) % len(key)
    ciphertext = ""
    for i, char in enumerate(plaintext):
        ciphertext += chr((ord(char) ^ ord(key[i])) + ord('a') % ord('a'))
    return ciphertext

def decrypt(ciphertext, key):
    return encrypt(ciphertext, key)