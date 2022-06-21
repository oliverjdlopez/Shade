This is my chess engine written in python, named Shade.

Currently the engine is headless, and meant to be run in a shell.
I'm working on a GUI, and will hopefully have that up and running soon. 

Shade uses pychess, a library for move generation and validation. While this 
library provides all of the functionality that an engine might need, it was written
with GUIs in mind. As a consequence, node generation is about 50x slower then competitive engines.
My own speed tests show that pychess runs at about 100k NPS, while competitive engines
on similar hardware run at about 5000k NPS. 


