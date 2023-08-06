"""Main commandline entry point"""
import argparse
import logging
import traceback
import json
import mimetypes
import hashlib
from pathlib import Path

import bottle

try:
    import metaindex
except ImportError:
    metaindex = None

if metaindex is None:
    try:
        import mutagen
    except ImportError:
        mutagen = None

from worksforme import version


FILES = {}
SETS = {}
TEMPLATE_PATH = Path(__file__).resolve().parent / 'templates'


class Sound:
    """A sound"""
    def __init__(self, filepath, soundid, mimetype=None):
        self.file = filepath
        self.mimetype = mimetype or \
                        mimetypes.guess_type(self.file, strict=False)
        self.titles = [self.file.stem]
        self.length = "0:00"
        self.albums = []
        self.tags = []
        self.soundid = soundid

    def as_dict(self):
        """The plain dictionary representation of the sound"""
        return {'titles': self.titles,
                'id': self.soundid,
                'tags': self.tags,
                'filename': self.file.stem,
                'length': self.length,
                'albums': self.albums,
                'search': ' '.join([v.lower()
                                    for v in self.titles + self.tags +
                                             self.albums + [self.file.stem]])}


def run():
    """Main entry point to run the soundboard"""
    args = parse_args()
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s")
    logging.getLogger().setLevel(args.log_level.upper())

    if len(FILES) == 0:
        load_files(args.paths)
        load_sets(args.set_file)

    bottle.route('/', ('GET',), callback=handle_index)
    bottle.route('/save', ('POST',), callback=handle_post)
    bottle.route('/sound/<soundid:re:[a-z0-9]+>',
                 'GET', callback=handle_sound)
    bottle.route('/<filename:re:[a-z0-9]+\\.(js|css|json|ico)>',
                 'GET', callback=handle_static)

    try:
        bottle.run(host=args.host,
                   port=args.port,
                   reloader=args.log_level == 'debug')
    except KeyboardInterrupt:
        logging.info("Shutting down")
    except Exception as exc:
        callstack = ''.join(traceback.format_tb(exc.__traceback__))
        logging.fatal("Unexpected exception: %s\n%s", exc, callstack)

    save_sets(args.set_file)


def load_sets(setfile):
    """Load pre-defined sets"""
    setfile = Path(setfile).expanduser().resolve()

    if not setfile.is_file():
        logging.info("Set file %s not found. Ignoring it", setfile)
        return

    SETS.clear()
    try:
        SETS.update(json.loads(setfile.read_text("utf-8")))
    except ValueError as exc:
        logging.error("Failed to read set file %s: %s", setfile, exc)


def save_sets(setfile):
    """Write the sets to file"""
    setfile = Path(setfile).expanduser().resolve()

    try:
        setfile.write_text(json.dumps(SETS), "utf-8")
    except (ValueError, OSError) as exc:
        logging.error("Failed to write set file %s: %s", setfile, exc)


