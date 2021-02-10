### word2vec을 이용한 대분류 매칭

big_topic = ['악세서리',
             '뷰티', '헤어', '화장품',
             '패션', '옷차림',
             '주류',
             '동물', '팻',
             '자동차', '오토바이',
             '키즈', '장난감', '육아',
             '커피', '전통차', '음료',
             '교육',
             '경제', '금융',
             '스포츠', '야외활동', '캠핑',
             '음식', '요리', '레시피', '식품',
             '피트니스', '헬스', '운동',
             '게임',
             '예술',
             '의료', '약',
             '기계', '테크놀로지',
             '음악',
             '웨딩',
             '책', '저널', '뉴스',
             '비즈니스', '직업', '경력', '취업',
             'DIY', '수공예',
             '개그', '재미',
             '리빙', '인테리어', '가구',
             '매니지먼트', '마케팅', '경영', '전략',
             '여행', '항공', '관광', '휴양',
             'TV', '영화', '드라마']

import MeCab

m = MeCab.Tagger()
import gensim
from gensim.models import Word2Vec
import pandas as pd
from sklearn.manifold import TSNE
from scipy import spatial
import numpy as np

for x in range(len(video_info)):
    video_info.loc[x, 'title_tag'] = video_info['video_title'][x] + ' ' + video_info['tags'][x]

video_info

# 학습된 임베딩 벡터 호출하여 사용
from gensim.models import Word2Vec

model = Word2Vec.load('/Users/yeogyeongi/Desktop/Hifen/word2vec/word2vec')
my_dict = dict({})
for idx, key in enumerate(model.wv.vocab):
    my_dict[key] = model.wv[key]

# 영상 제목 + 태그 + 상세정보 임베딩
word2vec_data = pd.DataFrame(video_info.groupby('channel_id')['title_tag'])
word2vec_data.columns = ['channel_id', 'context']

for x in range(len(word2vec_data)):
    word2vec_data.loc[x, 'context'] = ' '.join(word2vec_data['context'][x])
word2vec_data


def tokenize(sentence):
    s = ([x.split("\t")[0] for x in m.parse(sentence).split("\n") if not x == "EOS" and not x == ""])
    return s


video_info_data = []
for x in word2vec_data['context']:
    video_info_data.append(tokenize(x))

word2vec_data['topic'] = 0

# 대토픽 분류 임베딩 -> 토큰화 후 임베딩 된것 더해주기 (예) 전자기기 -> 전자 + 기기 (각 임베딩 더해주기)
category_vector = []
for i in range(len(big_topic)):
    try:
        category_vector.append(tokenize(big_topic[i]))
    except Exception as e:
        continue

category_vector2 = []
for x in range(len(category_vector)):
    temp = np.repeat(0, 100)
    for y in range(len(category_vector[x])):
        temp = temp + my_dict[category_vector[x][y]]
    category_vector2.append(temp)

category_vector2 = pd.DataFrame(category_vector2)

# word2vec 유사도 계산
for y in range(len(video_info_data)):
    video_info_vector = np.repeat(0, 100)
    most_similar = []

    for x in range(len(video_info_data[y])):
        try:
            video_info_vector = video_info_vector + my_dict[video_info_data[y][x]]
        except:
            pass

    sim_score = np.max(category_vector2.apply(lambda x: 1 - spatial.distance.cosine(x, video_info_vector), axis=1))

    if sim_score >= 0.5:
        # most_similar = big_topic[np.argmax(category_vector.apply(lambda x:  1 - spatial.distance.cosine(x, video_info_vector),axis=1))]
        most_similar.append(big_topic[np.argsort(
            category_vector2.apply(lambda x: 1 - spatial.distance.cosine(x, video_info_vector), axis=1))[
            len(big_topic) - 1]])
        most_similar.append(big_topic[np.argsort(
            category_vector2.apply(lambda x: 1 - spatial.distance.cosine(x, video_info_vector), axis=1))[
            len(big_topic) - 2]])
        most_similar.append(big_topic[np.argsort(
            category_vector2.apply(lambda x: 1 - spatial.distance.cosine(x, video_info_vector), axis=1))[
            len(big_topic) - 3]])

    word2vec_data.loc[y, 'topic'] = ', '.join(most_similar)

word2vec_data

