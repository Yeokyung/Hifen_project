# LDA 분석
data_lda = []
for x in range(len(video_info)):
        video_info.loc[x, 'lda_noun'] = text_processing(video_info['video_title'][x]) + ' ' + text_processing(video_info['description'][x]) + ' ' + text_processing(video_info['tags'][x])
video_info

# DTA matrix 생성
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df = 2, max_features= 1000)
X = vectorizer.fit_transform(video_info['lda_noun'])
X.shape # 문서 갯수 x 단어 갯수

# LDA 파라미터 그리드 서치
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from pprint import pprint

## 그리드 서치
# 파라미터 서치
search_params = {'n_components': [2,3,4,5,6,7,8,9,10], 'learning_decay': [.5, .7, .9]}

lda = LatentDirichletAllocation(max_iter=5, learning_method='online', learning_offset=50.,random_state=0)

model = GridSearchCV(lda, param_grid=search_params)

model.fit(X)

# 최적의 모델
best_lda_model = model.best_estimator_

# 파라미터 모델
print("Best Model's Params: ", model.best_params_)

# 최적의 스코어
print("Best Log Likelihood Score: ", model.best_score_)

# perplextiy 계산
print("Model Perplexity: ", best_lda_model.perplexity(X))


# 문서 - 토픽 행렬 -> 인플루언서 별로 할당확률 보기
lda_output = best_lda_model.transform(X)

# 토픽 명
topicnames = ["Topic" + str(i) for i in range(best_lda_model.n_components)]

# 문서 명
docnames = [i for i in video_info['channel_id']]

df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames)
df_document_topic['docnames'] = docnames

# 인플루언서별 평균 할당확률
df_document_topic = df_document_topic.groupby('docnames').mean()

dominant_topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic['dominant_topic'] = dominant_topic
df_document_topic


# 토픽 - 단어 행렬
df_topic_keywords = pd.DataFrame(best_lda_model.components_)

df_topic_keywords.columns = vectorizer.get_feature_names()
df_topic_keywords.index = topicnames

# 각 토픽에서 상위 n개 단어들 확인
# Show top n keywords for each topic
def show_topics(vectorizer, lda_model, n_words):
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
    return topic_keywords

topic_keywords = show_topics(vectorizer=vectorizer, lda_model=best_lda_model, n_words=20)

# 토픽 - 상위 n개 단어 데이터 프래임
df_topic_keywords = pd.DataFrame(topic_keywords)
df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
df_topic_keywords.transpose()