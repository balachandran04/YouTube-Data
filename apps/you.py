import streamlit as st
import pymysql
from streamlit_option_menu import option_menu
import pandas as pd
import time
from datetime import datetime
from Youtube_py import * 


def connect_to_db():
    conn = pymysql.connect(host="localhost", user="root", password="admin@123", database="youtube_sql")
    return conn




with st.sidebar:
        st.subheader(f":red[YouTube] Data Harvesting and Warehousing")
        nav_option = option_menu (
        menu_title="Menu",
        options=["Home", "Quiz","Store","Skill"],
        icons=["house","book","basket"],
        styles= {
            "nav-link" : {
                "--hover-color":"green",
                "font-weight" : "bold",
            },
            "nav-link-selected":{
                "background-color": "purple"
            }})
        if  nav_option == 'Home':
          st.sidebar.success("Welcome to Home Page 	:sparkles: ")
        elif nav_option == 'Quiz':
          st.sidebar.success("Welcome to Quizs ple solve :white_check_mark: ")
        elif nav_option == "Store":
          st.sidebar.success("Welcome  DataBase Enter the ID  ")
        else:
            st.sidebar.success("Welcome to skills Page ")

        



if nav_option == "Home":
    def fetch_channel_data(channel_id):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channel_details WHERE channel_id= %s", (channel_id,))
        data = cursor.fetchone()
        return data


    def display_channel_data(data):
        if data and len(data) >= 7:
            channel_info = {
                    "Channel Name": data[0],
                    "Description": data[1],
                    "Subscribers": data[2],
                    "Total Videos": data[3],
                    "Views": data[4],
                    "channel_id": data[5]
                }
            df = pd.DataFrame([channel_info])
            st.table(df)
            st.bar_chart(df, x='Subscribers', y='Views')

            

    def fetch_video_data(channel_id):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos_details WHERE channel_id= %s", (channel_id,))
        data = cursor.fetchall()
        return data


    def show_video(data):
        if data:
            st.subheader(":green[Videos Details]")
            
            # data[3] = data[3].astype('category')
            # df = pd.DataFrame(data,columns=["video_id","videos","discrption","pulishdata",'viewcount','like','dislike',"comments","favorite","durations","channel_id"])
            # video_info ={
            #     "video_ID", data[0],
            #     "video_name: ", data[1],
            #     "video_desciption :", data[2],
            #     "video_pulishdate: ", data[3].int(),
            #     "video_views: ", data[4],
            #     "video_likes: ", data[5],
            #     "video_dislikes: ", data[6],
            #     "video_comments: ", data[7],
            #     "durations: ", data[9]
                
            # }

            df = pd.DataFrame(data)

            st.table(df)


    def commments_data(channel_id): 
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM comments_details WHERE chan_id= %s", (channel_id,))
        data = cursor.fetchone()
        conn.close()  
        return data


    def comments_show(data):
        if data:
            st.subheader(":green[comments Details]")
            st.write("comments Text : ", data[0])
            st.write("commentID : ", data[1])
            st.write("AutherName : ", data[2])
            st.write("PulishDate : ", data[3])
            

            

    def main():
        st.subheader(":red[YouTube] Data Harvesting and Warehousing using SQL and Streamlit")

        channel_id = st.text_input(":blue[Enter YouTube Channel ID:]")
        fetch_channel = st.checkbox("**Channel Data Info**")
        fetch_video = st.checkbox(" **Video Data Info**")
        fetch_comments = st.checkbox(" **comments Data Info**")

        
       
        
        if fetch_channel:
            if channel_id:
                channel_data = fetch_channel_data(channel_id)
                display_channel_data(channel_data)
                

                
            else:
                st.warning("Please enter a valid channel ID.")

        if fetch_video:
            if channel_id:
                video_data = fetch_video_data(channel_id)
                show_video(video_data)
            else:
                st.warning("Please enter a valid channel ID.")
        if fetch_comments:
            if channel_id:
                comment = commments_data(channel_id)
                comments_show(comment)
            else:
                st.warning("Please enter a valid channel ID.")
        

    if __name__ == "__main__":
        main()


