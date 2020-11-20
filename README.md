# Authors Corpus for Machine Learning
Bart Massey

This directory contains the public-domain text of four novels from
[Project Gutenberg](http://gutenberg.org).

* Mary Wollstonecraft Shelley: Frankenstein, The First Man
* Jane Austen: Pride and Prejudice, Northanger Abbey

The original text as downloaded is in the `orig/`
directory. The `hacked/` directory contains the novels with
front and back matter manually removed. The `.txt` files in
this directory have been processed from the "hacked" files
using the Python program `paragraphs.py` found here, purging
them of header and footer material, proper names, and other
irrelevant information, as well as cleaned up some
formatting irregularities.

The program `vocab.py` found here assembles a dictionary of
words from these novels and reports on their statistics.
