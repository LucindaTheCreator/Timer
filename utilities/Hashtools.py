def FormatHash(hash):
    methds = {"int": int, "str": str, "s_meth": staticmethod, "bool": bool}
    datas = hash.split(",")
    dct = dict()
    for x in datas:
        var = x.split(":")
        if var[1] == "bool":
            dc = {"False":0,"True":1}
            var[2] = dc[var[2]]
        dct[var[0]] = methds[var[1]](var[2])
    return dct

def WriteToHash(data_dict):
    n_str = ""
    for x in data_dict.items():
        n_str += f"{x[0]}:{x[1].__class__.__name__}:{x[1]}"
    Runhash = open("runhash.dat","w")
    Runhash.write(n_str)
    Runhash.close()

