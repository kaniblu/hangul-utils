import sys
import argparse
import itertools

import tqdm
import map_async
from .preprocess import *
from .unicode import *


def process(args, text):
    text = text.strip()
    if args.sentencize:
        sents = sent_tokenize(text)
    else:
        sents = [text]
    new_sents = []
    for sent in sents:
        if args.normalize:
            sent = normalize(sent)
        delimiter = args.delimiter
        if args.word_tokenize:
            sent = delimiter.join(word_tokenize(sent))
        elif args.morph_tokenize:
            sent = delimiter.join(morph_tokenize(sent, pos=False))
        elif args.pos_tokenize:
            sent = delimiter.join(p for _, p in morph_tokenize(sent, pos=True))
        if args.split_syllables:
            sent = split_syllables(sent)
        elif args.join_jamos:
            sent = join_jamos(sent)
        new_sents.append(sent)
    return args.sentence_delimiter.join(new_sents)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", nargs="?")
    parser.add_argument("output_path", nargs="?")
    parser.add_argument("-P", "--progress", action="store_true", default=False,
                        help="Whether to display the progress bar using tqdm.")
    parser.add_argument("--processes", type=int, default=1,
                        help="Number of processes to utilize.")
    parser.add_argument("--skip-count", action="store_true", default=False,
                        help="If enabled, the number of lines will not be "
                             "pre-calculated before iterating the file content.")
    parser.add_argument("-d", "--delimiter", type=str, default=" ",
                        help="The delimiting character to use for splitting "
                             "text into tokens.")
    parser.add_argument("-s", "--sentencize", action="store_true",
                        default=False,
                        help="Split text into sentences, which are delimited "
                             "by sentence delimiters (default is new line).")
    parser.add_argument("--sentence-delimiter", default="\n",
                        help="Character to use for delimiting sentences.")
    parser.add_argument("-n", "--normalize", action="store_true", default=False,
                        help="Whether to perform unicode normalization.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-w", "--word-tokenize", action="store_true",
                       default=False,
                       help="Further tokenizes tokens into words.")
    group.add_argument("-m", "--morph-tokenize", action="store_true",
                       default=False,
                       help="Further tokenizes tokens into morphemes.")
    group.add_argument("-t", "--pos-tokenize", action="store_true",
                       default=False,
                       help="Further tokenizes tokens into POS tags.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--split-syllables", action="store_true",
                       default=False,
                       help="Splits syllables into jamos whenever possible.")
    group.add_argument("-j", "--join-jamos", action="store_true", default=False,
                       help="Joins jamos into syllables whenever possible.")
    args = parser.parse_args()
    num_lines = None
    if args.input_path is not None and args.progress and not args.skip_count:
        with open(args.input_path, "rb") as f:
            num_lines = sum(1 for _ in f)
    in_stream = (open(args.input_path, "r")
                 if args.input_path is not None else sys.stdin)
    out_stream = (open(args.output_path, "wb")
                  if args.output_path is not None else sys.stdout.buffer)
    desc = "processing text"
    tqdm_kwargs = dict(unit="lines", desc="processing text")
    if num_lines is not None:
        tqdm_kwargs["total"] = num_lines
    if args.processes == 1:
        it = itertools.starmap(
            process,
            tqdm.tqdm(
                iterable=zip(itertools.repeat(args), in_stream),
                disable=not args.progress, **tqdm_kwargs
            )
        )
    else:
        it = map_async.starmap_async(
            func=process,
            iterable=zip(itertools.repeat(args), in_stream),
            processes=args.processes,
            show_progress=args.progress,
            desc=desc,
            tqdm_kwargs=tqdm_kwargs
        )
    for line in it:
        out_stream.write(line.encode("utf-8", "surrogatepass"))
        out_stream.write(b"\n")


if __name__ == '__main__':
    main()
