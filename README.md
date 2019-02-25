# hangul-utils

An integrated library for Korean language preprocessing.

[![Build Status][1]][2]

This simple library has following features.

 * Text Normalization: typo and error correction using `open-korean-text`.
 * Tokenization: sentence and word-level tokenizations using `Mecab-ko`.
 * Character Manipulation: splitting and combining of jamo characters (our
 own implementation)

Python 2 is no longer supported.

## Getting Started

For text normalization, [Open Korean Text](https://github.com/twitter/twitter-korean-text) is required. For tokenizations, [Mecab-ko](https://bitbucket.org/eunjeon/mecab-ko) is required.
First, run `install_mecab_ko.sh` with sudo to install Mecab-ko system-wide.

    sudo bash install_mecab_ko.sh

**Note that `LD_LIBRARY_PATH` must be set to point to `/usr/local/lib:/usr/lib`** 

The script above will set that for you temporarily, but you must set it yourself after a restart.

Then install Open Korean Text Python Wrapper by running

    bash install_twkorean.sh
    
Sudo is not required for this one.

Finally install `hangul-utils` package by cloning this repo and running

    # install from source
    python setup.py install
    
Optionally, you could install the package from pypi, but it is not recommended,
as some of the required packages install properly only when installed from git repositories.

## Text Normalization

Text normalization is necessary for reducing noises in texts collected online
or transcribed from spoken language. To this date, the only open-sourced library
that tackles the problem is [Open Korean Text](https://github.com/twitter/twitter-korean-text).

Open Korean Text's normalization function is not meant to deal with all error
cases. The source code indicates that the normalization process largely
focuses on fixing typing errors and deals less on linguistic errors itself.
The entire process consists of following procedures:

* Removal of repeating jamos that have accidently become the final (e.g. -ㅋ) of
the preceding character: 왴ㅋㅋㅋㅋ-> 왜ㅋㅋㅋㅋ
* Shortening of jamos that repeat more than twice: ㅋㅋㅋㅋㅋㅋㅋ->ㅋㅋ
* Shortening of characters that repeat more than twice: 훌쩍훌쩍훌쩍 -> 훌쩍훌쩍
* Normalization of frequently shortened words: this mainly includes three cases (-ㄴ데, -ㄴ지, -ㄴ가)
* Normalization of [tense](https://en.wikibooks.org/wiki/Korean/Alphabet) jamos: ㅆ->ㅅ, 햇는데 -> 했는데
* Space normalization: \n\n\n -> \n

Any errors or variations beyond above cases will not be normalized.

### Usages

Normalization is available as a `Preprocessor` method or as a separate function.

    >>> from hangul_utils import Preprocessor
    >>> p = Preprocessor()
    >>> p.normalize("부들부들부들부들 내가 작간데 화가낰ㅋㅋㅋㅋ")
    "부들부들 내가 작가인데 화가나ㅋㅋㅋ"

    >>> from hangul_utils import normalize
    >>> normalize("부들부들부들부들 내가 작간데 화가낰ㅋㅋㅋㅋ")
    "부들부들 내가 작가인데 화가나ㅋㅋㅋ"

## Tokenizations

Sentence and word tokenization methods are available in this library, supported
by [mecab-ko](https://bitbucket.org/eunjeon/mecab-python-0.996) as the
backend.
Twitter's Korean text library also provides part-of-speech tokenization methods,
but it generally lacks the level of robustness offered by other taggers.
For example, a common grammatical mistake people make is to not separate "할"
and "수" when describing the ability to do something. Twitter's tagger fails to
tokenize correctly in such cases:

    >>> twitter_tokenize("작가가 할수 있는일이 있지.")
    [('작가', 'Noun'),
     ('가', 'Josa'),
     ('할수', 'Verb'),
     ('있는', 'Adjective'),
     ('일이', 'Noun'),
     ('있지', 'Adjective'),
     ('.', 'Punctuation')]

However, Mecab produces more ideal results for the same sentence due to the way
it ignores spaces during part-of-speech analysis:

    >>> mecab_tokenize("작가가 할수 있는일이 있지.")
    [('작가', 'NNG'),
     ('가', 'JKS'),
     ('할', 'VV+ETM'),
     ('수', 'NNB'),
     ('있', 'VV'),
     ('는', 'ETM'),
     ('일', 'NNG'),
     ('이', 'JKS'),
     ('있', 'VA'),
     ('지', 'EF'),
     ('.', 'SF')]

Additionally, Mecab is known to be much [faster](http://konlpy.org/en/v0.4.4/morph/#comparison-between-pos-tagging-classes).

Mecab also supports `SF` part-of-speech to indicate the end of a sentence (on which
our sentence tokenizer is based) unlike Twitter's tagger that classifies all
punctutations and special symbols to a more general `Punctutation` tag.

Overall, we found that using Mecab has proven to be much more productive in
most of our cases. However, it is entirely possible that other taggers could be
more suitable for other cases. We do not claim that our experience will be the same
for others.

### Usages

Sentence tokenization:

    >>> from hangul_utils import sent_tokenize
    >>> list(sent_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다. 현 시점에서 눈에 띄는 선수가 몇몇 있다."))
    ['그러나 베네수엘라는 독일 보다 한 단계 위였다.', '현 시점에서 눈에 띄는 선수가 몇몇 있다.']

Word tokenization (mainly using space):

    >>> from hangul_utils import word_tokenize
    >>> list(word_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다."))
    ['그러나', '베네수엘라는', '독일', '보다', '한', '단계', '위였다', '.']

Morpheme tokenization:

    >>> from hangul_utils import morph_tokenize
    >>> list(morph_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다."))
    ['그러나', '베네수엘라', '는', '독일', '보다', '한', '단계', '위', '였', '다', '.']

Morpheme tokenization with POS:

    >>> from hangul_utils import morph_tokenize
    >>> list(morph_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다.", pos=True))
    [('현', 'MM'),
     ('시점', 'NNG'),
     ('에서', 'JKB'),
     ('눈', 'NNG'),
     ('에', 'JKB'),
     ('띄', 'VV'),
     ('는', 'ETM'),
     ('선수', 'NNG'),
     ('가', 'JKS'),
     ('몇몇', 'MM'),
     ('있', 'VA'),
     ('다', 'EF'),
     ('.', 'SF')]

Simultaneous sentence and word tokenization (more efficient than calling each of them in succession):

    >>> from hangul_utils import sent_word_tokenize
    >>> list(sent_word_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다. 현 시점에서 눈에 띄는 선수가 몇몇 있다."))
    [['그러나', '베네수엘라는', '독일', '보다', '한', '단계', '위였다', '.'],
    ['현', '시점에서', '눈에', '띄는', '선수가', '몇몇', '있다', '.']]

Simultaneous sentence and morpheme tokenization (more efficient than calling each of them in succession):

    >>> from hangul_utils import sent_morph_tokenize
    >>> list(sent_morph_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다. 현 시점에서 눈에 띄는 선수가 몇몇 있다."))
    [['그러나', '베네수엘라', '는', '독일', '보다', '한', '단계', '위', '였', '다', '.'],
    ['현', '시점', '에서', '눈', '에', '띄', '는', '선수', '가', '몇몇', '있', '다', '.']]

Omission of incomplete sentences:

    >>> from hangul_utils import sent_tokenize
    >>> list(sent_tokenize("그러나 베네수엘라는 독일 보다 한 단계 위였다. 현 시점에서 눈에 띄는 선수가", residual=False))
    ['그러나 베네수엘라는 독일 보다 한 단계 위였다.']

Again, these functions are also available as methods of `Preprocessor`.

## Manipulating Korean Characters

Hangul is made of basic letters called 'jamo(자모)', and thus it is an
[agglutinative language][3].
As such, a tool for splitting and joining *jamos* could come very handy when
we want to perform character-level Korean text processing. Splitting a Korean
character is quite straight-forward:
a simple algebraic formula can deduce the unicode value of individual *jamo*
([Wiki][4]). However, the tricky part
is forming a string of Hanguls from a string of *jamos*, because the consonants
can be either [initials]([5]) or
[finals]([6]), some form of backtracking
is require.

### Functions

 * `split_syllables`: converts a string of syllables to a string of jamos
 * `join_jamos`: converts a string of jamos to a string of syllables

### Usages

    >>> from hangul_utils import split_syllable_char, split_syllables,
        join_jamos
    >>> print(split_syllable_char(u"안"))
    ('ㅇ', 'ㅏ', 'ㄴ')
    
    >>> print(split_syllables(u"안녕하세요"))
    ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ
    
    >>> sentence = u"앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.우리 집
        깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라."
    >>> s = split_syllables(sentence)
    >>> print(s)
    ㅇㅏㅍ ㅈㅣㅂ ㅍㅏㅌㅈㅜㄱㅇㅡㄴ ㅂㅜㄺㅇㅡㄴ ㅍㅏㅌ ㅍㅜㅅㅍㅏㅌㅈㅜㄱㅇㅣㄱㅗ,
    ㄷㅟㅅㅈㅣㅂ ㅋㅗㅇㅈㅜㄱㅇㅡㄴ ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ.ㅇㅜㄹㅣ
    ㅈㅣㅂ ㄲㅐㅈㅜㄱㅇㅡㄴ ㄱㅓㅁㅇㅡㄴ ㄲㅐ ㄲㅐㅈㅜㄱㅇㅣㄴㄷㅔ ㅅㅏㄹㅏㅁㄷㅡㄹㅇㅡㄴ
    ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ ㄲㅐㅈㅜㄱ ㅈㅜㄱㅁㅓㄱㄱㅣㄹㅡㄹ
    ㅅㅣㅀㅇㅓㅎㅏㄷㅓㄹㅏ.
    
    >>> sentence2 = join_jamos(s)
    >>> print(sentence2)
    앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.우리 집 깨죽은 검은 깨
    깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라.
    
    >>> print(sentence == sentence2)
    True
    
  [1]: https://travis-ci.com/kaniblu/hangul-utils.svg?branch=master
  [2]: https://travis-ci.com/kaniblu/hangul-utils
  [3]: https://en.wikipedia.org/wiki/Agglutinative_language
  [4]: https://en.wikipedia.org/wiki/Korean_language_and_computers#Hangul_in_Unicode
  [5]: https://en.wikipedia.org/wiki/Hangul_consonant_and_vowel_tables#Initials
  [6]: https://en.wikipedia.org/wiki/Hangul_consonant_and_vowel_tables#Finals
