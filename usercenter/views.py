# coding=utf-8
from django.shortcuts import render
from django.http import *
from models import *
# from datetime import datetime
from django.core.urlresolvers import reverse
from . import der
from django.core.paginator import Paginator


@der.login_yz
@der.login_name
def user_center_info(request, dic):
    # name = request.session.get('name')
    # user = UserInfo.objects.get(uName=name)
    # user = UserInfo.objects.get(uName='wangchao')
    if request.method == 'GET':
        recentsee = dic['user'].recentsee_set.all()
        goodlist = []
        for i in recentsee:
            goodlist.append(Goods.objects.get(id=int(i.goodsName)))
            # goodlist.append(Goods.objects.get(goodsName=i.goodsName))
        recv = goodlist[-5:]
        recv.reverse()
        dic = dict(dic, **{'recentsee': recv})
        return render(request, 'freshFruit/user_center_info.html', dic)
    elif request.method == 'POST':
        addr = request.POST.get('addr', None)
        phonenumber = request.POST.get('phonenumber', None)
        if addr and str(phonenumber).isdigit() and len(phonenumber) == 11:
            dic['user'].uPhoneNumber = phonenumber
            dic['user'].uAddr = addr
            dic['user'].save()
        return HttpResponseRedirect(reverse('usercenter:user_center_info'))


@der.login_yz
@der.login_name
def user_center_site(request, dic):
    if request.method == 'GET':
        # user = UserInfo.objects.get(uName='wangchao')
        user = dic['user']
        addrinfo = user.addrinfo_set.all().filter(isDelete=False)
        list2 = []

        for i in addrinfo:
            a = i.aPhoneNumber[0:]
            list2.append({
                'id': i.id,
                'aProvince': i.aProvince,
                'aCity': i.aCity,
                'aDis': i.aDis,
                'aAddressee': i.aAddressee,
                'aPhoneNumber': a[0:3] + u'****' + a[7:],
                'default': i.aDefaultAddr
                })
        dic = dict(dic, **{'addrinfo': list2})
        udelete = request.GET.get('delete', None)
        uchange = request.GET.get('change', None)
        if udelete:
            dAddr = AddrInfo.objects.get(id=udelete)
            dAddr.isDelete = True
            dAddr.save()
            return HttpResponseRedirect(reverse('usercenter:user_center_site'))
        if uchange:
            dAddr = AddrInfo.objects.get(id=uchange)
            try:
                deFault = AddrInfo.objects.filter(aUser=user.id).get(
                    aDefaultAddr=True)
            except Exception, e:
                pass
            else:
                deFault.aDefaultAddr = False
                deFault.save()
            dAddr.aDefaultAddr = True
            dAddr.save()
            return HttpResponseRedirect(reverse('usercenter:user_center_site'))
        return render(request, 'freshFruit/user_center_site.html', dic)

    elif request.method == 'POST':
        addressee = request.POST.get('addressee', None)
        province = request.POST.get('province', None)
        city = request.POST.get('city', None)
        dis = request.POST.get('dis', None)
        detaaddr = request.POST.get('detaaddr', None)
        postcode = request.POST.get('postcode', None)
        phonenumber = request.POST.get('phonenumber', None)

        if addressee and province and city and detaaddr and str(phonenumber).isdigit() and len(phonenumber) == 11:
            addrinfo = AddrInfo()
            addrinfo.aProvince = AreaInfo.objects.get(id__exact=province)
            addrinfo.aCity = AreaInfo.objects.get(id__exact=city)

            if dis:
                addrinfo.aDis = AreaInfo.objects.get(id__exact=dis)

            addrinfo.aAddressee = addressee
            addrinfo.aDetaAddr = detaaddr
            addrinfo.aPostCode = postcode
            addrinfo.aPhoneNumber = phonenumber
            # user = UserInfo.objects.get(uName__exact='wangchao')

            addrinfo.aUser = dic['user']
            addrinfo.save()
            print '写入完成'
            # addrinfo.aDefaultAddr =
            return HttpResponseRedirect(reverse('usercenter:user_center_site'))
            # return render(request,'usercenter/user_center_site.html')
        else:
            return HttpResponseRedirect(reverse('usercenter:user_center_site'))
            # return render(request,'usercenter/user_center_site.html')


def areal(request):

    list1 = AreaInfo.objects.filter(aParent__isnull=True)

    list2 = []
    for a in list1:
        list2.append({'id': a.id, 'title': a.aTitle})
    return JsonResponse({'data': list2})


def areal2(request, pid):
    # list1=AreaInfo.objects.filter(aParent_id=pid)
    list1 = AreaInfo.objects.get(pk=pid).areainfo_set.all()
    list2 = []
    for a in list1:
        list2.append({'id': a.id, 'title': a.aTitle})
    return JsonResponse({'data': list2})


@der.login_yz
@der.login_name
def user_center_order(request, dic):
    orderList = Orders.objects.filter(isDelete=False).filter(
        userOrder_id = dic['user'].id).order_by("-id").order_by("isFinish")

    # orderList=Orders.objects.filter(isDelete=False).filter(userOrder_id=dic['user'].id).filter(isFinish=False).order_by("id")+Orders.objects.filter(isDelete=False).filter(userOrder_id=dic['user'].id).filter(isFinish=True).order_by("id")
    pIndex = request.GET.get('page', None) # 获取页面index
    orderlist2, plist, pIndex = pagTab(orderList, pIndex, 2)  # 分页
    if len(plist) >= 3:   # 页码显示页数
        if len(plist) == pIndex:
            plist = plist[pIndex-3:pIndex]
        elif pIndex == 1:
            plist = plist[0:pIndex+2]
        else:
            plist = plist[pIndex-2:pIndex+1]

    orders = []
    for order in orderlist2:
        detaillist = []
        addr = AddrInfo.objects.get(id=order.addr)
        for i in order.orderdetail_set.all():
            detaillist.append({'od': i, 'good': i.good_id})
        orders.append({'order': order, 'orderdetail': detaillist, 'addr': addr})
    dic = dict(dic, **{
        'orderlist': orders,
        'plist': plist,
        'pIndex': pIndex
        })

    return render(request, 'freshFruit/user_center_order.html', dic)


@der.login_yz
@der.login_name
def pay(request, dic):
    orderId = request.GET.get('order', None)
    order = Orders.objects.get(id=int(orderId))
    order.isFinish = True
    order.save()
    return HttpResponseRedirect(reverse('usercenter:user_center_order'))


def pagTab(list1, pIndex, num):
    # print pIndex
    p = Paginator(list1, num)
    if pIndex == '' or pIndex == None:
        pIndex = '1'
    pIndex = int(pIndex)
    list2 = p.page(pIndex)
    plist = p.page_range
    return list2, plist, pIndex
