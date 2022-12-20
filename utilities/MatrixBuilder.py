from PIL import Image
from numpy import array

im_1 = Image.open(r"SelectButtonAreas.png")
im_1 = im_1.resize((50, 50))
ar = array(im_1)

dct = {2: 1, 3: 2, 4: 3}


def reformat(array):
    nar = list()
    for x in range(len(array)):
        nar.append([])
        for y in range(len(array[x])):
            nar[x].append(dct.get(array[x][y], 0))
    return nar


ar = reformat(ar)
for x in range(len(ar)):
    row = ""
    for y in ar[x]:
        row += str(y)
    ar[x] = row + "\n"

n = open("../Testing/SB_heatmap.utl", "w")
n.writelines(ar)
