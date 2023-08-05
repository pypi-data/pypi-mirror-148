# Datalang
Datalang it's an easy to use language with a similar syntax to YAML.<br>
It has a fast parser!

# How-to Install
You will need **GIT** or **PIP**
```sh
pip install datalang
# Or
git clone https://github.com/zsendokame/datalang; cd datalang; python setup.py
```

# How-to Use
```python
import datalang

datalangCode = """
str string: Value
int integer: 1
arr array: [Value 1, Value 2]

dictionary:
- Variable1: Value2
- Variable2: Value3
"""

print(datalang.load(datalangCode))

""" Output
{
    'string': 'Value',
    'integer': 1,
    'array': [
        'Value 1', 'Value 2'
    ],
    'dictionary': {
        'Variable1': 'Value2',
        'Variable2': 'Value3'
    }
}
"""

datalangDict = {
    'stringVariable': 'Value',
    'integerVariable': 1,
    'arrarVariable': ['value1', 'value2']

    'dictionaryValue': {
        'variable1': 'value2',
        'variable2': 'value3'
    }
}

print(datalang.dump(datalangDict))

"""
str stringVariable: Value
int integerVariable: 1
arr arrarVariable: [value1, value2]

dictionaryValue:
- variable1: value2
- variable2: value3
"""
```