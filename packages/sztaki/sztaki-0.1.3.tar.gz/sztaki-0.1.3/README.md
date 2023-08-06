## Sztaki

### Description
This package is meant to translate Hungarian words to English or Ukrainian.


### Usage

The main entry point is **SztakiTranslator** class.
The translator will translate words and store them into SkovorodaDictionary class.

```python
from sztaki.translator import SztakiTranslator


translator = SztakiTranslator(dict_name='Stay In God\'s Love.',
                                  dict_description='Translated 4th chapter '
                                                   'of Hundatian version Stay '
                                                   'In God\'s Love',
                                  dict_language='Hungarian')
translator.translate_word_with_sztaki('világ')
print(translator.sdict.to_dict())
print(translator.not_translated_words)
```