# Motivating example

```python
animals = [
  {
    'name': 'Wombat', 
    'avg_properties': {
      'height': {'value': 66, 'unit': 'cm'}, 
      'length':{'value': 108, 'unit': 'cm'},
      'weight': {'value': 27, 'unit': 'kg'}
    }
  },
  {
    'name': 'Duck', 
    'avg_properties': {
      'height': {'value': 62, 'unit': 'cm'}, 
      'weight': {'value': 1, 'unit': 'kg'}
    }
  },
  {
    'name': 'Dog', 
    'max_properties': {
      'height': {'value': 95, 'unit': 'cm'}, 
      'weight': {'value': 105, 'unit': 'kg'}
    }
  },
]
```

Let's query that above structure:

```python
for animal in animals:
  print(animal["name"], 
        'average length', 
        animal["avg_properties"]["length"]["value"])
```

This code will abort with error as no the `Duck` has no `length` key. We have to add one more check.

```python
for animal in animals:
  print(animal["name"], 
        'average length', 
        animal["avg_properties"]["length"]["value"] 
          if "length" in animal["avg_properties"] 
          else '-')
```

This improved code will still fail as `Dog` has only `max_property` key, we have to handle this situation too.

```python
for animal in animals:
  if "avg_properties" in animal 
      and "length" in animal["avg_properties"]:
    print(animal["name"], 
          'average length', 
          animal["avg_properties"]["length"]["value"])
  else:
    print(animal["name"], 
          'avarage length', 
          "-")
```

The above scenarios can be simplified by `quickpath`:

```python
from quickimport import getpath
for animal in animals:
  print(animal["name"], 
        'average length', 
        getpath(animal, 
                ("avg_properties", "length", "value"), 
                default='-'))
```

Alternatively, the keys can be represented as a single string:

```python
from quickimport import getpaths
for animal in animals:
  print(animal["name"], 
        'average length', 
        getpaths(animal, 
                "avg_properties.length.value"), 
                default='-'))
```

Separator can be changed to any alternative characters:

```python
from quickimport import getpaths
for animal in animals:
  print(animal["name"], 
        'average length', 
        getpaths(animal, 
                "avg_properties/length/value"), 
                default='-', 
                sep='/')
```
