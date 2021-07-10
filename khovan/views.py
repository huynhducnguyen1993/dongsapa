from time import sleep

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views import View
from django.contrib import messages
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from qlns.models import Nhanvien
from django.http import HttpResponse, response, QueryDict
import json
from django.shortcuts import get_object_or_404
import datetime
from django.contrib.auth.models import Permission
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail


# Create your views here.

class Nhaphangs(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        hanghoa = Hanghoa.objects.all()
        khohang = Khohang.objects.all()
        pnh_nonactive = Phieunhaphang.objects.filter(tinhtrang=False, tuchoi=False)

        pnh_disable = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=True)
        pnh_active = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=False)

        context = {
            'hanghoa': hanghoa,
            'khohang': khohang,
            'pnh_nonactive': pnh_nonactive,
            'pnh_active': pnh_active,
            'pnh_disable': pnh_disable,
        }
        return render(request, 'nhaphang.html', context)


class Phieunhapkho(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):

        hangsx = Hangsx.objects.all()
        hanghoa = Hanghoa.objects.all()
        khohang = Khohang.objects.all()
        thukho = Thukho_Khohang.objects.all()
        nhanvien = Nhanvien.objects.filter(phongban=3)
        nhancungcap = Nhacungcap.objects.all()
        k = Phieunhaphang.objects.all()
        sum_i = 0
        if k:
            for item in k:
                sum_i = item.id + 1

        else:
            sum_i = 1

        context = {
            'hangsx': hangsx,
            'hanghoa': hanghoa,
            'khohang': khohang,
            'thukho': thukho,
            'nhanvien': nhanvien,
            'nhancungcap': nhancungcap,
            'code': sum_i,
        }
        return render(request, 'phieunhapkho.html', context)

    def post(self, request):

        if request.method == 'POST':

            kho = Khohang.objects.get(pk=request.POST.get('kho'))
            code = request.POST.get('code')
            nhacungcap = Nhacungcap.objects.get(pk=request.POST.get('nhacungcap'))
            thoigiantao = request.POST.get('thoigiantao')
            thoigiannhanhang = request.POST.get('thoigiannhanhang')
            nhanvien = Nhanvien.objects.get(pk=request.POST.get('nhanvien'))
            ghichu = request.POST.get('ghichu')
            if request.POST.get('guiduyet') == 1:
                tinhtrang = True
                tuchoi = False
            if request.POST.get('guiduyet') == 0:
                tinhtrang = False
                tuchoi = False
            if request.POST.get('courses'):
                tenhang_d1 = Hanghoa.objects.get(pk=request.POST.get('courses'))
                tenhang_1 = tenhang_d1.tenhanghoa
            else:
                tenhang_1 = None
            if request.POST.get('courses2'):
                tenhang_d2 = Hanghoa.objects.get(pk=request.POST.get('courses2'))
                tenhang_2 = tenhang_d2.tenhanghoa
            else:
                tenhang_2 = None
            if request.POST.get('courses3'):
                tenhang_d3 = Hanghoa.objects.get(pk=request.POST.get('courses3'))
                tenhang_3 = tenhang_d3.tenhanghoa
            else:
                tenhang_3 = None
            if request.POST.get('courses4'):
                tenhang_d4 = Hanghoa.objects.get(pk=request.POST.get('courses4'))
                tenhang_4 = tenhang_d4.tenhanghoa
            else:
                tenhang_4 = None

            if request.POST.get('hang1'):
                ten_ = Hangsx.objects.get(pk=request.POST.get('hang1'))
                ten_hangsx1 = ten_.tenhangsx
            else:
                ten_hangsx1 = None

            if request.POST.get('hang2'):
                ten_ = Hangsx.objects.get(pk=request.POST.get('hang2'))
                ten_hangsx2 = ten_.tenhangsx
            else:
                ten_hangsx2 = None

            if request.POST.get('hang3'):
                ten_ = Hangsx.objects.get(pk=request.POST.get('hang3'))
                ten_hangsx3 = ten_.tenhangsx
            else:
                ten_hangsx3 = None

            if request.POST.get('hang4'):
                ten_ = Hangsx.objects.get(pk=request.POST.get('hang4'))
                ten_hangsx4 = ten_.tenhangsx
            else:
                ten_hangsx4 = None

            noidung = {
                'id_hangsx1': request.POST.get('hang1'),
                'ten_hangsx1': ten_hangsx1,
                'hang_1': request.POST.get('courses'),
                'tenhang_1': tenhang_1,
                'soluong_1': request.POST.get('soluong1'),
                'dongia_1': request.POST.get('dongia1'),
                'id_hangsx2': request.POST.get('hang2'),
                'ten_hangsx2': ten_hangsx2,
                'hang_2': request.POST.get('courses2'),
                'tenhang_2': tenhang_2,
                'soluong_2': request.POST.get('soluong2'),
                'dongia_2': request.POST.get('dongia2'),
                'id_hangsx3': request.POST.get('hang3'),
                'ten_hangsx3': ten_hangsx3,
                'hang_3': request.POST.get('courses3'),
                'tenhang_3': tenhang_3,
                'soluong_3': request.POST.get('soluong3'),
                'dongia_3': request.POST.get('dongia3'),
                'id_hangsx4': request.POST.get('hang4'),
                'ten_hangsx4': ten_hangsx4,
                'hang_4': request.POST.get('courses4'),
                'tenhang_4': tenhang_4,
                'soluong_4': request.POST.get('soluong4'),
                'dongia_4': request.POST.get('dongia14')
            }
            guiduyet = request.POST.get('guiduyet')
            print(guiduyet)
            if guiduyet == '1':
                tinhtrang = False
                tuchoi = False
            if guiduyet == '0':
                tinhtrang = True
                tuchoi = False
            
            Phieunhaphang.objects.create(code=code, guiduyet=guiduyet, nhacungcap=nhacungcap, noidung=noidung
                                         , username=request.user, nhanvien=nhanvien, kho=kho, tinhtrang=tinhtrang,xulykho=False,
                                         thoigiantao=thoigiantao
                                         , thoigiannhanhang=thoigiannhanhang, ghichu=ghichu, tuchoi=tuchoi)

            return redirect('quan-ly-nhap-hang')


