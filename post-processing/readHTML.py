
from bs4 import BeautifulSoup
from datetime import datetime

def readHTML():
    values = {}
    values['PatientID'] = "000-000-002"
    values['PatientName'] = "Adam"
    values['PatientSex'] = "M"
    values['StudyDescription'] = "Visible Human Male"
    values['SeriesDescription'] = "Hip"
    values['InstanceCreationDate'] = "20050726"
    values['InstanceCreationTime'] = "102049"
    values['Date'] = datetime.now().strftime('%Y-%m-%d')
    values['Time'] = datetime.now().strftime('%H:%M:%S')
    with open("Hüftendoprothetik-bearb.html") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        textareas = soup.find_all('textarea')
        inputs = soup.find_all('input')
        selects = soup.find_all('select')
        for tag in textareas:
            tagval = tag.string if tag.string is not None else '-'
            values[f"{tag['name']}"] = tagval
        for sel in selects:
            key = sel['name']
            options = sel.find('option', selected=True)
            #print(sel)
            values[f"{key}_select"] = options.string
        for inp in inputs:
            inatr = inp.attrs
            if "value" in inatr:
                values[inp['name']] = inatr.get('value').strip()
            else:
                values[inp['name']] = '-'
    return values

if __name__ == '__main__':
    values = readHTML()
    for key, val in values.items():
        print(f"{key}: {val}")

