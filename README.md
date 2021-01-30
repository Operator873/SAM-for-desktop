# SAM

[![GitHub issues](https://img.shields.io/github/issues/Operator873/SAM-for-desktop)](https://github.com/Operator873/SAM/issues)
[![GitHub forks](https://img.shields.io/github/forks/Operator873/SAM-for-desktop)](https://github.com/Operator873/SAM/network)
[![GitHub stars](https://img.shields.io/github/stars/Operator873/SAM-for-desktop)](https://github.com/Operator873/SAM/stargazers)
![GitHub All Releases](https://img.shields.io/github/downloads/Operator873/SAM-for-desktop/total)
![GitHub contributors](https://img.shields.io/github/contributors/Operator873/SAM-for-desktop)

Steward/Sysop Action Module (SAM) Desktopo Python desktop module which supports Wikimedia sysops, global sysops, checkusers, and stewards by allowing block and lock actions from their desktop. It could be modified quite easily to work with Miraheze or any other Mediawiki install.

I take absolutely no responsibility for anything you do on wiki with this module. Play stupid games, win stupid prizes... like being desysopped. 

# Dependencies

This module requires Python3.x and libraries: requests, json, re, configparser, PySimpleGUI, and requests_oauthlib. This module requires all files to be in the same directory, but can be installed anywhere. I will consider packaging it as a later task.

# WYSIWYG

I'm not a professional programmer. At best, I think of myself as a Python hobbyist. Everything I write is pretty much a hack job. If you notice something that could be improved or fixed, please either fix it, or open an issue for me to fix it. Thanks.

# Installation

1. Unzip/Untar into /where/ever/is/convientent
2. from a command prompt: ```python main.py```
3. You can optionally create a desktop shortcut

# Configuration

This module requires OAuth 1.0a tokens configured on https://meta.wikimedia.org/wiki/Special:OAuthConsumerRegistration/propose.

* Application name --> Anything you want it to be. I suggest SAM
* Consumer version --> Anything
* OAuth protocol version --> OAuth 1.0a
* Application description --> Bot module to assist with blocks and locks.
* This consumer is for use only by _____ --> ***YOU MUST CHECK THIS BOX***
* OAuth "callback" URL --> Blank
* Allow consumer to specify a callback in requests and use "callback" URL above as a required prefix. --> Unchecked
* Requests authorization for specific permissions
  * High-volume editing
  * Edit existing pages
  * Create, edit, and move pages
  * Block and unblock users
 
* Allowed IP ranges: --> Optional
* Public RSA --> blank
* Check the bottom box and click Propose consumer

**SAVE YOUR TOKENS** or leave them on your screen. You will need them during the OAuth setup.