elif nav_option == "Quiz":

    qustion = st.selectbox("select your qustions",("1.What are the names of all the videos and their corresponding channels?",
                                                    "2.Which channels have the most number of videos, and how many videos do they have?",
                                                    "3.What are the top 10 most viewed videos and their respective channels?",
                                                    "4.How many comments were made on each video, and what are their corresponding video names?",
                                                    "5.Which videos have the highest number of likes, and what are their corresponding channel names?",
                                                    "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                                    "7.What is the total number of views for each channel, and what are their corresponding channel names?",
                                                    "8.What are the names of all the channels that have published videos in the year 2022?",
                                                    "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                                    "10.Which videos have the highest number of comments, and what are their corresponding channel names? "))                     

    if qustion == "1.What are the names of all the videos and their corresponding channels?":
        query = """
            SELECT cd.name AS channel_name, v.video_name AS video_name
            FROM channel_details cd
            INNER JOIN videos_details v ON cd.channel_id = v.channel_id
        """
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["channel_name", "video_name"])
        st.subheader(':green[Video Channels and Names: ]')
        st.table(df)
        

        
        
    elif qustion == "2.Which channels have the most number of videos, and how many videos do they have?":
        query = """
            SELECT  name,total_vidoe FROM channel_details ORDER BY total_vidoe DESC;

        """
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("This Channel Have Most number of video")
        df = pd.DataFrame(data, columns=["channel_name", "No of Videos"])
        st.table(df)

    elif qustion == "3.What are the top 10 most viewed videos and their respective channels?":
        query = """
            SELECT v.video_ID, v.video_name AS video_title, c.name AS channel_name, v.views
            FROM videos_details v
            INNER JOIN channel_details c ON v.channel_id = c.channel_id
            ORDER BY v.views DESC
            LIMIT 10;

            

        """
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("The Top Most viewd Videos")
        df = pd.DataFrame(data, columns=["Video_ID", "Video_Title","Channel_Name","Viwes"])
        st.table(df)

    elif qustion == "4.How many comments were made on each video, and what are their corresponding video names?":
        query = """
            SELECT v.video_id, v.video_name AS video_name, COUNT(c.CommentID) AS comment_count
            FROM videos_details v
            INNER JOIN comments_details c ON v.video_ID = c.video_ID
                GROUP BY v.video_id, v.video_name;

        """
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("comments were made on each video")
        df = pd.DataFrame(data, columns=["Video_ID", "Video_Title","Comments_Counts"])
        st.table(df)
    elif qustion == "5.Which videos have the highest number of likes, and what are their corresponding channel names?":
        query = """
                SELECT v.video_name AS video_name, c.name AS channel_name, v.likes
                FROM videos_details v
                INNER JOIN channel_details c ON v.channel_id = c.channel_id
                ORDER BY v.likes DESC
                LIMIT 10;
    """
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("highest number of likes")
        df = df = pd.DataFrame(data, columns=["Video_name", "Channel_name","Likes_Counts"])
        st.table(df)

    elif qustion == "6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
        query = """
                SELECT v.video_name AS video_name, 
                SUM(v.likes) AS total_likes, 
                SUM(v.dislikes) AS total_dislikes
                FROM videos_details v
                GROUP BY v.video_name;
        """
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("The Top Most viewd Videos")
        df = df = pd.DataFrame(data, columns=["Video_name", "Total_likes","Total_dislike"])
        st.table(df)
        
    elif qustion == "7.What is the total number of views for each channel, and what are their corresponding channel names?":
        query = """
                SELECT cd.name AS channel_name, 
                SUM(v.views) AS total_views
                FROM channel_details cd
                INNER JOIN videos_details v ON cd.channel_id = v.channel_id
                GROUP BY cd.name;
        """


        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("total number of views")
        df = df = pd.DataFrame(data, columns=["channel_name", "viwer"])
        st.table(df)
    elif qustion == "8.What are the names of all the channels that have published videos in the year 2022?":
        query = """
                SELECT DISTINCT cd.name AS channel_name
                FROM channel_details cd
                INNER JOIN videos_details v ON cd.channel_id = v.channel_id
                WHERE YEAR(v.publish) = 2022;


        """


        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        st.subheader("published videos in the year 2022")
        df = df = pd.DataFrame(data, columns=["channel_name"])
        st.table(df)

    elif qustion == "9.What is the average duration of all videos in each channel, and what are their corresponding channel names?":
        query = """
               SELECT video_name AS channelname, AVG(duration) AS averageduration 
                FROM videos_details 
                GROUP BY video_name;
        """

        import re
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=['video_name', 'duration'])
        df['duration'] = pd.to_datetime(df['duration'])
        st.table(df)
        
        

    else:
        query = """
                SELECT v.video_name AS video_title, cd.name AS channel_name
                FROM videos_details v
                INNER JOIN channel_details cd ON v.channel_id = cd.channel_id
                ORDER BY v.comments DESC
                ;


        """


        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Vidoe_names","Channel_name"])
        st.write(df)


elif nav_option == "Store":
    main()

else:
    st.header("what :red[skills] are I Used")
    st.write("1. Python")
    st.write("2. Streamlit")
    st.write("3. My_Sql")
    st.write("4. Youtube_ABI")
    st.write("5. Pandas")
    st.write("6. etc,")
    

    
    
