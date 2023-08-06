from ..EanCheck import isCorrectEan, EanType
from ._BarcodeRendering import BarcodeRendering



setA = {
    "0":"0001101",
    "1":"0011001",
    "2":"0010011",
    "3":"0111101",
    "4":"0100011",
    "5":"0110001",
    "6":"0101111",
    "7":"0111011",
    "8":"0110111",
    "9":"0001011",
}

setB = {
    "0":"0100111",
    "1":"0110011",
    "2":"0011011",
    "3":"0100001",
    "4":"0011101",
    "5":"0111001",
    "6":"0000101",
    "7":"0010001",
    "8":"0001001",
    "9":"0010111",
}

setC = {
    "0":"1110010",
    "1":"1100110",
    "2":"1101100",
    "3":"1000010",
    "4":"1011100",
    "5":"1001110",
    "6":"1010000",
    "7":"1000100",
    "8":"1001000",
    "9":"1110100",
}


class _EanGeneratorProto:
    '''
    abstract class for Generate EAN
    '''

    eanValue:str = None
    barcodeValue:str = None
    _renderer:BarcodeRendering = None

    def __init__(self):
        pass

    def _calculateBareCodeValue(self):
        pass

    def showBarcode(self):
        self._renderer.renderInWindow(self.eanValue, self.barcodeValue)

    def saveAsSvg(self, filePath):
        self._renderer.saveAsSvg(filePath, self.barcodeValue)

    def saveAsImg(self, filePath):
        self._renderer.saveAsImg(filePath, self.barcodeValue)

class Ean13Generator(_EanGeneratorProto):
    '''
    Generate EAN 13 barcode
    '''

    def __init__(self,value:str):
        if isCorrectEan(value, EanType.EAN13):
            self.eanValue = value
            self._calculateBareCodeValue()
            self._renderer = BarcodeRendering()

        else:
            raise Exception("Invalid EAN13")


    def _calculateBareCodeValue(self):
        '''
        Calculate bits encoding barcode from ean value
        '''
        self.barcodeValue = "101"

        firstPartRaw = self.eanValue[1:7]
        secondPartRaw = self.eanValue[7:]

        prefix = self.eanValue[0]

        for index, element in enumerate(firstPartRaw):
            setToApply = self.__calculateSetFromPrefix(prefix,index)
            if setToApply == "A":
                self.barcodeValue = self.barcodeValue + setA[element]
            else:
                self.barcodeValue = self.barcodeValue + setB[element]

        self.barcodeValue = self.barcodeValue + "01010"

        for element in secondPartRaw:
            self.barcodeValue = self.barcodeValue + setC[element]

        self.barcodeValue = self.barcodeValue + "101"

    def __calculateSetFromPrefix(self, prefix:str, index:int) -> str:
        '''
        Found odd set (set A) or even set (set B) by prefix value
        '''
        if index == 0:
            return "A"

        if prefix == 0:
            return "A"

        elif prefix == "1":
            return "A" if index in [1,3] else "B"

        elif prefix == "2":
            return "A" if index in [1,4] else "B"

        elif prefix == "3":
            return "A" if index in [1,5] else "B"

        elif prefix == "4":
            return "A" if index in [2,3] else "B"

        elif prefix == "5":
            return "A" if index in [3,4] else "B"

        elif prefix == "6":
            return "A" if index in [4,5] else "B"

        elif prefix == "7":
            return "A" if index in [2,4] else "B"

        elif prefix == "8":
            return "A" if index in [2,5] else "B"

        elif prefix == "9":
            return "A" if index in [3,5] else "B"

class Ean8Generator(_EanGeneratorProto):
    '''
    Generate EAN 8 barcode
    '''

    def __init__(self,value:str):
        if isCorrectEan(value, EanType.EAN8):
            self.eanValue = value
            self._calculateBareCodeValue()
            self._renderer = BarcodeRendering()

        else:
            raise Exception("Invalid EAN8")

    def _calculateBareCodeValue(self):
        self.barcodeValue = "101"

        firstPartRaw = self.eanValue[:4]
        secondPartRaw = self.eanValue[4:]

        for element in firstPartRaw:
            self.barcodeValue = self.barcodeValue + setA[element]

        self.barcodeValue = self.barcodeValue + "01010"

        for element in secondPartRaw:
            self.barcodeValue = self.barcodeValue + setC[element]

        self.barcodeValue = self.barcodeValue + "101"
