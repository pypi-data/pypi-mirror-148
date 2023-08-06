# pyModularJSON

Allows recursive loading of JSON files featuring comments.
Now uses json5 so it is a bit less picky on line terminations


Authored by Edwin Peters

## Install
`pip install pyLoadModularJson`

or

`setup.py install`

## Usage

Also check *tests* folder for a few examples

base.json:
```
// comments
{
    "param2a": 2,
    "nestedParam2a":{
	"a": "notaNumber",
	"c": "set by base"
    }
}
```

main.json:
```
// comments
{
    "configBase": ["base.json"], // parent config file name relative to this file
    "param1": 4,
    "nestedParam1":{
	"a":39,
	"b":["peee","e","new"],
	"c": "set by main"
    } 
}
```

In Python:
```
from pyLoadModularJson import loadModularJson

cfg = loadModularJson('base.json')

print(cfg)

```

Child files will overwrite attributes from base files.


See more examples in `tests`
