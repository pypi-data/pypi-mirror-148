## Bingen

### Description 
This package is German words to Ukrainian translator.

### Usage

```python
from bingen.translator import translate

tokens = ['Liebe']
sk_dict, not_translated_counter = translate(tokens)
print(f'Not translated: {not_translated_counter}')
print(sk_dict.to_dict())
```