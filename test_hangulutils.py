# encoding: UTF-8

from __future__ import unicode_literals

import six
import random

from hangul_utils import *

CHAR = "안"
SENT = "앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽. " \
       "우리 집 깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 " \
       "죽먹기를 싫어하더라."

SENT_SPLIT = "ㅇㅏㅍ ㅈㅣㅂ ㅍㅏㅌㅈㅜㄱㅇㅡㄴ ㅂㅜㄺㅇㅡㄴ ㅍㅏㅌ " \
            "ㅍㅜㅅㅍㅏㅌㅈㅜㄱㅇㅣㄱㅗ, ㄷㅟㅅㅈㅣㅂ ㅋㅗㅇㅈㅜㄱㅇㅡㄴ " \
            "ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ. ㅇㅜㄹㅣ ㅈㅣㅂ " \
            "ㄲㅐㅈㅜㄱㅇㅡㄴ ㄱㅓㅁㅇㅡㄴ ㄲㅐ ㄲㅐㅈㅜㄱㅇㅣㄴㄷㅔ " \
            "ㅅㅏㄹㅏㅁㄷㅡㄹㅇㅡㄴ ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ " \
            "ㅋㅗㅇㅈㅜㄱ ㄲㅐㅈㅜㄱ ㅈㅜㄱㅁㅓㄱㄱㅣㄹㅡㄹ " \
            "ㅅㅣㅀㅇㅓㅎㅏㄷㅓㄹㅏ."


def generate(n):
    StringIO = six.StringIO
    s = StringIO()

    for i in range(n):
        s.write(random.choice(INITIALS + MEDIALS + FINALS))

    return s.getvalue()


def test_split_char():
    r = split_syllable_char(u"안")
    assert r == tuple(u"ㅇㅏㄴ")


def test_split_str():
    r = split_syllables(u"안녕하세요")
    assert r == u"ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"


def test_split_str_long():
    r = split_syllables(SENT)
    assert r == SENT_SPLIT


def test_join_char():
    r = split_syllable_char(CHAR)
    assert join_jamos_char(*r) == CHAR


def test_join_str():
    r = split_syllables(SENT)
    r = join_jamos(r)

    assert r == SENT


def test_join_random():
    for i in range(100):
        print(join_jamos(generate(20)))
