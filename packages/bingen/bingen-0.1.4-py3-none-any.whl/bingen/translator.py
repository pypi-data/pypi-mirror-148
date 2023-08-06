import re
from typing import List

from googletrans import Translator

from bingen.models import Translation, WordMetadata, SkovorodaDict
from bingen.stardict.processor import build_de_dict


def prepare_word_test(word:WordMetadata):
    test_str = "".join([tr.translation.strip() for tr in word.translations])
    foreign_word = word.foreign_word
    # Removes foreign word occurrence in translation
    test_str = test_str.replace('\n', ' ')
    test_str = test_str.replace(foreign_word, '~')
    # Removes transcript in translation
    match = re.search('\[.*\]', test_str)
    if match:
        test_str_beginning = test_str[:match.start()]
        test_str_ending = test_str[match.end()-1:]
        test_str = test_str_beginning + test_str_ending
    word.test = test_str[:251]


def translate(tokens: List[str]) -> SkovorodaDict:
    dicts = build_de_dict()
    not_translated_counter = 0
    sk_dict = SkovorodaDict(name='Bleib in Gottes Liebe Kap.4',
                            description='Bleib in Gottes Liebe. Kapitel 4. '
                                        'Autorität respektieren.',
                            language='German')
    for token in tokens:
        translation = dicts[0].get_dict_by_word(token)
        if translation:

            translation = translation[0].get('x')
            translation = str(translation, encoding='utf8')
            result = re.search('<k>\w.*</k>', translation)
            start, end = result.span()
            token = translation[start: end].strip('<k>').strip('</k>')
            translation = translation[end:]
            translation = translation.strip()
            translation = _translate_ua(translation)
            translation = Translation(translation=translation)
            token = WordMetadata(foreign_word=token)
            token.translations.append(translation)
            prepare_word_test(token)
            sk_dict.words.append(token)
        else:
            not_translated_counter += 1
    return sk_dict, not_translated_counter


def _translate_ua(text):
    translator = Translator()
    translation =  translator.translate(text, dest='uk', src='ru')
    text = translation.text
    if 'посл.' in text:
        text = text.replace('посл.', 'присл.')
    if 'кому-л.' in text:
        text = text.replace('кому-л.', 'кому-н.')
    if 'високий.' in text:
        text = text.replace('високий.', 'піднес.')
    return text


if __name__ == '__main__':
    tokens = ['Liebe']
    sk_dict, not_translated_counter = translate(tokens)
    print(f'Not translated: {not_translated_counter}')
    print(sk_dict.to_dict())
