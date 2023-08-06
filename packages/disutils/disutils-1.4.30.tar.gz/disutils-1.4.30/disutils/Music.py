import random
from warnings import warn
import aiohttp
import re

try:
    import youtube_dl
    import discord

    has_voice = True
except ImportError:
    has_voice = False

if has_voice:
    youtube_dl.utils.bug_reports_message = lambda: ""
    ytdl = youtube_dl.YoutubeDL(
        {
            "format": "bestaudio/best",
            "restrictfilenames": True,
            "noplaylist": True,
            "nocheckcertificate": True,
            "ignoreerrors": True,
            "logtostderr": False,
            "quiet": True,
            "no_warnings": True,
            "source_address": "0.0.0.0",
        }
    )


# ANCHOR Exceptions
class EmptyQueue(Exception):
    """Cannot skip because queue is empty"""


class NotConnectedToVoice(Exception):
    """Cannot create the player because bot is not connected to voice"""


class NotPlaying(Exception):
    """Cannot <do something> because nothing is being played"""


class YoutubeError(Exception):
    pass


# ANCHOR Song
class Song(object):
    def __init__(self, source: str, data: dict):
        self.source = source
        self.data = data
        self.is_looping = False

    def __getattribute__(self, __name: str):
        """Get the attribute from self or from self.data"""
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            try:
                return self.data[__name]
            except KeyError:
                raise AttributeError(
                    f"'{__name}' is not an attribute of {self} nor a key of {self.data}")


async def ytbettersearch(query):
    """This opens youtube.com and searches for the query, then returns the first result"""
    url = f"https://www.youtube.com/results?search_query={query}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
    regex = r"(?<=watch\?v=)\w+"
    v = re.search(regex, html).group()
    url = f"https://www.youtube.com/?v={v}"
    return url


def is_url(url):
    """This checks if url is a url or not"""
    if re.match(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        url,
    ):
        return True
    else:
        return False


async def get_video_data(self, query, bettersearch, loop) -> Song:
    """This gets the video data from youtube.com and returns it as a Song object"""
    if not has_voice:
        raise RuntimeError(
            "disutils[voice] install needed in order to use voice")

    if not is_url(query) and not bettersearch:
        ytdl_ = youtube_dl.YoutubeDL(
            {
                "format": "bestaudio/best",
                "restrictfilenames": True,
                "noplaylist": True,
                "nocheckcertificate": True,
                "ignoreerrors": True,
                "logtostderr": False,
                "quiet": True,
                "no_warnings": True,
                "default_search": "auto",
                "source_address": "0.0.0.0",
            }
        )
        data = await loop.run_in_executor(
            None, lambda: ytdl_.extract_info(query, download=False)
        )
        try:
            data = data["entries"][0]
        except KeyError or TypeError:
            pass
        del ytdl_
    else:
        if not is_url(query) and bettersearch:
            url = await ytbettersearch(query)
        elif is_url(query):
            url = query
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=False)
        )
        if data is None:
            raise YoutubeError()

    return Song(data["url"], data)


def play_next(ctx, opts, music, after, loop):
    """This should not be called directly!"""
    if not has_voice:
        raise RuntimeError(
            "disutils[voice] install needed in order to use voice")

    try:
        player = music.get_player(ctx)
        queue = player._song_queue
        song = queue[0]
    except NotConnectedToVoice or IndexError:
        return

    if song.is_looping:
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(queue[0].source, **opts), player.volume)
        ctx.voice_client.play(
            source, after=lambda _e: after(ctx, opts, music, after, loop))
    else:
        try:
            queue.pop(0)
        except IndexError:
            player.stop()
            return

        if len(queue) > 0:
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(queue[0].source, **opts), player.volume)
            ctx.voice_client.play(
                source, after=lambda _e: after(ctx, opts, music, after, loop))


# ANCHOR Music
class Music(object):
    def __init__(self):
        if not has_voice:
            raise RuntimeError(
                "disutils[voice] install needed in order to use voice")
        self.players = []  # List of MusicPlayers

    def create_player(self, ctx, **kwargs):
        """This creates a new MusicPlayer. 
        This should not be called directly as the new update creates a new player with the get_player method if there is none."""
        if not ctx.voice_client:
            raise NotConnectedToVoice(
                "Cannot create the player because bot is not connected to voice"
            )
        player = MusicPlayer(ctx, self, **kwargs)
        self.players.append(player)
        return player

    def get_player(self, ctx):
        """This gets the player from the ctx or creates a new one if there is none in that context"""
        for player in self.players:
            if player.voice_client.channel == ctx.voice_client.channel:
                return player
        return self.create_player(ctx)


