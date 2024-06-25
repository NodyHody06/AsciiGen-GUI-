from PIL import Image, ImageDraw
import GetCharacter as GC

def mapping(im, width, height, font, txt_file, oneCharWidth, oneCharHeight, interval, charArray):
    pix = im.load()
    imageOutput = Image.new('RGB', (oneCharWidth * width, oneCharHeight * height), color=(0, 0, 0))
    d = ImageDraw.Draw(imageOutput)

    for i in range(height):
        for j in range(width):
            r, g, b = pix[j, i]
            gray = int((r + g + b) / 3)
            pix[j, i] = (gray, gray, gray)
            char = GC.getChar(gray, interval, charArray)
            txt_file.write(char)
            #if someone wants color use -> (fill = (r, g, b))
            d.text((j * oneCharWidth, i * oneCharHeight), char, font=font, fill=(255, 255, 255))
        txt_file.write('\n')

    return imageOutput
