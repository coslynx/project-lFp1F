import os
import psycopg2
import pymongo
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        self.database_type = os.getenv("DATABASE_TYPE", "postgresql")  # Default to PostgreSQL

        self.connection = None  # Initialize connection as None

        if self.database_type.lower() == "postgresql":
            self.connect_postgresql()
        elif self.database_type.lower() == "mongodb":
            self.connect_mongodb()

    def connect_postgresql(self):
        """Connects to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.cursor = self.connection.cursor()
            print("Connected to PostgreSQL database.")
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")

    def connect_mongodb(self):
        """Connects to the MongoDB database."""
        try:
            self.connection = pymongo.MongoClient(self.database_url)
            self.db = self.connection["discord_music_bot"]
            print("Connected to MongoDB database.")
        except Exception as e:
            print(f"Error connecting to MongoDB database: {e}")

    def create_tables(self):
        """Creates tables or collections in the database (if using PostgreSQL)."""
        if self.database_type.lower() == "postgresql":
            try:
                # Create tables (if using PostgreSQL)
                # Replace with your actual table creation queries
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS servers (
                        server_id BIGINT PRIMARY KEY,
                        prefix VARCHAR(10),
                        music_channel BIGINT,
                        log_channel BIGINT
                    );
                """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        server_id BIGINT,
                        preferences JSONB
                    );
                """)
                self.connection.commit()
                print("Tables created successfully.")
            except Exception as e:
                print(f"Error creating tables: {e}")

    def set_server_prefix(self, server_id, prefix):
        """Sets the command prefix for a server."""
        if self.database_type.lower() == "postgresql":
            try:
                self.cursor.execute(
                    "INSERT INTO servers (server_id, prefix) VALUES (%s, %s) ON CONFLICT (server_id) DO UPDATE SET prefix = %s",
                    (server_id, prefix, prefix),
                )
                self.connection.commit()
                print(f"Prefix set for server {server_id}: {prefix}")
            except Exception as e:
                print(f"Error setting prefix: {e}")
        elif self.database_type.lower() == "mongodb":
            try:
                self.db.servers.update_one(
                    {"server_id": server_id},
                    {"$set": {"prefix": prefix}},
                    upsert=True,
                )
                print(f"Prefix set for server {server_id}: {prefix}")
            except Exception as e:
                print(f"Error setting prefix: {e}")

    def get_server_prefix(self, server_id):
        """Retrieves the command prefix for a server."""
        if self.database_type.lower() == "postgresql":
            try:
                self.cursor.execute("SELECT prefix FROM servers WHERE server_id = %s", (server_id,))
                result = self.cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
            except Exception as e:
                print(f"Error getting prefix: {e}")
                return None
        elif self.database_type.lower() == "mongodb":
            try:
                server_data = self.db.servers.find_one({"server_id": server_id})
                if server_data:
                    return server_data.get("prefix")
                else:
                    return None
            except Exception as e:
                print(f"Error getting prefix: {e}")
                return None

    def set_server_channel(self, server_id, action, channel_id):
        """Sets a specific channel for bot actions (e.g., music playback)."""
        if self.database_type.lower() == "postgresql":
            try:
                self.cursor.execute(
                    f"UPDATE servers SET {action}_channel = %s WHERE server_id = %s",
                    (channel_id, server_id),
                )
                self.connection.commit()
                print(f"{action.capitalize()} channel set for server {server_id}: {channel_id}")
            except Exception as e:
                print(f"Error setting {action} channel: {e}")
        elif self.database_type.lower() == "mongodb":
            try:
                self.db.servers.update_one(
                    {"server_id": server_id},
                    {"$set": {f"{action}_channel": channel_id}},
                    upsert=True,
                )
                print(f"{action.capitalize()} channel set for server {server_id}: {channel_id}")
            except Exception as e:
                print(f"Error setting {action} channel: {e}")

    def get_server_channel(self, server_id, action):
        """Retrieves the channel ID for a specific action on a server."""
        if self.database_type.lower() == "postgresql":
            try:
                self.cursor.execute(
                    f"SELECT {action}_channel FROM servers WHERE server_id = %s",
                    (server_id,),
                )
                result = self.cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
            except Exception as e:
                print(f"Error getting {action} channel: {e}")
                return None
        elif self.database_type.lower() == "mongodb":
            try:
                server_data = self.db.servers.find_one({"server_id": server_id})
                if server_data:
                    return server_data.get(f"{action}_channel")
                else:
                    return None
            except Exception as e:
                print(f"Error getting {action} channel: {e}")
                return None

    def close_connection(self):
        """Closes the database connection."""
        if self.connection:
            if self.database_type.lower() == "postgresql":
                self.cursor.close()
                self.connection.close()
                print("PostgreSQL database connection closed.")
            elif self.database_type.lower() == "mongodb":
                self.connection.close()
                print("MongoDB database connection closed.")

    def __del__(self):
        """Closes the database connection when the object is garbage collected."""
        self.close_connection()