# ANCHOR MusicPlayer
class MusicPlayer(object):
    def __init__(self, ctx, music):
        if not has_voice:
            raise RuntimeError(
                "disutils[voice] install needed in order to use voice")
        self.ctx = ctx
        self.voice_client = ctx.voice_client
        self.loop = ctx.bot.loop
        self.bot = ctx.bot
        self.music = music
        self._song_queue = []
        self.after_func = play_next
        self.volume = .5
        self.ffmpeg_options = {
            "options": "-vn -loglevel quiet -hide_banner -nostats",
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 0 -nostdin",
        }

    @property
    def song_queue(self):
        return self._song_queue[1:]

    @property
    def is_playing(self):
        return self.voice_client.is_playing()

    async def queue(self, query, bettersearch=True):
        """Adds the query to the queue"""
        song = await get_video_data(self, query, bettersearch, self.loop)
        self._song_queue.append(song)
        self.bot.dispatch("disutils_music_queue", self.ctx, song)
        return song

    async def play(self):
        """This plays the first song in the queue"""
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(
            self._song_queue[0].source, **self.ffmpeg_options), self.volume)
        self.voice_client.play(
            source,
            after=lambda error: self.after_func(
                self.ctx,
                self.ffmpeg_options,
                self.music,
                self.after_func,
                self.loop,
            ),
        )
        song = self._song_queue[0]
        self.bot.dispatch("disutils_music_play", self.ctx, song)
        return song

    async def skip(self, force=True):
        """This skips the current song"""
        if len(self._song_queue) == 0:
            raise NotPlaying("Cannot loop because nothing is being played")
        elif not len(self._song_queue) > 1 and not force:
            raise EmptyQueue("Cannot skip because queue is empty")
        else:
            old = self._song_queue[0]
            old.is_looping = True if old.is_looping else False
            self.voice_client.stop()
            try:
                new = self._song_queue[1]
                self.bot.dispatch("disutils_music_skip", self.ctx, old, new)
                return (old, new)
            except IndexError:
                self.bot.dispatch("disutils_music_skip", self.ctx, old, None)
                return (old, None)

    async def stop(self):
        """Stops the player and clears the queue"""
        try:
            self._song_queue = []
            self.voice_client.stop()
            self.music.players.remove(self)
        except:
            raise NotPlaying("Cannot loop because nothing is being played")
        self.bot.dispatch("disutils_music_stop", self.ctx)

    async def pause(self):
        """Pauses the player"""
        try:
            self.voice_client.pause()
            song = self._song_queue[0]
        except:
            raise NotPlaying("Cannot pause because nothing is being played")
        self.bot.dispatch("disutils_music_pause", self.ctx, song)
        return song

    async def resume(self):
        """Resumes the player if it is paused"""
        try:
            self.voice_client.resume()
            song = self._song_queue[0]
        except:
            raise NotPlaying("Cannot resume because nothing is being played")
        self.bot.dispatch("disutils_music_resume", self.ctx, song)
        return song

    def current_queue(self):
        warn("player.current_queue() is deprecated, use player.song_queue instead",
             DeprecationWarning, stacklevel=2)
        return self._song_queue

    def now_playing(self):
        """Returns the song that is currently playing"""
        try:
            return self._song_queue[0]
        except:
            return None

    async def toggle_song_loop(self):
        """Toggles the current songs looping"""
        try:
            song = self._song_queue[0]
        except:
            raise NotPlaying("Cannot loop because nothing is being played")
        if not song.is_looping:
            song.is_looping = True
        else:
            song.is_looping = False
        self.bot.dispatch("disutils_music_toggle_loop", self.ctx, song)
        return song

    async def change_volume(self, vol: float):
        """Changes the volume of the player"""
        self.voice_client.source.volume = self.volume = vol
        try:
            song = self._song_queue[0]
        except:
            raise NotPlaying(
                "Cannot change volume because nothing is being played")
        self.bot.dispatch("disutils_music_volume_change", self.ctx, song, vol)
        return (song, vol)

    async def remove_from_queue(self, index):
        """Removes a song from the queue"""
        if index == 0:
            try:
                song = self._song_queue[0]
            except:
                raise NotPlaying("Cannot loop because nothing is being played")
            await self.skip(force=True)
            return song
        song = self._song_queue[index]
        self._song_queue.pop(index)
        self.bot.dispatch("disutils_music_remove_from_queue", self.ctx, song)
        return song

    def shuffle_queue(self):
        """Shuffles the queue"""
        # The reason i don't just use random.shuffle is because the 0. element is the current song and should not be shuffled
        self._song_queue = [self._song_queue[0], *
                            random.sample(self._song_queue[1:], len(self._song_queue[1:]))]
