# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot
import io
import os
import time
from datetime import datetime as d

import asyncpraw
import discord
import Image as I
import requests
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

from keep_alive import keep_alive

load_dotenv()


class Record:
    """Record all file that success send"""

    def __init__(self, image=0, gif=0, video=0, nonformat=0):
        self.image = image
        self.gif = gif
        self.video = video
        self.nonformat = nonformat

    def addImage(self):
        self.image = int(self.image) + 1

    def addGif(self):
        self.gif = int(self.gif) + 1

    def addVideo(self):
        self.video = int(self.video) + 1

    def addNonformat(self):
        self.nonformat = int(self.nonformat) + 1

    def Def(self, image, gif, video, nonformat):
        self.image = image
        self.gif = gif
        self.video = video
        self.nonformat = nonformat

    def total(self):
        """all total"""
        return self.image + self.gif + self.video + self.nonformat


all = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=all)

subsChannel = []
broadcast = ["red", "rg", "rv", "non-embed", "terminal", "hi"]

contentRecord = Record()
recordChannel = []

terminal = None
hi = None
red = None
rg = None
rv = None
nonEmbed = None

last = []
lastUrls = []
lastNames = []
lastpostTime = False
Code = 1
n = 0
timer15M = False

subsDB = """UcanUse+ToAddTwo+orMore"""  # use + to sprate the subs
banFlairs = []
bansFrom = [
    "youtu.be",
    "youtube",
    "comments",
    "patreon",
    "pixiv.net",
    "twitter",
]  # bans anything relate to
bansTitle = []
imageFormats = [
    ".apng",
    ".avif",
    ".gif",
    ".jpg",
    ".jpeg",
    ".jfif",
    ".pjpeg",
    ".pjp",
    ".png",
    ".svg",
    ".gifv",
]
videoFormats = [
    ".mp4",
    ".webm",
    ".mkv",
    ".flv",
    ".flv",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
    ".m4v",
    ".mpg, .mpeg, .m2v",
    ".mpg",
    ".mp2",
    ".mpe",
    ".mpv",
    ".m4p",
    ".amv",
    ".asf",
    ".viv",
    ".rmvb",
    ".rm",
    ".yuv",
    ".wmv",
    ".mov",
    ".qt",
    ".MTS",
    ".M2TS",
    ".TS",
    ".vob",
]


def cooldown(t):
    start = time.time()
    print(f"coldown {t}'s")
    while time.time() < start + t:
        pass


def checkFormat(url, formats):
    if isinstance(formats, list):
        for format in formats:
            if url.find(format) != -1:
                return format

    if isinstance(formats, str):
        if url.find(formats) != -1:
            return url
    return False


def didUrlSame(url):
    for lastUrl in lastUrls:
        if lastUrl == url:
            return lastUrl
    return False


async def checkSize(format, url):
    if format == ".gif" or format == ".gifv" or format == ".avif":
        return
    imgrequest = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
        },
    )  # the Request object
    imgstring = imgrequest.content  # the image as a string
    imgiostream = io.BytesIO(imgstring)  # PIL needs a file-like object like io.BytesIO
    img = I.open(imgiostream)
    # im = Image.open(imgiostream)
    # print('HIT')
    # print(im.info)

    print(img.info)
    width, height = img.size
    print("Width:", width, "Height:", height)

    if width >= 2560 and height >= 1440 or width >= 2000 and height >= 2560:
        return f"/High_res/ w:{width}px h:{height}px"
    if width <= 1080 and height > 1700:
        await terminal.send(
            f"""Skipp ► Phone Screenshot
    Width: {width} px
    Height: {height} px
    """
        )
        return True
    if width >= 0 and width <= 720:
        await terminal.send(
            f"""Skipp ► lowres Content
    Width: {width} px
    Height: {height} px
    """
        )
        return True
    if width < 720 or height < 720:
        await terminal.send(
            f"""Skipp ► lowres Content
    Width: {width} px
    Height: {height} px
    """
        )
        cooldown(2)
        return True
    if width <= 720 and height <= 720:
        await terminal.send(
            f"""Skipp ► lowres Content
    Width: {width} px
    Height: {height} px
  """
        )
        cooldown(2)
        return True
    return False


def didNameSame(name):
    for lastName in lastNames:
        if lastName == name:
            return lastName
    return False


