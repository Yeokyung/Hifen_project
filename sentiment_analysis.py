
import urllib.request
import pandas as pd

# 네이버 영화 리뷰 데이터 호출
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt", filename="ratings_train.txt")
urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt", filename="ratings_test.txt")

train_data = pd.read_table('ratings_train.txt')
test_data = pd.read_table('ratings_test.txt')

train_data = pd.DataFrame(train_data)
train_data.columns = ['id','text','label']
X_train = train_data['text']
Y_train = train_data['label']

test_data = pd.DataFrame(test_data)
test_data.columns = ['id','text','label']
X_test = test_data['text']
Y_test = test_data['label']

# train data 토큰 모음
tokens = [y for x in X_train for y in x]

# 가장 자주 사용되는 단어
import nltk
text = nltk.Text(tokens, name='NMSC')

# 전체 토큰의 개수
print(len(text.tokens))

# 중복을 제외한 토큰의 개수
print(len(set(text.tokens)))

# 출현 빈도가 높은 상위 토큰 10개
print(text.vocab().most_common(10))

# CountVectorization
# 시간이 꽤 걸림 -> 가장 많이 나온 단어 10000개
selected_words = [f[0] for f in text.vocab().most_common(1000)]

def term_frequency(doc):
    return [doc.count(word) for word in selected_words]

train_x = [term_frequency(d) for d in X_train]
test_x = [term_frequency(d) for d in X_test]
train_y = [c for c in Y_train]
test_y = [c for c in Y_test]

# 데이터 float형으로 변환
import numpy as np

x_train = np.asarray(train_x).astype('float32')
x_test = np.asarray(test_x).astype('float32')
y_train = np.asarray(train_y).astype('float32')
y_test = np.asarray(test_y).astype('float32')

x_train.shape

# 모형 학습
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(1000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=optimizers.RMSprop(lr=0.001),
             loss=losses.binary_crossentropy,
             metrics=[metrics.binary_accuracy])


training_samples = 100000
validation_samples = 49995
epoch = 100

x_train2 = x_train[:training_samples]
y_train2 = y_train[:training_samples]
x_val = x_train[training_samples: training_samples + validation_samples]
y_val = y_train[training_samples: training_samples + validation_samples]

history = model.fit(x_train, y_train, epochs=epoch, batch_size=32, validation_data=(x_val, y_val))
results = model.evaluate(x_test, y_test)
results



# train, validation 에러 그래프

import matplotlib.pyplot as plt

acc = history.history['binary_accuracy']
val_acc = history.history['val_binary_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, epoch + 1)

plt.plot(epochs, acc, 'b', label='Training acc', color ='red')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Training loss', color ='red')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

# 인플루언서 댓글 데이터에 모형 적합

def predict_pos_neg(review):
    tf = term_frequency(review)
    data = np.expand_dims(np.asarray(tf).astype('float32'), axis=0)
    score = float(model.predict(data))

    if (score > 0.5):
        return 1
    else:
        return 0


for x in range(len(video_comment['comments'])):
    bad_word = 0
    data = []
    for y in video_comment['comments'][x]:
        data.append(predict_pos_neg(y))

    pos_cnt = data.count(1)
    neg_cnt = data.count(0)
    print('pos_cnt' + str(pos_cnt))
    print('neg_cnt' + str(neg_cnt))
    polarity = (pos_cnt - neg_cnt) / (pos_cnt + neg_cnt)

    video_comment.loc[x, 'polarity'] = polarity

video_comment






