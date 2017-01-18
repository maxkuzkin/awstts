#!/usr/bin/env python

import os
import sys
import yaml

from collections import OrderedDict
from subprocess import call
from optparse import OptionParser

SCRIPT_FILE = 'tts.yaml'
CACHE_DIR = '.tts'
TTS_VOICE = 'Amy'
FORCE_SYNTHESIZE = False
START_INDEX = 1


def read_file(filename):
    ret = None
    try:
        stream = open(filename, 'r')
        ret = stream.read()
        stream.close()
    except:
        pass
    return ret


def write_file(filename, text):
    stream = open(filename, 'w')
    stream.write(text)
    stream.close()


def get_filenames(counter):

    return (
        os.path.join(CACHE_DIR, '{counter}.mp3'.format(counter=counter)),
        os.path.join(CACHE_DIR, '{counter}.cache'.format(counter=counter))
        )

def synthesize(text_array, counter):

    text = ' '.join(str(x) for x in text_array)
    cached_text = TTS_VOICE + ': ' + text

    (filename_mp3, filename_text) = get_filenames(counter)
    text_before = read_file(filename_text)
    if cached_text == text_before:
        if os.path.exists(filename_mp3):
            if not FORCE_SYNTHESIZE:
                print '  {counter}. Already in cache: {text}'.format(counter=counter, text=cached_text)
                return

    print '  {counter}: synthesizing: {text}'.format(counter=counter, text=text)
    ret = call([
        'aws',
        'polly',
        'synthesize-speech',
        '--text', '<speak>' + text + '</speak>',
        '--text-type', 'ssml',
        '--voice-id', TTS_VOICE,
        '--output-format', 'mp3',
        filename_mp3
        ])
    assert ret == 0

    write_file(filename_text, cached_text)


def say(counter):

    (filename_mp3, filename_text) = get_filenames(counter)
    text = read_file(filename_text)
    print '  {counter}: {text}'.format(counter=counter, text=text)
    filename_mp3 = os.path.join(CACHE_DIR, '{counter}.mp3'.format(counter=counter))
    ret = call([
        'afplay',
        filename_mp3
        ])
    assert ret == 0


def pause():
    try:
        input('Press Enter to continue...')
    except SyntaxError:
        pass

def error(text):
    sys.exit('Error: ' + text)

def execute_script(items):

    global TTS_VOICE
    global START_INDEX

    print
    print 'Synthesizing:'
    counter = 1
    for item in items:
        if item == 'pause':
            pass
        elif item.has_key('say'):
            synthesize(item['say'], counter)
            counter = counter + 1
        elif item.has_key('voice'):
            TTS_VOICE = item['voice']
        else:
            error('unknown script item: ' + str(item))

    print
    print 'Executing:'
    counter = START_INDEX
    for item in items:
        if item == 'pause':
            pause()
        elif item.has_key('say'):
            say(counter)
            counter = counter + 1
        elif item.has_key('voice'):
            pass
        else:
            error('unknown script item')

    print 'Done.'

def create_sample_yaml_tts(filename):
    print 'Initializing sample yaml tts file: {filename}'.format(filename=filename)
    if os.path.exists(filename):
        error('File already exists')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    example_file = os.path.join(dir_path, 'example.yaml')

    contents = read_file(example_file)
    write_file(filename, contents)
    print 'Sample yaml created.'
    return 0   

def main():

    global SCRIPT_FILE
    global CACHE_DIR
    global TTS_VOICE
    global FORCE_SYNTHESIZE
    global START_INDEX

    parser = OptionParser()
    parser.add_option('-i', '--input', dest='script_file', default=SCRIPT_FILE,
        help='Yaml script file to be interpreted. Default: ' + SCRIPT_FILE, metavar='FILE')
    parser.add_option('-d', '--dir', dest='cache_dir', default=CACHE_DIR,
        help='Directory to be used for MP3 caching. Default: ' + CACHE_DIR)
    parser.add_option('-v', '--voice', dest='tts_voice', default=TTS_VOICE,
        help='Voice to be used by default (unless overriden in the script). Default: ' + TTS_VOICE)
    parser.add_option('-f', '--force', dest='force_synthesize', action='store_true',
        help='Force MP3 files to be synthesized even if cached version exists. Default: ' + str(FORCE_SYNTHESIZE))
    parser.add_option('-s', '--start', dest='start_index', default=START_INDEX,
        help='Start saying phrases from the specified index. Default: ' + str(START_INDEX))
    parser.add_option('-c', '--create', dest='sample_yaml_tts', action='store_true',
        help='Initialize sample yaml script file')

    (options, args) = parser.parse_args()

    if options.sample_yaml_tts:
        return create_sample_yaml_tts(SCRIPT_FILE)

    SCRIPT_FILE = options.script_file
    CACHE_DIR = options.cache_dir
    TTS_VOICE = options.tts_voice
    FORCE_SYNTHESIZE = options.force_synthesize
    START_INDEX = options.start_index

    print 'Script: {script}'.format(script=SCRIPT_FILE)
    stream = open(SCRIPT_FILE, 'r')
    script = yaml.load(stream)
    stream.close()
    script_items = script.items()

    assert script_items[0][0] == 'tts'
    assert script_items[1][0] == 'script'

    print 'Title: {tts}'.format(tts = script_items[0][1])
    print 'Cache: {cache_dir}'.format(cache_dir = CACHE_DIR)
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    execute_script(script_items[1][1])


if __name__ == "__main__":
    main()

