# -*- coding:utf-8 -*-
import sys
import requests
import json
# import mp3play
import time


def talk(info):
    appkey = "e5ccc9c7c8834ec3b08940e290ff1559"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit'
        '/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safar'
        'i/537.36',
    }
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s" % (appkey, info)
    content = requests.get(url, headers=headers)
    answer = json.loads(content.text)
    baidu_api = 'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=5&pit=5'.format(answer['text'])
    res = requests.get(baidu_api, headers=headers)
    with open(r'E:\python_demo\tuling.mp3', 'wb') as f:
        f.write(res.content)
    return answer['text']


def main(info):
    info = info.decode('gb2312').encode('utf-8')
    import pdb
    pdb.set_trace()
    answer = talk(info)
    # mp3 = mp3play.load(r'test.mp3')
    # mp3.play()
    time.sleep(40)
    # time.sleep(min(40, mp3.seconds()))
    # mp3.stop()
    try:
        print 'Tuling: %s' % answer
    except UnicodeEncodeError:
        print u'我说了个啥子哟.'


if __name__ == '__main__':
    print u'开始你的表演。'
    while True:
        info = raw_input('Studog:')
        if info == '88':
            break
main(info)
