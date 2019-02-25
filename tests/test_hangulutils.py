# encoding: UTF-8

import io
import random

from hangul_utils import *

CHAR = "안"
SENT = "앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽. " \
       "우리 집 깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 " \
       "죽먹기를 싫어하더라."
SENT2 = "KT향 단말기의 경우 SKT 유심 인식 이력이 있어야 합니다. 주변의 SKT 사용 " \
        "고객의 유심, 혹은 가까운 SKT 매장의 유심을 고객님의 핸드폰에 꽂은 후 2-3번 " \
        "정도 껐다 킨 다음 유심을 꽂아주세요!"
SENT2_WORDS = ['KT', '향', '단말기의', '경우', 'SKT', '유심', '인식', '이력이',
               '있어야', '합니다', '.', '주변의', 'SKT', '사용', '고객의', '유심',
               ',', '혹은', '가까운', 'SKT', '매장의', '유심을', '고객님의',
               '핸드폰에', '꽂은', '후', '2', '-', '3', '번', '정도', '껐다',
               '킨', '다음', '유심을', '꽂아주세요', '!']
SENT_WORDS = [
    '앞',
    '집',
    '팥죽은',
    '붉은',
    '팥',
    '풋팥죽이고',
    ',',
    '뒷집',
    '콩죽은',
    '햇콩',
    '단콩',
    '콩죽',
    '.',
    '우리',
    '집',
    '깨죽은',
    '검은',
    '깨',
    '깨죽인데',
    '사람들은',
    '햇콩',
    '단콩',
    '콩죽',
    '깨죽',
    '죽먹기를',
    '싫어하더라',
    '.'
]
SENT_MORPHS = [
    '앞',
    '집',
    '팥죽',
    '은',
    '붉',
    '은',
    '팥',
    '풋',
    '팥죽',
    '이',
    '고',
    ',',
    '뒷집',
    '콩죽',
    '은',
    '햇',
    '콩',
    '단',
    '콩',
    '콩죽',
    '.',
    '우리',
    '집',
    '깨죽',
    '은',
    '검',
    '은',
    '깨',
    '깨죽',
    '인데',
    '사람',
    '들',
    '은',
    '햇',
    '콩',
    '단',
    '콩',
    '콩죽',
    '깨죽',
    '죽',
    '먹',
    '기',
    '를',
    '싫어하',
    '더라',
    '.'
]
SENT_MORPHS_POS = [
    ('앞', 'NNG'),
    ('집', 'NNG'),
    ('팥죽', 'NNG'),
    ('은', 'JX'),
    ('붉', 'VA'),
    ('은', 'ETM'),
    ('팥', 'NNG'),
    ('풋', 'XPN'),
    ('팥죽', 'NNG'),
    ('이', 'VCP'),
    ('고', 'EC'),
    (',', 'SC'),
    ('뒷집', 'NNG'),
    ('콩죽', 'NNG'),
    ('은', 'JX'),
    ('햇', 'VV+EP'),
    ('콩', 'NNG'),
    ('단', 'MM'),
    ('콩', 'NNG'),
    ('콩죽', 'NNG'),
    ('.', 'SF'),
    ('우리', 'NP'),
    ('집', 'NNG'),
    ('깨죽', 'NNG'),
    ('은', 'JX'),
    ('검', 'VA'),
    ('은', 'ETM'),
    ('깨', 'NNG'),
    ('깨죽', 'NNG'),
    ('인데', 'VCP+EC'),
    ('사람', 'NNG'),
    ('들', 'XSN'),
    ('은', 'JX'),
    ('햇', 'VV+EP'),
    ('콩', 'NNG'),
    ('단', 'MM'),
    ('콩', 'NNG'),
    ('콩죽', 'NNG'),
    ('깨죽', 'NNG'),
    ('죽', 'MAG'),
    ('먹', 'VV'),
    ('기', 'ETN'),
    ('를', 'JKO'),
    ('싫어하', 'VV'),
    ('더라', 'EF'),
    ('.', 'SF')
]
SENT_SENTS = [
    '앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.',
    '우리 집 깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라.'
]
SENT_SENTS_NORESIDUAL = [
    '앞 집 팥죽은 붉은 팥 풋팥죽이고, 뒷집 콩죽은 햇콩 단콩 콩죽.',
    '우리 집 깨죽은 검은 깨 깨죽인데 사람들은 햇콩 단콩 콩죽 깨죽 죽먹기를 싫어하더라.'
]
SENT_SENT_MORPHS = [
    ['앞',
     '집',
     '팥죽',
     '은',
     '붉',
     '은',
     '팥',
     '풋',
     '팥죽',
     '이',
     '고',
     ',',
     '뒷집',
     '콩죽',
     '은',
     '햇',
     '콩',
     '단',
     '콩',
     '콩죽',
     '.'],
    ['우리',
     '집',
     '깨죽',
     '은',
     '검',
     '은',
     '깨',
     '깨죽',
     '인데',
     '사람',
     '들',
     '은',
     '햇',
     '콩',
     '단',
     '콩',
     '콩죽',
     '깨죽',
     '죽',
     '먹',
     '기',
     '를',
     '싫어하',
     '더라',
     '.']
]
SENT_SENT_WORDS = [
    ['앞',
     '집',
     '팥죽은',
     '붉은',
     '팥',
     '풋팥죽이고',
     ',',
     '뒷집',
     '콩죽은',
     '햇콩',
     '단콩',
     '콩죽',
     '.'],
    ['우리',
     '집',
     '깨죽은',
     '검은',
     '깨',
     '깨죽인데',
     '사람들은',
     '햇콩',
     '단콩',
     '콩죽',
     '깨죽',
     '죽먹기를',
     '싫어하더라',
     '.']
]
SENT_SPLIT = "ㅇㅏㅍ ㅈㅣㅂ ㅍㅏㅌㅈㅜㄱㅇㅡㄴ ㅂㅜㄺㅇㅡㄴ ㅍㅏㅌ " \
             "ㅍㅜㅅㅍㅏㅌㅈㅜㄱㅇㅣㄱㅗ, ㄷㅟㅅㅈㅣㅂ ㅋㅗㅇㅈㅜㄱㅇㅡㄴ " \
             "ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ ㅋㅗㅇㅈㅜㄱ. ㅇㅜㄹㅣ ㅈㅣㅂ " \
             "ㄲㅐㅈㅜㄱㅇㅡㄴ ㄱㅓㅁㅇㅡㄴ ㄲㅐ ㄲㅐㅈㅜㄱㅇㅣㄴㄷㅔ " \
             "ㅅㅏㄹㅏㅁㄷㅡㄹㅇㅡㄴ ㅎㅐㅅㅋㅗㅇ ㄷㅏㄴㅋㅗㅇ " \
             "ㅋㅗㅇㅈㅜㄱ ㄲㅐㅈㅜㄱ ㅈㅜㄱㅁㅓㄱㄱㅣㄹㅡㄹ " \
             "ㅅㅣㅀㅇㅓㅎㅏㄷㅓㄹㅏ."


