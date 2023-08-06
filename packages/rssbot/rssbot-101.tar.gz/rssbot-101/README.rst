NAME
====

**RSSBOT** - rss feed fetcher for irc channels.

SYNOPSIS
========

``rsscmd <cmd> [options] [key=value] [key==value]``

INSTALL
=======

| ``pip3 install rssbot``

| * default channel/server is #rssbot on localhost

DESCRIPTION
===========

**RSSBOT** is a IRC bot that fetches rss feeds and displays them into irc 
channels. It runs as a background daemon for 24/7 a day presence in a IRC
channel. 

**RSSBOT** is a messenger that only messages, no commands or DCC capabilities.


CONFIGURATION
==============

| ``rsscmd cfg server=<server> channel=<channel> nick=<nick>``

| ``rsscmd cfg users=True``
| ``rsscmd met <userhost>``

| ``rsscmd pwd <nickservnick> <nickservpass>``
| ``rsscmd cfg password=<outputfrompwd>``

| ``rsscmd rss <url>``


COPYRIGHT
=========

**RSSBOT** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

Bart Thate 
