# -*- coding: utf-8 -*-
"""
Replaces the mathjax version used in markdeep.js from version 2.x.x to the
latest version 3, which is still under development but consists of some
changes to syntax (eg. in \color). The script also replaces the mathjax custom
commands with my own, but is easily customisable through the code.

The markdeep.js file essentially contains one large function which is executed,
so it is not possible to change its functionality without replacing the entire
function entirely. The following script simply replaces the local MATHJAX_CONFIG
and MATHJAX_URL variables using regex.

Additional notes:
    + If you're looking to configure window.MathJax, it is not possible here as
      MATHJAX_CONFIG is added after the MathJax script. I can't be bothered to
      modify the js file myself but you can add a <script> tag to the beginning
      of your .md.html file to load it instead.
    + The BOM mark required for emacs is not preserved when editing/downloading
      markdeep.js
"""

import re
import requests

def get_markdeep_latest() -> str:
    """Gets the latest version of markdeep as a string.
    """
    return requests.get("https://morgan3d.github.io/markdeep/latest/markdeep.js").text

def new_config(matchobj:re.Match) -> str:
    """Returns the new_config string using a list of new commands (NC =
    \newcommand). matchobj required as the function will be used in re.sub.
    """
    new_commands = [
        r"NC{\up}[1]{\mathrm{#1}}",
        r"NC{\italic}[1]{\mathit{#1}}",
        r"NC{\bold}[1]{\mathbf{#1}}",
        r"NC{\bolditalic}[1]{\boldsymbol{#1}}",
        r"NC{\struck}[1]{\mathbb{#1}}",
        r"NC{\call}[1]{\mathcal{#1}}",
        r"NC{\script}[1]{\mathscr{#1}}",
        r"NC{\gothic}[1]{\mathfrak{#1}}",
        r"NC{\round}[1]{\mathsf{#1}}",
        r"NC{\mono}[1]{\mathtt{#1}}",
        r"NC{\brackets}[1]{\left[#1\right]}",
        r"NC{\paren}[1]{\left(#1\right)}",
        r"NC{\curls}[1]{\left\{#1\right\}}",
        r"NC{\verts}[1]{\left\lvert#1\right\rvert}",
        r"NC{\groups}[1]{\left\lgroup#1\right\rgroup}",
        r"NC{\pointy}[1]{\left\langle#1\right\rangle}",
        r"NC{\floor}[1]{\left\lfloor#1\right\rfloor}",
        r"NC{\ceiling}[1]{\left\lceil#1\right\rceil}",
        r"NC{\d}{\mathrm{d}}",
        r"NC{\deg}{{^{\large\circ}}}",
        r"NC{\transpose}{\mathsf{T}}",
        r"NC{\reynolds}{\mathcal{R}\!e}",
        r"NC{\vectori}{\hat{\boldsymbol{\imath}}}",
        r"NC{\vectorj}{\hat{\boldsymbol{\jmath}}}",
        r"NC{\vectork}{\hat{\boldsymbol{\kappa}}}",
        r"NC{\vectore}{\hat{\boldsymbol{e}}}",
        r"NC{\fun}[1]{\operatorname{#1}}",
        r"NC{\funct}[1]{\operatorname*{#1}}",
        r"NC{\double}[2]{\genfrac..{0}{0}{#1}{#2}}",
        r"NC{\boxed}[1]{\bbox[4px, border:1px solid black]{#1}}",
        r"NC{\csch}{\operatorname{csch}}",
        r"NC{\sech}{\operatorname{sech}}",
        r"NC{\arsinh}{\operatorname{arsinh}}",
        r"NC{\arcosh}{\operatorname{arcosh}}",
        r"NC{\artanh}{\operatorname{artanh}}",
        r"NC{\arcsch}{\operatorname{arcsch}}",
        r"NC{\arsech}{\operatorname{arsech}}",
        r"NC{\artanh}{\operatorname{artanh}}",
        r"NC{\varoint}{\mathop{\vcenter{\mathchoice{\huge\unicode{x222E}\,}{\unicode{x222E}}{\unicode{x222E}}{\unicode{x222E}}}\,}\nolimits}",
        r"NC{\varoiint}{\mathop{\vcenter{\mathchoice{\huge\unicode{x222F}\,}{\unicode{x222F}}{\unicode{x222F}}{\unicode{x222F}}}\,}\nolimits}",
        r"NC{\varoiiint}{\mathop{\vcenter{\mathchoice{\huge\unicode{x2230}\,}{\unicode{x2230}}{\unicode{x2230}}{\unicode{x2230}}}\,}\nolimits}",
    ]
    # now requires concat and \ -> \\ for escaping in javascript, which
    # requires repl having 8 backslashes since python needs escaping as well
    commands_string = "".join([re.sub(r"\\", "\\\\\\\\", entry) for entry in new_commands])
    return """var MATHJAX_CONFIG ='<span style="display:none">' + '$$""" +\
           commands_string + r"$$\n'.rp(/NC/g, '\\newcommand') + '</span>\n';"

def mathjax2to3(filename:str = None) -> None:
    """Replaces the MATHJAX_CONFIG and MATHJAX_URL variables.
    """
    if filename is None:
        text = get_markdeep_latest()
    else:
        with open(filename, mode="r", encoding="utf-8") as f:
            text = f.read()
    
    # slightly awkward as there is a semicolon within quotes, so i have
    # to match two
    text = re.sub(r"var MATHJAX_CONFIG ?=[\w\W]*?;[\w\W]*?;", new_config, text)
    
    new_url = "var MATHJAX_URL ='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js';"
    text = re.sub(r"var MATHJAX_URL ?=[\w\W]*?;", new_url, text)
    
    with open("markdeep.js", mode="w", encoding="utf-8") as s:
        s.write(text)

if __name__ == "__main__":
    mathjax2to3("markdeep.js")