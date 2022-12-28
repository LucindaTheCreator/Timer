

def build_utl(filename):
    file = open(filename, "r")
    lines = list(file.readlines())
    for x in range(len(lines)):
        if not x == len(lines) - 1:
            lines[x] = [int(i) for i in lines[x][:-1]]
        else:
            last = lines[x].replace("\n", "")
            lines[-1] = [int(i) for i in last]
    return lines


def CheckAreaOnUtl(utl, wdg, mp):
    print()
    scalars = (wdg.size[0] / len(utl[0]), wdg.size[1] / len(utl))
    r_pos = (int((mp[0] - wdg.pos[0]) / scalars[0]), int((wdg.size[1] - (mp[1] - wdg.pos[1])) / scalars[1]))
    return utl[r_pos[1]][r_pos[0]]
