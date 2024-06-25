from PIL import Image

def resize_image(im, scaleFactor, oneCharWidth, oneCharHeight):
    width, height = im.size
    resized_im = im.resize(
        (int(scaleFactor * width), int(scaleFactor * height * (oneCharWidth / oneCharHeight))), 
        Image.NEAREST
    )
    return resized_im
