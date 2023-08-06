# pyEanGenerator

Python package to:

- generate ean8 and ean13 barcode

````Python
from pyEanGenerator import Ean8Generator,Ean13Generator

# EAN 8

testBarCode = Ean8Generator(myEan)

## show barecode on window
testBarCode.showBarcode()

## save EAN as svg file
testBarCode.saveAsSvg("myEan.svg")

## save EAN as png file (need pillow)
testBarCode.saveAsImg("myEan.png")

# EAN 13

testBarCode = Ean13Generator(myEan)

## show barecode on window
testBarCode.showBarcode()

## save EAN as svg file
testBarCode.saveAsSvg("myEan.svg")

## save EAN as png file (need pillow)
testBarCode.saveAsImg("myEan.png")

````

- verify if a string can be an ean8 or ean13

```Python
from pyEanGenerator import isCorrectEan, EanType

# test if ean8 or ean13
isEan = isCorrectEan(myEan)

# test if ean8
isEan8 = isCorrectEan(myEan, EanType.EAN8)

# test if ean13
isEan13 = isCorrectEan(myEan, EanType.EAN13)

```

- calculate checksum digit of ean

```Python
from pyEanGenerator import calculateDigitCheck

checkSumDigit = calculateDigitCheck(myEanWithouCheckSumDigit)
```
