import io
import os
import binascii
import base64
from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass

"""
  TODO:
    - Take care of __init__
"""

@dataclass
class rgbColors:
  r: int
  g: int
  b: int

@dataclass
class LinePoints:
  x1: float
  y1: float
  x2: float
  y2: float

@dataclass
class EllipsePoints:
  x1: float
  y1: float
  x2: float
  y2: float

"""
We defined three data classes which we are going to use to make code easier to understand
if we need to create a line we just do line1 = LinePoints(x1, y1, x2, y2) and then call draw
and get values by calling line1.x1,... This make code way easier to update and understand
"""


class generateCaptcha:
  def __init__(self):
    self.key = "abc"


  @staticmethod
  def imageToBase64EncodedBytes(image: Image.Image) -> str:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='png')
    imgByteArr = imgByteArr.getvalue()
    return base64.b64encode(imgByteArr).decode("ascii")


  # We made wrapper for random number generation in case we want to change in future
  @staticmethod
  def generateRandomInt(start: int, end: int) -> int:
    rangeSize = start - end + 1
    rand = int(binascii.hexlify(os.urandom(32)), 16) % rangeSize + end
    return rand


  def generateNoise(self, draw: ImageDraw.ImageDraw) -> ImageDraw.ImageDraw:

    base = self.generateRandomInt(200, 600)

    x1 = self.generateRandomInt(0, 150)+base
    x2 = self.generateRandomInt(-150, 0)+base
    x3 = self.generateRandomInt(-75, 75)+base
    y1 = self.generateRandomInt(-150, 0)+base
    y2 = self.generateRandomInt(-75, 75)+base
    y3 = self.generateRandomInt(0, 150)+base


    width1 = self.generateRandomInt(1, 10)
    width2 = self.generateRandomInt(1, 10)
    width3 = self.generateRandomInt(1, 10)

    line1 = LinePoints(x1, y1, x2, y2)
    line2 = LinePoints(x2, y2, x3, y3)
    line3 = LinePoints(x3, y3, x1, y1)
    rgb1 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))
    rgb2 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))
    rgb3 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))
    self.drawLine(draw, line1, width1, rgb1)
    self.drawLine(draw, line2, width2, rgb2)
    self.drawLine(draw, line3, width3, rgb3)

    font = ImageFont.truetype('fonts/FreeSans.otf', 36)

    numb = self.generateRandomInt(0, 10000)

    rgb4 = rgbColors(self.generateRandomInt(170, 255), self.generateRandomInt(170, 255), self.generateRandomInt(170, 255))

    textSize = (x2+self.generateRandomInt(100, 150), y2+self.generateRandomInt(100, 150))

    draw.text(textSize, str(numb), font=font, fill=(rgb4.r, rgb4.g, rgb4.b))

    radius = self.generateRandomInt(50, 100)

    circleBase = self.generateRandomInt(150, 300)

    x4 = self.generateRandomInt(100, 900)
    y4 = self.generateRandomInt(100, 900)
    x5 = self.generateRandomInt(100, 900)
    y5 = self.generateRandomInt(100, 900)
    randomLinePoint = LinePoints(x4, y4, x5, y5)

    width4 = self.generateRandomInt(1, 24)
    rgb5 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))

    self.drawLine(draw, randomLinePoint, width4, rgb5)

    circle = EllipsePoints(circleBase-radius, circleBase-radius, circleBase+radius, circleBase+radius)
    self.drawEllipse(draw, circle, width2, rgb3)

    return draw

  @staticmethod
  def drawLine(draw: ImageDraw.ImageDraw, line: LinePoints, width: int, rgb: rgbColors) -> ImageDraw.ImageDraw:
    draw.line((line.x1, line.y1, line.x2, line.y2), fill=(rgb.r, rgb.g, rgb.b), width=width)

    return draw

  @staticmethod
  def drawEllipse(draw: ImageDraw.ImageDraw, ellipse: EllipsePoints, width: int, rgb: rgbColors) -> ImageDraw.ImageDraw:
    draw.ellipse((ellipse.x1, ellipse.y1, ellipse.x2, ellipse.y2), outline=(rgb.r, rgb.b, rgb.g), width=width)

    return draw

  def drawTriangle(self, draw: ImageDraw.ImageDraw) -> (int, int):
    x1 = self.generateRandomInt(0, 450)
    x2 = self.generateRandomInt(550, 800)
    x3 = self.generateRandomInt(0 , 800)
    y1 = self.generateRandomInt(0, 450)
    y2 = self.generateRandomInt(0, 450)
    y3 = self.generateRandomInt(550, 800)


    width1 = self.generateRandomInt(1, 10)
    width2 = self.generateRandomInt(1, 10)
    width3 = self.generateRandomInt(1, 10)

    line1 = LinePoints(x1, y1, x2, y2)
    line2 = LinePoints(x2, y2, x3, y3)
    line3 = LinePoints(x3, y3, x1, y1)
    rgb1 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))
    rgb2 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))
    rgb3 = rgbColors(self.generateRandomInt(0, 255), self.generateRandomInt(0, 255), self.generateRandomInt(0, 255))
    self.drawLine(draw, line1, width1, rgb1)
    self.drawLine(draw, line2, width2, rgb2)
    self.drawLine(draw, line3, width3, rgb3)

    return (x1, y1)

  def generateImage(self) -> (str, str):
    rgb = rgbColors(self.generateRandomInt(0, 150), self.generateRandomInt(0, 150), self.generateRandomInt(0, 150))
    imgSize = (self.generateRandomInt(1000, 1010), self.generateRandomInt(1000, 1010))

    img = Image.new('RGB', imgSize, color = (rgb.r, rgb.g, rgb.g))

    draw = ImageDraw.Draw(img)
    question = self.drawTriangle(draw)

    randomNoise = self.generateRandomInt(3, 6)
    for noise in range(0, randomNoise):
      self.generateNoise(draw)

    font = ImageFont.truetype('fonts/FreeSans.otf', 36)

    answer = self.generateRandomInt(0, 10000)

    rgb2 = rgbColors(self.generateRandomInt(170, 255), self.generateRandomInt(170, 255), self.generateRandomInt(170, 255))

    textSize = (question[0]+self.generateRandomInt(10, 20), question[1]+self.generateRandomInt(10, 20))

    draw.text(textSize, str(answer), font=font, fill=(rgb2.r, rgb2.g, rgb2.b))

    b64Image = self.imageToBase64EncodedBytes(img)

    return (b64Image, answer)
