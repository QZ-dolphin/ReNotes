from PIL import Image

file_path = "./pics/Shooting-Star-Dragon.jpg"

image = Image.open(file_path)

image.save("output.ico", format="ICO", size=(32, 32))
