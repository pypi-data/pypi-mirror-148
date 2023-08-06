# -*- coding: utf-8 -*-#
import pickle, random, datetime, os,itertools, time, sxtwl
import numpy as np

class Iching():
    #64卦、4096種卦爻組合資料庫，爻由底(左)至上(右)起
    def __init__(self):
        base = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(base, 'data.pkl')
        self.data = pickle.load(open(path, "rb"))
        self.sixtyfourgua = self.data.get("數字排六十四卦")
        self.sixtyfourgua_description = self.data.get("易經卦爻詳解")
        self.eightgua = self.data.get("八卦數值")
        self.eightgua_element = self.data.get("八卦卦象")
        self.tiangan = self.data.get("干")
        self.dizhi = self.data.get("支")
        self.wuxin = self.data.get("五行")
        self.down = self.data.get("下卦數")
        self.up = self.data.get("上卦數")
        self.gua = self.data.get("八卦")
        self.sixtyfour_gua_index = self.data.get("六十四卦")
        self.shiying2 = self.data.get("世應排法")
        self.findshiying = dict(zip(list(self.data.get("八宮卦").values()), self.shiying2))
        self.liuqin = self.data.get("六親")
        self.liuqin_w = self.data.get("六親五行")
        self.mons = self.data.get("六獸")
        self.chin_list = self.data.get("二十八宿")
        self.gua_down_code = dict(zip(self.gua,self.down))
        self.gua_up_code = dict(zip(self.gua,self.up))
        self.ymc = [11,12,1,2,3,4,5,6,7,8,9,10]
        self.rmc = list(range(1,32))
        
    def new_list(self, olist, o):
        zhihead_code = olist.index(o)
        res1 = []
        for i in range(len(olist)):
            res1.append( olist[zhihead_code % len(olist)])
            zhihead_code = zhihead_code + 1
        return res1

    def chin_iter(self, olist, chin):
        new_chin_list = self.new_list(olist, chin)
        return itertools.cycle(new_chin_list)
    
    def jiazi(self):
        return [self.tiangan[x % len(self.tiangan)] + self.dizhi[x % len(self.dizhi)] for x in range(60)]
    
    def multi_key_dict_get(self, d, k):
        for keys, v in d.items():
            if k in keys:
                return v
        return None
    
    def find_six_mons(self, daygangzhi):
        mons = [i[1] for i in self.data.get("六獸")]
        return self.new_list(mons, self.multi_key_dict_get(dict(zip([tuple(i) for i in '甲乙,丙丁,戊,己,庚辛,壬癸'.split(",")], mons)), daygangzhi[0]))

    def show_sixtyfourguadescription(self, gua):
        sixtyfourguadescription = self.sixtyfourgua_description
        return sixtyfourguadescription.get(gua)
    
    def rev(self, l):
        r = []
        for i in l:
            r.insert(0, i)
        return r
    
    #干支
    def gangzhi(self, year, month, day, hour):
        if hour == 23:
            d = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S") + datetime.timedelta(hours=1)
        else:
            d = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S") 
        cdate = sxtwl.fromSolar(d.year, d.month, d.day)
        return [self.tiangan[cdate.getYearGZ().tg] + self.dizhi[cdate.getYearGZ().dz], self.tiangan[cdate.getMonthGZ().tg] + self.dizhi[cdate.getMonthGZ().dz], self.tiangan[cdate.getDayGZ().tg] + self.dizhi[cdate.getDayGZ().dz], self.tiangan[cdate.getHourGZ(d.hour).tg] + self.dizhi[cdate.getHourGZ(d.hour).dz]]
    
    #農曆
    def lunar_date_d(self, year, month, day, hour):
        day = sxtwl.fromSolar(year, month, day)
        return {"月": day.getLunarMonth(), "日":day.getLunarDay()}

    def mget_bookgua_details(self, guayao):
        getgua = self.multi_key_dict_get(self.sixtyfourgua, guayao)
        yao_results = self.sixtyfourgua_description.get(getgua)
        bian_yao = guayao.replace("6","1").replace("9","1").replace("7","0").replace("8","0")
        dong_yao = bian_yao.count("1")
        explaination = "動爻有【"+str(dong_yao )+"】根。"
        dong_yao_change = guayao.replace("6","7").replace("9","8")
        g_gua = self.multi_key_dict_get(self.sixtyfourgua, dong_yao_change)
        g_gua_result = self.sixtyfourgua_description.get(g_gua)
        b_gua_n_g_gua = "【"+getgua+"之"+g_gua+"】"
        top_bian_yao = bian_yao.rfind("1")+int(1)
        second_bian_yao = bian_yao.rfind("1",0, bian_yao.rfind("1"))+int(1)
        top_jing_yao = bian_yao.rfind("0") + int(1)
        second_jing_yao = bian_yao.rfind("0", 0, bian_yao.rfind("0"))+int(1)
        top = yao_results.get(top_bian_yao)
        second = yao_results.get(second_bian_yao)
        explaination2 = None
        try:
            if dong_yao == 0:
                explaination2 = explaination, "主要看【"+getgua+"】卦彖辭。",  yao_results[7][2:]
            elif dong_yao == 1: 
                explaination2 = explaination, b_gua_n_g_gua, "主要看【"+top[:2]+"】",  top
            elif dong_yao == 2:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【"+top[:2]+"】，其次看【"+second[:2]+"】。", top, second
            elif dong_yao == 3:
                if bian_yao.find("1") == 0:
                    explaination2 = b_gua_n_g_gua, explaination,  "【"+getgua+"】卦為貞(我方)，【"+g_gua+"】卦為悔(他方)。前十卦，主貞【"+getgua+"】卦，請參考兩卦彖辭", yao_results[7][2:], g_gua_result[7][2:]
                elif bian_yao.find("1") > 0:
                    explaination2 = b_gua_n_g_gua, explaination,  "【"+getgua+"】卦為貞(我方)，【"+g_gua+"】卦為悔(他方)。後十卦，主悔【"+g_gua+"】卦，請參考兩卦彖辭", g_gua_result[7][2:],  yao_results[7][2:]
            elif dong_yao == 4:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【"+g_gua+"】的"+g_gua_result.get(second_jing_yao)[:2]+"，其次看"+g_gua_result.get(top_jing_yao)[:2]+"。", g_gua_result.get(second_jing_yao), g_gua_result.get(top_jing_yao)
            elif dong_yao == 5:    
                explaination2 = b_gua_n_g_gua, explaination,  "主要看【"+g_gua+"】的"+g_gua_result.get(top_jing_yao)[:2]+"。", g_gua_result.get(top_jing_yao)
            elif dong_yao == 6:
                explaination2 = b_gua_n_g_gua, explaination, "主要看【"+g_gua+"】卦的彖辭。", g_gua_result[7][2:]
        except (TypeError, UnboundLocalError):
            pass
        return [guayao, getgua, g_gua, yao_results, explaination2]
    
    def bookgua(self): #由底至上起爻
        shifa_results = []
        for i in range(6):
            stalks_first = 50-1 #一變 (分二、掛一、揲四、歸奇)
            dividers = sorted(random.sample(range(24, stalks_first), 1))
            first_division  = [a - b for a, b in zip(dividers + [stalks_first+10], [10] + dividers)]
            guayi = 1
            right = first_division[0] - guayi
            left_extract = first_division[1] % 4 
            if left_extract == 0:
                left_extract = 4
            right_extract = right % 4
            if right_extract == 0:
                right_extract = 4
            yibian  = left_extract + right_extract + guayi #二變 (分二、掛一、揲四、歸奇)
            stalks_second = stalks_first - yibian
            second_dividers = sorted(random.sample(range(12, stalks_second), 1))
            second_division  = [a - b for a, b in zip(second_dividers + [stalks_second+5], [5] + second_dividers)]
            right_second = second_division[0] - guayi
            left_extract_second = second_division[1] % 4 
            if left_extract_second == 0:
                left_extract_second = 4
            right_extract_second = right_second % 4 
            if right_extract_second == 0:
                right_extract_second = 4
            erbian = left_extract_second + right_extract_second + guayi #三變 (分二、掛一、揲四、歸奇)
            stalks_third = stalks_second - erbian
            third_dividers = sorted(random.sample(range(6, stalks_third), 1))
            third_division  = [a - b for a, b in zip(third_dividers + [stalks_third+3], [3] + third_dividers)]
            right_third = third_division[0] - guayi
            left_extract_third = third_division[1] % 4
            if left_extract_third  == 0:
                left_extract_third = 4
            right_extract_third = right_third % 4 
            if right_extract_third == 0:
                right_extract_third = 4
            sanbian = left_extract_third + right_extract_third + guayi
            yao = int((stalks_first - yibian - erbian - sanbian) / 4)
            shifa_results.append(yao)
        return "".join(str(e) for e in shifa_results[:6])
    
    def datetime_bookgua(self, y,m,d,h):
        gangzhi = self.gangzhi(y,m,d,h)
        ld = self.lunar_date_d(y,m,d,h)
        zhi_code = dict(zip(self.dizhi, range(1,13)))
        yz_code = zhi_code.get(gangzhi[0][1])
        hz_code = zhi_code.get(gangzhi[3][1])
        cm = ld.get("月")
        cd =  ld.get("日")
        eightgua = {1:"777", 2:"778", 3:"787", 4:"788", 5:"877", 6:"878", 7:"887", 8:"888"}
        upper_gua_remain = (yz_code +cm+cd) % 8
        if upper_gua_remain == 0:
            upper_gua_remain = int(8)
        upper_gua = eightgua.get(upper_gua_remain)
        lower_gua_remain = (yz_code+cm+cd+hz_code) % 8
        if lower_gua_remain == 0:
            lower_gua_remain = int(8)
        lower_gua = eightgua.get(lower_gua_remain)
        combine_gua1 =lower_gua+upper_gua
        combine_gua = list(combine_gua1)
        bian_yao = (yz_code+cm+cd+hz_code) % 6
        if bian_yao == 0:
            bian_yao = int(6)
        elif bian_yao != 0:
            combine_gua[bian_yao -1] = combine_gua[bian_yao-1].replace("7","9").replace("8","6")
        bian_gua = "".join(combine_gua)
        ben_gua = self.multi_key_dict_get(self.sixtyfourgua, bian_gua)
        description = self.multi_key_dict_get(self.sixtyfourgua_description,  ben_gua)
        g_gua = self.multi_key_dict_get(self.sixtyfourgua, (bian_gua.replace("6", "7").replace("9", "8")))
        return ben_gua+"之"+g_gua, self.eightgua_element.get(upper_gua_remain)+self.eightgua_element.get(lower_gua_remain)+ben_gua , "變爻為"+description[bian_yao][:2], description[bian_yao][3:]
        
    def bookgua_details(self):
        return self.mget_bookgua_details(self.bookgua())
        
    def current_bookgua(self):
        now = datetime.datetime.now()
        return self.datetime_bookgua(int(now.year), int(now.month), int(now.day), int(now.hour))
    
    def decode_gua(self, gua, daygangzhi):
        fivestars = self.data.get("五星")
        eightgua = self.data.get("數字排八卦")
        sixtyfourgua =  self.data.get("數字排六十四卦")
        su_yao = self.data.get("二十八宿配干支")
        shiying = self.multi_key_dict_get(self.data.get("八宮卦"), self.multi_key_dict_get(sixtyfourgua, gua))
        Shiying = list(self.findshiying.get(shiying))
        dgua = self.multi_key_dict_get(eightgua, gua[0:3])
        down_gua = self.gua_down_code.get(dgua)
        ugua = self.multi_key_dict_get(eightgua,gua[3:6])
        up_gua = self.gua_up_code.get(ugua)
        dt = [self.tiangan[int(g[0])] for g in [down_gua[i].split(',') for i in range(0,3)]]
        dd = [self.dizhi[int(g[1])] for g in [down_gua[i].split(',') for i in range(0,3)]]
        dw = [self.wuxin[int(g[2])] for g in [down_gua[i].split(',') for i in range(0,3)]]
        ut = [self.tiangan[int(g[0])] for g in [up_gua[i].split(',') for i in range(0,3)]]
        ud = [self.dizhi[int(g[1])] for g in [up_gua[i].split(',') for i in range(0,3)]]
        uw = [self.wuxin[int(g[2])] for g in [up_gua[i].split(',') for i in range(0,3)]]
        t = dt+ut
        d = dd+ud
        w = dw+uw
        find_gua_wuxing = self.multi_key_dict_get(self.data.get("八宮卦五行"), self.multi_key_dict_get(sixtyfourgua, gua))
        liuqin = [i[0] for i in self.liuqin]
        lq = [self.multi_key_dict_get(self.liuqin_w,i+find_gua_wuxing) for i in dw+uw]
        gua_name = self.multi_key_dict_get(sixtyfourgua, gua)
        find_su = dict(zip(self.sixtyfour_gua_index, self.chin_iter(self.chin_list, "參"))).get(gua_name)
        sy = dict(zip(self.sixtyfour_gua_index, su_yao)).get(gua_name)
        ng = [t[i]+d[i] for i in range(0,6)]
        sy2 =  [c== sy for c in ng]
        sy3 = [str(i).replace("False", "").replace("True", find_su) for i in sy2]
        ss = dict(zip(self.sixtyfour_gua_index, self.chin_iter(fivestars, "鎮星"))).get(gua_name)
        try:
            position = sy3.index(find_su)
        except ValueError:
            position = 0
        if position == 0:
            g = self.new_list(self.chin_list, find_su)[0:6]
        elif position == 5:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:]
        elif position == 4:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][1:] + [list(reversed(self.new_list(self.chin_list, find_su)))[0]] 
        elif position == 3:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][2:] + list(reversed(self.new_list(self.chin_list, find_su)))[0:2] 
        elif position == 2:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][3:] + list(reversed(self.new_list(self.chin_list, find_su)))[0:3] 
        elif position == 1:
            g = list(reversed(self.new_list(self.chin_list, find_su)))[-6:][4:] + list(reversed(self.new_list(self.chin_list, find_su)))[0:4] 
        build_month_code = dict(zip(self.data.get("六十四卦"),self.data.get("月建"))).get(gua_name)
        build_month = self.new_list(self.jiazi(), build_month_code)[0:6]
        accumulate_code = dict(zip(self.data.get("六十四卦"),self.data.get("積算"))).get(gua_name)
        accumulate = self.new_list(self.jiazi(), accumulate_code)
        aa = list(set(lq))
        fu =  [value for value in liuqin if value not in aa]
        
        return {"卦":gua_name, 
                "五星":ss, 
                "世應卦":shiying+"卦",  
                "星宿":g, 
                "天干":t, 
                "地支":d, 
                "五行":w, 
                "世應":Shiying, 
                "六親":lq, 
                "六獸":self.find_six_mons(daygangzhi),
                "納甲":ng, 
                "建月":build_month, 
                "積算":[list(i) for i in np.array_split(accumulate, 10)]}
    
    
    def decode_two_gua(self, bengua, ggua, daygangzhi):
        a = self.decode_gua(bengua, daygangzhi)
        b = self.decode_gua(ggua, daygangzhi)
        return {"本卦":a, "之卦":b}
    
    def qigua_time(self, y, m, d, h):
        gangzhi = self.gangzhi(y,m,d,h)
        ld = self.lunar_date_d(y,m,d,h)
        zhi_code = dict(zip(self.dizhi, range(1,13)))
        yz_code = zhi_code.get(gangzhi[0][1])
        hz_code = zhi_code.get(gangzhi[3][1])
        cm = ld.get("月")
        cd =  ld.get("日")
        eightgua = self.data.get("八卦數值")
        upper_gua_remain = (yz_code +cm+cd+hz_code) % 8
        if upper_gua_remain == 0:
            upper_gua_remain = int(8)
        upper_gua = eightgua.get(upper_gua_remain)
        lower_gua_remain = (yz_code+cm+cd) % 8
        if lower_gua_remain == 0:
            lower_gua_remain = int(8)
        lower_gua = eightgua.get(lower_gua_remain)
        combine_gua1 =lower_gua+upper_gua
        combine_gua = list(combine_gua1)
        bian_yao = (yz_code+cm+cd+hz_code) % 6
        if bian_yao == 0:
            bian_yao = int(6)
        elif bian_yao != 0:
            combine_gua[bian_yao -1] = combine_gua[bian_yao-1].replace("7","9").replace("8","6")
        bian_gua = "".join(combine_gua)
        ggua = bian_gua.replace("6","7").replace("9","8")
        return {**{'日期':gangzhi[0]+"年"+gangzhi[1]+"月"+gangzhi[2]+"日"+gangzhi[3]+"時"}, **{"大衍筮法":self.mget_bookgua_details(bian_gua)}, **self.decode_two_gua(bian_gua, ggua, gangzhi[2])}
  
    def qigua_now(self):
        now = datetime.datetime.now()
        return self.qigua_time(now.year, now.month, now.day, now.hour)

if __name__ == '__main__':
    tic = time.perf_counter()
    print(Iching().qigua_now())
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")