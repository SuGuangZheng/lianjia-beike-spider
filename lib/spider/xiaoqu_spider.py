#!/usr/bin/env python
# coding=utf-8
# author: suguangzheng
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取小区数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.xiaoqu import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version


class XiaoQuBaseSpider(BaseSpider):
    def collect_area_xiaoqu_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有小区的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        self.clear_csv(area_name)
        ershous = self.get_xiaoqu_info(city_name, area_name)
        # district_name = area_dict.get(area_name, "")
        # csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
        # with open(csv_file, "w") as f:
        #     # 开始获得需要的板块数据
        #     xqs = self.get_xiaoqu_info(city_name, area_name)
        #     # 锁定
        #     if self.mutex.acquire(1):
        #         self.total_num += len(xqs)
        #         # 释放
        #         self.mutex.release()
        #     if fmt == "csv":
        #         for xiaoqu in xqs:
        #             f.write(self.date_string + "," + xiaoqu.text() + "\n")
        # print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
        # logger.info("Finish crawl area: " + area_name + ", save data to : " + csv_file)


    def clear_csv(self,area_name):
        district_name = self.area_dict.get(area_name, "")
        csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
        with open(csv_file, "w",encoding = 'utf8') as f:
            f.write('')

    def write_tocsv(self,ershous,area_name,page = 1,fmt='csv'):
        if ershous:
            district_name = self.area_dict.get(area_name, "")
            csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
            with open(csv_file, "a",encoding = 'utf8') as f:
                # 开始获得需要的板块数据`
                # ershous = self.get_area_ershou_info(city_name, area_name)`
                # 锁定，多线程读写
                if self.mutex.acquire(1):
                    self.total_num += len(ershous)
                    # 释放
                    self.mutex.release()
                if fmt == "csv":
                    for ershou in ershous:
                        f.write(self.date_string + "," + ershou.text() + "\n")
            print("+++++++++++++++++完成板块: " + area_name+'.Page.'+ str(page) + "   数据保存到 : " + csv_file+'+++++++++++++++++')
        else:
            pass

    @staticmethod
    def makeSoup(city_name,area_name):
        # s = requests.session()
        # s.keep_alive = False
        # page = 'http://{0}.{1}.com/ershoufang/{2}/'.format(city_name, SPIDER_NAME, area_name)
        page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city_name, SPIDER_NAME, area_name)
        print('开始板块:'+ area_name)  # 打印版块地址
        headers = create_headers()
        response = requests.get(page, timeout=100, headers=headers)
        response.close()
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        return soup

    def get_xiaoqu_info(self,city_name, area_name):
        s = requests.session()
        s.keep_alive = False
        total_page = 1
        # district = self.area_dict.get(arcity_nameea, "")
        # chinese_district = get_chinese_district(district)
        # chinese_area = chinese_area_dict.get(city_name, "")

        district_name = self.area_dict.get(area_name, "")
        chinese_district = get_chinese_district(district_name)
        chinese_area = chinese_area_dict.get(area_name, "")
        xiaoqu_list = list()

        #本循环获取板块总页数total_page
        while True:
            #重构发送请求函数makeSoup
            soup = XiaoQuBaseSpider.makeSoup(city_name, area_name)
            # 获得总的页数，通过查找总页码的元素信息
            #有房源的和无房源的都有page-box,有房源的两个page-box，第二个有totalPage
            #无房源的无totalPage
            # try:
            page_box = soup.find_all('div', class_='page-box')
            if page_box:
                text = ''
                for pgText in page_box:
                    text = text + str(pgText)
                page_box = text
                matches = re.search('.*"totalPage":(\d+),.*', page_box)
                if matches:
                    total_page = int(matches.group(1))
                else:#无房源无totalbox,直接返回空list即可
                    return list()
                break
            else:#找不到page-box的div可能是被反爬虫了，应该把delay打开
                print('找不到类名为page-box的div，可能被反爬虫了!!!')
                print('找不到page-box的页面：'+'http://{0}.{1}.com/xiaoqu/{2}/'.format(city_name, SPIDER_NAME, area_name))
                # 等待输入ok后再继续
                stop = input("请刷新页面手动进行人机验证，完成后输入任意字符回车，程序继续运行。如果输入stop则结束该板块内容\n")
                if stop == 'stop':
                    return xiaoqu_list
                else:
                    pass

        # page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDER_NAME, city_name)
        # print(page)
        # logger.info(page)

        # headers = create_headers()
        # response = requests.get(page, timeout=10, headers=headers)
        # html = response.content
        # soup = BeautifulSoup(html, "lxml")

        # # 获得总的页数
        # try:
        #     page_box = soup.find_all('div', class_='page-box')[0]
        #     matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
        #     total_page = int(matches.group(1))
        # except Exception as e:
        #     print("\tWarning: only find one page for {0}".format(city_name))
        #     print(e)


        max_flag = False
        for num in range(1, total_page + 1):
            xiaoqu_list = list()#存进csv后清空xiaoqu_list，避免存过的占用内存
            if max_flag:
                break
            page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city_name, SPIDER_NAME, city_name, num)
            print('\n==================开始板块:'+area_name+\
                '页数:' + str(num) + '/' + str(total_page) + \
                    '===================')
            while True:
                headers = create_headers()
                BaseSpider.random_delay()
                response = requests.get(page, timeout=100, headers=headers)
                response.close()
                html = response.content
                soup = BeautifulSoup(html, "lxml")
                house_elements = soup.find_all('li', class_="xiaoquListItem")
                if not house_elements:
                    #如果house_elements为空
                    print('找不到板块的某一页，可能被反爬虫了!!!')
                    print('找不到的页面：'+ page)
                    # 等待输入ok后再继续
                    stop1 = input("请刷新页面手动进行人机验证，完成后输入任意字符回车，程序继续运行。如果输入stop则结束该板块内容\n")
                    if stop1 == 'stop':
                        return xiaoqu_list
                    else:
                        continue
                else:
                    break
        # 从第一页开始,一直遍历到最后一页
        # for i in range(1, total_page + 1):
        #     headers = create_headers()
        #     page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, city_name, i)
        #     print(page)  # 打印版块页面地址
        #     BaseSpider.random_delay()
        #     response = requests.get(page, timeout=10, headers=headers)
        #     html = response.content
        #     soup = BeautifulSoup(html, "lxml")

        #     # 获得有小区信息的panel
        #     house_elems = soup.find_all('li', class_="xiaoquListItem")
            # 获取每一页中的每个房子信息
            for (i,house_elem) in enumerate(house_elements):
                xuhao = (num-1)*30 + i
                price = house_elem.find('div', class_="totalPrice").find('span')
                name = house_elem.find('div', class_='title')
                #在售二手房套数
                on_sale = house_elem.find('div', class_="xiaoquListItemSellCount")
                builtYear = house_elem.find('div', class_="positionInfo").text.strip()
                detail_href = name.find('a').attrs['href']
                while True:
                    headers = create_headers()
                    BaseSpider.random_delay()
                    response = requests.get(detail_href, timeout=100, headers=headers)
                    response.close()
                    html = response.content
                    chnHtml = html.decode()
                    matches = re.search("resblockPosition:'(\d+.\d*),(\d+.\d*)'", chnHtml)
                    if not matches:
                        print('找不到某个房屋详情页，可能被反爬虫了!!!')
                        print('找不到的页面：'+ detail_href)
                        # 等待输入ok后再继续
                        stop1 = input("请刷新页面手动进行人机验证，完成后输入任意字符回车，程序继续运行。如果输入stop则结束该板块内容\n")
                        if stop1 == 'stop':
                            return xiaoqu_list
                        else:
                            continue
                    else:
                        break
                coord = matches.group(2) +',' + matches.group(1)
                #'41.754335,123.503577'
                # 继续清理数据
                price = price.text.strip()
                name = name.text.replace("\n", "")
                on_sale = on_sale.text.replace("\n", "").strip()
                on_sale = re.search('(.+)套在售二手房',on_sale).group(1)
                builtYear = "".join(builtYear.split())
                builtYear = re.search('/(.+)年建成',builtYear).group(1)
                print(str(xuhao)+'/'+ str(total_page*30) +'.' + "{0},{1},{2},{3},{4},{5},{6} ".format(
                    chinese_district, chinese_area, coord,price,name,builtYear,on_sale))

                # 作为对象保存
                xiaoqu = XiaoQu(chinese_district, chinese_area,coord,name, price,builtYear,on_sale)
                xiaoqu_list.append(xiaoqu)
            #完成一页就写入csv文件
            self.write_tocsv(xiaoqu_list,area_name,num)
        return xiaoqu_list

    def get_area_dict(self,city):
        '''
        获得城市所有区县，areas=['shenhe','tiexi',...],area_dict={'sanhaojie':'heping',...}
        '''
        districts = get_districts(city)
        print('城市: {0}'.format(city))
        print('全部区县: {0}'.format(districts))
        # 获得每个区的板块, area: 板块
        areas = list()
        for district in districts:
            areas_of_district = get_areas(city, district)
            print('区县:{0}, 全部板块:{1}'.format(district, areas_of_district))
            # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
            areas.extend(areas_of_district)
            # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
            for area in areas_of_district:
                area_dict[area] = district
        return areas,area_dict

    def start(self):
        city = get_city()
        self.today_path = create_date_path("{0}/xiaoqu".format(SPIDER_NAME), city, self.date_string)
        t1 = time.time()  # 开始计时
        areas,self.area_dict = self.get_area_dict(city)
        # 获得城市有多少区列表, district: 区县
        # districts = get_districts(city)

        # 获得每个区的板块, area: 板块
        # areas = list()
        # for district in districts:
        #     areas_of_district = get_areas(city, district)
        #     print('{0}: Area list:  {1}'.format(district, areas_of_district))
        #     # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
        #     areas.extend(areas_of_district)
        #     # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
        #     for area in areas_of_district:
        #         area_dict[area] = district
        # print("Area:", areas)
        # print("District and areas:", area_dict)

        # 准备线程池用到的参数
        nones = [None for i in range(len(areas))]
        city_list = [city for i in range(len(areas))]
        args = zip(zip(city_list, areas), nones)
        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_xiaoqu_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出
        # 计时结束，统计结果
        t2 = time.time()
        print("共爬取了 {0} 个板块.".format(len(areas)))
        print("总用时 {0} 秒， 爬取了 {1} 条数据.".format(t2 - t1, self.total_num))
        wordsLast()


if __name__ == "__main__":
    # urls = get_xiaoqu_area_urls()
    # print urls
    # get_xiaoqu_info("sh", "beicai")
    spider = XiaoQuBaseSpider("lianjia")
    spider.start()
