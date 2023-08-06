# Works For Me

A very basic soundboard to build an atmospheric background sound, for example
for role playing games.

## Installation

Just use PyPi:

    pip install worksforme

I strongly recommend to use [metaindex](https://vonshednob.cc/metaindex/) with
the `audio` package together with `worksforme`:

    pip install metaindex[audio]

If you'd rather not, at least install
[mutagen](https://github.com/quodlibet/mutagen), otherwise even less metadata
will be available in the web interface.


## Usage

You point the soundboard to your audio libraries or library and it starts a
primitive web server at `localhost:8050`:

    worksforme ~/Music ~/that/other/music/library

That's it. Open your browser at `localhost:8050` and start playing around.


## License

MIT.
