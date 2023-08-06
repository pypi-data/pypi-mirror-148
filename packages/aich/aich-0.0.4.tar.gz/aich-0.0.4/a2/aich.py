
# File Processor
# ==============
def readictionary(handle):
    filename = 'a2/dict.txt'
    words = {}
    ctr = 0
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
    for line in lines:  
                if(handle == 'enc'):
                        words[line.lower()] = ctr
                else:
                        words[ctr] = line.lower()

                ctr = ctr + 1
    return words



# Encrypt
# ================
def aichin(search_word_enc):
    phrase_enc = search_word_enc.split(' ')
    encrypted = ''
    words_enc = readictionary('enc')

    for p_enc in phrase_enc:
            if p_enc.lower() in words_enc:
                position = hex(words_enc.get(p.lower()))
            else:
                position = p_enc
            encrypted = encrypted + str(position) + '.'        
    return (encrypted)



# Decrypt
# ================
def aichout(search_word_dec):
        phrase_dec = search_word_dec.split('.')
        words_dec = readictionary('dec')
        decrypted = ''

        for p_dec in phrase_dec:
                try:
                        tmp = words_dec[int(p_dec, 16)]
                except:
                        tmp = p_dec
                decrypted = decrypted + str(tmp) + ' '        
        print (decrypted)