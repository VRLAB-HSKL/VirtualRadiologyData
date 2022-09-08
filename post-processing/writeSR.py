import re, os, pydicom
import readHTML, sendSR, extractCID

def writeSR(values):
    codes = extractCID.getcodes()
    with open("huefttepV1templ.xml", 'r') as sr:
        txt = sr.read()
    codeliste = re.findall('([\t| ]*){code\|(\d.*)\|(.*)}', txt)
    zuweisung = {}
    for elem in codeliste:
        zuweisung[elem[2]] = (elem[1], elem[0])
    for zk, zv in zuweisung.items():
        vv = values[f"{zk}"]
        for ok, ov in codes[zv[0]][2].items():
            if vv == ov[1]:
                pat = '{code\|'+zv[0]+'\|'+zk+'}'
                code = f"<code>\n"\
                f"{zv[1]}   <relationship>CONTAINS</relationship>\n"\
                f"{zv[1]}   <concept>\n"\
                f"{zv[1]}       <value>{zv[0]}</value>\n"\
                f"{zv[1]}       <scheme>\n"\
                f"{zv[1]}           <designator>{codes[zv[0]][0]}</designator>\n"\
                f"{zv[1]}       </scheme>\n"\
                f"{zv[1]}       <meaning>{codes[zv[0]][1]}</meaning>\n"\
                f"{zv[1]}   </concept>\n"\
                f"{zv[1]}   <value>{ok}</value>\n"\
                f"{zv[1]}   <scheme>\n"\
                f"{zv[1]}       <designator>{ov[0]}</designator>\n"\
                f"{zv[1]}   </scheme>\n"\
                f"{zv[1]}   <meaning>{ov[1]}</meaning>\n"\
                f"{zv[1]}</code>"
                txt = re.sub(pat, code, txt)


    for k, v in values.items():
        pat = "{"+k+"}"
        print(f"{pat}: {v}")
        txt = re.sub(pat, v, txt)
    with open("output.xml", 'w') as out:
        out.write(txt)
    os.system("xml2dsr output.xml output.dcm")
    with pydicom.dcmread("output.dcm") as ds:
        #print(ds)
        pass
    os.system("dsr2html +U8 output.dcm output.html")
    #sendSR.sendSR(ds)
