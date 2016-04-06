# hangul-utils

A python library for manipulating Korean alphabets

[![Build Status](http://img.shields.io/travis/jacebrowning/template-python/master.svg)](https://github.com/kaniblu/hangul-utils)

Hangul is made of basic letters called 'jamo(자모)', and thus it is an [agglutinative language](https://en.wikipedia.org/wiki/Agglutinative_language). As such, a tool for splitting and joining *jamos* could come very handy when we want to perform character-level Korean text processing. The method for manipulating Korean alphabets at character-level is quite straight-forward, as it is apparent from the simple formula for deducing the unicode value of an agglutinated character is [quite simple](https://en.wikipedia.org/wiki/Korean_language_and_computers#Hangul_in_Unicode). However, the tricky part is when forming a string of Hanguls from a string of raw *jamos*, because some of the consonants can be either [initials](https://en.wikipedia.org/wiki/Hangul_consonant_and_vowel_tables#Initials) or [finals](https://en.wikipedia.org/wiki/Hangul_consonant_and_vowel_tables#Finals), requiring at least some form of backtracking (if you have used Korean input before, you probably know what I'm talking about). This simple library is intended to abstract away the details and help you do all the dirty work.

## Get Started

Install `hangul-utils` just like any other python projects.

    $ pip install hangul-utils

The library provides two basic functionalities.

 * `split_syllables`: converts a string of syllables to a string of jamos
 * `join_jamos`: converts a string of jamos to a string of syllables
 
## Examples

    >>> print(split_syllable_char(u"안"))
    ('ㅇ', 'ㅏ', 'ㄴ')
    
    >>> print(split_syllables(u"안녕하세요"))
    ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ
    
    >>> sentence = u"앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.우리 집 깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라."
    >>> s = split_syllables(sentence)
    >>> print(s)
    ㅇㅏㅍ ㅈㅣㅂ ㅍㅏㅌㅈㅜㄱㅇㅡㄴ ㅂㅜㄺㅇㅡㄴ ㅍㅏㅌ ㅍㅜㅅㅍㅏㅌㅈㅜㄱㅇㅣㄱㅗ, ㄷㅟㅅㅈㅣㅂ ㅋㅗㅇㅈㅜㄱㅇㅡㄴ ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ.ㅇㅜㄹㅣ ㅈㅣㅂ ㄲㅐㅈㅜㄱㅇㅡㄴ ㄱㅓㅁㅇㅡㄴ ㄲㅐ ㄲㅐㅈㅜㄱㅇㅣㄴㄷㅔ ㅅㅏㄹㅏㅁㄷㅡㄹㅇㅡㄴ ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ ㄲㅐㅈㅜㄱ ㅈㅜㄱㅁㅓㄱㄱㅣㄹㅡㄹ ㅅㅣㅀㅇㅓㅎㅏㄷㅓㄹㅏ.
    
    >>> sentence2 = join_jamos(s)
    >>> print(sentence2)
    앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.우리 집 깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라.
    
    >>> print(sentence == sentence2)
    True