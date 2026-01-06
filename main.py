import re
#I have commented the code that makes the guesses
#so the code can run directly without downloading the nltk library necessary for making the guesses


#We will use nltk library to estimate the uncomplete words so in order to start guessing,
#You need to download nltk in your machine
#Using pip install nltk
#Then download the corpse of english words using nltk.download('words') present at the end of the code
#Then comment #nltk.download('words') and run the code again
 
import nltk
import re
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def srh(word):
    completions = nltk.corpus.words.words()
    ln=len(word)
    word=word.replace('-','\w')
    pattern=r"{}".format(word)
    results=[word for word in completions if re.match(pattern,word) and len(word)==ln]
    return results
    




# Read the input from a file
file_name = "input.txt"  # Replace with the actual file name
with open(file_name, "r") as file:
    ciphertext = file.read()

ciphertext=ciphertext.split()




# Convert the ciphertext from hexadecimal to binary
binary=[]
for cipher in ciphertext:
    cipher = bin(int(cipher, 16))[2:]
    binary.append(cipher)



cipherB=[]


for cipher in binary:
    match=re.findall(r"\d{8}",cipher)
    cipherB.append(match)




    


asc={
    'space':'00010000'
    
    }







#Make a list of lists,2D array , to carry the message
plain_txt=[ ['-' for i in range(29)] for _ in range(6)]

#Loop across the words 3 characters by 3 characters and start XORing the words in the same column
#Check if the result of the seventh bit from the right,in the result of xoring 2 ciphers, is 1
#If it is 1 so one of the words is a space
#Perform the XORing with all the words ,in the same column, which have the same key



fnd=[]
for j in range(29):
    for i in range(4):
        prev=cipherB[i][j]
        cur=cipherB[i+1][j]
        nxt=cipherB[i+2][j]
        res1=int(prev,2)^int(cur,2)
        res1=bin(res1)[2:].zfill(8)
        seventh_bit1 = (int(res1,2) >> 6) & 1
        
        res2=int(cur,2)^int(nxt,2)
        res2=bin(res2)[2:].zfill(8)
        seventh_bit2 = (int(res2,2) >> 6) & 1
        
        res3=int(prev,2)^int(nxt,2)
        res3=bin(res3)[2:].zfill(8)
        seventh_bit3 = (int(res3,2) >> 6) & 1

        if seventh_bit1==1 and seventh_bit2==1 and seventh_bit3==0:#the space is the current character
            fnd.append((j,cur))
        elif seventh_bit1==1 and seventh_bit3==1 and seventh_bit2==0:#the space is the previous character
            fnd.append((j,prev))
        elif seventh_bit3==1 and seventh_bit2==1 and seventh_bit1==0:#the space is the next character
            fnd.append((j,nxt))
        elif seventh_bit1==1 and seventh_bit2==1 and seventh_bit3==1:#The 3 characters are spaces, choose any one of them
            fnd.append((j,prev))
        
#print(fnd)
unique_dict = {}
for item in fnd:
    key = item[0]
    if key not in unique_dict:
        unique_dict[key] = item

fnd = list(unique_dict.values())

#print(fnd)

for j in range(29):
    for item in fnd:
        if item[0]==j:
            key=int(item[1],2)^int('00100000',2)
            for i in range(6):
        
                plain_txt[i][j]=chr(int(cipherB[i][j],2)^key)
        else:
            pass
        

#####################################
            
#Guessing the remaining characters
#And Using strt function to give us estimations of the words to speedup the process
for i in range(6):
    k3=int('01010001',2)
    plain_txt[i][2]=chr(int(cipherB[i][2],2)^k3)
    k1=int('11001010',2)
    plain_txt[i][0]=chr(int(cipherB[i][0],2)^k1)
    k16=int('01111100',2)
    plain_txt[i][16]=chr(int(cipherB[i][16],2)^k16)
    k17=int('11011011',2)
    plain_txt[i][17]=chr(int(cipherB[i][17],2)^k17)
    letters=['t','i','c','a','t','i','o','n']
    k=21
    for l in letters:
        ascii_value=ord(l)
        binary_value=bin(ascii_value)[2:].zfill(8)
        
        key=int(binary_value,2)^int(cipherB[1][k],2)
        
        plain_txt[i][k]=chr(int(cipherB[i][k],2)^key)
        k+=1
    letters=['v','e','r']
    k2=8
    for l in letters:
        ascii_value=ord(l)
        binary_value=bin(ascii_value)[2:].zfill(8)
        
        key=int(binary_value,2)^int(cipherB[0][k2],2)
        
        plain_txt[i][k2]=chr(int(cipherB[i][k2],2)^key)
        k2+=1
    k12=int('01101001',2)
    plain_txt[i][12]=chr(int(cipherB[i][12],2)^k12)  


pln2=list(map(lambda x: "".join(x),plain_txt))
##########################################################
#uncomment this part if you want to use this function to select the column of the words you want to guess
#strt is the sentences


#strt=[]
#for i in pln2:
#    strt=i.split()
 #   if strt[1]:
 #       print(strt[1])
#        print(srh(strt[1]))
    




for i in pln2:
    print(i)




#nltk.download('words')
