import string
def IsKey(Key):
     return ((Key[0] in string.ascii_uppercase) and ((int(Key[1:]) < 100) and (int(Key[1:]) > 0)) )

def NextKey(Key,PrevKey):
    
    PrevKeyNum = int(PrevKey[1:])
    PrevKeyLetter = PrevKey[0]
    
    KeyNum = int(Key[1:])
    KeyLetter = Key[0]
    
    Result = False
    # either same letter, one more
    if(KeyLetter == PrevKeyLetter and KeyNum == PrevKeyNum + 1):
        Result = True
 
    if( (string.ascii_uppercase.index(KeyLetter) == string.ascii_uppercase.index(PrevKeyLetter) + 1) and KeyNum == 1):
        Result = True
    
    return Result
    #or different letter 1
    
    