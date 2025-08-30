Summary:

* goal: generate simple text screens for trmnl
* read input text file, pick a paragraph, render it
* generating HTML and using trmnl screenshot plugin to display it


Notes:

Basing HTML off of this starter: https://docs.usetrmnl.com/go/private-plugins/templates

Variations I want:

* left justified so the right hand side of poems look jagged
* no/smaller title
* title and label at top and bottom of page to give content more space
* preserve leading whitespace for weird poem formatting?

Markdown metadata formats: https://stackoverflow.com/questions/44215896/markdown-metadata-format
I'm thinking yaml front matter for top level styles (eg everything under an
H1) and % for per para directives, if needed.
