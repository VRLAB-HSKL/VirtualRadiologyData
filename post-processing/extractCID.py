import re

def getcodes():
    codes = {}
    with open("./CID.md", 'r') as f:
        txt = f.read()
    codelist = re.findall('# CID \d.*?\((.*?), (.*?), (.*?)\).*?\n(?:.*?\n){2}((?:\| \d.*? \| .*? \| .*? \|\n)*)', txt)
    print(codelist)
    for line in codelist:
        coptions = {}
        options = re.findall('^\|\s+(.*?)\s+\|\s+(.*?)\s+\|\s+(.*?)\s+\|', line[3], re.M)
        for elem in options:
            coptions[elem[0]] = (elem[1], elem[2])
        codes[line[0]] = (line[1], line[2], coptions)
        print(options)
    return codes

if __name__ == "__main__":
    codes = getcodes()
    for key, val in codes.items():
        print(f"{key}: {val}")
