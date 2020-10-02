#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 板块信息相关函数

from lib.zone.district import *
from lib.const.xpath import *
from lib.request.headers import *
from lib.spider.base_spider import SPIDER_NAME

sy_areas = ['kangpingxian1', 'fakuxian1', 'xinminshi1', 'fakuxian1', 'kangpingxian1', 'liaozhongqu1', 'xinminshi1', 'baogongbei', 'baogongnan', 'beierlu', 'beiyilu', 'gongrencun1', 'huaxiang2', 'jihong', 'jingjijishukaifaqu', 'qigongjie', 'tiexiguangchang', 'xinggongjie', 'xizhan1', 'yanfen', 'yuhongguangchang', 'yunfeng', 'zhangshi', 'zhongdechanyeyuan', 'zhonggongjie', 'beishi', 'changbai', 'hepingguangchang1', 'huizhanzhongxin1', 'maluwan', 'manrong', 'nanhu10', 'nanshichang', 'sanhaojie', 'shashan', 'taiyuanjie1', 'xinhuaguangchang', 'xita', 'zhongshanlu12', 'daxi', 'dongwulihe', 'fangjialan', 'jinlang', 'jinrongzhongxin', 'maguanqiao', 'nanta', 'quanyuan', 'shifu1', 'wanliutang', 'wuai', 'xinlibao', 'zhongjie', 'aoti4', 'baita1', 'changqing1114', 'donghu5', 'ershiyishiji', 'huizhanzhongxin1', 'ligongdaxue1', 'lixiang', 'qipanshan', 'shenfuxincheng', 'taoxian', 'xinnanzhan', 'xinshifu', 'yingchengzi', 'bawangsi', 'dongbeidamalu', 'dongzhongjie', 'ertaizi', 'liming', 'shangyuan', 'taocicheng', 'wanghua', 'wanliutang', 'beiling1', 'beixing', 'beizhanbei', 'changke', 'dingxianghu', 'lingdong', 'santaizi', 'shoufuxinqu', 'sitaizi', 'tawan1', 'zaohua', 'dingxianghu', 'helancun', 'hongqitai', 'lingxi', 'shaling', 'xisantaizi', 'yuhongguangchang', 'yuhongxincheng', 'zaohua', 'baita1', 'bayi2', 'huizhanzhongxin1', 'quzhongxin', 'sujiatunqu', 'tonggouxincheng', 'daoyi', 'hushitai', 'puhexincheng', 'qipanshan', 'sitaizi', 'xinchengzi', 'zhengliang']
sy_area_dict = {'kangpingxian1': 'fakuxian', 'fakuxian1': 'fakuxian', 'xinminshi1': 'liaozhongqu', 'liaozhongqu1': 'liaozhongqu', 'baogongbei': 'tiexi', 'baogongnan': 'tiexi', 'beierlu': 'tiexi', 'beiyilu': 'tiexi', 'gongrencun1': 'tiexi', 'huaxiang2': 'tiexi', 'jihong': 'tiexi', 'jingjijishukaifaqu': 'tiexi', 'qigongjie': 'tiexi', 'tiexiguangchang': 'tiexi', 'xinggongjie': 'tiexi', 'xizhan1': 'tiexi', 'yanfen': 'tiexi', 'yuhongguangchang': 'yuhong', 'yunfeng': 'tiexi', 'zhangshi': 'tiexi', 'zhongdechanyeyuan': 'tiexi', 'zhonggongjie': 'tiexi', 'beishi': 'heping1', 'changbai': 'heping1', 'hepingguangchang1': 'heping1', 'huizhanzhongxin1': 'sujiatun', 'maluwan': 'heping1', 'manrong': 'heping1', 'nanhu10': 'heping1', 'nanshichang': 'heping1', 'sanhaojie': 'heping1', 'shashan': 'heping1', 'taiyuanjie1': 'heping1', 'xinhuaguangchang': 'heping1', 'xita': 'heping1', 'zhongshanlu12': 'heping1', 'daxi': 
'shenhe', 'dongwulihe': 'shenhe', 'fangjialan': 'shenhe', 'jinlang': 'shenhe', 'jinrongzhongxin': 'shenhe', 'maguanqiao': 'shenhe', 'nanta': 'shenhe', 'quanyuan': 'shenhe', 'shifu1': 'shenhe', 'wanliutang': 'dadong', 'wuai': 'shenhe', 'xinlibao': 'shenhe', 'zhongjie': 'shenhe', 'aoti4': 'hunnan', 
'baita1': 'sujiatun', 'changqing1114': 'hunnan', 'donghu5': 'hunnan', 'ershiyishiji': 'hunnan', 'ligongdaxue1': 'hunnan', 'lixiang': 'hunnan', 'qipanshan': 'shenbeixinqu', 'shenfuxincheng': 'hunnan', 'taoxian': 'hunnan', 'xinnanzhan': 'hunnan', 'xinshifu': 'hunnan', 'yingchengzi': 'hunnan', 'bawangsi': 'dadong', 'dongbeidamalu': 'dadong', 'dongzhongjie': 'dadong', 'ertaizi': 'dadong', 'liming': 'dadong', 'shangyuan': 'dadong', 'taocicheng': 'dadong', 'wanghua': 'dadong', 'beiling1': 'huanggu', 'beixing': 'huanggu', 'beizhanbei': 'huanggu', 'changke': 'huanggu', 'dingxianghu': 'yuhong', 'lingdong': 'huanggu', 'santaizi': 'huanggu', 'shoufuxinqu': 'huanggu', 'sitaizi': 'shenbeixinqu', 'tawan1': 'huanggu', 'zaohua': 'yuhong', 'helancun': 
'yuhong', 'hongqitai': 'yuhong', 'lingxi': 'yuhong', 'shaling': 'yuhong', 'xisantaizi': 'yuhong', 'yuhongxincheng': 'yuhong', 'bayi2': 'sujiatun', 'quzhongxin': 'sujiatun', 'sujiatunqu': 'sujiatun', 'tonggouxincheng': 'sujiatun', 'daoyi': 'shenbeixinqu', 'hushitai': 'shenbeixinqu', 'puhexincheng': 'shenbeixinqu', 'xinchengzi': 'shenbeixinqu', 'zhengliang': 'shenbeixinqu'}
def get_district_url(city, district):
    """
    拼接指定城市的区县url
    :param city: 城市
    :param district: 区县
    :return:
    """
    return "http://{0}.{1}.com/xiaoqu/{2}".format(city, SPIDER_NAME, district)


