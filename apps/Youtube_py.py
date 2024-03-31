import streamlit as st
import os
import googleapiclient.discovery
import pymysql
from datetime import datetime
from googleapiclient.errors import HttpError

def connection():
    conn = pymysql.connect(host="localhost", user="root", password="admin@123", database="youtube_sql")
    return conn

# Function to store channel data, videos, and comments into MySQL
def store_data(channel_id, api_key):
    conn = connection()
    cursor = conn.cursor()

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics,status",
        id=channel_id
    )
    response = request.execute()

    for item in response['items']:
        channel_id = item["id"]
        name = item["snippet"]["title"]
        subscribers = item["statistics"]["subscriberCount"]
        viewer = item["statistics"]["viewCount"]
        total_video = item["statistics"]["videoCount"]
        description = item["snippet"]["description"]
        uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]

        insert_query = "INSERT INTO channel_details (channel_id ,Name, description, subscribers, total_vidoe, viwer) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (channel_id, name, description, subscribers, total_video, viewer)
        cursor.execute(insert_query, values)
        conn.commit()
#videos
        next_page_token = None
        while True:
                request = youtube.playlistItems().list(
                    part="snippet",
                    playlistId=uploads,
                    maxResults=50,
                    pageToken=next_page_token
                )

                response = request.execute()

                for item in response.get("items", []):
                    video_id = item["snippet"]["resourceId"]["videoId"]

                    video_request = youtube.videos().list(
                        part="snippet,statistics,status,contentDetails",
                        id=video_id
                    )

                    video_response = video_request.execute()

                    for video_item in video_response["items"]:
                        video_ID = video_item["id"]
                        video_name = video_item["snippet"]["title"]
                        video_description = video_item["snippet"]["description"]
                        publish_str = video_item["snippet"]["publishedAt"]  # format
                        publish = datetime.strptime(publish_str, "%Y-%m-%dT%H:%M:%SZ")
                        views = video_item['statistics']['viewCount']
                        likes = video_item['statistics']['likeCount']
                        dislikes = video_item['statistics'].get('dislikeCount', 0)
                        comments = video_item['statistics'].get('commentCount', 0)
                        favorite = video_item["statistics"].get('favoriteCount', 0)
                        duration = video_item["contentDetails"]["duration"]
                        channel = video_item["snippet"]["channelId"]
                        
                        insert_data = "INSERT INTO videos_details (video_ID, video_name, video_description, publish, views, likes, dislikes, comments, favorite, duration, channel_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        values = (video_ID, video_name, video_description, publish, views, likes, dislikes, comments, favorite, duration, channel)
                        cursor.execute(insert_data, values)
                        conn.commit()
                        

                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break  

                #cooments 

                try:
                    response = youtube.commentThreads().list(
                        part='snippet',
                        videoId=video_id,
                        maxResults=50
                    ).execute()

                    for comment_item in response['items']:
                        comment = comment_item['snippet']['topLevelComment']['snippet']['textDisplay']
                        com_ID = comment_item["id"]
                        com_author = comment_item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        com_publish = comment_item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                        com_like = comment_item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                        videoid = comment_item["snippet"]["videoId"]
                        chan_id  = comment_item["snippet"]["channelId"]

                        insert_data = """INSERT INTO comments_details values(%s,%s,%s,%s,%s,%s,%s)"""
                        value = (comment, com_ID, com_author, com_publish, com_like, videoid,chan_id)
                        cursor.execute(insert_data, value)
                        conn.commit()

                except HttpError as e:
                    error_message = e._get_reason()
                    if 'commentsDisabled' in error_message:
                        print("Comments are disabled for this video.")
                    else:
                        print("An error occurred:", error_message)

           
def main():
    st.title("YouTube Data Storage")
    channel_id = st.text_input("Enter YouTube Channel ID:")
    if st.button("Store Data"):
        API_KEY = "AIzaSyA4DtJWY9upkUMybPKEZMfps28meIE-BFY"
        if channel_id:
            store_data(channel_id, API_KEY)
            st.success("Data stored successfully!")
        else:
            st.error("Please enter a valid YouTube Channel ID.")








