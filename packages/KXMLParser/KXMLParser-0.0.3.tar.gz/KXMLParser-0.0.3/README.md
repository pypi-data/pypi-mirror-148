# KXMLParser
Rest-Framework Parser Convert xml to json, including attributes

##Getting Started
#### Dependencies
You need Python 3.7 or later

You also need json and xmltodict packages available from PyPI, if you have pip just run:

```bash
pip install xmltodict
```

####Instalation

```bash
pip install KXMLParser
```

Setting parser, edit settings.py :

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'KXMLParser.parsers.XMLParser',
        
    ],
}
```



## Features
- File structure for PyPI packages
- Setup with package informations
- License example