async def searchLastMessage():
    notfound = True
    content = 2
    _ = 1
    if not last:
        await terminal.send(
            """‎
+-+-+-+-+-+ ‎ ‎ +-+-+ ‎ ‎ +-+-+-+-+-+ ‎ ‎ +-+-+-+-+-+
‎|#|#|#|#|#| ‎ ‎ ‎ ‎ ‎|I|M| ‎  ‎ ‎ ‎ |A|L|I|V|E|  ‎ ‎ ‎ ‎ |A|G|A|I|N|
+-+-+-+-+-+ ‎ ‎ +-+-+ ‎ ‎ +-+-+-+-+-+ ‎ ‎ +-+-+-+-+-+
"""
        )
    cooldown(2)
    await terminal.send("...Searching LastGift BepBop◎◉⦿")
    print("##### IM ALIVE AGAIN")

    while notfound:
        historyIndex = 2

        # async for message in subsChannel[0].history(limit=content):
        async for message in terminal.history(limit=content):
            if content != historyIndex:
                historyIndex += 1
            elif message.author == bot.user:

                def getUrl():
                    try:
                        description = message.embeds[0].description
                        # print(description)
                        start = description.find("ID: ") + 4
                        end = start + 10
                        url = description.split("Content:")[-1].split(" ")[1]
                        unix = float(description[start:end])
                        return [url, unix]
                    except Exception as e:
                        # print(e)
                        return False

                url = getUrl()
                if url:
                    # url = description.split("Content:")[-1].split(" ")[1]
                    # url = (url[:253] + '...') if len(url) > 256 else url
                    last.append(url[0])
                    last.append(url[1])
                    # lastUrls.append(url)
                    info = discord.Embed(
                        description=f"""
          ▻ Last Post
          ‎
          {message.embeds[0].description}"""
                    )
                    await terminal.send(
                        content=f"""‎
          Gotcha▼
          """,
                        embed=info,
                    )
                    notfound = False
        content += 1
        print(f"Searching.. attempt history#{content}")


async def recordContent():
    global Code
    # print(contentRecord.image)
    # print(contentRecord.total())
    if Code == 3:
        await searchLastMessage()
        Code = 1

    now = d.now()

    current_time = now.strftime("%H:%M:%S")
    desc = discord.Embed(
        description=f"""
      ======== Content ========
      # ‎Image ‎ +-+-+-+-+-+ ‎‎: _{contentRecord.image}_
      # ‎Gif ‎ ‎ ‎ ‎ ‎ ‎ ‎ +-+-+-+-+-+ ‎: _{contentRecord.gif}_
      # ‎Video ‎ ‎ +-+-+-+-+-+ ‎: _{contentRecord.video}_
      # ‎Non-Format[url] ‎ + ‎: _{contentRecord.nonformat}_
      # ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ +-+-+-+-+-+
      # ‎Total ‎ ‎ +-+-+-+-+-+ ‎ ‎: _{contentRecord.total()}_
      ======== {current_time} ========
      """
    )
    async for message in recordChannel.history(limit=10):
        if message.author == bot.user:
            await message.edit(embed=desc)
            break
    # await recordChannel[0].send(embed= desc)


def sleep(timeout, retry=3):
    def the_real_decorator(function):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < retry:
                try:
                    value = function(*args, **kwargs)
                    if value is None:
                        return
                except:
                    print(f"Sleeping for {timeout} seconds")
                    time.sleep(timeout)
                    retries += 1

        return wrapper

    return the_real_decorator


async def subscribe(subs):
    for channelName in subs:
        for guild in bot.guilds:
            if guild.name == "TC's server":
                for channel in guild.text_channels:
                    if channel.name == channelName:
                        subsChannel.append(channel)
                        break
                break


