# AICH-Encryption
 Encrypt Words Found In A Dictionary. Helpful In Tokenizing Blockchain Wallet Passwords.


# Installation
sudo pip install aich

# Usage
from a2 import aich

search_word = input('Enter your encryption phrase:')

encrypted = aich.aichin(search_word)

print (encrypted)

search_word = input('Enter your decryption phrase:')

encrypted = aich.aichout(search_word)

print (encrypted)

# Encryption Example
{Inputs: this is freedom , Outputs: 0x6322a.0x3057e.0x23cef.}

# Decryption Example
{Inputs: 0x6322a.0x3057e.0x23cef , Outputs: this is freedom}


