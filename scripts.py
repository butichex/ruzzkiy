from random import choice

SYMBOLS = "QAZWSXEDCRFVTGBYHNUJMIKOLP1234567890"

def generate_promocode(): 
    promocode = ""
    for i in range(6): 
        promocode += choice(SYMBOLS)
    return promocode
        
    
    