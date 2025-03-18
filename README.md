# Quran Detector/Annotator API

This repository provides an API for detecting Quranic verses and fragments in any given text. The original tool was created to identify Quranic verses and verse fragments (greater than 3 words) and to handle minor typos and missing words. This version has been restructured to work as a RESTful API, making it easy to integrate into other applications and services.

## Features
- **Verse Detection**: Detects Quranic verses or fragments of 3 words or more in any text.
- **Error Detection**: Capable of identifying minor typos and missing words.
- **API Access**: Provides an API endpoint for easy integration into other applications.
- **Customizable**: Allows enabling/disabling error detection and missing word detection.

## Use Cases
- Sentiment analyzers
- Emotion detectors
- Automatic speech-to-text transcribers
- Any application requiring the identification of Quranic verses in text

## How It Works
The API can identify Quranic verses in any text input, even if there are minor errors or typos. The core functionality is based on exact matching, but error detection can be turned on or off for more flexible use cases.

## Paper
The approach behind this tool is described in the following paper:
[Quranic Verse Detection Approach](https://www.sciencedirect.com/science/article/pii/S1877050921012321)

