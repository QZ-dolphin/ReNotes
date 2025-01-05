from PIL import Image

file_path = "./pics/1.png"

image = Image.open(file_path)

image.save("favicon.ico", format="ICO", size=(32, 32))
