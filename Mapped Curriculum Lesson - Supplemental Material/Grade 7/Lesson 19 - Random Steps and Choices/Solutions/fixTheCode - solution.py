import random
random.seed(4)
even_step = random.randrange(2, 13, 2)
colours = ["red", "blue", "gold"]
colour = random.choice(colours)
print("Move:", even_step)
print("Colour:", colour)
