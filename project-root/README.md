# Discord Music Bot

This is a Discord bot designed to play music in voice channels. It integrates with YouTube, Spotify, and SoundCloud, allowing users to enjoy music together within their Discord servers.

## Features:

- **Music Playback:**
    - Play songs from YouTube, Spotify, and SoundCloud.
    - Support for various audio formats (MP3, WAV, etc.).
- **Queue Management:**
    - Add songs to a queue for continuous playback.
    - View, reorder, and remove songs from the queue.
- **Voice Channel Management:**
    - Join and leave voice channels for music playback.
    - Adjust volume and playback quality.
- **User Interaction:**
    - Use text and voice commands for easy interaction.
    - Help and information commands for guidance.
- **Customizations:**
    - Define music preferences like genres and playlists.
    - Customize bot appearance (e.g., custom prefixes, welcome messages).

## Installation

1. **Create a Virtual Environment:**
   ```bash
   python -m venv env
   ```
2. **Activate the Virtual Environment:**
   ```bash
   source env/bin/activate
   ```
3. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Create a Discord Application:**
   - Go to [https://discord.com/developers/applications](https://discord.com/developers/applications).
   - Create a new application.
2. **Add a Bot User:**
   - Add a bot user to your application.
3. **Create a `.env` File:**
   - Create a `.env` file with the following environment variables:
   ```
   DISCORD_TOKEN=your_discord_bot_token
   YOUTUBE_API_KEY=your_youtube_api_key
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   SOUNDCLOUD_CLIENT_ID=your_soundcloud_client_id
   SOUNDCLOUD_CLIENT_SECRET=your_soundcloud_client_secret
   # DATABASE_URL=your_database_connection_string (if using a database)
   ```
   - Replace the placeholders with your actual API keys and tokens.
4. **Configure the Database (Optional):**
   - If you choose to use a database (PostgreSQL or MongoDB), configure the `DATABASE_URL` environment variable in your `.env` file and update the database connection settings in the `main.py` file.

## Running the Bot

```bash
python main.py
```

## Usage

**Commands:**

- `!play <song_name>`: Plays a song from YouTube, Spotify, or SoundCloud.
- `!queue`: Shows the current playback queue.
- `!skip`: Skips to the next song in the queue.
- `!stop`: Stops playback.
- `!join`: Joins the current voice channel.
- `!leave`: Leaves the current voice channel.
- `!volume <volume>`: Sets the playback volume (0-100).
- **More commands will be available based on the bot's implementation.**

## Contribution

Contributions are welcome! Please follow these guidelines:

- Fork the repository.
- Create a new branch for your changes.
- Make your changes and commit them.
- Push your changes to your fork.
- Create a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- Discord.py
- FFmpeg
- Pygame
- requests
- asyncio
- PyNaCl
- dotenv
- psycopg2 (or pymongo)
- logging
- SpeechRecognition