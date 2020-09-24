#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version


class ErShouSpider(BaseSpider):
    def collect_area_ershou_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        ershous = self.get_area_ershou_info(city_name, area_name)
        if ershous:
            district_name = area_dict.get(area_name, "")
            csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
            with open(csv_file, "w") as f:
                # 开始获得需要的板块数据`
                # ershous = self.get_area_ershou_info(city_name, area_name)`
                # 锁定，多线程读写
                if self.mutex.acquire(1):
                    self.total_num += len(ershous)
                    # 释放
                    self.mutex.release()
                if fmt == "csv":
                    for ershou in ershous:
                        # print(date_string + "," + xiaoqu.text())
                        f.write(self.date_string + "," + ershou.text() + "\n")
            print("完成板块: " + area_name + " \n数据保存到 : " + csv_file+'\n')
        else:
            pass

    @staticmethod
    def get_area_ershou_info(city_name, area_name):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_name: 城市
        :param area_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        district_name = area_dict.get(area_name, "")
        # 中文区县
        chinese_district = get_chinese_district(district_name)
        # 中文版块
        chinese_area = chinese_area_dict.get(area_name, "")

        ershou_list = list()
        page = 'http://{0}.{1}.com/ershoufang/{2}/'.format(city_name, SPIDER_NAME, area_name)
        print('开始板块:'+ area_name)  # 打印版块地址
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        # try:
        page_box = soup.find_all('div', class_='page-box')[0]
        matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
        # 检测是否有房源——added by sugz 2020年9月23日
        if matches:
            total_page = int(matches.group(1))
        else:
            return list()
        # except Exception as e:
        #     print("\tWarning: only find one page for {0}".format(area_name))
        #     print(e)

        # 从第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}.{1}.com/ershoufang/{2}/pg{3}'.format(city_name, SPIDER_NAME, area_name, num)
            # print(page)  # 打印每一页的地址
            print('\n==================开始板块:'+area_name+\
                '页数:' + str(num) + '/' + str(total_page) + \
                    '===================')
            headers = create_headers()
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            # 检测是否有房源——added by sugz 2020年9月23日
            # noResFlag = soup.find_all('div',class_='m-noresult')
            # if noResFlag:
            #     print('注意:'+area_name+'板块无房源!!!')
            #     continue
            # else:
            #     print(area_name+'有房子')
            # 检测是否有房源-end

            house_elements = soup.find_all('li', class_="clear")
            # for house_elem in house_elements:
            for (i,house_elem) in enumerate(house_elements):
                xuhao = (num-1)*30 + i
                # price由原来的总价改为单价——modified by sugz 2020年9月23日
                price = house_elem.find('div', class_="unitPrice").attrs['data-price']
                name = house_elem.find('div', class_='title')
                desc = house_elem.find('div', class_="houseInfo")
                pic = house_elem.find('a', class_="img").find('img', class_="lj-lazy")

                #加入获取楼盘坐标——added by sugz 2020年9月23日
                detail_href = name.find('a').attrs['href']
                response = requests.get(detail_href, timeout=10, headers=headers)
                html = response.content
                chnHtml = html.decode()
                matches = re.search("resblockPosition:'(\d+.\d*),(\d+.\d*)'", chnHtml)
                coord = matches.group(2) +',' + matches.group(1)
                #'41.754335,123.503577'

                # 继续清理数据
                # price = price.text.strip()
                name = name.text.replace("\n", "")
                desc = desc.text.replace("\n", "").strip()
                # pic = pic.get('data-original').strip()
                pic = pic.get('src').strip()
                print(str(xuhao)+'/'+ str(total_page*30) +'.' + "{0},{1},{2},{3},{4} ".format(
                    chinese_district, chinese_area, coord,price,name))


                # 作为对象保存
                ershou = ErShou(chinese_district, chinese_area, name, price, desc, pic,coord)
                ershou_list.append(ershou)
        return ershou_list

    def start(self):
        city = get_city()
        self.today_path = create_date_path("{0}/ershou".format(SPIDER_NAME), city, self.date_string)

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
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


        #for test——added by sugz
        # area_dict={'aoti4': 'hunnan', 'baita1': 'sujiatun', 'baogongbei': 'tiexi', 'baogongnan': 'tiexi'}
        # areas=['kangpingxian1', 'fakuxian1', 'xinminshi1', 'fakuxian1', 'kangpingxian1', 'liaozhongqu1', 'xinminshi1', 'baogongbei']
        #for test End——added by sugz
        
        print("Area:", areas)
        print("District and areas:", area_dict)

        # 准备线程池用到的参数
        nones = [None for i in range(len(areas))]
        city_list = [city for i in range(len(areas))]
        args = zip(zip(city_list, areas), nones)
        # areas = areas[0: 1]   # For debugging

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_ershou_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == '__main__':
    pass