async def collector():
    reddit = asyncpraw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        password=os.getenv("passwordRD"),
        user_agent="Odessy",
        username=os.getenv("username"),
        ratelimit_seconds=300,
    )

    subreddit = await reddit.subreddit(subsDB)
    await searchLastMessage()

    async def sendTheNewOne():
        async def newOne():
            cooldown(2)
            await terminal.send("▲ SEND THE NEW ONE ▲")
            if last:
                last.clear()
            await searchLastMessage()

        # i = 0
        async for submission in subreddit.top(time_filter="hour"):
            # i = i + 1
            url = submission.url or False
            name = submission.title
            name = (name[:253] + "...") if len(name) > 256 else name

            lastUrl = didUrlSame(url)
            lastName = didNameSame(name)

            if not url or lastUrl or lastName:
                continue

            if not url:
                await terminal.send("```Skipp ► url Empty ```")
                print("Skipp url Empty")
                continue

            flair = submission.link_flair_text

            for flair_ in banFlairs:
                if flair_ == flair:
                    await terminal.send(f"```Skipp ► Flair {flair_} ```")
                    print("Skipp Flair Match")
                    continue
            if flair:
                flair = f"Flair: {flair} "
            else:
                flair = ""

            em = discord.Embed(title=name, url=url)
            embedSource = discord.Embed(
                description=f"""```python
        ID: {submission.created} 
        PostTime: {d.fromtimestamp(submission.created)} v2
        ```
        {flair}
        Subreddit : r/{submission.subreddit},
        Title: {name},
        Content: {url}
        """
            )

            vReddit = url.find("v.redd.it") != -1
            v = checkFormat(url, videoFormats)
            image = False
            gif = False
            veiledContent = checkFormat(url, bansFrom)
            gallery = False

            if not v:
                gallery = checkFormat(url, "reddit.com/gallery")
                image = checkFormat(url, imageFormats)
                if image == ".gifv" or image == ".gif" or image == ".avif":
                    gif = True
                    # url = url[:-1]
                # gif = url.find('.gif') > 0

            # Skip ban souce
            if veiledContent:
                try:
                    await terminal.send(embed=embedSource)
                    await terminal.send(
                        f"""```-> {url.split('/')[2]} ⇑ [false/missguide/notExtractable] ⦿ Pass! <-```"""
                    )
                    print(url.split("/")[3] + " Pass! \n =========")
                    cooldown(3)
                    break
                except Exception as e:
                    await terminal.send("FAIL to send veiled Engine 2")
                    print("FAIL to send")
                    print(e)
                    continue

            # Mostly Blob Vid
            if vReddit or v:
                if vReddit:
                    v = ".mp4"
                    em = discord.Embed(title=name, url=url + "/DASH_720.mp4")

                try:
                    await rv.send(embed=em)
                    cooldown(2)
                    await terminal.send(embed=embedSource)
                    cooldown(2)
                    await terminal.send(
                        f"""↾
          Video{v} Done
          =========="""
                    )
                    # cooldown(2)
                    print("Video Done  \n =========")

                    contentRecord.addVideo()
                    await recordContent()
                    await newOne()
                    break
                except Exception as e:
                    await terminal.send("FAIL to send rv Engine 2")
                    print("FAIL to send")
                    print(e)
                    cooldown(2)
                    continue

            # Gallery
            if gallery:
                await terminal.send("◍ HIT Gallery ◍")
                cooldown(2)
                media = False

                try:
                    media = submission.media_metadata
                except:
                    await terminal.send("Gallery don't have media metadata")
                    cooldown(2)
                    continue

                for index, id in enumerate(media.keys(), 1):
                    url = media[id]["s"]["u"] if media[id]["s"]["u"] else False
                    if not url:
                        continue
                    type = f""".{media[id]["m"].split("/")[1]}"""
                    print(url)
                    name = f"{id} : {index}"
                    name = (name[:253] + "...") if len(name) > 256 else name

                    em = discord.Embed(title=name, url=url)
                    embedSource = discord.Embed(
                        description=f"""```python
            ID: {submission.created}
            PostTime:{d.fromtimestamp(submission.created)}
            ```
            {flair}
            Subreddit : r/{submission.subreddit}
            Title: {name} 
            Gallery: {url}
            Content: {submission.url}
            """
                    )
                    v = checkFormat(type, videoFormats)
                    gif = False

                    if v:
                        vReddit = url.find("v.redd.it") != -1
                    else:
                        image = checkFormat(type, imageFormats)
                        if image == ".gifv" or image == ".gif" or image == ".avif":
                            gif = True

                    # V
                    if vReddit or v:
                        if vReddit:
                            v = ".mp4"
                            em = discord.Embed(title=name, url=url + "/DASH_720.mp4")

                        try:
                            await rv.send(embed=em)
                            cooldown(2)
                            await terminal.send(embed=embedSource)
                            cooldown(2)
                            await terminal.send(
                                f"""↾
              Video{v} Done 
              =============="""
                            )
                            # cooldown(2)
                            print("Video Done \n =========")

                            contentRecord.addVideo()
                            await recordContent()
                            cooldown(2)
                            continue
                        except Exception as e:
                            await terminal.send("FAIL to send rv")
                            print("FAIL to send")
                            print(e)
                            cooldown(2)
                            continue
                    # IMG
                    if image:
                        checkSizeResult = await checkSize(image, url)
                        if checkSizeResult == True:
                            continue
                        if checkSizeResult != False:
                            em = discord.Embed(
                                title=f"{name} {checkSizeResult}", url=url
                            )
                        em.set_image(url=url)
                        try:
                            if gif:
                                await rg.send(embed=em)
                                contentRecord.addGif()
                            else:
                                if checkSizeResult == False:
                                    await red.send(embed=em)
                                else:
                                    await hi.send(embed=em)
                                contentRecord.addImage()
                            cooldown(2)
                            await terminal.send(embed=embedSource)
                            cooldown(2)
                            await terminal.send(
                                f"""↾
              Embed{image} Done
              =============="""
                            )
                            # cooldown(2)
                            print("Embed Done \n =========")

                            await recordContent()
                            cooldown(2)
                            continue
                        except Exception as e:
                            await terminal.send("FAIL to send red")
                            print("FAIL to send")
                            print(e)
                            cooldown(2)
                            continue
                    # Throw non format
                    try:
                        await nonEmbed.send(content=url)
                        cooldown(2)
                        await terminal.send(embed=embedSource)
                        cooldown(2)
                        await terminal.send(
                            """↾
            NoN Embed Done 
            =============="""
                        )
                        # cooldown(2)
                        print("NoN Embed Done \n =========")

                        contentRecord.addNonformat()
                        await recordContent()
                        cooldown(2)
                    except Exception as e:
                        await terminal.send("FAIL to send non-embed")
                        print("FAIL to send")
                        cooldown(2)
                        print(e)
                await terminal.send("↿ HIT Gallery DONE ↾")
                continue

            # Mostly Img
            if image:
                checkSizeResult = await checkSize(image, url)
                if checkSizeResult is True:
                    continue
                if checkSizeResult is not False:
                    em = discord.Embed(title=f"{name} {checkSizeResult}", url=url)
                em.set_image(url=url)
                try:
                    if checkSizeResult == False:
                        await red.send(embed=em)
                    else:
                        await hi.send(embed=em)
                    cooldown(2)
                    await terminal.send(embed=embedSource)
                    cooldown(2)
                    await terminal.send(
                        f"""↾
          Embed Done 
          =========="""
                    )
                    # cooldown(2)
                    print("Embed Done \n =========")

                    if gif:
                        contentRecord.addGif()
                    else:
                        contentRecord.addImage()
                    await recordContent()
                    await newOne()
                    break
                except Exception as e:
                    await terminal.send("FAIL to send red Engine 2")
                    print("FAIL to send")
                    print(e)
                    cooldown(2)
                    continue

            # Throw non format
            try:
                await nonEmbed.send(content=url)
                cooldown(2)
                await terminal.send(embed=embedSource)
                cooldown(2)
                await terminal.send(
                    """↾
        NoN Embed Done 
        =============="""
                )
                # cooldown(2)
                print("NoN Embed Done \n =========")

                contentRecord.addNonformat()
                await recordContent()
                await newOne()
                break
            except Exception as e:
                await terminal.send("FAIL to send non-embed Engine 2")
                print("FAIL to send")
                print(e)
                cooldown(2)

    # Start the stream

    # await sendTheNewOne()
    async def Stream():
        global n
        # global lastUrls
        # global lastNames
        global lastpostTime
        global Code
        global terminal
        global timer15M

        try:
            async for submission in subreddit.stream.submissions():
                # global n
                if n == 404 or Code == 3:
                    # n == 201 or
                    print("break TOP")
                    break

                # continue
                if subsChannel:
                    n = n + 1
                    print(n)
                    # material
                    name = submission.title
                    name = (name[:253] + "...") if len(name) >= 256 else name
                    url = submission.url or False

                    print(f"=====> r/{submission.subreddit}")
                    print(name)

                    # HOLDER
                    # comment this for test run not continue run
                    if last:
                        # await terminal.send(f'=====> r/{submission.subreddit}')
                        # await terminal.send(name)
                        # await terminal.send(n)
                        # lastNotSame = last[0] != url
                        def valid():
                            if last[0] == url:
                                return f"""-> {last[0].split("/")[-1]} = {url.split("/")[-1]} <-"""
                            if last[1] <= submission.created:
                                return f"-> {last[1]} = {submission.created} <-"
                            return False

                        lastPostMatchWStream = valid()
                        if timer15M:
                            if timer15M < time.time():
                                await terminal.send(
                                    f"""‎
                ⚠︎ TIMEOUT⏱ HIT
                """
                                )
                                print("TIMEOUT 15M HIT")
                                Code = 3
                                last.clear()
                                timer15M = False

                        if not lastPostMatchWStream and n == 100:
                            print("NOT FOUND 100 Files")
                            if Code == 1:
                                n = 404
                                Code = 2
                                await terminal.send(
                                    f"""‎
              ⚠︎ NOT FOUND In 100 Files
              """
                                )
                                # await searchLastMessage()
                                break
                            else:
                                await terminal.send(
                                    f"""‎
              ⚠︎ New One NOT FOUND In 100 Files
              ▸ Continue to 200 Files ◂
              ⓘ ₘₐybₑ ₜₐₖₑ ₛₒₘₑₜᵢₘₑₛ wₐᵢₜᵢₙg ₜₕₑ ₛₜᵣₑₐₘ ₕᵢₜ ₜₒ ₂₀₀...
              """
                                )
                                timer15M = time.time() + 900
                                await terminal.send(
                                    """‎
                ⏱ Set 15M Timer...
              """
                                )
                        if not lastPostMatchWStream and n == 200:
                            await terminal.send(
                                f"""‎
              ⚠︎ NOT FOUND In 200 Files
              """
                            )
                            print("NOT FOUND 200 Files")
                            Code = 3
                            last.clear()
                            # n = 404
                            # await searchLastMessage()
                            # break

                        if Code == 3:
                            await terminal.send(
                                f"""‎
              ⚠︎ ATTEMPT CODE #3 ⚠︎
              """
                            )
                            print("Attempt CODE 3")
                        else:
                            if not lastPostMatchWStream:
                                continue
                            # else: n = 0
                            # if lastUrl : n = 0
                            n = 0
                            # Send confirmation
                            await terminal.send("HIT ◉ @everyone ")
                            await terminal.send(
                                f"""‎
              ==========  ==========  ==========
              HIT HIT HIT   HIT HIT HIT   HIT HIT HIT
              ==========  ==========  ==========
              {lastPostMatchWStream}"""
                            )
                            # -> {name[0:3]} = {last[0][0:3]} <-""")
                            # print(f" =============== \n       HIT \n =============== \n -> {name[0:3]} = {last[0][0:3]} <-")
                            print(
                                f""" =============== \n       HIT \n =============== \n -> {lastPostMatchWStream} <-"""
                            )
                            # remove the holder
                            # add holder post time
                            lastpostTime = submission.created - 60
                            await terminal.send(
                                f"""
                ```python
                ID: {submission.created}
                LastPost:{d.fromtimestamp(last[1])}
                PostTime:{d.fromtimestamp(submission.created)}```"""
                            )
                            cooldown(2)
                            last.clear()
                            await terminal.send("    CONTINUE▼")
                            print("    CONTINUE")
                            continue

                    lastUrl = didUrlSame(url)
                    lastName = didNameSame(name)
                    # Content Check
                    if lastpostTime:
                        print(d.fromtimestamp(lastpostTime))
                        pastPostTime = lastpostTime <= submission.created
                        if pastPostTime:
                            if not lastUrls:
                                print("HIT THE NEW ONE")
                                await terminal.send("▼ HIT THE NEW ONE ▼")
                            else:
                                print(
                                    """Checked : 
                still Newest Content"""
                                )

                        else:
                            await terminal.send(
                                f"""Skipp ► past content 
              ```-> {lastNames[-1]} = {d.fromtimestamp(lastpostTime)} ⤫ {d.fromtimestamp(submission.created)} = {name} <-```
              """
                            )
                            print("Skipp ► past content")
                            continue

                    lastpostTime = submission.created - 60

                    if not url or lastUrl or lastName:
                        if lastUrl:
                            await terminal.send(
                                f"""Skipp ► content url Same
              ```-> {url.split("/")[-1]} == {lastUrl.split("/")[-1]} <-```
              """
                            )
                            print("Skipp ► url Same")
                        elif lastName:
                            await terminal.send(
                                f"""Skipp ► content Same
              ```-> {name} == {lastName} <-```
              """
                            )
                            print("Skipp content Same")
                        else:
                            await terminal.send("```Skipp ► url Empty ```")
                            print("Skipp ► url Empty")

                        continue

                    lastUrls.append(url)
                    lastNames.append(name)
                    flair = submission.link_flair_text

                    for flair_ in banFlairs:
                        if flair_ == flair:
                            await terminal.send(f"```Skipp ► Flair {flair_} ```")
                            print("Skipp Flair Match")
                            continue
                    if flair:
                        flair = f"Flair: {flair} "
                    else:
                        flair = ""

                    # CONTINUE THE ENGINE
                    em = discord.Embed(title=name, url=url)

                    vReddit = url.find("v.redd.it") != -1
                    # mp4 = url[-4:] == ".mp4" or url[-4:] == ".mov"
                    v = checkFormat(url, videoFormats)
                    image = False
                    gif = False
                    gallery = False
                    veiledContent = checkFormat(url, bansFrom)

                    if not v:
                        gallery = checkFormat(url, "reddit.com/gallery")
                        image = checkFormat(url, imageFormats)
                        if image == ".gifv" or image == ".gif" or image == ".avif":
                            # url = url[:-1]
                            gif = True
                        #   gifv = url[-5:] == ".gifv"
                        # if gifv:
                        # gif = url.find('.gif') > 0

                    embedSource = discord.Embed(
                        description=f"""```python
            ID: {submission.created}
            PostTime:{d.fromtimestamp(submission.created)}
            ```
            {flair}
            Subreddit : r/{submission.subreddit}
            Title: {name} 
            Content: {url}
            """
                    )
                    print(url)

                    # Skip non format redd gallery
                    if veiledContent:
                        try:
                            await terminal.send(embed=embedSource)
                            await terminal.send(
                                f"""```-> {url.split('/')[2]} ⇑ [false/missguide/notExtractable/ban] ⦿ Pass! {veiledContent} <-```"""
                            )
                            print(url.split("/")[3] + " Pass! \n =========")
                            cooldown(3)
                            continue
                        except Exception as e:
                            await terminal.send("FAIL to send veiled")
                            print("FAIL to send")
                            print(e)
                            continue

                    # Mostly Blob Vid
                    if vReddit or v:
                        if vReddit:
                            v = ".mp4"
                            em = discord.Embed(title=name, url=url + "/DASH_720.mp4")

                        try:
                            await rv.send(embed=em)
                            cooldown(2)
                            await terminal.send(embed=embedSource)
                            cooldown(2)
                            await terminal.send(
                                f"""↾
              Video{v} Done 
              =============="""
                            )
                            # cooldown(2)
                            print("Video Done \n =========")

                            contentRecord.addVideo()
                            await recordContent()
                            cooldown(2)
                            continue
                        except Exception as e:
                            await terminal.send("FAIL to send rv")
                            print("FAIL to send")
                            print(e)
                            cooldown(2)
                            continue

                    # Gallery
                    if gallery:
                        await terminal.send("◍ HIT Gallery ◍")
                        cooldown(2)
                        media = False

                        try:
                            media = submission.media_metadata
                        except:
                            await terminal.send("Gallery don't have media metadata")
                            cooldown(2)
                            continue

                        for index, id in enumerate(media.keys(), 1):
                            url = media[id]["s"]["u"] if media[id]["s"]["u"] else False
                            if not url:
                                continue
                            type = f""".{media[id]["m"].split("/")[1]}"""
                            print(url)
                            name = f"{id} : {index}"
                            name = (name[:253] + "...") if len(name) > 256 else name

                            em = discord.Embed(title=name, url=url)
                            embedSource = discord.Embed(
                                description=f"""```python
                ID: {submission.created}
                PostTime:{d.fromtimestamp(submission.created)}
                ```
                {flair}
                Subreddit : r/{submission.subreddit}
                Title: {name} 
                Gallery: {url}
                Content: {submission.url}
                """
                            )
                            v = checkFormat(type, videoFormats)
                            gif = False

                            if v:
                                vReddit = url.find("v.redd.it") != -1
                            else:
                                image = checkFormat(type, imageFormats)
                                if (
                                    image == ".gifv"
                                    or image == ".gif"
                                    or image == ".avif"
                                ):
                                    gif = True

                            # V
                            if vReddit or v:
                                if vReddit:
                                    v = ".mp4"
                                    em = discord.Embed(
                                        title=name, url=url + "/DASH_720.mp4"
                                    )

                                try:
                                    await rv.send(embed=em)
                                    cooldown(2)
                                    await terminal.send(embed=embedSource)
                                    cooldown(2)
                                    await terminal.send(
                                        f"""↾
                  Video{v} Done 
                  =============="""
                                    )
                                    # cooldown(2)
                                    print("Video Done \n =========")

                                    contentRecord.addVideo()
                                    await recordContent()
                                    cooldown(2)
                                    continue
                                except Exception as e:
                                    await terminal.send("FAIL to send rv")
                                    print("FAIL to send")
                                    print(e)
                                    cooldown(2)
                                    continue
                            # IMG
                            if image:
                                checkSizeResult = await checkSize(image, url)
                                if checkSizeResult == True:
                                    continue
                                if checkSizeResult != False:
                                    em = discord.Embed(
                                        title=f"{name} {checkSizeResult}", url=url
                                    )
                                em.set_image(url=url)
                                try:
                                    if gif:
                                        await rg.send(embed=em)
                                        contentRecord.addGif()
                                    else:
                                        if checkSizeResult == False:
                                            await red.send(embed=em)
                                        else:
                                            await hi.send(embed=em)
                                        contentRecord.addImage()
                                    cooldown(2)
                                    await terminal.send(embed=embedSource)
                                    cooldown(2)
                                    await terminal.send(
                                        f"""↾
                  Embed{image} Done
                  =============="""
                                    )
                                    # cooldown(2)
                                    print("Embed Done \n =========")

                                    await recordContent()
                                    cooldown(2)
                                    continue
                                except Exception as e:
                                    await terminal.send("FAIL to send red")
                                    print("FAIL to send")
                                    print(e)
                                    cooldown(2)
                                    continue
                            # Throw non format
                            try:
                                await nonEmbed.send(content=url)
                                cooldown(2)
                                await terminal.send(embed=embedSource)
                                cooldown(2)
                                await terminal.send(
                                    """↾
                NoN Embed Done 
                =============="""
                                )
                                # cooldown(2)
                                print("NoN Embed Done \n =========")

                                contentRecord.addNonformat()
                                await recordContent()
                                cooldown(2)
                            except Exception as e:
                                await terminal.send("FAIL to send non-embed")
                                print("FAIL to send")
                                cooldown(2)
                                print(e)
                        await terminal.send("↿ HIT Gallery DONE ↾")
                        continue
                    # Mostly Img
                    if image:
                        checkSizeResult = await checkSize(image, url)
                        if checkSizeResult == True:
                            continue
                        if checkSizeResult != False:
                            em = discord.Embed(
                                title=f"{name} {checkSizeResult}", url=url
                            )
                        em.set_image(url=url)
                        try:
                            if gif:
                                await rg.send(embed=em)
                                contentRecord.addGif()
                            else:
                                if checkSizeResult == False:
                                    await red.send(embed=em)
                                else:
                                    await hi.send(embed=em)
                                contentRecord.addImage()
                            cooldown(2)
                            await terminal.send(embed=embedSource)
                            cooldown(2)
                            await terminal.send(
                                f"""↾
              Embed{image} Done
              =============="""
                            )
                            # cooldown(2)
                            print("Embed Done \n =========")

                            await recordContent()
                            cooldown(2)
                            continue
                        except Exception as e:
                            await terminal.send("FAIL to send red")
                            print("FAIL to send")
                            print(e)
                            cooldown(2)
                            continue

                    # Throw non format
                    try:
                        await nonEmbed.send(content=url)
                        cooldown(2)
                        await terminal.send(embed=embedSource)
                        cooldown(2)
                        await terminal.send(
                            """↾
            NoN Embed Done 
            =============="""
                        )
                        # cooldown(2)
                        print("NoN Embed Done \n =========")

                        contentRecord.addNonformat()
                        await recordContent()
                        cooldown(2)
                    except Exception as e:
                        await terminal.send("FAIL to send non-embed")
                        print("FAIL to send")
                        cooldown(2)
                        print(e)

                    # send to all subsChannel
                    # for c in subsChannel:
                    #   try:
                    #     await c.send(embed= em)
                    #   except:
                    #     pass

        except Exception as e:
            print(e)
            pass

        if n == 101:
            # await sendTheNewOne()
            print("◎ Attempt Code 101 ◎")
            await terminal.send("◎ Attempt Code 101 ◎")
            await searchLastMessage()
            n = 0
            await Stream()
        elif n == 404:
            print("◎ Attempt Code 404 ◎")
            await terminal.send("◎ Attempt Code 404 ◎")
            await sendTheNewOne()
            n = 0
            await Stream()
        else:
            print("◎ Attempt Code L00P ◎")
            await terminal.send("◎ Attempt Code L00P ◎")
            Code = 1
            n = 0
            await Stream()
            cooldown(60)

    # if n == 100:
    #   # await sendTheNewOne()
    #   await searchLastMessage()
    #   n = 0
    #   await Stream()
    # elif n == 404:
    #   await sendTheNewOne()
    #   await searchLastMessage()
    #   n = 0
    #   await Stream()
    await Stream()


