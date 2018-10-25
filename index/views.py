# coding=utf-8
import simplejson
from django.shortcuts import render
from django.http import *
from models import *
# import json
from usercenter import der
from django.core import urlresolvers
# the third moudles imports
from yuyin_recording import my_record, play
from voice_conversion import voice_conversition


# 首页
# @der.login_yz
@der.login_name
def index(request, dic):
    # 拿到产品分类信息
    SortsMsg = GoodSort.objects.all()
    message = []
    for sort in SortsMsg:
        message.append({
            'sort': sort,
            'goodMsgList': sort.goods_set.all().order_by('goodsName')[0:4],
            'goodOtherList': sort.goods_set.all().order_by('goodsName')[4:7]})

    dic = dict(dic, **{
        'message': message,
        })
    return render(request, 'freshFruit/index.html', dic)


def loginOut(request):
    del request.session['name']
    return HttpResponseRedirect(reverse('index:indexPage'))


# 关于我们页面
def aboutus(request):
    return render(request, 'freshFruit/aboutus.html')


# 联系我们页面
def callus(request):
    return render(request, 'freshFruit/callus.html')


# 招聘人才界面
def joinus(request):
    return render(request, 'freshFruit/joinus.html')


def choujiang(request):
    return render(request, 'freshFruit/choujiang.html')


def voice_search(request):
    from django.utils.http import urlquote
    filename = "search.wav"
    status = 'init'
    if request:
        my_record(filename)
        print('录音Over!')
        status = "录音成功"
        play(filename)
        result = voice_conversition(filename)
        # 输出结果
        # {"status": "转换成功", "result": {"err_no": 0, "corpus_no": "6486711964816946024", "err_msg": "success.", "result": ["羊肉，"], "sn": "84913870901510305321"}, "success": true}
        status = "转换成功"
        success = True
        data = {
            'status': status,
            'result': result,
            'success': success,
            }
        redirect_url = urlresolvers.reverse('search_view')
        # redirect_url  = "http://127.0.0.1:8000/search/?q=%s" % result
        # redirect_url  = "http://127.0.0.1:8000/search/?q=%s" % result
        # redirect_url = urlresolvers.reverse('search')
        return HttpResponseRedirect(urlquote(redirect_url))
        # return HttpResponseRedirect(redirect_url)
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False))
