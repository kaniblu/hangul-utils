import os
import argparse
import itertools
import multiprocessing.pool as mp

import tqdm

from hangul_utils import *


def process(texts):
    global args

    ret = []

    for idx, text in texts:
        text = text.strip()

        if args.sent_tokenize:
            sents = sent_tokenize(text)
        else:
            sents = [text]

        for sent in sents:
            if args.normalize:
                sent = normalize(sent)

            if args.word_tokenize:
                sent = " ".join(word_tokenize(sent))
            elif args.morph_tokenize:
                if args.morph_tags:
                    sent = " ".join(
                        "/".join(w) for w in morph_tokenize(sent, pos=True))
                else:
                    sent = " ".join(w for w in morph_tokenize(sent))
            elif args.tag_tokenize:
                sent = " ".join(w[1] for w in morph_tokenize(sent, pos=True))

            if args.split_syllables:
                sent = split_syllables(sent)
            elif args.join_jamos:
                sent = join_jamos(sent)

            ret.append((idx, sent))

    return ret


def mp_initialize(options):
    global args
    args = options


def chunks(it, n, k):
    buffer = [[] for _ in range(n)]
    buf_it = iter(itertools.cycle(buffer))

    for item in it:
        buf_item = next(buf_it)

        if len(buf_item) == k:
            yield buffer
            buffer = [[] for _ in range(n)]
            buf_it = iter(itertools.cycle(buffer))
            buf_item = next(buf_it)

        buf_item.append(item)

    if all(buffer):
        yield buffer


def process_mp(texts, args, pool=None):
    if pool is None:
        pool = mp.Pool(args.n_processes,
                       initializer=mp_initialize,
                       initargs=(args, ))

    iterator = chunks(enumerate(texts),
                      n=args.n_processes,
                      k=args.n_processes * 1000)

    if args.progress:
        t = tqdm.tqdm()
    else:
        t = None

    results = []

    for batches in iterator:
        n_items = sum(len(x) for x in batches)

        result = pool.map_async(process, batches)
        result = result.get()
        result = [i for batch in result for i in batch]
        result.sort(key=lambda x: x[0])

        idx, result = zip(*result)
        results.extend(result)

        if args.progress:
            t.update(n_items)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--progress", action="store_true", default=False)
    parser.add_argument("--n_processes", type=int, default=1)
    parser.add_argument("--sent_tokenize", action="store_true", default=False)
    parser.add_argument("--normalize", action="store_true", default=False)

    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("--word_tokenize", action="store_true", default=False)
    me_group.add_argument("--morph_tokenize", action="store_true", default=False)
    me_group.add_argument("--tag_tokenize", action="store_true", default=False,
                          help="tokenizing method is identical to `morph_tokenize`, "
                               "except that only pos tags are used.")

    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("--split_syllables", action="store_true", default=False)
    me_group.add_argument("--join_jamos", action="store_true", default=False)

    parser.add_argument("--morph_tags", action="store_true", default=False,
                        help="whether to include morphology tags (delimited by /)"
                             "if morph_tokenize == True")

    args = parser.parse_args()

    assert os.path.exists(args.input_path)

    try:
        os.makedirs(os.path.dirname(args.output_path))
    except:
        pass

    with open(args.input_path, "r") as f:
        results = process_mp(f, args)

    with open(args.output_path, "w") as f:
        for r in results:
            f.write(r)
            f.write("\n")


if __name__ == '__main__':
    main()
