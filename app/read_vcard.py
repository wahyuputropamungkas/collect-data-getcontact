import os
import re

def readVcf(filename):
    contacts = []

    with open(os.path.join('./contacts', filename), 'r') as f:
        lines = f.read().replace("\n", '|')

        splitCard = lines.split('END:VCARD')

        if len(splitCard) > 0:
            for line in splitCard:
                currentContact = {}
                currentContact['name'] = None
                currentContact['cell'] = None

                for number in line.split('|'):
                    if number.startswith('FN'):
                        lineFN = number.split(':')
                        contactName = '?'

                        if len(lineFN) == 2:
                            contactName = lineFN[1]

                        currentContact['name'] = contactName.replace(' ', '_').replace('-', '_').replace('.', '').replace(',', '').lower()

                    if number.startswith('TEL'):
                        lineTEL = number.split(';')

                        if len(lineTEL) > 0:
                            if lineTEL[1].startswith('CELL') or lineTEL[1].startswith('X-Ponsel') or lineTEL[1].startswith(''):
                                lineCELL = lineTEL[1].split(':')

                                if len(lineCELL) > 0:
                                    currentContact['cell'] = re.sub('[^\d\.]', '', lineCELL[1])

                contacts.append(currentContact)

    return contacts

def getContacts():
    contacts = []

    for vcf in os.listdir('./contacts'):
        if vcf.endswith('.vcf'):
            currentVcf = readVcf(vcf)

            contacts.append(currentVcf)

    return contacts

getContacts()