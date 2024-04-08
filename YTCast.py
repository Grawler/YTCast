import random
import datetime
import pychromecast
import pytube
import time
from pytube import YouTube, Playlist

# Pick any playlist you like, I'm using mine
playlist_link = "https://www.youtube.com/playlist?list=PLw4Em0Fd2t8RfKnbmZX0StLMV-zGxJ9YM"
video_links = Playlist(playlist_link).video_urls
video_url = []
video_titles = []
video_length = []
keep_playing = True
# You have to select a Chromecast device to stream to. Uncomment the line below to create a list.
# print(pychromecast.get_chromecasts())
chromecast, browser = pychromecast.get_listed_chromecasts(["Slaapkamer Hub"])
cast = chromecast[0]
randomUrl = ""
randomVid = 0
shortVid = 0
longVid = 0
videoFound = False

# Populate arrays with url, title and length of each video
for link in video_links:
    video_url.append(YouTube(link).video_id)
    video_titles.append(YouTube(link).title)
    video_length.append(YouTube(link).length)
    print("Found " + str(link))

video_length_short = 0
video_length_long = 0
video_length_verylong = 0

for i in video_length:
    if i < 1800:
        video_length_short += 1
    if 1800 <= i < 7200:
        video_length_long += 1
    if i >= 7200:
        video_length_verylong += 1

print("Short: " + str(video_length_short) + ", Long: " + str(video_length_long) + ", Very Long: " + str(
    video_length_verylong))


def getrandomvid():
    return random.randint(0, len(video_links)) - 1


def getrandomurl():
    return "https://www.youtube.com/watch?v=" + video_url[randomVid]


while keep_playing:

    while not videoFound:
        if longVid < 1:
            randomVid = getrandomvid()
            randomUrl = getrandomurl()
            if video_length[randomVid] >= 1800:
                longVid += 1
                videoFound = True
                print("Found long video")
                break
        if shortVid < 3:
            randomVid = getrandomvid()
            randomUrl = getrandomurl()
            if video_length[randomVid] < 1800:
                shortVid += 1
                videoFound = True
                print("Found short video, counter: " + str(shortVid))
                break
        if longVid > 0 and shortVid >= 3:
            longVid = 0
            shortVid = 0
            print("Counters reset")
    try:
        vidstreams = pytube.YouTube(randomUrl).streams.get_highest_resolution()
    except:
        print("Found error, selecting new random video. Error found in: " + str(video_titles[randomVid]))
        randomVid = getrandomvid()
        randomUrl = getrandomurl()
        vidstreams = pytube.YouTube(randomUrl).streams.get_highest_resolution()
    cast.wait()
    mediaController = cast.media_controller
    time_done = datetime.datetime.now() + datetime.timedelta(seconds=video_length[randomVid] - 5)

    print(
        "[" + datetime.datetime.now().strftime("%H:%M:%S") + "] Casting " + str(video_titles[randomVid]) + " (" + str(
            video_length[randomVid]) + " seconds (" + str(
            round(video_length[randomVid] / 60, 2)) + " minutes)). Done at " + time_done.strftime("%H:%M:%S"))
    mediaController.play_media(vidstreams.url, "video/mp4")

    time.sleep(video_length[randomVid] - 5)
    videoFound = False
