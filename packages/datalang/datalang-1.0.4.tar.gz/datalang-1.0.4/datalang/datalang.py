import re

arrayRe = re.compile('(?<=\[)(.*)(?=\])')
dictionaryRe = re.compile('(?<=\A)(.*)(?=:\Z)')
dictionaryNameRe = re.compile('(?<=-\s)(.*)(?=:)')
valueRe = re.compile('(?<=:\s)(.*)(?=\Z)')
variableNameRe = re.compile('(?<=\s)(.*)(?=:\s.*)')

def load(code):
    code = code.strip().split('\n')
    dataCode = {}
    lastVariable = ''

    for line in code:
        if dictionaryRe.search(line):
            lastVariable = dictionaryRe.findall(line)[0]
            dataCode[lastVariable] = {}

        elif dictionaryNameRe.search(line):
            variable = dictionaryNameRe.findall(line)[0]
            dataCode[lastVariable][variable] = valueRe.findall(line)[0]

        elif variableNameRe.search(line):
            variable = variableNameRe.findall(line)[0]

            if line.startswith('int'):
                value = int(valueRe.findall(line)[0])

            elif line.startswith('str'):
                value = str(valueRe.findall(line)[0])

            elif line.startswith('arr'):
                value = str(valueRe.findall(line)[0])
                value = re.sub('\[|\]', '', value).split(', ')

            dataCode[variable] = value

    return dataCode

def loadFile(fileObject):
    with open(fileObject) as fileObject:
        loaded = load(fileObject.read())

    return loaded

def dump(dictionary):
    datalang = ''

    for key in dictionary:
        keyValue = dictionary.get(key)

        if isinstance(keyValue, (str, int)):
            valueType = str(type(keyValue))[8:11]
            datalang += f'{valueType} {key}: {keyValue}\n'

        elif isinstance(keyValue, list):
            datalang += f"arr {key}: [{', '.join(map(str, keyValue))}]\n"

        elif isinstance(keyValue, dict):
            datalang += key + ':\n'
            for dictKey in keyValue:
                datalang += f'- {dictKey}: {keyValue.get(dictKey)}\n'

        datalang += '\n'

    return datalang