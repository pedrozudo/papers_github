# -*- coding: utf-8 -*-
"""
    Lexers for ProbLog.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments import token

from pygments.util import guess_decode
from pygments.lexer import _encoding_map
from pygments.filter import apply_filters
from pygments.lexer import RegexLexer, bygroups, words, include
from pygments.token import (
    Text,
    Comment,
    Operator,
    Keyword,
    Name,
    String,
    Escape,
    Number,
    Punctuation,
)

__all__ = ["ProbLogLexer"]


class ProbLogLexer(RegexLexer):
    """
    Lexer for Prolog files.
    """

    name = "ProbLog"
    aliases = ["problog"]
    filenames = ["*.ecl", "*.prolog", "*.pro", "*.pl"]
    mimetypes = ["text/x-problog"]

    flags = re.UNICODE | re.MULTILINE

    def predicates_callback(lexer, match):
        print("predicates_callback")
        print(match)
        # print(match.group(0), 0),
        # print(match.group(1), 1)
        # print(match.group(2), 2)
        # print(match.group(3), 3)

        if match.group(1) in lexer.random_variables:
            token = Punctuation
        else:
            token =Punctuation

        return bygroups(token, Text, Punctuation)(lexer, match)

    def atoms_callback(lexer, match):

        print("atoms_callback")
        print(match)
        if match.group(0) in lexer.random_variables:
            token = Punctuation
        else:
            token = Punctuation

        yield match.start(0), token, match.group(0)

    def atoms_callback_bang(lexer, match):
        print("atoms_callback_bang")
        print(match)
        if match.group(0) in lexer.random_variables:
            token = Punctuation
        else:
            token = Punctuation

        yield match.start(0), token, match.group(0)

    tokens = {
        "root": [
            (r"/\*", Comment.Multiline, "nested-comment"),
            (r"%.*", Comment.Single),
            # character literal
            (r"\@(.*?)\@", Escape),
            include("comparison_builtins"),
            include("operators"),
            (r"0\'.", String.Char),
            include("numbers"),
            include("builtins"),
            include("inspection"),
            include("punctuation"),
            (
                r'"(?:\\x[0-9a-fA-F]+\\|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8}|'
                r'\\[0-7]+\\|\\["\nabcefnrstv]|[^\\"])*"',
                String.Double,
            ),
            (r"'(?:''|[^'])*'", Punctuation),  # quoted atom
            (r"_", Name.Variable),  # The don't-care variable
            include("distributions"),
            # (r'([a-z]+)(:)', bygroups(Name.Namespace, Punctuation)), no fucking idea what this thing is doing here
            # (u'([a-z\u00c0-\u1fff\u3040-\ud7ff\ue000-\uffef]'
            #  u'[\\w$\u00c0-\u1fff\u3040-\ud7ff\ue000-\uffef]*)'
            #  u'(\\s*)(:-|-->)',
            #  bygroups(Name.Function, Text, Operator)),  # function defn
            (
                u"([a-z\u00c0-\u1fff\u3040-\ud7ff\ue000-\uffef]"
                u"[\\w$\u00c0-\u1fff\u3040-\ud7ff\ue000-\uffef]*)"
                u"(\\s*)(\\()",
                # predicates_callback,
                bygroups(Punctuation, Text, Punctuation),
            ),
            (
                u"[a-z\u00c0-\u1fff\u3040-\ud7ff\ue000-\uffef]"
                u"[\\w$\u00c0-\u1fff\u3040-\ud7ff\ue000-\uffef]*",
                # atoms_callback,
                Punctuation,
            ),  # atom, characters
            # This one includes !
            (
                u"[#&*+\\-./:<=>?@\\\\^~\u00a1-\u00bf\u2010-\u303f]+",
                Punctuation,
                # atoms_callback_bang,
            ),  # atom, graphics
            (r"[A-Z_]\w*", Name.Variable),
            (u"\\s+|[\u2000-\u200f\ufff0-\ufffe\uffef]", Text),
        ],
        "numbers": [
            (r"0b[01]+", Number.Bin),
            (r"0o[0-7]+", Number.Oct),
            (r"0x[0-9a-fA-F]+", Number.Hex),
            # literal with prepended base
            (r"\d\d?\'[a-zA-Z0-9]+", Number.Integer),
            (r"(\d+\.\d*|\d*\.\d+)([eE][+-]?[0-9]+)?", Number.Float),
            (r"\d+", Number.Integer),
        ],
        "punctuation": [
            ("'", Punctuation),
            (r"[\[\](){}|.,;!]", Punctuation),
            (r"[\[\](){}|::]", Punctuation),
            (r"[\[\](){}|~]", Punctuation),
            (r"[\[\](){}|:-]", Punctuation),
            (r":-|-->", Punctuation),
            (r"\\\+", Punctuation),
        ],
        "inspection": [
            (
                words(
                    (
                        "integer",
                        "real",
                        "symbol",
                        "compound",
                        "number",
                        "atom",
                        "distribution",
                        "random_variable",
                        "random_number",
                        "vector",
                        "matrix",
                        "arithmetic",
                    ),
                    prefix=r"(?<!\.)",
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
        ],
        "comparison_builtins": [
            (r"(<|>|=<|>=|==|=:=|=\\\=|=|/|//|\*|\+|-|\\\+)", Name.Punctuation),
        ],
        "builtins": [
            (
                words(
                    (
                        "measurable",
                        "dimension",
                        "comparison",
                        "eq",
                        "neq",
                        "lt",
                        "le",
                        "gt",
                        "ge",
                        "query",
                        "query_density",
                        "query_distribution",
                        "evidence",
                        "observation",
                        "transpose",
                        "rv",
                        "holds",
                        "test",
                        "map",
                        "rv",
                        "sample",
                        "samples",
			"delta_interval",
                    ),
                    prefix=r"(?<!\.)",
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
        ],
        "operators": [
            # Needs to not be followed by an atom.
            # (r'=(?=\s|[a-zA-Z\[])', Operator),
            (r"is\b", Name.Builtin),
            (
                r"(<|>|=<|>=|==|=:=|=\\\=|=|/|//|\*|\+|-|\\\+)(?=\s|[a-zA-Z0-9\[])",
                Name.Punctuation,
            ),
            (r"(mod|div|not)\b", Operator),
        ],
        "distributions": [
            (
                words(
                    (
                        "dist",
                        "normal",
                        "poisson",
                        "uniform",
                        "delta",
                        "beta",
                        "flip",
                        "discrete",
                        "finite",
                        "normal2D",
                    ),
                    prefix=r"(?<!\.)",
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
        ],
        "nested-comment": [
            (r"\*/", Comment.Multiline, "#pop"),
            (r"/\*", Comment.Multiline, "#push"),
            (r"[^*/]+", Comment.Multiline),
            (r"[*/]", Comment.Multiline),
        ],
    }

    def analyse_text(text):
        return ":-" in text

    def get_tokens(self, text, unfiltered=False):
        """
        Return an iterable of (tokentype, value) pairs generated from
        `text`. If `unfiltered` is set to `True`, the filtering mechanism
        is bypassed even if filters are defined.
        Also preprocess the text, \ie expand tabs and strip it if
        wanted and applies registered filters.
        """

        variables = text.split(".")
        variables = [v for v in variables if "~" in v]
        variables = [v.split("~")[0].strip("\n").strip(" ") for v in variables]
        random_variables = []
        for v in variables:
            if "(" in v:
                random_variables.append(v.split("(")[0])
            else:
                random_variables.append(v)
        self.random_variables = tuple(random_variables)

        if not isinstance(text, str):
            if self.encoding == "guess":
                text, _ = guess_decode(text)
            elif self.encoding == "chardet":
                try:
                    import chardet
                except ImportError as e:
                    raise ImportError(
                        "To enable chardet encoding guessing, "
                        "please install the chardet library "
                        "from http://chardet.feedparser.org/"
                    ) from e
                # check for BOM first
                decoded = None
                for bom, encoding in _encoding_map:
                    if text.startswith(bom):
                        decoded = text[len(bom) :].decode(encoding, "replace")
                        break
                # no BOM found, so use chardet
                if decoded is None:
                    enc = chardet.detect(text[:1024])  # Guess using first 1KB
                    decoded = text.decode(enc.get("encoding") or "utf-8", "replace")
                text = decoded
            else:
                text = text.decode(self.encoding)
                if text.startswith("\ufeff"):
                    text = text[len("\ufeff") :]
        else:
            if text.startswith("\ufeff"):
                text = text[len("\ufeff") :]

        # text now *is* a unicode string
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        if self.stripall:
            text = text.strip()
        elif self.stripnl:
            text = text.strip("\n")
        if self.tabsize > 0:
            text = text.expandtabs(self.tabsize)
        if self.ensurenl and not text.endswith("\n"):
            text += "\n"

        def streamer():
            for _, t, v in self.get_tokens_unprocessed(text):
                yield t, v

        stream = streamer()
        if not unfiltered:
            stream = apply_filters(stream, self.filters, self)
        return stream
