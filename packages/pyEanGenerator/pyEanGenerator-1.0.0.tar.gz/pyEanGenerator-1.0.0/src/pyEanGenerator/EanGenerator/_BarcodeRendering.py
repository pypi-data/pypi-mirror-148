
import tkinter as tk
from tkinter import Canvas
from xml.etree import ElementTree as ET

try:
    from PIL import Image
    pillowImported = True
except:
    pillowImported = False

class BarcodeRendering:
    '''
    Class to render barcode in different ways
    '''
    width:str = 4
    height:str = 40
    color:str = "black"

    def __init__(self, width:int=4, height:int = 40, color:str="black"):
        self.width = width
        self.color = color

    
    def renderInWindow(self, eanValue:str, barcodeValue:str):
        '''
        Render barcode on tkinter window
        '''
        app = tk.Tk()
        app.title(eanValue)
        app.geometry("700x200")
        canvas = Canvas(app,width=len(barcodeValue)*10)
        canvas.pack()

        index = 10
        for el in barcodeValue:
            if el == "1":
                canvas.create_line(index, 10, index, 10 + self.height, width=self.width, fill=self.color)
            index = index + self.width

        app.mainloop()


    def saveAsSvg(self,filePath, barcodeValue:str):
        '''
        save barcode to svg file
        filePath: path to saved svg file
        '''
        initialStr = '''
        <svg version='1.1' baseProfile='full' width='700' height='200' xmlns='http://www.w3.org/2000/svg'>
        </svg>'''
        root = ET.XML(initialStr)
        barcodeZone = ET.SubElement(root,"g")
        barcodeZone.set("stroke", self.color)
        index = 10
        for el in barcodeValue:
            if el == "1":
                line = ET.SubElement(barcodeZone,"line")
                line.set("stroke-width",str(self.width))
                line.set("y1",str(10))
                line.set("x1",str(index))
                line.set("y2",str(10 + self.height))
                line.set("x2",str(index))
            index = index + self.width

        tree = ET.ElementTree(root)
        ET.register_namespace("","http://www.w3.org/2000/svg")

        tree.write(filePath, encoding="utf-8",xml_declaration=True)

    def saveAsImg(self,filePath, barcodeValue:str):
        if pillowImported:
            rowSpace = [(255,255,255) for i in range(10)]
            rowOnlyData = []
            for line in barcodeValue:
                if line == "1":
                    rowOnlyData.append((0,0,0))
                    rowOnlyData.append((0,0,0))
                    rowOnlyData.append((0,0,0))
                    rowOnlyData.append((0,0,0))
                else:
                    rowOnlyData.append((255,255,255))
                    rowOnlyData.append((255,255,255))
                    rowOnlyData.append((255,255,255))
                    rowOnlyData.append((255,255,255))

            rowWithData = []
            rowWithData.extend(rowSpace)
            rowWithData.extend(rowOnlyData)
            rowWithData.extend(rowSpace)

            lineSpace = [(255,255,255) for i in range(len(rowWithData))]

            linesSpace =[lineSpace for i in range(10)]

            imgArrayData = [rowWithData for i in range(10 + self.height)]

            imgArray = []

            imgArray.extend(linesSpace)
            imgArray.extend(imgArrayData)
            imgArray.extend(linesSpace)

            img = Image.new('RGB', [len(rowWithData),len(imgArray)], 255)
            dataImg = img.load()

            for x in range(img.size[0]):
                for y in range(img.size[1]):
                    dataImg[x,y] = imgArray[y][x]
            
            img.save(filePath)
        else:
            raise Exception("please install pillow package to generate an image")