def load_files(basepaths):
    """Find and load all sound files"""
    queue = [Path(p).expanduser().resolve() for p in basepaths]
    candidates = set()

    logging.debug("Searching through %s", queue)
    while len(queue) > 0:
        path = queue.pop(0)

        for item in path.iterdir():
            if item.is_dir():
                queue.append(item)
                continue

            mimetype, _ = mimetypes.guess_type(item, strict=False)
            if mimetype is None:
                logging.debug("Unknon mimetype for %s", item)
                continue
            if mimetype.startswith('audio/'):
                candidates.add(item)

    logging.debug("Found %s candidates", len(candidates))

    mi_config = None
    if metaindex is not None:
        mi_config = metaindex.Configuration()
        mi_config.load_addons()
        mi_config.load_mimetypes()

    for soundfile in candidates:
        soundid = hashlib.md5(bytes(str(soundfile), 'utf-8')).hexdigest()
        mimetype = None
        titles = [soundfile.stem]
        tags = []
        albums = []
        length = ''

        if mi_config is not None and metaindex is not None:
            results = metaindex.index_files([soundfile], mi_config)
            result = results[0]
            if not result.success:
                logging.warning("Could not index %s", soundfile)
                continue
            metadata = result.info
            mimetype = str(metadata['mimetype'][0])
            titles = [str(t) for t in metadata['extra.title'] +
                                      metadata['id3.title']]
            tags = [str(t) for t in metadata['extra.tags'] +
                                    metadata['extra.subject'] +
                                    metadata['id3.album'] +
                                    metadata['id3.artist'] +
                                    metadata['id3.genre']]
            albums = [str(a) for a in metadata['extra.album'] +
                                      metadata['id3.album']]
            length = [str(l) for l in metadata['audio.length']][0]

        elif mutagen is not None:
            metadata = mutagen.File(str(soundfile), easy=True)
            parsed = [titles, [], []]
            for idx, key in enumerate(['title', 'genre', 'album']):
                if key not in metadata:
                    continue
                if isinstance(metadata[key], list):
                    parsed[idx] = metadata[key]
                else:
                    parsed[idx] = [metadata[key]]
            titles, tags, albums = parsed

            if hasattr(metadata, 'info') and hasattr(metadata.info, 'length'):
                length = int(metadata.info.length)
                length = f"{str(length // 60)}:{str(length % 60):0>2}"

        logging.debug("Adding %s", soundfile)
        sound = Sound(soundfile, mimetype)
        FILES[soundid] = sound

        sound.titles = titles
        sound.tags = tags
        sound.albums = albums
        sound.length = length


def handle_index():
    """The index page handler"""
    bottle.response.content_type = 'text/html'
    return (TEMPLATE_PATH / 'base.html').read_text()


def handle_post():
    """Handle post requests"""
    content = bottle.request.json
    if content is None:
        bottle.abort(404, "No such thing")

    SETS.clear()
    SETS.update(content)
    logging.debug("received updated set list: %s", content)
    return 'ok'


def handle_sound(soundid):
    """Handle this request for the sound with the given soundid"""
    if soundid not in FILES:
        bottle.abort(404, "No such thing")

    sound = FILES[soundid]
    bottle.response.content_type = sound.mimetype
    return sound.file.read_bytes()


def handle_static(filename):
    """Try to get this static file"""
    filename = Path(filename)

    if filename.suffix not in ('.css', '.js', '.json', '.ico'):
        bottle.abort(401, "Forbidden")

    if filename.name == 'sounds.json':
        bottle.response.content_type = 'application/json'
        return json.dumps({k: f.as_dict() for k, f in FILES.items()})

    if filename.name == 'sets.json':
        bottle.response.content_type = 'application/json'
        return json.dumps(SETS)

    if filename.suffix == '.json':
        bottle.abort(404, "No such thing")

    if filename.suffix == '.ico':
        bottle.response.content_type = 'image/svg+xml'
        return '<svg width="16" height="16" version="1.1" viewBox="0 0 ' \
               '4 4" xmlns="http://www.w3.org/2000/svg"></svg>'

    filepath = (TEMPLATE_PATH / filename.name)
    if not filepath.is_file():
        bottle.abort(404, "No such thing")

    if filename.suffix == '.js':
        bottle.response.content_type = 'text/javascript'
    if filename.suffix == '.css':
        bottle.response.content_type = 'text/css'

    return filepath.read_text()


def parse_args():
    """Parse the command line arguments and return the argparse result"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--version',
                        action='version',
                        version=f'worksforme {version.__version__}')
    parser.add_argument('-l', '--log-level',
                        default='warning',
                        choices=['fatal', 'error', 'warning', 'info', 'debug'],
                        help="Log level. Defaults to %(default)s")

    parser.add_argument('-H', '--host',
                        default='localhost',
                        type=str,
                        help="What host to listen on. Defaults to %(default)s")
    parser.add_argument('-p', '--port',
                        default=8050,
                        type=int,
                        help="What port to listen on. Defaults to %(default)s")

    parser.add_argument('-s', '--set-file',
                        default='sets.json',
                        type=str,
                        help="What file to use for sound sets. "
                             "Defaults to %(default)s.")

    parser.add_argument('paths',
                        type=str,
                        nargs='+',
                        help="The paths to sound files.")

    return parser.parse_args()
