#! /usr/bin/env python3

print('Heloo. Welcome to Youtube playlist downloader\n')

from pytube import YouTube, Playlist
import os, urllib, re, time, sys
import datetime


if __name__ == '__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 2:
		print('USAGE: python3 filename.py playlisturl')
		exit(1)
	else:
		url = sys.argv[1]
		today = datetime.datetime.now()
		directory = os.getcwd() + '/Download-' + today.strftime('%h-%d--%H-%M')
		try:
			os.system('mkdir ' + directory)
		except OSError as e:
			print(e.reason)
			exit(1)

		pl = Playlist(url)
		pl.download_all(directory)