class Viewphieunhap(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request, code_id):
        phieunhaphang = Phieunhaphang.objects.get(pk=code_id)
        nd = phieunhaphang.noidung
        hangsx = Hangsx.objects.all()
        hanghoa = Hanghoa.objects.all()
        khohang = Khohang.objects.get(tenkho=phieunhaphang.kho)
        thukho = Thukho_Khohang.objects.exclude(kho=phieunhaphang.kho)
        nhanvien = Nhanvien.objects.get(tennv=phieunhaphang.nhanvien)
        nhancungcap_ = Nhacungcap.objects.get(tennhacungcap=phieunhaphang.nhacungcap)
        nhancungcap = Nhacungcap.objects.exclude(
            tennhacungcap=nhancungcap_.tennhacungcap)  # Loại phần tử trong queryset
        formedit = Editnhaphang(instance=phieunhaphang)

        context = {
            'phieunhaphang': phieunhaphang,
            'noidung': nd,
            'hangsx': hangsx,
            'hanghoa': hanghoa,
            'khohang': khohang,
            'thukho': thukho,
            'nhanvien': nhanvien,
            'nhancungcap': nhancungcap,
            'nhacungcap_': nhancungcap_,
            'form': formedit,

        }
        return render(request, 'viewphieunhaphang.html', context)

    def post(self, request, code_id):

        pl = Phieunhaphang.objects.get(pk=code_id)
        if request.POST.get('courses'):
            tenhang_d1 = Hanghoa.objects.get(pk=request.POST.get('courses'))
            tenhang_1 = tenhang_d1.tenhanghoa
        else:
            tenhang_1 = None
        if request.POST.get('courses2'):
            tenhang_d2 = Hanghoa.objects.get(pk=request.POST.get('courses2'))
            tenhang_2 = tenhang_d2.tenhanghoa
        else:
            tenhang_2 = None
        if request.POST.get('courses3'):
            tenhang_d3 = Hanghoa.objects.get(pk=request.POST.get('courses3'))
            tenhang_3 = tenhang_d3.tenhanghoa
        else:
            tenhang_3 = None
        if request.POST.get('courses4'):
            tenhang_d4 = Hanghoa.objects.get(pk=request.POST.get('courses4'))
            tenhang_4 = tenhang_d4.tenhanghoa
        else:
            tenhang_4 = None

        if request.POST.get('hang1'):
            ten_ = Hangsx.objects.get(pk=request.POST.get('hang1'))
            ten_hangsx1 = ten_.tenhangsx
        else:
            ten_hangsx1 = None

        if request.POST.get('hang2'):
            ten_ = Hangsx.objects.get(pk=request.POST.get('hang2'))
            ten_hangsx2 = ten_.tenhangsx
        else:
            ten_hangsx2 = None

        if request.POST.get('hang3'):
            ten_ = Hangsx.objects.get(pk=request.POST.get('hang3'))
            ten_hangsx3 = ten_.tenhangsx
        else:
            ten_hangsx3 = None

        if request.POST.get('hang4'):
            ten_ = Hangsx.objects.get(pk=request.POST.get('hang4'))
            ten_hangsx4 = ten_.tenhangsx
        else:
            ten_hangsx4 = None
        noidung = {
            'id_hangsx1': request.POST.get('hang1'),
            'ten_hangsx1': ten_hangsx1,
            'hang_1': request.POST.get('courses'),
            'tenhang_1': tenhang_1,
            'soluong_1': request.POST.get('soluong1'),
            'dongia_1': request.POST.get('dongia1'),
            'id_hangsx2': request.POST.get('hang2'),
            'ten_hangsx2': ten_hangsx2,
            'hang_2': request.POST.get('courses2'),
            'tenhang_2': tenhang_2,
            'soluong_2': request.POST.get('soluong2'),
            'dongia_2': request.POST.get('dongia2'),
            'id_hangsx3': request.POST.get('hang3'),
            'ten_hangsx3': ten_hangsx3,
            'hang_3': request.POST.get('courses3'),
            'tenhang_3': tenhang_3,
            'soluong_3': request.POST.get('soluong3'),
            'dongia_3': request.POST.get('dongia3'),
            'id_hangsx4': request.POST.get('hang4'),
            'ten_hangsx4': ten_hangsx4,
            'hang_4': request.POST.get('courses4'),
            'tenhang_4': tenhang_4,
            'soluong_4': request.POST.get('soluong4'),
            'dongia_4': request.POST.get('dongia4')
        }
        a = request.POST.get('csrfmiddlewaretoken')

        querydict = QueryDict('', mutable=True)
        querydict.update(
            {'csrfmiddlewaretoken': a, 'noidung': json.dumps(noidung), 'kho': request.POST.get('kho'), 'code': code_id,
             'username': request.user, 'nhanvien': pl.nhanvien, 'phanhoi': pl.phanhoi, 'nhacungcap': pl.nhacungcap,
             'ghichu': request.POST.get('ghichu'), 'thoigiantao': request.POST.get('thoigiantao'),
             'thoigiannhanhang': request.POST.get('thoigiannhanhang')})
        # 'noidung':json.dumps(noidung): chuyển thành JSON

        form = Editnhaphang(querydict, instance=pl)

        if form.is_valid():
            form.save()

        return redirect('nhap-hang')