def generate(n):
    s = io.StringIO()
    for i in range(n):
        s.write(random.choice(CHAR_INITIALS + CHAR_MEDIALS + CHAR_FINALS))
    return s.getvalue()


def list_compare(l1, l2):
    return all(e1 == e2 for e1, e2 in zip(l1, l2))


def test_split_char():
    r = split_syllable_char(u"안")
    assert r == tuple("ㅇㅏㄴ")


def test_split_str():
    r = split_syllables("안녕하세요")
    assert r == "ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"


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


def test_sent_tokenize():
    ret = sent_tokenize(SENT)
    assert list_compare(ret, SENT_SENTS)

    ret = sent_tokenize(SENT, residual=False)
    assert list_compare(ret, SENT_SENTS_NORESIDUAL)


def test_word_tokenize():
    ret = word_tokenize(SENT)
    ret2 = word_tokenize(SENT2)

    assert list_compare(ret, SENT_WORDS)
    assert list_compare(ret2, SENT2_WORDS)


def test_morph_tokenize():
    ret = morph_tokenize(SENT)
    assert list_compare(ret, SENT_MORPHS)

    ret = morph_tokenize(SENT, pos=True)
    assert list_compare(ret, SENT_MORPHS_POS)


def test_sent_word_tokenize():
    ret = sent_word_tokenize(SENT)
    assert all(list_compare(a, b) for a, b in zip(ret, SENT_SENT_WORDS))


def test_sent_morph_tokenize():
    ret = sent_morph_tokenize(SENT)
    assert all(list_compare(a, b) for a, b in zip(ret, SENT_SENT_MORPHS))
