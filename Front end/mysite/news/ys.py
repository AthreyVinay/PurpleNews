
import urllib.request
import urllib.parse
import re

def ysearch(keyword):
    #keywords = keyword.__add__('2015')
    query_string = urllib.parse.urlencode({"search_query" : keyword})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?search_sort=video_date_uploaded&" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    result = "http://www.youtube.com/embed/" + search_results[0]
    #result2 = "http://www.youtube.com/embed/" + search_results[2]
    #result = [result1, result2]
    return result

# ysearch('nba')

# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
#
#
# # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# # tab of
# #   https://cloud.google.com/console
# # Please ensure that you have enabled the YouTube Data API for your project.
#
# argparser.print_help()
# class ysResult:
#
#     # def __init__(self, keyword):
#     #     """
#     #
#     #     :type keyword: object
#     #     """
#     #     self.keyword = keyword
#
#
#     def ysearch(self,keyword):
#         # if __name__ == "__main__":
#             to_search = keyword
#             #language = lan
#             argparser.add_argument("--q3", help="Search term", default="")
#             argparser.add_argument("--order",help="order",default="relevance")
#             #argparser.add_argument("--relevanceLanguage",help="relevanceLanguage",default=language)
#             argparser.add_argument("--max-results", help="Max results", default=5)
#             args = argparser.parse_args()
#             results= []
#             try:
#                 results = self.youtube_search(args)
#
#             except HttpError as e:
#                  print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
#
#             return results
#
#     def youtube_search(options):
#         DEVELOPER_KEY = "AIzaSyDeTeuxawKX24ZhTnJYz_yVvXMhL2CEIw0"
#         YOUTUBE_API_SERVICE_NAME = "youtube"
#         YOUTUBE_API_VERSION = "v3"
#         youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#         developerKey=DEVELOPER_KEY)
#
#         # Call the search.list method to retrieve results matching the specified
#         # query term.
#         search_response = youtube.search().list(
#         q=options.q3,
#         part="id,snippet",
#          #order=options.order,
#         #relevanceLanguage=options.relevanceLanguage,
#         maxResults=options.max_results
#         ).execute()
#
#         videos = []
#         channels = []
#         playlists = []
#
#         # Add each result to the appropriate list, and then display the lists of
#         # matching videos, channels, and playlists.
#         for search_result in search_response.get("items", []):
#             if search_result["id"]["kind"] == "youtube#video":
#                 videos.append("https://www.youtube.com/embed/"+"%s" % (search_result["id"]["videoId"]))
#             elif search_result["id"]["kind"] == "youtube#channel":
#                 channels.append("%s (%s)" % (search_result["snippet"]["title"],
#                                    search_result["id"]["channelId"]))
#             elif search_result["id"]["kind"] == "youtube#playlist":
#                 playlists.append("%s (%s)" % (search_result["snippet"]["title"],
#                                     search_result["id"]["playlistId"]))
#
#
#         return videos
#         #print ("Channels:\n", "\n".join(channels), "\n")
#         #print ("Playlists:\n", "\n".join(playlists), "\n")
#
# # t = ysResult
# # m = t.ysearch(t, 'nba')
# # m2 = t.ysearch(t, 'nba')
# #
# # print(m)