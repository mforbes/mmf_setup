try:
    import mmf_setup
    mmf_setup.nbinit()
except ImportError:
    import subprocess
    import sys
    from IPython.display import HTML, Javascript, display
    
    display(HTML(r"""<style>@import url('http://fonts.googleapis.com/css?family=Lato:700');
@import url('http://fonts.googleapis.com/css?family=Ubuntu+Mono');
@import url('http://fonts.googleapis.com/css?family=Inconsolata');

// http://typecast.com/images/uploads/modernscale.css

// html {font-size: 32pt;}

body, caption, th, td, input, textarea, select, option, legend, fieldset, h1, h2, h3, h4, h5, h6, .CodeMirror {
  font-size-adjust: 0.5;
}

// This is the containing div, so we set the base size here.
// All other elements will resize accordingly (not menus)
// Unfortunately, it does not work...
div #notebook_panel {
  font-size: 1em;
  /* 1em equivalent to 16px */
}

#notebook {
  font-size: 1.2em;
  line-height: 1.25;
  /* equivalent to 20px */
}

@media (min-width: 43.75em) {
  #notebook {
    font-size: 1.2em;
    line-height: 1.375;
    /* equivalent to 22px */
  }
}

h1 {
  font-size: 2em;
  /* 2x body copy size = 32px */
  line-height: 1.25;
  /* 45px / 36px */
}

@media (min-width: 43.75em) {
  h1 {
    font-size: 2.5em;
    /* 2.5x body copy size = 40px */
    line-height: 1.125;
  }
}

@media (min-width: 56.25em) {
  h1 {
    font-size: 3em;
    /* 3x body copy size = 48px */
    line-height: 1.05;
    /* keep to a multiple of the 20px line height and something more appropriate for display headings */
  }
}

h2 {
  font-size: 1.625em;
  /* 1.625x body copy size = 26px */
  line-height: 1.15384615;
  /* 30px / 26px */
}

@media (min-width: 43.75em) {
  h2 {
    font-size: 2em;
    /* 2x body copy size = 32px */
    line-height: 1.25;
  }
}

@media (min-width: 56.25em) {
  h2 {
    font-size: 2.25em;
    /* 2.25x body copy size = 36px */
    line-height: 1.25;
  }
}

h3 {
  font-size: 1.375em;
  /* 1.375x body copy size = 22px */
  line-height: 1.13636364;
  /* 25px / 22px */
}

@media (min-width: 43.75em) {
  h3 {
    font-size: 1.5em;
    /* 1.5x body copy size = 24px */
    line-height: 1.25;
  }
}

@media (min-width: 56.25em) {
  h3 {
    font-size: 1.75em;
    /* 1.75x body copy size = 28px */
    line-height: 1.25;
  }
}

h4 {
  font-size: 1.125em;
  /* 1.125x body copy size = 18px */
  line-height: 1.11111111;
}

@media (min-width: 43.75em) {
  h4 {
    line-height: 1.22222222;
    /* (22px / 18px */
  }
}


/* These need some adjustments */
blockquote {
  font-size: 1em;
  /* 20px / 16px */
  line-height: 1.25;
  /* 25px / 20px */
}

@media (min-width: 43.75em) {
  blockquote {
    font-size: 1em;
    /* 24px / 16px = */
    line-height: 1.45833333;
    /* 35px / 24px */
  }
}

#notebook-container {
    background-color: #fcfaf2;
}

div.text_cell_render {
    font-family: "Palatino Linotype", "Palatino", "Book Antiqua",
                 "URW Palladio L", serif;
}

.CodeMirror pre {
    font-family: Inconsolata, Consolas, monocco, monospace;
}

/* This was an attempt to make it more obvious that long lines */
/* extended to the right, but causes a problem with the left bar of trhe */
/* input areas overflowing down and obscuring the output */

/* .CodeMirror { */
/*     overflow: visible; */
/* } */

div.input_area {
    border-color: rgba(0,0,0,0.10);
    background: rbga(1,0,0,0.5);
    max-width: 48.8em; /* 80 characters instead of 100%, */
}

div.text_cell_render p {
    max-width: 45em; /* instead of 100%, */
}

h1, h2, h3, h4 {
    font-family: Lato, Verdana, sans-serif;
}

.rendered_html ol {
    list-style:decimal;
    margin: 1em 2em;
}

/* My overrrides */
div.output_subarea {
    background: rgba(0,0,0,0.02);
}

.rendered_html pre,
.rendered_html code {a
    line-height: 105%;
    font-family: Inconsolata, Consolas, monocco, monospace;
    background-color: #fcfaf2;
}

figure {
    display: inline-block;
    width: 100%;
    max-width: 45em;
}

figure img {
    align: center;
}

figure figcaption {
    text-align: center;
}

.grade {
   background-color: #66FFCC;
}
</style>"""))
    display(Javascript(r"""// MathJaX customization, custom commands etc.
console.log('Updating MathJax configuration');
MathJax.Hub.Config({
  "HTML-CSS": {
      //availableFonts: ["Neo-Euler"], preferredFont: "Neo-Euler",
      //webFont: "Neo-Euler",
      //scale: 85, // Euler is a bit big.
      mtextFontInherit: true,
      matchFontHeight: true,
      scale: 90, // STIX is a bit big.

  },
  // This is not working for some reason.
  "TeX": {
    Macros: {
        d: ["\\mathrm{d}"],
        I: ["\\mathrm{i}"],
        vect: ["\\vec{#1}", 1],
        uvect: ["\\hat{#1}", 1],
        abs: ["\\lvert#1\\rvert", 1],
        Abs: ["\\left\\lvert#1\\right\\rvert", 1],
        norm: ["\\lVert#1\\rVert", 1],
        Norm: ["\\left\\lVert#1\\right\\rVert", 1],
        ket: ["|#1\\rangle", 1],
        bra: ["\\langle#1|", 1],
        Ket: ["\\left|#1\\right\\rangle", 1],
        Bra: ["\\left\\langle#1\\right|", 1],
        braket: ["\\langle#1\\rangle", 1],
        Braket: ["\\left\\langle#1\\right\\rangle", 1],
        op: ["\\mathbf{#1}", 1],
        mat: ["\\mathbf{#1}", 1],
        pdiff: ["\\frac{\\partial^{#1} #2}{\\partial {#3}^{#1}}", 3, ""],
        diff: ["\\frac{\\d^{#1} #2}{\\d {#3}^{#1}}", 3, ""],
        ddiff: ["\\frac{\\delta^{#1} #2}{\\delta {#3}^{#1}}", 3, ""],
        floor: ["\\left\\lfloor#1\\right\\rfloor", 1],
        ceil: ["\\left\\lceil#1\\right\\rceil", 1],
        Tr: "\\mathop{\\mathrm{Tr}}\\nolimits",
        erf: "\\mathop{\\mathrm{erf}}\\nolimits",
        erfi: "\\mathop{\\mathrm{erfi}}\\nolimits",
        sech: "\\mathop{\\mathrm{sech}}\\nolimits",
        sgn: "\\mathop{\\mathrm{sgn}}\\nolimits",
        order: "\\mathop{\\mathcal{O}}\\nolimits",
        diag: "\\mathop{\\mathrm{diag}}\\nolimits",

        mylabel: ["\\label{#1}\\tag{#1}", 1],
        degree: ["^{\\circ}"],
    },
  }
});

// Jupyter.notebook.config.update({"load_extensions":{"calico-document-tools":true}});
// Jupyter.notebook.config.update({"load_extensions":{"calico-cell-tools":true}});
// Jupyter.notebook.config.update({"load_extensions":{"calico-spell-check":true}});
"""))        
    display(HTML(r"""<script id="MathJax-Element-48" type="math/tex">
\newcommand{\vect}[1]{\mathbf{#1}}
\newcommand{\uvect}[1]{\hat{#1}}
\newcommand{\abs}[1]{\lvert#1\rvert}
\newcommand{\norm}[1]{\lVert#1\rVert}
\newcommand{\I}{\mathrm{i}}
\newcommand{\ket}[1]{\left|#1\right\rangle}
\newcommand{\bra}[1]{\left\langle#1\right|}
\newcommand{\braket}[1]{\langle#1\rangle}
\newcommand{\Braket}[1]{\left\langle#1\right\rangle}
\newcommand{\op}[1]{\mathbf{#1}}
\newcommand{\mat}[1]{\mathbf{#1}}
\newcommand{\d}{\mathrm{d}}
\newcommand{\pdiff}[3][]{\frac{\partial^{#1} #2}{\partial {#3}^{#1}}}
\newcommand{\diff}[3][]{\frac{\d^{#1} #2}{\d {#3}^{#1}}}
\newcommand{\ddiff}[3][]{\frac{\delta^{#1} #2}{\delta {#3}^{#1}}}
\newcommand{\floor}[1]{\left\lfloor#1\right\rfloor}
\newcommand{\ceil}[1]{\left\lceil#1\right\rceil}
\DeclareMathOperator{\Tr}{Tr}
\DeclareMathOperator{\erf}{erf}
\DeclareMathOperator{\erfi}{erfi}
\DeclareMathOperator{\sech}{sech}
\DeclareMathOperator{\sgn}{sgn}
\DeclareMathOperator{\order}{O}
\DeclareMathOperator{\diag}{diag}

\newcommand{\mylabel}[#1]{\label{#1}\tag{#1}}
\newcommand{\degree}{\circ}
</script>
<i>
<p>This cell contains some definitions for equations and some CSS for styling the notebook.  If things look a bit strange, please try the following:

<ul>
  <li>Choose "Trust Notebook" from the "File" menu.</li>
  <li>Re-execute this cell.</li>
  <li>Reload the notebook.</li>
</ul>
</p>
</i>
"""))

    try:
        HGROOT = subprocess.check_output(['hg', 'root']).strip()
        if HGROOT not in sys.path:
            sys.path.insert(0, HGROOT)
    except subprocess.CalledProcessError:
        # Could not run hg or not in a repo.
        pass
