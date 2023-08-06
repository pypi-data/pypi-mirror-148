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
Example
```xml
<?xml version="1.0" encoding="UTF-8"?>
<pessoas>
    <pessoa codigo="1" nome="Fulano" telefone="2222-2222">
        <endereco>
            <rua>Rua Marfim</rua>
            <numero>1</numero>
            <cidade>Ouro Preto</cidade>
            <cep>35400-000</cep>
        </endereco>
    </pessoa>
    <pessoa codigo="2" nome="Beltrano" telefone="3333-3333">
            <endereco>
            <rua>Rua Marfim</rua>
            <numero>2</numero>
            <cidade>Ouro Preto</cidade>
            <cep>35400-000</cep>
        </endereco>
    </pessoa>
    <pessoa codigo="1" nome="Ciclano" telefone="4444-4444">
            <endereco>
            <rua>Rua Marfim</rua>
            <numero>3</numero>
            <cidade>Ouro Preto</cidade>
            <cep>35400-000</cep>
        </endereco>
    </pessoa>
</pessoas>
```
Result
```json
{
    "pessoas": {
        "pessoa": [
            {
                "@codigo": "1",
                "@nome": "Fulano",
                "@telefone": "2222-2222",
                "endereco": {
                    "rua": "Rua Marfim",
                    "numero": "1",
                    "cidade": "Ouro Preto",
                    "cep": "35400-000"
                }
            },
            {
                "@codigo": "2",
                "@nome": "Beltrano",
                "@telefone": "3333-3333",
                "endereco": {
                    "rua": "Rua Marfim",
                    "numero": "2",
                    "cidade": "Ouro Preto",
                    "cep": "35400-000"
                }
            },
            {
                "@codigo": "1",
                "@nome": "Ciclano",
                "@telefone": "4444-4444",
                "endereco": {
                    "rua": "Rua Marfim",
                    "numero": "3",
                    "cidade": "Ouro Preto",
                    "cep": "35400-000"
                }
            }
        ]
    }
}
```

## Features
- File structure for PyPI packages
- Setup with package informations
- License example

