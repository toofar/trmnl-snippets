#!/usr/bin/env python3

import sys
import argparse
import random
from subprocess import run, PIPE
from dataclasses import dataclass, field

import jinja2

# TODO:
# * save a log and read from that to make the random mode avoid repetition?
# * should I make all single line text centered? The Motivational Quotes
#   plugin is centered and that looks fine.

@dataclass(slots=True)
class Snippet:
    text: list[str] = field(default_factory=list)
    attribution: str = ""
    title: str = ""
    section: str = ""
    style: list[str] = field(default_factory=list)
    theme: list[str] = field(default_factory=list)
    enabled: bool = True

    @classmethod
    def from_lines(cls, lines, section):
        snippet = Snippet(section=section)
        for line in lines:
            if line.startswith("%"):  # directive like % key[: value]
                line = line[1:].strip()
                if line == "disabled":
                    snippet.enabled = False
                elif ":" in line:
                    key, value = line.split(":", maxsplit=1)
                    if isinstance(getattr(snippet, key), list):
                        setattr(snippet, key, value.strip().split())
                    else:
                        setattr(snippet, key, value.strip())
                else:
                    raise ValueError(f"Unknown directive '{line}'")
            elif line.startswith("//"):
                continue
            elif line.startswith("-"):
                snippet.attribution = line[1:]
            elif line.startswith("#"):
                snippet.title = line[1:].strip()
            else:
                snippet.text.append(line)

        # Assuming multi-line snippets have deliberate line breaks. Turn off
        # wrapping for them so we don't introduce new ones.
        # We might need better heuristics for this eventually, for example if
        # it's a multi-line snippet but with just a couple of really long
        # lines the text will end up really small and just taking up a little
        # bit of space in the middle of the screen.
        if len(snippet.text) > 1:
            snippet.style.append("nowrap")
        return snippet


def parse_input_file(path):
    with open(path, encoding="utf-8") as in_file:
        lines = in_file.read().splitlines()

    snippets = []
    current_paragraph = []
    in_block_comment = False
    section = ""
    for idx, line in enumerate(lines):
        if line.strip() == "<!--":
            in_block_comment = True
            continue
        elif in_block_comment:
            if line.strip() == "-->":
                in_block_comment = False
            continue
        elif not line.strip():
            snippets.append(Snippet.from_lines(current_paragraph, section))
            current_paragraph.clear()
        elif line[0] == "#" and not lines[idx + 1].strip():
            section = line[1:].strip()
        else:
            current_paragraph.append(line)
    snippets.append(Snippet.from_lines(current_paragraph, section))

    return [s for s in snippets if s.text and s.enabled]


def render_snippet(args, snippet):
    with open(args.output, "w", encoding="utf-8") as out_file:
        out_file.write(
            template.render(
                {
                    key: getattr(snippet, key)
                    for key in
                    snippet.__slots__
                }
            )
        )

def pick_snippet_with_fzf(args, snippets):
    def to_text(s):
        return "\n".join(
            s.text + [f"-{s.attribution}"]
        )

    args = "fzf --read0 --gap --highlight-line".split()
    input_text = [to_text(s) for s in snippets]
    fzf = run(args, stdout=PIPE, text=True, input="\0".join(input_text))
    fzf.check_returncode()
    if not fzf.stdout:
        sys.exit(0)

    chosen = "\n".join(fzf.stdout.splitlines())
    return [
        s
        for s in snippets
        if to_text(s) == chosen
    ][0]


selection_methods = {
    "random": lambda args, snippets: random.choice(snippets),
    "index": lambda args, snippets: snippets[args.index],
    "fzf": pick_snippet_with_fzf,
}

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file to draw text from")
parser.add_argument("-i", "--index", help="Index of snippet to render")
parser.add_argument(
    "-o",
    "--output",
    help="Path to write rendered HTML to",
    default="out.html",
)
parser.add_argument(
    "-m",
    "--method",
    choices=selection_methods.keys(),
    help="Method used to choose a snippet",
    default="random",
)


if __name__ == '__main__':
    args = parser.parse_args()
    snippets = parse_input_file(args.file)

    template_fie = "base.j2"
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("."),
    )
    template = env.get_template("base.j2")

    method = args.method
    if args.index:
        method = "index"
    snippet = selection_methods[method](args, snippets)

    render_snippet(args, snippet)
