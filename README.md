---
title: Pandoc Filters for Scientific Writing
author: Michael Färber
---

This package contains several filters for [Pandoc](https://pandoc.org/)
to facilitate writing scientific texts.

Supported features are:

* Definition lists as LaTeX environments, see [](#defenv).
* Links as intra-document references, see [](#linkref).
* Tables with the `tabular` environment, see [](#tables).
* Floating code blocks with captions, see [](#listing).

To use the filters, you need `pandoc` and `python-pandocfilters`.
Run `make` to generate PDF and HTML output for this example file.


# Definition Environments {#defenv}

The `defenv` filter interprets definition lists as LaTeX environments.
The first word of the definition is the environment type.
It can be followed by a label as well as by a name.
An example with a name follows:

Definition (Tree)
: A *tree* is a tuple $(N, \rightarrow)$, where
  $N$ is a set of tree nodes and
  $\rightarrow \in N \times N$ is a cycle-free relation.

Let us now reference a theorem, namely [](#thm:inftrees).

Theorem thm:inftrees
: Let $N$ be an infinite set.
  Then there exists an infinite number of trees for $N$.

Proof
: Trivial!


# Link References {#linkref}

The `linkref` filter renders links of the shape `[](#ref)`
as intra-document references.
In LaTeX, this is rendered as `\autoref{ref}`, whereas
in HTML, this is rendered as `<a href="#ref">ref</a>`.


# Tables

The `tabular` filter renders LaTeX tables using the `tabular` package
instead of the `longtable` package used by Pandoc by default.
Unfortunately, we still have to use `\label` to reference tables.
For a more complete solution, you may consider using something like
[pandoc-tablenos](https://github.com/tomduck/pandoc-tablenos).

An example is shown in [](#tab:example).

Table: Demonstration of pipe table syntax.
  \label{tab:example}

| Right | Left | Default | Center |
|------:|:-----|---------|:------:|
|   12  |  12  |    12   |    12  |
|  123  |  123 |   123   |   123  |
|    1  |    1 |     1   |     1  |


# Code Blocks {#listing}

The `listing` filter renders Pandoc code blocks as
floating code blocks with a caption.
By default, Pandoc creates floating code blocks
only when using the `--listings` option.
However, I find the output of the `listings` package
not as aesthetically pleasing as the one from Pandoc.
This filter thus allows to obtain
the beautiful output from Pandoc within a floating code block.
An example is given in [](#hello-world).

~~~ {#hello-world .c caption="Hello World in C."}
#include <stdio.h>

int main()
{
    printf("Hello World!\n");
    return 0;
}
~~~

Notice that this filter requires some LaTeX code to create the `listing` environment.
It can be found in `header.tex`.