@bot.event
async def on_ready():
    global recordChannel
    global red
    global rg
    global rv
    global nonEmbed
    global terminal
    global hi
    print("We have logged in as {0.user}".format(bot))
    for guild in bot.guilds:
        if guild.name == "TC's server":
            for channel in guild.text_channels:
                if channel.name == "record":
                    recordChannel = channel
                    break
            break
    async for message in recordChannel.history(limit=10):
        if message.author == bot.user:
            description = message.embeds[0].description
            description = description.split("_")
            # contentRecord = {}
            # contentRecord["image"] = int(description[1])
            # contentRecord["gif"] = int(description[3])
            # contentRecord["video"] = int(description[5])
            # contentRecord["nonformat"] = int(description[7])
            contentRecord.Def(
                int(description[1]),
                int(description[3]),
                int(description[5]),
                int(description[7]),
            )
            # await message.delete()
            break
        break
    await subscribe(broadcast)
    red = subsChannel[0]
    rg = subsChannel[1]
    rv = subsChannel[2]
    nonEmbed = subsChannel[3]
    terminal = subsChannel[4]
    hi = subsChannel[5]
    # await recordContent()

    try:
        print("collector 1")
        await collector()
    except:
        try:
            print("collector 2")
            await collector()
        except:
            print("collector 3")
            await collector()
            os.system("kill 1")

        # await recordContent()

        # RESET Count DONT TOUCH!!!
        # desc = discord.Embed(description= f"""
        #   ======== Content ========
        #   # ‎Image ‎ +-+-+-+-+-+ ‎‎: _0_
        #   # ‎Gif ‎ ‎ ‎ ‎ ‎ ‎ ‎ +-+-+-+-+-+ ‎: _0_
        #   # ‎Video ‎ ‎ +-+-+-+-+-+ ‎: _0_
        #   # ‎Non-Format[url] ‎ + ‎: _0_
        #   # ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ +-+-+-+-+-+
        #   # ‎Total ‎ ‎ +-+-+-+-+-+ ‎ ‎: _0_
        #   ========================
        #   """)
        # await recordChannel[0].send(embed= desc)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("server --kill"):
        try:
            await terminal.send("#### KILL THE SERVER ####")
        except Exception as e:
            print(e)
        os.system("kill 1")


try:
    keep_alive()
    token = os.getenv("TOKEN")
    token = token if isinstance(token, str) else ""
    print("HELLOOOOOOOOO")
    print(token)
    bot.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        os.system("kill 1")
        print("The Discord servers denied the connection for making too many requests")
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        os.system("kill 1")
        raise e
