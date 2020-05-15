import random

def random_color():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)

def color_array(num_of_colors):
    palette = ['#0AFFAB','#2509EB','#FF3D37','#EBBA28','#2BFF33','#BDECFF','#4226EB','#FF57FA','#EB350C','#FFD791']
    colors = []
    for i in range(num_of_colors):
        if i<len(palette):
            colors.append(palette[i])
        else:
            colors.append(random_color())
    return colors