class Xuathang(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        return render(request, 'xuathang.html')


class Dieuchuyenkho(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        return render(request, 'dieuchuyenkho.html')


class Tonkho(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        return render(request, 'tonkho.html')


class load_courses(View):

    def get(self, request):
        programming_id = request.GET.get('programming')
        programming_id2 = request.GET.get('programming2')
        programming_id3 = request.GET.get('programming3')
        programming_id4 = request.GET.get('programming4')
        nhanvien_id = request.GET.get('nhanvien_id')

        nhanvien = Nhanvien.objects.filter(id=nhanvien_id)

        courses = Hanghoa.objects.filter(hangsx=programming_id).order_by('tenhanghoa')
        courses2 = Hanghoa.objects.filter(hangsx=programming_id2).order_by('tenhanghoa')
        courses3 = Hanghoa.objects.filter(hangsx=programming_id3).order_by('tenhanghoa')
        courses4 = Hanghoa.objects.filter(hangsx=programming_id4).order_by('tenhanghoa')

        context = {
            'courses': courses,
            'courses2': courses2,
            'nhanvien': nhanvien,
            'courses3': courses3,
            'courses4': courses4,

        }
        return render(request, 'load_hanghoa.html', context)


class Quanlynhaphang(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        phieuhang = Phieunhaphang.objects.all()
        if phieuhang:
            demph_duyet = 0
            demph_chua_duyet_gap = 0
            demph_chua_duyet = 0
            i = 0
            j = 0
            k = 0
            l = 0
            for item in phieuhang:
                if item.tinhtrang == True and item.tuchoi == False:
                    i += 1
                if item.tinhtrang == False:
                    j += 1
                if item.tinhtrang == False and item.tuchoi == False:

                    if 'GẤP' in item.ghichu:
                        k += 1
                if item.tinhtrang == True and item.tuchoi == True:
                    l += 1
                demph_tuchoi = l
                demph_duyet = i
                demph_chua_duyet = j
                demph_chua_duyet_gap = k

            context = {
                'demph_duyet': demph_duyet,
                'demph_chua_duyet': demph_chua_duyet,
                'demph_chua_duyet_gap': demph_chua_duyet_gap,
                'demph_tuchoi': demph_tuchoi
            }
            return render(request, 'quanly.html', context)
        else:
            context = {
                'demph_duyet': 0,
                'demph_chua_duyet': 0,
                'demph_chua_duyet_gap': 0,
                'demph_tuchoi': 0
            }
            return render(request, 'quanly.html', context)

    def post(self, request):
        pass


class Nhaphangchuaduyet(LoginRequiredMixin, View):
    login_url = 'login/'

    def get(self, request):
        hanghoa = Hanghoa.objects.all()
        khohang = Khohang.objects.all()
        pnh_nonactive = Phieunhaphang.objects.filter(tinhtrang=False)

        context = {
            'hanghoa': hanghoa,
            'khohang': khohang,
            'pnh_nonactive': pnh_nonactive,

        }
        return render(request, 'nhaphangchuaduyet.html', context)


class Nhaphangchuaduyetgap(LoginRequiredMixin, View):
    login_url = 'login/'
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        hanghoa = Hanghoa.objects.all()
        khohang = Khohang.objects.all()
        pnh_nonactive = Phieunhaphang.objects.filter(tinhtrang=False, ghichu='GẤP')

        context = {
            'hanghoa': hanghoa,
            'khohang': khohang,
            'pnh_nonactive': pnh_nonactive,

        }
        return render(request, 'nhaphangchuaduyetgap.html', context)


class Duyetnhaphang(LoginRequiredMixin, View):
    def get(self, request, code_id):
        user = request.user

        if user.username == 'thangnguyen':
            nhaphang = Phieunhaphang.objects.get(pk=code_id)
            form = Nhaphangchuaduyetgaps(instance=nhaphang)
            context = {
                'phieunhaphang': nhaphang,
                'form': form
            }
            return render(request, 'duyetnhaphang.html', context)
        else:
            return HttpResponse("Ban Khong Phai Nguyen Minh Thang")

    def post(self, request, code_id):

        user = request.user
        if user.username == 'thangnguyen':
            pl = Phieunhaphang.objects.get(pk=code_id)
            form = Nhaphangchuaduyetgaps(request.POST, instance=pl)

            if form.is_valid():
                form.save()
        return redirect('nhaphangchuaduyetgap')


class Nhaphangdaduyet(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        pnh_active = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=False)

        context = {
            'pnh_active': pnh_active
        }
        return render(request, 'nhaphangdapheduyet.html', context)


class Thukho_Canxuly(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        pnh_active = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=False,xulykho=False)
        donhangchoxuly = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=False,xulykho=False)
        item_donhangchoxuly = 0
        for item in donhangchoxuly:
            if item.id:
                item_donhangchoxuly += 1

        context = {

            'pnh_active': pnh_active,
            'donhangchoxuly': donhangchoxuly,
            'item_donhangchoxuly': item_donhangchoxuly,
        }
        return render(request, 'thukho-canxuly.html', context)

class Thukho_Treo(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        pnh_active = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=False)
        donhangchoxuly = Phieunhaphang.objects.filter(tinhtrang=True, tuchoi=False)
        item_donhangchoxuly = 0

        for item in donhangchoxuly:
            if item.id:
                item_donhangchoxuly += 1

        context = {
            'pnh_active': pnh_active,
            'donhangchoxuly': donhangchoxuly,
            'item_donhangchoxuly': item_donhangchoxuly,
        }
        return render(request, 'thukho-treo.html', context)

 
class Formxulynhapkho(LoginRequiredMixin,View):

    def get(self,request,code_id):

        phieunhaphang =  Phieunhaphang.objects.get(pk=code_id)
        nhanvien = Nhanvien.objects.get(tennv=phieunhaphang.nhanvien)
        kho = Khohang.objects.all()

        if phieunhaphang.noidung['hang_1']:
            try:
                tonkho_h1 = Ton_kho.objects.filter(hanghoa=phieunhaphang.noidung['hang_1'])
                lst = list()
                for item in tonkho_h1:

                   tonkho_1 = item.soluongnhap - item.soluongxuat
                   lst.append([item.kho,tonkho_1]) 
                   
                
            except Ton_kho.DoesNotExist:
                tonkho_h1 = None
        else:
            tonkho_h1 = None
        if phieunhaphang.noidung['hang_2']:
            try:
                tonkho_h2 = Ton_kho.objects.filter(hanghoa=phieunhaphang.noidung['hang_2'])
                
            except Ton_kho.DoesNotExist:
                tonkho_h2 = None
        else:
            tonkho_h2 = None
        if phieunhaphang.noidung['hang_3']:
            try:
                tonkho_h3 = Ton_kho.objects.filter(hanghoa=phieunhaphang.noidung['hang_3'])
                
            except Ton_kho.DoesNotExist:
                tonkho_h3 = None
        else:
            tonkho_h3 = None  

        context = {
                    'phieunhaphang': phieunhaphang,
                    'nhanvien': nhanvien,
                    'kho': kho,
                    'tonkho_h1': lst,
                    'tonkho_h2': tonkho_h2,
                    'tonkho_h3': tonkho_h3,
                    'form':Nhaphangxulykho,
                }
        return render(request, 'form-xu-ly-kho.html', context)

    def post(seft,request,code_id):

        phieunhaphang =  Phieunhaphang.objects.get(pk=code_id)
        soluong1 = request.POST.get('soluong1')
        soluong1_2 =request.POST.get('soluong1_2')

        kho1 = request.POST.get('kho1')
        kho1_2 = request.POST.get('kho1_2')
        tong1 = int(soluong1) + int(soluong1_2)
        soluong2 = request.POST.get('soluong2')
        soluong2_2 =request.POST.get('soluong2_2')

        kho2 = request.POST.get('kho1')
        kho2_2 = request.POST.get('kho1_2')
        tong2 = int(soluong2) + int(soluong2_2)
        code = Phieunhaphang.objects.filter(id = code_id).first()

        if int(request.POST.get('xulykho')) == 1:

            if tong1 == int(phieunhaphang.noidung['soluong_1']):
                csrf = request.POST.get('csrfmiddlewaretoken')
                
                noidung = {

                'id_hangsx1':phieunhaphang.noidung['id_hangsx1'],
                'ten_hangsx1': phieunhaphang.noidung['ten_hangsx1'],
                'hang_1':phieunhaphang.noidung['hang_1'],
                'tenhang_1': phieunhaphang.noidung['tenhang_1'],
                'soluong_1': phieunhaphang.noidung['soluong_1'],
                'dongia_1':phieunhaphang.noidung['dongia_1'],
                'soluong1':soluong1,
                'kho1':kho1,
                'soluong1_2':soluong1_2,
                'kho1_2':kho1_2,
                'id_hangsx2': phieunhaphang.noidung['id_hangsx2'],
                'ten_hangsx2':phieunhaphang.noidung['ten_hangsx2'],
                'hang_2': phieunhaphang.noidung['hang_2'],
                'tenhang_2': phieunhaphang.noidung['tenhang_2'],
                'soluong_2': phieunhaphang.noidung['soluong_2'],
                'dongia_2': phieunhaphang.noidung['dongia_2'],
                'id_hangsx3': phieunhaphang.noidung['id_hangsx3'],
                'ten_hangsx3': phieunhaphang.noidung['ten_hangsx3'],
                'hang_3': phieunhaphang.noidung['hang_3'],
                'tenhang_3': phieunhaphang.noidung['tenhang_3'],
                'soluong_3':phieunhaphang.noidung['soluong_3'],
                'dongia_3': phieunhaphang.noidung['dongia_3'],
                'id_hangsx4': phieunhaphang.noidung['id_hangsx4'],
                'ten_hangsx4':phieunhaphang.noidung['ten_hangsx4'],
                'hang_4': phieunhaphang.noidung['hang_4'],
                'tenhang_4': phieunhaphang.noidung['tenhang_4'],
                'soluong_4': phieunhaphang.noidung['soluong_4'],
                'dongia_4': phieunhaphang.noidung['dongia_4']

                }

                # querydict_1 = QueryDict('', mutable=True)
                # querydict_1.update(
                # {
                #     'csrfmiddlewaretoken': csrf,
                #     'code':code,
                #     'noidung': json.dumps(noidung),
                #     'tinhtrang_hoanthanh':True,
                #     'tinhtrang_treo':False

                
                #  })
                plform = Phieunhaphang.objects.get(pk=code_id)
                form_phieunhaphang = Nhaphangxulykho(request.POST,instance = plform)
                if form_phieunhaphang.is_valid():
                    form_phieunhaphang.save()

                Nhapkho.objects.create(code=code,noidung=noidung,tinhtrang_hoanthanh=True,tinhtrang_treo=False)
                return redirect("thu-kho-can-xu-ly")
        
            else:
                return HttpResponse("Đã Treo")
        if int(request.POST.get('xulykho'))==2:
            return HttpResponse("Ban Da Chon Huy ")
        