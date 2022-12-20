def build_utl(filename):
    file = open(filename, "r")
    lines = list(file.readlines())
    for x in range(len(lines)):
        if not x == len(lines) - 1:
            lines[x] = [int(i) for i in lines[x][:-1]]
        else:
            lines[-1] = [int(i) for i in lines[x]]
    return lines