def get_areas(city, district):
    """
    通过城市和区县名获得下级板块名
    :param city: 城市
    :param district: 区县
    :return: 区县列表
    """
    page = get_district_url(city, district)
    areas = list()
    try:
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        root = etree.HTML(html)
        links = root.xpath(DISTRICT_AREA_XPATH)

        # 针对a标签的list进行处理
        for link in links:
            relative_link = link.attrib['href']
            # 去掉最后的"/"
            relative_link = relative_link[:-1]
            # 获取最后一节
            area = relative_link.split("/")[-1]
            # 去掉区县名,防止重复
            if area != district:
                chinese_area = link.text
                chinese_area_dict[area] = chinese_area
                # print(chinese_area)
                areas.append(area)
        return areas
    except Exception as e:
        print(e)

def getAreaFromUser():
    #返回list，如空list[]表示爬取全部板块
    #其实还应该用正则检测是否只有数字和字母，以后再加吧
    rightFlag = True
    while rightFlag:
        userAreaList = []
        userArea = input('请输入本次要爬取的板块，爬取全部板块请直接回车，多个板块请用[]括起来，如：[beierlu,maluwan]')
        try:
            if '[' in userArea:
                if '，' in userArea:
                   userAreaList = userArea.strip('[]').split('，')
                else:
                    userAreaList = userArea.strip('[]').split(',')
                print('OK,本次爬取的板块：'+ str(userAreaList)+'\n请务必确保输入准确！')
            elif userArea.strip() == '':
                userAreaList = []
                print('OK,本次爬取的板块：全部板块'+'，请务必确保输入准确！')
            else:
                userAreaList.append(userArea.strip())
                print('OK,本次爬取的板块：'+ str(userAreaList)+'\n请务必确保输入准确！')
            confirm = input('确定请输入y，重新输入本次爬取板块请输入n：').strip()
            if  confirm == 'y':
                rightFlag = False
            else:
                pass
        except Exception as e:
            print('输入格式错误，请重新输入~')
    return userAreaList

if __name__ == "__main__":
    print(get_areas("sh", "huangpu"))

