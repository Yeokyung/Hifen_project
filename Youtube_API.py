# 데이터 처리

# 최근 한달 내의 게시글 업로드 주기 계산하기
from datetime import datetime


def post_period(time):
    period = [x for x in time if (datetime.now() - datetime(int(x[:4]), int(x[5:7]), int(x[8:10]))).days <= 30]
    period_mean = []

    for x in range(len(period) - 1):
        time1_year = int(period[x][:4])
        time1_month = int(period[x][5:7])
        time1_day = int(period[x][8:10])

        time2_year = int(period[x + 1][:4])
        time2_month = int(period[x + 1][5:7])
        time2_day = int(period[x + 1][8:10])

        time1 = datetime(time1_year, time1_month, time1_day)  # 년 월 일 시 분
        time2 = datetime(time2_year, time2_month, time2_day)  # 년 월 일 시 분

        period_mean.append((time1 - time2).days)

    result = sum(period_mean) / len(period_mean)

    if result < 1:
        return str(int(round(result * 24, 0))) + '시간'

    else:
        return str(int(round(result, 0))) + '일'


video_info['avg_period'] = video_info.groupby(['channel_id'])['publishedAt'].transform(post_period)

### 텍스트 전처리 함수
import MeCab


def text_processing(text_row):
    comments2 = re.sub(r'[@%\\*=()~#&?-\|\.\:\;\!\-\,\_\~\$\'\"\❤\♡\★\☆\/\♥\<>\\\u200d\♀️️️️\“”\+\분\초]', '',
                       text_row)  # 구둣점 제거
    comments2 = re.sub('[0-9]+', ' ', comments2)  # 숫자 제거
    comments2 = re.sub('\n', ' ', comments2)  # 줄바꿈 제거
    comments2 = re.sub('[ㄱ-ㅎ]+|[ㅏ-ㅣ]+', ' ', comments2)  # 자음만 있는 경우 제거()
    comments2 = only_text(comments2)  # 이모티콘 제거

    # 형태소 분석 & 형용사 / 명사만 추출
    data_noun = []
    m = MeCab.Tagger()
    for i in range(len(comments2)):
        data_noun = [x.split("\t")[0] for x in m.parse(comments2).split("\n") if "NNG" in x or "VA" in x or "NNP" in x]

    # 한글자 제외
    comment_tokenize = [d for d in data_noun if len(d) >= 2]
    comments2 = ' '.join(comment_tokenize)

    # 맞춤법 검사 & 띄어쓰기도 같이 해줌 -> 500자까지만 처리해줌 for 문 돌리기
    spell = []
    for x in range(int(len(comments2) / 500) + 1):
        length = x * 500
        spell.append(spell_checker.check(comments2[0 + length: 500 + length]).checked)

    comments2 = ''.join(spell)
    comments2 = re.sub('\s+', ' ', comments2)  # 화이트 스페이스 제거

    # 꼬꼬마 형태소 분석
    tokenizer = Kkma()
    comments2 = tokenizer.morphs(comments2)  # -> 꼬꼬마로 형태소 분석

    return comments2



