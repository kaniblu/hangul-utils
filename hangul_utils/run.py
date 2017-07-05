import os
import argparse

import tqdm

from . import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    parser.add_argument("--progress", action="store_true", default=False)
    parser.add_argument("--sent_tokenize", action="store_true", default=False)
    parser.add_argument("--normalize", action="store_true", default=False)

    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("--word_tokenize", action="store_true", default=False)
    me_group.add_argument("--morph_tokenize", action="store_true", default=False)

    me_group = parser.add_mutually_exclusive_group()
    me_group.add_argument("--split_syllables", action="store_true", default=False)
    me_group.add_argument("--join_jamos", action="store_true", default=False)

    parser.add_argument("--morph_tags", action="store_true", default=False,
                        help="whether to include morphology tags "
                             "if morph_tokenize == True")

    args = parser.parse_args()

    assert os.path.exists(args.input_path)

    try:
        os.makedirs(os.path.dirname(args.output_path))
    except:
        pass

    with open(args.input_path, "r") as fi:
        with open(args.output_path, "w") as fo:
            if args.progress:
                iterator = tqdm.tqdm(fi)
            else:
                iterator = fi

            for line in iterator:
                line = line.strip()

                if args.sent_tokenize:
                    sents = sent_tokenize(line)
                else:
                    sents = [line]

                for sent in sents:
                    if args.normalize:
                        sent = normalize(sent)

                    if args.word_tokenize:
                        sent = " ".join(word_tokenize(sent))
                    elif args.morph_tokenize:
			if args.morph_tags:
	                    sent = " ".join("/".join(w) for w in morph_tokenize(sent, pos=True))
			else:
			    sent = " ".join(w for w in morph_tokenize(sent))

                    if args.split_syllables:
                        sent = split_syllables(sent)
                    elif args.join_jamos:
                        sent = join_jamos(sent)

                    fo.write(sent)
                    fo.write("\n")


if __name__ == '__main__':
    main()
