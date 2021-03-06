from PIL import Image
from os import path
import imghdr
import random
import json

def encodeVigenere(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

def decodeVigenere(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

def getRGBBytes(pixels, width, height):
    zeros = []
    ones = []
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for i in range(3):
                if pixel[i] % 2 == 1:
                    ones.append((x, y, i))
                else:
                    zeros.append((x, y, i))

    return [zeros, ones]

def extractFromList(myList, n):
    return random.sample(myList,n)

def strToBinary(string):
  byteArray = bytearray(string, "utf-8")
  byteList = []

  for byte in byteArray:
      binaryRepresentation = format(byte, '#010b')[2:]
      byteList.append(binaryRepresentation)

  return ''.join(byteList)

def binaryToStr(binMsg):
  n = int('0b'+binMsg,2)
  return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def encodeMessage(image, message):
  binaryMessage = strToBinary(message)
  width, height = image.size

  if len(binaryMessage) > width*height*3:
    return "NU MERGE"

  pixels = image.load()
  tple = getRGBBytes(pixels, width, height)
  onesCount = binaryMessage.count('1')
  zerosCount = binaryMessage.count('0')

  diffZero = zerosCount - len(tple[0])
  diffOne = onesCount - len(tple[1])
  if diffOne > 0:
      zerosCount += diffOne
      onesCount = len(tple[1])
  elif diffZero > 0:
      onesCount += diffZero
      zerosCount = len(tple[0])

  zerosList = extractFromList(tple[0], zerosCount)
  onesList = extractFromList(tple[1], onesCount)
  finalList = []

  for i in range (len(binaryMessage)):
        if int(binaryMessage[i]) == 0:
            if diffZero > 0:
                pixel = onesList[onesCount - 1]
                aux = list(pixels[pixel[0], pixel[1]])
                if aux[pixel[2]] < 255:
                    aux[pixel[2]] += 1
                else:
                    aux[pixel[2]] = 254
                pixels[pixel[0], pixel[1]] = tuple(aux)
                finalList.append(pixel)
                onesCount -= 1
                diffZero -= 1
            else:
                finalList.append(zerosList[zerosCount - 1])
                zerosCount -= 1
        else:
            if diffOne > 0:
                pixel = zerosList[zerosCount - 1]
                aux = list(pixels[pixel[0], pixel[1]])
                aux[pixel[2]] += 1
                pixels[pixel[0], pixel[1]] = tuple(aux)
                finalList.append(pixel)
                zerosCount -= 1
                diffOne -= 1
            else:
                finalList.append(onesList[onesCount - 1])
                onesCount -= 1

  return image, finalList

def decodeImg(image, finalList):
  pixels = image.load()
  message = ''

  for i in range(len(finalList)):
      RGBValue = pixels[finalList[i][0], finalList[i][1]][finalList[i][2]]
      message += ''.join(str(RGBValue % 2))

  return binaryToStr(message)

def checkFormat(imagePath):
  imgFormat = imghdr.what(imagePath)
  if imgFormat not in ['png', 'jpg', 'jpeg']:
    return False
  return True

def readPath():
  usrPth = input("Path to image: ")
  while not path.exists(usrPth) or not checkFormat(usrPth):
    if not path.exists(usrPth):
      usrPth = input("Enter a valid path: ")
    else:
      usrPth = input("Enter a valid image file: ")
  return usrPth

def readMessage():
  usrMsg = input("Message to encode: ")
  while len(usrMsg) < 1:
    usrMsg = input("Message to encode can't be empty: ")
  return usrMsg

def readKey():
  usrKy = input("Key you got after encoding: ")
  while len(usrKy) < 1:
    usrKy = input("Key you got after encoding can't be empty: ")
  return usrKy

def readPassword():
  usrPsswrd = input("Password to use to encode: ")
  while len(usrPsswrd) < 1:
    usrPsswrd = input("Password to use to encode can't be empty: ")
  return usrPsswrd

def printMenu():
  print('1. Encode')
  print('2. Decode')
  print('3. Exit')

def doEncoding():
  userPath = readPath()
  userMessage = readMessage()
  userPassword = readPassword()
  img = Image.open(userPath)
  updatedImage, finalList = encodeMessage(img, userMessage)
  updatedImage.save("C:/Chestii/Scoala/untitled/result.png", "PNG")
  file = open('key.txt', 'w+', encoding="utf-16")
  file.write(encodeVigenere(userPassword, json.dumps(finalList)))
  file.close()
  print("Saved in F:/Scoala/untitled/ as `result.png`")
  print("Your key is in the key.txt file")
  print("To be able to decode your message, save the key file and remember the password you used for encoding.")

def doDecoding():
  userPath = readPath()
  userPassword = readPassword()
  userKey = readKey()
  img = Image.open(userPath)
  finalList = decodeVigenere(userPassword, userKey)
  print("The encoded message was: " + decodeImg(img, json.loads(finalList)))

def doExit():
  print("Thank you for using this")

if __name__ == "__main__":
  print('Steganography')
  while True:
    printMenu()
    userInput = input("Your Choice: ")

    if userInput == '1':
      doEncoding()
    elif userInput == '2':
      doDecoding()
    elif userInput == '3':
      doExit()
      break