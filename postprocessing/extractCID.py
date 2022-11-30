import re

def getcodes(cidpath="./postprocessing/CID.md"):
    codes = {}
    with open(cidpath, 'r', encoding='utf-8') as f:
        txt = f.read()
    codelist = re.findall('# CID (\d.*?)\n(?:.*?\n){2}((?:\| \d.*? \| .*? \| .*? \|\n)*)', txt)
    for line in codelist:
        coptions = {}
        options = re.findall('^\|\s+(.*?)\s+\|\s+(.*?)\s+\|\s+(.*?)\s+\|', line[1], re.M)
        print(options)
        for elem in options:
            coptions[elem[0]] = (elem[1], elem[2])
        codes[line[0]] = coptions
    return codes

if __name__ == "__main__":
    codes = getcodes(cidpath="./test.md")
    for key, val in codes.items():
        print(f"{key}: {val}")
    print(codes)