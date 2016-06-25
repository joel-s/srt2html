#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
The SRT parsing is based on a python2 script:
http://activearchives.org/wiki/Srt2html
"""

import re

#=============================================================================
# SRT PARSING

srt_timecodes = re.compile(
    r"""^
    (^
    ((?P<seq>\d+)\r?\n)?
    (?P<start> ((\d\d):)? (\d\d): (\d\d) ([,.]\d{1,3})?)
    \s* --> \s*
    (?P<end> ((\d\d):)? (\d\d): (\d\d) ([,.]\d{1,3})?)?
    \s*)
    $""",
    re.X|re.M
)

def spliterator(pattern, text):
    """
    Utility function for splitting on a "header" pattern
    Yields (match, text), where text is what's between match and the next match
    """
    lastm = None
    cur = 0
    for m in pattern.finditer(text):
        if lastm:
            yield lastm, text[cur:m.start()]
        lastm = m
        cur = m.end()
    if lastm:
        yield m, text[cur:]

#=============================================================================
# HTML GENERATION

start_html = """\
<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <title>{0}</title>
  <style>
  .main {{
    margin-top: 30px;
    max-width: 700px;
    width: 100%;
    font-family: Georgia, Times, "Times New Roman", serif;
    font-size: 24px;
    line-height: 1.5;
  }}
  .main h1 {{
    font-family: Arial, sans-serif;
    font-size:36px;
  }}
  span.mouseover {{
    border-bottom: 1px dotted #000;
  }}
  </style>
</head>

<body>
  <div class="main">
    <h1>{0}</h1>
    <p>
"""

span_html = """\
      <span class="mouseover" title="{0}">{1}</span>
"""

end_html = """\
    </p>
  </div>
</body>

</html>
"""

def make_title(fname):
    """
    Return the last subdirectory and filename joined together "like/this".
    """
    import os
    last_dir = os.path.basename(os.path.dirname(fname))
    return os.path.join(last_dir, os.path.basename(fname))

def convert_to_html(infile, outfile, title):
    """Convert SRT from <infile> to HTML in <outfile>."""
    text = infile.read()
    outfile.write(start_html.format(title))
    for m, body in spliterator(srt_timecodes, text):
        mvars = m.groupdict()
        start = mvars.get("start")
        outfile.write(span_html.format(start, body.strip()))
    outfile.write(end_html)

if __name__ == "__main__":
    import sys
    fname = sys.argv[1]
    infile = open(fname, "r")
    convert_to_html(infile, sys.stdout, make_title(fname))
