from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


YOUTUBE_ID = ['channel-id']
DEVELOPER_KEY = "token-key"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


# 1. 채널정보 수집
def get_channel_info(idn, maxResults):
    data = youtube.channels().list(part="snippet", id=idn).execute()
    data1 = youtube.channels().list(part="statistics", id=idn).execute()
    data2 = youtube.channels().list(part="brandingSettings", id=idn).execute()

    channel_id = idn  # 채널 고유 아이디
    channel_title = data['items'][0]['snippet']['title']  # 채널 타이틀
    channel_description = data['items'][0]['snippet']['description']  # 채널 정보
    try:
        channel_topic = data2['items'][0]['brandingSettings']['channel']['keywords']  # 채널 키워드
    except:
        channel_topic = ''

    tot_view_cnt = data1['items'][0]['statistics']['viewCount']  # 총 뷰 수
    tot_subs_cnt = data1['items'][0]['statistics']['subscriberCount']  # 총 구독자 수
    tot_video_cnt = data1['items'][0]['statistics']['videoCount']  # 총 비디오 수

    # 한 채널의 최근 5 개 동영상 리스트 가져오기
    videos = youtube.search().list(part="snippet", channelId=idn, maxResults=maxResults, order='date').execute()

    videos_list = []

    for x in range(maxResults):
        videos_list.append(videos['items'][x]['id']['videoId'])

    result = [channel_id, channel_title, channel_description, channel_topic, tot_view_cnt, tot_subs_cnt, tot_video_cnt,
              videos_list]
    return result


# 데이터 적재
channel_info = []
maxResults = 30

for x in YOUTUBE_ID:
    channel_info.append(get_channel_info(x, maxResults))

channel_info = pd.DataFrame(channel_info)
channel_info.columns = ['channel_id', 'channel_title', 'channel_description', 'channel_topic', 'tot_view_cnt',
                        'tot_subs_cnt', 'tot_video_cnt', 'videos_list']

channel_info

# 2. 영상 반응 수치 수집
from youtube_transcript_api import YouTubeTranscriptApi


def get_video(idn):
    videos = youtube.videos().list(part="statistics", id=idn).execute()
    videos2 = youtube.videos().list(part="contentDetails", id=idn).execute()
    videos3 = youtube.videos().list(part="snippet", id=idn).execute()
    comment_response = youtube.commentThreads().list(part="snippet", videoId=idn, textFormat='plainText',
                                                     maxResults=100).execute()
    try:
        caption = YouTubeTranscriptApi.get_transcript(idn, languages=['ko'])
    except:
        caption = ''

    channel_Id = videos3['items'][0]['snippet']['channelId']  # 채널 아이디
    video_Id = videos3['items'][0]['id']  # 비디오 아이디

    title = videos3['items'][0]['snippet']['title']  # 영상 제목
    description = videos3['items'][0]['snippet']['description']  # 영상 설명

    try:
        tags = ' '.join(videos3['items'][0]['snippet']['tags'])  # 영상 태그
    except:
        tags = ''

    publishedAt = videos3['items'][0]['snippet']['publishedAt']  # 영상 게시일
    publishedAt = publishedAt.replace('T', ' ').replace('Z', '')

    duration = videos2['items'][0]['contentDetails']['duration']  # 영상 길이
    duration = duration.replace('PT', '').replace('M', '분').replace('S', '초')

    commentCount = videos['items'][0]['statistics']['commentCount']  # 댓글수
    likeCount = videos['items'][0]['statistics']['likeCount']  # 좋아요수
    dislikeCount = videos['items'][0]['statistics']['dislikeCount']  # 싫어요
    viewCount = videos['items'][0]['statistics']['viewCount']  # 조회수

    caption = ' '.join([x['text'] for x in caption])  # 한글 자막

    data = [channel_Id, video_Id, title, description, tags, publishedAt, duration, commentCount, likeCount,
            dislikeCount, viewCount, caption]

    return data


# 데이터 적재
video_info = []

for x in range(len(YOUTUBE_ID)):
    for y in range(maxResults):
        video_info.append(get_video(channel_info['videos_list'][x][y]))

video_info = pd.DataFrame(video_info)
video_info.columns = ['channel_id', 'video_id', 'video_title', 'description', 'tags', 'publishedAt', 'duration',
                      'commentCount', 'likeCount', 'dislikeCount', 'viewCount', 'caption']


# 3. 비디오 댓글 수집
def get_comment(channel_id, video_id):
    comments = []

    comment_response = youtube.commentThreads().list(
        videoId=video_id,
        order='time',
        part='snippet',
        textFormat='plainText',
        maxResults=100
    ).execute()

    while comment_response:
        for item in comment_response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if 'nextPageToken' in comment_response:
            pageToken = comment_response['nextPageToken']
            comment_response = youtube.commentThreads().list(
                videoId=video_id,
                order='time',
                part='snippet',
                textFormat='plainText',
                pageToken=pageToken,
                maxResults=100
            ).execute()
        else:
            break

    channel_id = channel_id  # 채널 고유 아이디
    video_id = comment_response['items'][0]['snippet']['videoId']  # 비디오 고유 아이디
    comment_cnt_rp_x = len(comments)  # 대댓글 없는 전체 댓글 수
    comments = ' '.join(comments)  # 댓글 내용

    data = [channel_id, video_id, comment_cnt_rp_x, comments]
    return data


# 데이터 적재
video_comment = []

for x in range(len(YOUTUBE_ID)):
    for y in range(maxResults):
        video_comment.append(get_comment(YOUTUBE_ID[x], channel_info['videos_list'][x][y]))

video_comment = pd.DataFrame(video_comment)
video_comment.columns = ['channel_id', 'video_id', 'comment_cnt_rp_x', 'comments']

