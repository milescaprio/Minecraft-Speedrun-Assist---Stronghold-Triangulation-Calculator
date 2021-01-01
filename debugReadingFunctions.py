from tkinter.filedialog import askopenfile
from PIL import Image
import mcfont
#img = Image.open(askopenfile().name, 'r');
def scaleDebugScreen(img, hudSize, monitorSize):
    if monitorSize == 1:
        #img.crop((0,23,1919,1042)).resize((1920//3 - 1, 1020//3 - 1)).show()
        imgcropped = img.crop((0,23,1920,1040))
        #imgcropped.show()
        if hudSize in [1,2,3,4]:
            imgresized = imgcropped.resize((1920//hudSize, 1017//hudSize))
            for col in range(0,1920-hudSize,hudSize):
                for row in range(0,1017-hudSize,hudSize):
                    i = imgcropped.load()
                    if i[col,row] == (221,221,221,255) or i[col,row] == (221,221,221):
                        imgresized.load()[col//hudSize, row//hudSize] = (221,221,221,255)
                        #print(col,row,"Was white.")
                    else:
                        imgresized.load()[col//hudSize, row//hudSize] = (0,0,0,255)
                        #print(col,row,"Was not white.")
            #imgresized.show()
            return imgresized
        
def readProcessedScreen(scaledimg):
    #STEP 1. FIND THE PARENTHESIS LOCATION FOR THE FACING.
    i = scaledimg.load()
    parenthesisPixelsSouth =[(178,121),(178,122),(178,123),(179,124),(179,120),(180,125),(180,119)]
    parenthesisPixelsWest =[(176,121),(176,122),(176,123),(177,124),(177,120),(178,125),(178,119)]
    parenthesisPixelsNorth =[(182,121),(182,122),(182,123),(183,124),(183,120),(184,125),(184,119)]
    parenthesisPixelsEast =[(172,121),(172,122),(172,123),(173,124),(173,120),(174,125),(174,119)]

    flag = 1
    for loc in parenthesisPixelsSouth:
        if not(i[loc] == (221,221,221,255) or i[loc] == (221,221,221)):
            flag = 0
    if flag:
        facingValueLoc = [182,119]

    flag = 1
    for loc in parenthesisPixelsWest:
        if not(i[loc] == (221,221,221,255) or i[loc] == (221,221,221)):
            flag = 0
    if flag:
        facingValueLoc = [180,119]

    flag = 1
    for loc in parenthesisPixelsNorth:
        if not(i[loc] == (221,221,221,255) or i[loc] == (221,221,221)):
            flag = 0
    if flag:
        facingValueLoc = [186,119]

    flag = 1
    for loc in parenthesisPixelsEast:
        if not(i[loc] == (221,221,221,255) or i[loc] == (221,221,221)):
            flag = 0
    if flag:
        facingValueLoc = [176,119]

    #print(facingValueLoc)
    #STEP 2. READ OUT THE PIXELS.
    #Step 2.1: facing
    facingValueString = ''
    place = 0
    while place < 6: #This is the max digits that a facing value can have: eg -150.5. Also this is an artificial for loop.
        digit = str(checkDigit(scaledimg, facingValueLoc[0], facingValueLoc[1]))
        if digit == '10':
            digit = '-'
        if digit == '12':
            digit = '.'
            place = 4 #this way it will only continue reading one more digit
        if digit != '-1':
            facingValueString+=digit
            if digit == '.':
                facingValueLoc[0] += 2
            else:
                facingValueLoc[0] += 6
        else:
            print("Unidentified debug screen readout at Facing. Halting.")
        place += 1 #increment for artificial for loop
    #print(facingValueString)
    #Step 2.2: X
    coordsLoc = [34,101]
    xValueString = ''
    yValueString = ''
    zValueString = ''
    isEndOfX = 0
    isEndOfY = 0
    isEndOfZ = 0
    while not isEndOfX:
        digit = str(checkDigit(scaledimg, coordsLoc[0], coordsLoc[1]))
        if digit == '10':
            digit = '-'
        if digit == '13':
            digit = ' '
        if digit != '-1':
            xValueString += digit
            if digit == ' ':
                coordsLoc[0] += 4
                isEndOfX = 1;
            else:
                coordsLoc[0] += 6
        else:
            print("Unidentified debug screen readout at x coords. Halting.")
            
    while not isEndOfY:
        digit = str(checkDigit(scaledimg, coordsLoc[0], coordsLoc[1]))
        if digit == '10':
            digit = '-'
        if digit == '13':
            digit = ' '
        if digit != '-1':
            yValueString += digit
            if digit == ' ':
                coordsLoc[0] += 4
                isEndOfY = 1;
            else:
                coordsLoc[0] += 6
        else:
            print("Unidentified debug screen readout at y coords. Halting.")
            
    while not isEndOfZ:
        digit = str(checkDigit(scaledimg, coordsLoc[0], coordsLoc[1]))
        if digit == '10':
            digit = '-'
        if digit == '13':
            digit = ' '
        if digit != '-1':
            zValueString += digit
            if digit == ' ':
                coordsLoc[0] += 4
                isEndOfZ = 1;
            else:
                coordsLoc[0] += 6
        else:
            print("Unidentified debug screen readout at z coords. Halting.")

    #print(xValueString,yValueString,zValueString)
    return [int(xValueString), int(zValueString), float(facingValueString)]
#172,121 EAST
#182,121 NORTH
#176,121 WEST
#178,121 SOUTH

def checkDigit(img, locCol, locRow):
    #from a certain image and top-right pixel, determine what minecraft digit it is.
    i = img.load()
    correctDigit = -1;
    for pixelDigit in mcfont.pixelList:
        flag = 1
        for row in range(7):
            for col in range(5):
                if (pixelDigit[row][col] == 1 and not(isWhite(i[locCol+col,locRow+row]))) or (pixelDigit[row][col] == 0 and isWhite(i[locCol+col,locRow+row])):
                    flag = 0
        if flag == 1:
            correctDigit = mcfont.pixelList.index(pixelDigit)
    if correctDigit == -1:
        if [isWhite(i[locCol,locRow+n]) for n in range(7)] == [0,0,0,0,0,0,1]:
            #print("Found a decimal point");
            correctDigit = 12
        if [[isWhite(i[locCol+c,locRow+n]) for n in range(7)] for c in range(3)] == [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]]:
            #print("Found a Space");
            correctDigit = 13
    #print(correctDigit)
    return correctDigit
def isWhite(rgb):
    if rgb == (221,221,221,255) or rgb == (221,221,221):
        return True
    else:
        return False
