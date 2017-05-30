# encoding: utf-8

import functools

import MeCab
import twkorean

_preprocessor = None


class _Mecab(object):
    def __init__(self, dic_path):
        self._dic_path = dic_path
        self._tagger = MeCab.Tagger("-d {}".format(
            dic_path
        ))

    def parse(self, text):
        nodes = self._tagger.parseToNode(text)

        while nodes:
            form = nodes.surface
            pos = nodes.feature.split(",")[0]
            nodes = nodes.next

            if pos == "BOS/EOS":
                continue

            yield form, pos


class Preprocessor(object):
    def __init__(self):
        self._mecab = None
        self._twitter = None

    def _init_mecab(self):
        if self._mecab is not None:
            return

        self._mecab = _Mecab("/usr/local/lib/mecab/dic/mecab-ko-dic")

        # Run a test to sacrifice two words
        # There is a bug in mecab that makes it omit first two words.
        _ = list(self._mecab.parse("foo bar"))
        del _

    def _init_twitter(self):
        if self._twitter is not None:
            return

        self._twitter = twkorean.TwitterKoreanProcessor()

    def normalize(self, text):
        """Normalize a text using open-korean-text.
        
        Arguments:
            text: text string.
            
        Returns:
            Normalized text string.
        """
        self._init_twitter()

        return self._twitter.normalize(text)

    def sent_tokenize(self, text, residual=True):
        """Tokenize a bulk of text into list of sentences (using Mecab-ko).
        
        Arguments:
            text: text string.
            residual: whether to include an incomplete sentence at the end of
                the text.
        Returns:
            Generator that generates a list of sentence strings in their 
            original forms.
        """
        self._init_mecab()

        index = 0

        for f, pos in self._mecab.parse(text):
            index = text.find(f, index)
            index += len(f)

            if pos == "SF":
                sent = text[:index].strip()

                yield sent

                text = text[index:]
                index = 0

        if residual and index > 0:
            sent = text.strip()

            yield sent

    def word_tokenize(self, text, pos=False):
        """Tokenize a sentence into word tokens (using Mecab-ko).
        
        Arguments:
            text: sentence string.
            pos: whether to include part-of-speech tags.
            
        Returns:
            If pos is False, then a list generator of word strings is returned. 
            Otherwise, a list generator of word and pos tuples is returned.
        """
        self._init_mecab()

        if pos:
            for item in self._mecab.parse(text):
                yield item
        else:
            for f, _ in self._mecab.parse(text):
                yield f

    def sent_word_tokenize(self, text, residual=True, pos=False):
        """Tokenize a bulk of text into list of sentences (using Mecab-ko).
        
        Each sentence is a list of words. This is slightly more efficient than
        tokenizing text into sents and words in succession.
        
        Arguments:
            text: text string.
            residual: whether to include an incomplete sentence at the end of
                the text.
            pos: whether to include part-of-speech tag.
        Returns:
            If pos is False, then a list generator of word lists is returned. 
            Otherwise, a list generator of word and pos tuples list is returned.
        """
        self._init_mecab()

        sent = []

        for f, p in self._mecab.parse(text):
            if pos:
                sent.append((f, p))
            else:
                sent.append(f)

            if p == "SF":
                yield sent
                sent = []

        if residual and sent:
            yield sent


def normalize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.normalize(text, *args, **kwargs)


def sent_tokenize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.sent_tokenize(text, *args, **kwargs)


def word_tokenize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.word_tokenize(text, *args, **kwargs)


def sent_word_tokenize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.sent_word_tokenize(text, *args, **kwargs)


functools.update_wrapper(normalize, Preprocessor.normalize)
functools.update_wrapper(sent_tokenize, Preprocessor.sent_tokenize)
functools.update_wrapper(word_tokenize, Preprocessor.word_tokenize)
functools.update_wrapper(sent_word_tokenize, Preprocessor.sent_word_tokenize)