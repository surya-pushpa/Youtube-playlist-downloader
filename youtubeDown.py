#! /usr/bin/env python3

print('Heloo. Welcome to Youtube playlist downloader\n')

from pytube import YouTube, Playlist
import os, urllib, re, time, sys
import datetime


def getPageAsHtml(url):
	try:
		return str(urllib.request.urlopen(url).read())
	except Exception as e:
		print(e)
		exit(1)


def getPlaylistUrlID(url):
    if 'list=' in url:
        eq_idx = url.index('=') + 1
        pl_id = url[eq_idx:]
        if '&' in url:
            amp = url.index('&')
            pl_id = url[eq_idx:amp]
        return pl_id   
    else:
        print(url, "is not a youtube playlist.")
        exit(1)


def getFinalVideoUrl(vid_urls):
    final_urls = []
    for vid_url in vid_urls:
        url_amp = len(vid_url)
        if '&' in vid_url:
            url_amp = vid_url.index('&')
        final_urls.append('http://www.youtube.com/' + vid_url[:url_amp])
    return final_urls


def getPlaylistVideoUrls(page_content, url):
    playlist_id = getPlaylistUrlID(url)

    vid_url_pat = re.compile(r'watch\?v=\S+?list=' + playlist_id)
    vid_url_matches = list(set(re.findall(vid_url_pat, page_content)))

    if vid_url_matches:
        final_vid_urls = getFinalVideoUrl(vid_url_matches)
        print("Found",len(final_vid_urls),"videos in playlist.")
        print(final_vid_urls)
        return final_vid_urls
    else:
        print('No videos found.')
        exit(1)


def download_Video_Audio(path, vid_url, file_no):
    try:
        yt = YouTube(vid_url)
    except Exception as e:
        print("Error:", str(e), "- Skipping Video with url '"+vid_url+"'.")
        exit(1)

    print("downloading", yt.title+" Video and Audio...")
    try:
        # bar = progressBar()
        # video.download(path, on_progress=bar.print_progress, on_finish=bar.print_end)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        stream.download(path)
        print("successfully downloaded", yt.title, "!")
    except OSError:
        print(yt.title, "already exists in this directory! Skipping video...")




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

		playlist_page_content = getPageAsHtml(url)
		video_urls = getPlaylistVideoUrls(playlist_page_content, url)

		for i, video_url in enumerate(video_urls):
			download_Video_Audio(directory, video_url, i)
			time.sleep(1)

		# pl = Playlist(url)
		# pl.download_all(directory)
