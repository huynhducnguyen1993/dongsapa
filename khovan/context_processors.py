from khovan.models import *

def extras(request):
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
            if item.tinhtrang == True and item.tuchoi==False:
                i += 1
            if item.tinhtrang == False:
                j += 1
            if item.tinhtrang == False and item.tuchoi == False:

                if 'GẤP' in item.ghichu:
                    k += 1
            if item.tinhtrang==True and item.tuchoi == True:
                l+=1
            demph_tuchoi = l
            demph_duyet = i
            demph_chua_duyet = j
            demph_chua_duyet_gap = k

        context = {
                'demph_duyet': demph_duyet,
                'demph_chua_duyet': demph_chua_duyet,
                'demph_chua_duyet_gap': demph_chua_duyet_gap,
                'demph_tuchoi':demph_tuchoi
            }
        return {'context':context}
    else:
        context = {
            'demph_duyet': 0,
            'demph_chua_duyet': 0,
            'demph_chua_duyet_gap': 0,
            'demph_tuchoi': 0
        }
        return {'context': context}



def extras_kho(request):
    phieuhang = Phieunhaphang.objects.filter(xulykho=False)
    if phieuhang:

        demph_duyet = 0
        demph_chua_duyet_gap = 0
        demph_chua_duyet = 0
        i = 0
        j = 0
        k = 0
        l = 0
        for item in phieuhang:
            if item.tinhtrang == True and item.tuchoi==False:
                i += 1
            if item.tinhtrang == False:
                j += 1
            if item.tinhtrang == False and item.tuchoi == False:

                if 'GẤP' in item.ghichu:
                    k += 1
            if item.tinhtrang==True and item.tuchoi == True:
                l+=1
            demph_tuchoi = l
            demph_duyet = i
            demph_chua_duyet = j
            demph_chua_duyet_gap = k

        context = {
                'demph_duyet': demph_duyet,
                'demph_chua_duyet': demph_chua_duyet,
                'demph_chua_duyet_gap': demph_chua_duyet_gap,
                'demph_tuchoi':demph_tuchoi
            }
        return {'con':context}
    else:
        context = {
            'demph_duyet': 0,
            'demph_chua_duyet': 0,
            'demph_chua_duyet_gap': 0,
            'demph_tuchoi': 0
        }
        return {'con': context}        