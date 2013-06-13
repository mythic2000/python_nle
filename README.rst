======
README
======

Now developed and hosted on bitbucket: https://bitbucket.org/singerb/python_nle.

Overview
--------

Why should code always be presented linearly? There's no reason it can't be shown in a more logical fashion, and re-arranged to help the user understand the code flow. This set of tools generates an HTML page for a Python file showing all the functions/methods in that file in draggable blocks.

Requirements
------------

Install these via virtualenv; ``pygments, tornado``.

Description
-----------

The tools works in the following steps:

#. Parse the supplied file via Python's built-in ast module.
#. Walk the ast node tree with a visitor, finding all functions/methods and associated line numbers.
#. Convert the function bodies into syntax highlighted HTML blocks via pygments.
#. Combine a tornado template, base style sheet, the pygments style sheet, and the styled function HTML blocks into a single HTML file.
#. The tornado template HTML contains the jQuery UI code to make each block draggable.

Further Directions
------------------

- Make the code interactive via some sort of HTML-based editor
- Handle multiple files
- Link call sites to definitions somehow (SVG instead of HTML?)
- Turn it into either a full web app or an embedded Webkit app to make it a real editor
