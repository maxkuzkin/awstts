# Amazon Web Services text-to-speech (Polly) helper

[![pypi](https://img.shields.io/pypi/v/gcpmetrics.svg)](https://img.shields.io/pypi/v/awstts.svg)
[![Build Status](https://travis-ci.org/odin-public/gcpmetrics.svg?branch=master)](https://travis-ci.org/maxkuzkin/awstts)

Homepage: https://github.com/maxkuzkin/awstts

## 1. Overview

Amazon Polly (https://aws.amazon.com/polly/) is an API that translates text into lifelike speech.

This tool helps to utilize that API in your small projects: presentations, video recordings, etc.

It allows you to create a small Yaml file, similar to the one below:

tts: Text-to-speech project for the educational purposes
script:
    - exec: echo command-line
    - Amazon Polly is a service that turns text into lifelike speech. Polly lets you create
    - applications that talk, enabling you to build entirely new categories of speech-enabled products.
    - voice: Amy
    - Hello! Welcome to the text to speech test.
    - <break time="1s"/> 
    - I can speak <prosody volume="x-loud">very loudly</prosody>, or I can speak <prosody volume="x-soft">very quietly</prosody>. 
    - I can speak <prosody rate="x-slow">really slowly</prosody>, or  I can speak <prosody rate="x-fast">really fast</prosody>
    - For sure. 
    - delay: 0.5
    - pause
    - voice: Brian
    - Another voice is here. My name is Brian.
    - <emphasis level='strong'>Hello</emphasis> world how are you?

and then control execution of that script from the command line.

## 2. Installation

You can install this tool simply by running

```
$ pip install --upgrade awstts
```
