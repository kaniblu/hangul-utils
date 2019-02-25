import os
import sys
import argparse
import itertools
import multiprocessing.pool as mp

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
                sent = args.delimiter.join(word_tokenize(sent))
            elif args.morph_tokenize:
                sent = args.delimiter.join(morph_tokenize(sent, pos=False))
            elif args.tag_tokenize:
                sent = args.delimiter.join(p for _, p in morph_tokenize(sent, pos=True))

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
        import tqdm
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
    parser.add_argument("-I", "--input", type=str, default=None, dest="input_path",
                        help="if specified, text is load from the input path. "
                             "Otherwise, it is load from stdin.")
    parser.add_argument("-O", "--output", type=str, default=None, dest="output_path",
                        help="if specified, output is written to the output path. "
                             "Otherwise, it is written to stdout.")
    parser.add_argument("--progress", action="store_true", default=False)
    parser.add_argument("--n_processes", type=int, default=1)
    parser.add_argument("-d", "--delimiter", type=str, default=" ")
    parser.add_argument("-s", "--sent", action="store_true", default=False, dest="sent_tokenize")
    parser.add_argument("-n", "--norm", action="store_true", default=False, dest="normalize")

    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("-w", "--word", action="store_true", default=False, dest="word_tokenize")
    me_group.add_argument("-m", "--morph", action="store_true", default=False, dest="morph_tokenize")
    me_group.add_argument("-t", "--tag", action="store_true", default=False, dest="tag_tokenize",
                          help="tokenizing method is identical to `morph_tokenize`, "
                               "except that only pos tags are produced.")

    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("-p", "--split", action="store_true", default=False, dest="split_syllables")
    me_group.add_argument("-j", "--join", action="store_true", default=False, dest="join_jamos")

    args = parser.parse_args()

    try:
        os.makedirs(os.path.dirname(args.output_path))
    except:
        pass

    if args.input_path is not None:
        in_stream = open(args.input_path, "r")
    else:
        in_stream = sys.stdin

    if args.output_path is not None:
        out_stream = open(args.output_path, "w")
    else:
        out_stream = sys.stdout

    results = process_mp(in_stream, args)
    for r in results:
        out_stream.write(r)
        out_stream.write("\n")


if __name__ == '__main__':
    main()
