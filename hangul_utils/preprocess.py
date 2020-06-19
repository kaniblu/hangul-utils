__all__ = ["Preprocessor", "normalize", "word_tokenize", "sent_tokenize",
           "morph_tokenize", "sent_word_tokenize", "sent_morph_tokenize"]

import functools

_preprocessor = None


class _Mecab(object):
    def __init__(self, dic_path):
        try:
            import MeCab
        except ImportError:
            raise ImportError("could not import `MeCab`; make sure that "
                              "`mecab-python` is installed by running "
                              "`install_mceab_ko.sh` in the repository. ")
        self._dic_path = dic_path
        self._tagger = MeCab.Tagger("-d {}".format(
            dic_path
        ))

    def parse(self, text):
        nodes = self._tagger.parseToNode(text)

        while nodes:
            form = nodes.surface.strip()
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
        self._mecab = _Mecab("/usr/local/lib/mecab/dic/mecab-ko-dic")

        # Run a test to sacrifice two words
        # There is a bug in mecab that makes it omit first two words.
        try:
            _ = list(self._mecab.parse("mecab mecab"))
            del _
        except UnicodeDecodeError:
            pass

    def _init_twitter(self):
        try:
            import twkorean
        except ImportError:
            raise ImportError("could not import `twkorean`; make sure that "
                              "the package is installed by running "
                              "`install_twkorean.sh` in the repository. ")
        self._twitter = twkorean.TwitterKoreanProcessor()

    def normalize(self, text):
        """Normalize a text using open-korean-text.
        
        Arguments:
            text: text string.
            
        Returns:
            Normalized text string.
        """
        if self._twitter is None:
            self._init_twitter()

        return self._twitter.normalize(text)

    def word_tokenize(self, text):
        """Tokenize a text into space-separated words.
          
        This is the most basic form of tokenization, where we do not wish to
        analyze morphology of each individual word. 
        
        Arguments:
            text: text string.
            
        Returns:
            Generator for a list of space-tokenized words.
        """
        if self._mecab is None:
            self._init_mecab()

        tokens = text.split()
        tokens_it = iter(tokens)

        try:
            token = next(tokens_it)
            index = 0

            for f, pos in self._mecab.parse(text):

                if index >= len(token):
                    if token:
                        yield token

                    token = next(tokens_it)
                    index = 0

                # token_f = token[index:index + len(f)]
                # if token_f != f:
                #     print(token, index, token_f, f)

                if pos.startswith("S"):
                    if index:
                        t, token = token[:index], token[index:]

                        if t:
                            yield t

                        index = 0

                    t, token = token[index:index + len(f)], token[
                                                            index + len(f):]

                    if t:
                        yield t

                    index = 0
                else:
                    index += len(f)

            if token and index:
                yield token[:index]

        except StopIteration:
            pass

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

    def morph_tokenize(self, text, pos=False):
        """Tokenize a sentence into morpheme tokens (using Mecab-ko).
        
        Arguments:
            text: sentence string.
            pos: whether to include part-of-speech tags.
            
        Returns:
            If pos is False, then a generator of morphemes is returned. 
            Otherwise, a generator of morpheme and pos tuples is returned.
        """
        self._init_mecab()

        if pos:
            for item in self._mecab.parse(text):
                yield item
        else:
            for f, _ in self._mecab.parse(text):
                yield f

    def sent_morph_tokenize(self, text, residual=True, pos=False):
        """Tokenize a bulk of text into list of sentences (using Mecab-ko).

        Each sentence is a list of morphemes. This is slightly more efficient than
        tokenizing text into sents and morphemes in succession.

        Arguments:
            text: text string.
            residual: whether to include an incomplete sentence at the end of
                the text.
            pos: whether to include part-of-speech tag.
        Returns:
            If pos is False, then a generator of morphemes list is returned. 
            Otherwise, a generator of morpheme and pos tuples list is returned.
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

    def sent_word_tokenize(self, text, residual=True):
        """Tokenize a bulk of text into list of sentences (using Mecab-ko).

        Each sentence is a list of words. This is slightly more efficient than
        tokenizing text into sents and words in succession.

        Arguments:
            text: text string.
            residual: whether to include an incomplete sentence at the end of
                the text.
        Returns:
            A generator of words list. 
        """
        self._init_mecab()

        sent = []
        tokens = text.split()
        tokens_it = iter(tokens)

        try:
            token = next(tokens_it)
            index = 0
            yield_sent = False

            for f, pos in self._mecab.parse(text):

                if index >= len(token):
                    if token:
                        sent.append(token)

                    token = next(tokens_it)
                    index = 0

                    if yield_sent:
                        yield sent
                        yield_sent = False
                        sent = []

                # assert token[index:index + len(f)] == f

                if pos.startswith("S"):
                    if index:
                        t, token = token[:index], token[index:]

                        if t:
                            sent.append(t)

                        index = 0

                    t, token = token[index:index + len(f)], token[
                                                            index + len(f):]

                    if t:
                        sent.append(t)

                    index = 0

                    if pos == "SF":
                        yield_sent = True
                else:
                    index += len(f)

            if token and index:
                sent.append(token[:index])

            if sent and (yield_sent or residual):
                yield sent

        except StopIteration:
            pass


def normalize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.normalize(text, *args, **kwargs)


def morph_tokenize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.morph_tokenize(text, *args, **kwargs)


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


def sent_morph_tokenize(text, *args, **kwargs):
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = Preprocessor()

    return _preprocessor.sent_morph_tokenize(text, *args, **kwargs)


functools.update_wrapper(normalize, Preprocessor.normalize)
functools.update_wrapper(sent_tokenize, Preprocessor.sent_tokenize)
functools.update_wrapper(morph_tokenize, Preprocessor.morph_tokenize)
functools.update_wrapper(word_tokenize, Preprocessor.word_tokenize)
functools.update_wrapper(sent_word_tokenize, Preprocessor.sent_word_tokenize)
functools.update_wrapper(sent_morph_tokenize, Preprocessor.sent_morph_tokenize)
