#!/usr/bin/env python

from bottle import get, run, redirect, static_file, view, request, response
from os import fork, execv, _exit, listdir, mkfifo
from signal import signal, SIGCHLD, SIG_IGN
from mutagen import File
from urllib2 import urlopen
from random import shuffle
import json

MPLAYER = '/usr/bin/mplayer'
ROOT = '/root'
MPLAYER_FIFO = '/tmp/mplayer.fifo'
MUSIC_DIR = '%s/music' % ROOT
STATIC_DIR = '%s/static' % ROOT
DOUBAN_URL = 'http://douban.fm/j/mine/playlist?type=n&sid=1424797&pt=29.6&channel=1000027&pb=64&from=mainsite&r=c3d64b0618'
DEBUG = True

songs = {}
volume = 10
pausing = 0

@get('/')
@view('home')
def _():
    sl = songs.keys()
    q = unicode(request.query.q).encode('utf-8').strip()
    if q:
        sl = filter(lambda s: s.find(q) + 1, sl)
    return dict(songs=sl)

@get('/play/<name>')
def _(name):
    global pausing
    if name == 'douban.fm':
        slist = filter(lambda url: url.endswith('mp3'), 
                [s['url'] for s in douban()+douban()+douban()+douban()+douban()])
        shuffle(slist)
    else:
        pos = songs.keys().index(name)
        slist = ['%s/%s' % (MUSIC_DIR, s) for s in songs.keys()[pos:]+songs.keys()[:pos]]
    mplayer('\n'.join('loadfile "%s" %d' % (slist[i], 1 if i else 0) for i in range(len(slist))))
    mplayer('pause') if pausing else ''
    pausing = 0

@get('/cover/<name>')
def _(name):
    response.content_type = 'image/jpeg'
    response.add_header('Cache-Control', 'max-age=31536000')
    return songs.get(name)

@get('/pause')
def _():
    global pausing
    mplayer('pause')
    pausing = 0 if pausing else 1

@get('/volup')
def _():
    global volume
    volume += 3 if volume <= 97 else 0
    mplayer('volume %d 1' % volume)

@get('/voldown')
def _():
    global volume
    volume -= 3 if volume >= 3 else 0
    mplayer('volume %d 1' % volume)

@get('/<path:path>')
def _(path):
    return static_file(path, root=STATIC_DIR)

def image(mp3):
    f = File(mp3)
    try:
        key = filter(None, [k if k.startswith('APIC') else '' for k in f.tags.keys()])[0]
        return f.tags[key].data
    except IndexError:
        return ''

def douban(url=DOUBAN_URL):
    return json.loads(urlopen(url).read())['song']

def mplayer(cmd):
    f = open(MPLAYER_FIFO, 'w')
    f.write('%s\n' % cmd)
    f.close()

if __name__ == '__main__':
    # avoid zombie sub-processes
    signal(SIGCHLD, SIG_IGN) 
    # update local media library
    for s in listdir(MUSIC_DIR):
        if not s.endswith('mp3'): continue
        songs[s] = image('%s/%s' % (MUSIC_DIR, s))
    # create fifo for slave-mode player
    try:
        mkfifo(MPLAYER_FIFO)
    except OSError:
        pass
    # start slave-mode mplayer
    pid = fork()
    if pid == 0:
        execv(MPLAYER, 
                (MPLAYER, '-idle', '-slave', '-input', 'file=%s' % MPLAYER_FIFO, '-volume', '%s' % volume))
        _exit(0)
    run(host='0.0.0.0', port=80)
