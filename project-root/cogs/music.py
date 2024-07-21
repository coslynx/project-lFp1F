import discord
from discord.ext import commands
import asyncio
import logging
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

logging.basicConfig(level=logging.INFO)

class MusicPlayer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.voice_client = None
        self.queue = []
        self.current_song = None
        self.volume = 0.5
        self.playback_quality = "high" 

    async def play_music(self, song_url=None):
        if song_url is None:
            if len(self.queue) > 0:
                self.current_song = self.queue.pop(0)
            else:
                await self.ctx.send("Queue is empty! Add some music.")
                return
        else:
            self.current_song = song_url

        if self.voice_client is None:
            await self.join_voice_channel()

        try:
            # Use FFmpeg to convert the audio stream to a playable format
            ffmpeg_process = subprocess.Popen(
                [
                    "ffmpeg",
                    "-i",
                    self.current_song,
                    "-vn",  # Remove video
                    "-acodec",
                    "libopus",
                    "-ar",
                    "48000",
                    "-f",
                    "opus",
                    "-",
                ],
                stdout=subprocess.PIPE,
            )

            # Play the audio using Pygame
            self.voice_client.play(
                discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(
                        ffmpeg_process.stdout,
                        bitrate=128000,
                        executable="ffmpeg",
                    ),
                    volume=self.volume,
                ),
                after=lambda error: self.check_play_next(error),
            )
            await self.ctx.send(f"Now playing: {self.current_song}")
        except Exception as e:
            logging.error(f"Error playing music: {e}")
            await self.ctx.send(f"Error playing music: {e}")

    async def stop_music(self):
        if self.voice_client is not None and self.voice_client.is_playing():
            self.voice_client.stop()
            await self.ctx.send("Stopped playing.")
        else:
            await self.ctx.send("Nothing is playing.")

    async def pause_music(self):
        if self.voice_client is not None and self.voice_client.is_playing():
            self.voice_client.pause()
            await self.ctx.send("Paused playing.")
        else:
            await self.ctx.send("Nothing is playing.")

    async def resume_music(self):
        if self.voice_client is not None and self.voice_client.is_paused():
            self.voice_client.resume()
            await self.ctx.send("Resumed playing.")
        else:
            await self.ctx.send("The player is not paused.")

    async def skip_music(self):
        if self.voice_client is not None and self.voice_client.is_playing():
            self.voice_client.stop()
            await self.ctx.send("Skipped to next song.")
        else:
            await self.ctx.send("Nothing is playing.")

    async def add_to_queue(self, song_url):
        self.queue.append(song_url)
        await self.ctx.send(f"Added {song_url} to queue.")

    def get_queue(self):
        return self.queue

    async def remove_from_queue(self, index):
        if 0 <= index < len(self.queue):
            removed_song = self.queue.pop(index)
            await self.ctx.send(f"Removed {removed_song} from queue.")
        else:
            await self.ctx.send("Invalid queue index.")

    async def clear_queue(self):
        self.queue.clear()
        await self.ctx.send("Queue cleared.")

    async def join_voice_channel(self):
        if self.voice_client is not None and self.voice_client.is_connected():
            return

        try:
            channel = self.ctx.author.voice.channel
            self.voice_client = await channel.connect()
            await self.ctx.send(f"Joined {channel.name}")
        except AttributeError:
            await self.ctx.send("You must be connected to a voice channel.")
        except discord.errors.VoiceConnectionError as e:
            logging.error(f"Error joining voice channel: {e}")
            await self.ctx.send(f"Error joining voice channel: {e}")

    async def leave_voice_channel(self):
        if self.voice_client is not None and self.voice_client.is_connected():
            await self.voice_client.disconnect()
            await self.ctx.send("Left the voice channel.")
        else:
            await self.ctx.send("Not connected to any voice channel.")

    async def adjust_volume(self, volume):
        if self.voice_client is not None and self.voice_client.is_playing():
            self.volume = volume / 100
            self.voice_client.source.volume = self.volume
            await self.ctx.send(f"Volume set to {volume}%")
        else:
            await self.ctx.send("Nothing is playing.")

    async def set_playback_quality(self, quality):
        if quality.lower() in ["high", "medium", "low"]:
            self.playback_quality = quality.lower()
            await self.ctx.send(f"Playback quality set to {self.playback_quality}.")
        else:
            await self.ctx.send("Invalid playback quality. Choose from 'high', 'medium', or 'low'.")

    def check_play_next(self, error):
        if error:
            logging.error(f"Error playing music: {error}")
            asyncio.run_coroutine_threadsafe(self.ctx.send(f"Error playing music: {error}"), self.ctx.bot.loop)
        if len(self.queue) > 0:
            asyncio.run_coroutine_threadsafe(self.play_music(), self.ctx.bot.loop)

class MusicCog(commands.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot
        self.music_players = {}  # Store music players for each server

    @commands.command(name="play", help="Plays a song from YouTube, Spotify, or SoundCloud.")
    async def play(self, ctx, *, song_url):
        server_id = ctx.guild.id
        if server_id not in self.music_players:
            self.music_players[server_id] = MusicPlayer(ctx)
        player = self.music_players[server_id]
        await player.join_voice_channel()
        await player.add_to_queue(song_url)

        if not player.voice_client.is_playing():
            await player.play_music()

    @commands.command(name="stop", help="Stops the currently playing song.")
    async def stop(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.stop_music()

    @commands.command(name="pause", help="Pauses the currently playing song.")
    async def pause(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.pause_music()

    @commands.command(name="resume", help="Resumes playback after pausing.")
    async def resume(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.resume_music()

    @commands.command(name="skip", help="Skips to the next song in the queue.")
    async def skip(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.skip_music()

    @commands.command(name="queue", help="Shows the current playback queue.")
    async def queue(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            queue = player.get_queue()
            if len(queue) > 0:
                await ctx.send(f"Queue: {', '.join(queue)}")
            else:
                await ctx.send("Queue is empty.")
        else:
            await ctx.send("No music player is active on this server.")

    @commands.command(name="remove", help="Removes a song from the queue by index.")
    async def remove(self, ctx, index: int):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.remove_from_queue(index)
        else:
            await ctx.send("No music player is active on this server.")

    @commands.command(name="clear", help="Clears the entire playback queue.")
    async def clear(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.clear_queue()
        else:
            await ctx.send("No music player is active on this server.")

    @commands.command(name="join", help="Connects the bot to your voice channel.")
    async def join(self, ctx):
        server_id = ctx.guild.id
        if server_id not in self.music_players:
            self.music_players[server_id] = MusicPlayer(ctx)
        player = self.music_players[server_id]
        await player.join_voice_channel()

    @commands.command(name="leave", help="Disconnects the bot from the voice channel.")
    async def leave(self, ctx):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.leave_voice_channel()
        else:
            await ctx.send("Not connected to any voice channel.")

    @commands.command(name="volume", help="Sets the playback volume (0-100).")
    async def volume(self, ctx, volume: int):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.adjust_volume(volume)
        else:
            await ctx.send("No music player is active on this server.")

    @commands.command(name="quality", help="Sets the playback quality (high, medium, low).")
    async def quality(self, ctx, quality: str):
        server_id = ctx.guild.id
        if server_id in self.music_players:
            player = self.music_players[server_id]
            await player.set_playback_quality(quality)
        else:
            await ctx.send("No music player is active on this server.")

def setup(bot):
    bot.add_cog(MusicCog(bot))