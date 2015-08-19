

def parse_settings(filename):
    if(len(filename) <= 0):
        return None
    out = {}
    with open(filename) as fp:
        for line in fp:
            splits = line.split("=")
            out[splits[0]] = "=".join(splits[1:]).strip()
    return out
