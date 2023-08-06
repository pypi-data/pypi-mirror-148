from enum import Enum

class EanType(Enum):
    EAN8 = 8
    EAN13 = 13


def isCorrectEan(possibleEan:str, eanTypeToCheck:EanType=None)-> bool:
    '''
    test if an string is ether an EAN 8 or an EAN 13
    possibleEan: string to test
    eanTypeToCheck (optional): filter to verify strictly if the string is an EAN 8 or an EAN 13 
    '''

    if not possibleEan:
        return False

    testLen = len(possibleEan)

    # check longueur
    try:
        testType=EanType(testLen)

        if eanTypeToCheck:
            if not testType == eanTypeToCheck:
                return False

        elif testLen not in [8,13]:
            return False

    except Exception:
        return False

    # check regex
    if not (possibleEan.isnumeric() and int(possibleEan) > 0):
        return False


    # control digit check
    eanDigitLess = possibleEan[0:testLen-1]
    possibleDigitCheck = possibleEan[testLen-1]
    if not possibleDigitCheck == calculateDigitCheck(eanDigitLess):
        return False
            
    return True


def calculateDigitCheck(eanDigitCheckLess:str) -> str:
    '''
    Calculate digit check of an EAN
    '''
    lenstrCalcul = len(eanDigitCheckLess)
    factor = 3
    somme = 0

    # check regex
    if not (eanDigitCheckLess.isnumeric() and int(eanDigitCheckLess) >0):
        return "KO"

    for index in range(lenstrCalcul-1,-1,-1):
        somme += int(eanDigitCheckLess[index]) * factor
        factor = 4 - factor
        
    digitCheck = str((10 - (somme % 10))%10)

    return digitCheck

