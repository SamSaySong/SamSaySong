


str_tesst= {"content":"""total:7;2021-10-22 15:14:59:1(-1) (-1):84394741700:Hi|E;2021-10-22 15:27:26:1(-1)
(-1):84902275712:Chao|E;2021-10-22 17:31:30:1(-1) (-1):84374057111:ronv aaaa|E;2021-10-28 09:41:08:1(-1) (-1):VNM_TB:TK
goc cua QK hien con duoi 1.000d, vui long nap the de duy tri lien lac. Nap the online, truy cap
https://www.vietnamobile.com.vn chon NAP TIEN. LH 789 (0d).|E;2021-11-01 08:28:52:1(-1) (-1):092:QUA TANG TRI AN! Chuc
mung Quy khach da nhan duoc 2GB data toc do cao & 30 phut goi noi mang MIEN PHI (han su dung 2 ngay) tu Vietnamobile.
Vui long bam *101# de kiem tra tai khoan. Tran trong!|E;2021-11-04 09:11:16:1(-1)
(+84935109193):84902275712:Jejhe|E;2021-11-04 09:12:24:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:03364103|E"""}


"Ban dang giao dich nop ho so khai thue. Ma xac thuc giao dich dien tu cua ban la:48575851"
# "".split(';')[-1].split('|')[0].replace(' ','')

a = str_tesst["content"].split(';')[-1].split("(-1)")
load= a [0]
print(load)

b = a[1].split('|')[0].split(":")[-1]


print(b)