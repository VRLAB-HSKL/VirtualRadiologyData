import re, os, pydicom
from postprocessing import sendSR, extractCID

def writeSR(values):
    codes = extractCID.getcodes()
    with open("./output/output.xml", 'r', encoding='utf-8') as sr:
        txt = sr.read()
    codeliste = re.findall('([\t ]*){code\|([\d_]+)\|(\w+)}', txt)
    zuweisung = {}
    for elem in codeliste:
        zuweisung[elem[2]] = (elem[1], elem[0])
    for zk, zv in zuweisung.items():
        vv = values[f"{zk}"]
        for ok, ov in codes[zv[0]].items():
            if vv.upper() == ov[1].upper():
                pat = '{code\|'+zv[0]+'\|'+zk+'}'
                code = f"<value>{ok}</value>\n"\
                f"{zv[1]}<scheme>\n"\
                f"{zv[1]}   <designator>{ov[0]}</designator>\n"\
                f"{zv[1]}</scheme>\n"\
                f"{zv[1]}<meaning>{ov[1]}</meaning>"
                txt = re.sub(pat, code, txt)


    for k, v in values.items():
        if "date" in k:
            v = v.replace('-', '')
        pat = "{"+k+"}"
        txt = re.sub(pat, v, txt)
    with open("./output/output.xml", 'w', encoding='utf-8') as out:
        out.write(txt)
    os.system("xml2dsr ./output/output.xml ./output/output.dcm")
    with pydicom.dcmread("./output/output.dcm") as ds:
        pass
    os.system("dsr2html +U8 ./output/output.dcm ./output/output.html")
    sendSR.sendSR(ds)
