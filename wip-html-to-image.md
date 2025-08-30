Some old, incomplete, notes for generating an image somehow.

Playwright works fine based off of this example: https://www.htmltoimage.com/python/playwright/png
See to_png.py.
But the image isn't rendering in trmnl, it just shows an all white page. Not
sure why. Switching to just using the screenshot plugin to make the image from
HTML now.

Going off of: https://unix.stackexchange.com/questions/138804/how-to-transform-a-text-file-into-a-picture
Can use imagemagick like so:

    convert -size 360x360 xc:white -font "FreeMono" -pointsize 34 -fill black -gravity center -draw 'text 15,15 "hello there"' image.png ; feh image.png

But the font is fixed size. There are examples using label here which are
supposed to have fitted text, but it didn't work for me: https://imagemagick.org/Usage/text/

Someone also pointed to pango-view which is neat:

    pango-view --font=mono -qo image.png file

But it's not on a fixed width canvas. Could potentially resize it with
imagemagick, but again, not stretched to fit.

Hmm, can get a bigger canvas and align horizontally like so, but no vertical
align or text sizing:

    pango-view --font=monospace -qo image.png --align=center --height=360 --width=360 stuff.txt ; feh image.png

Hmm, I tried using
https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
but the PDF it rendered was all messed up. It printed lots of warnings about
ignored CSS directives, I think tinyhtml maybe isn't complaint with the CSS
TRMNL is using.

This person has a setup to draw images directly using pillow, cool! https://github.com/OptimumMeans/TRMNL-Chuck-Norris/blob/main/src/services/display.py
Could probably use pygame or something too.
