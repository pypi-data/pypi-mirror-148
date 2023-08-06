import lrslib.tkin
import lrslib.tools

name = 'lrslib'

"""
Doc   文档
'tkin.Window':'对Tk()进行优化的适合中国人的一个类',
'tools.pront':'一个一个地打印文本',
'tools.show_image':'显示图片在pygame窗口中'
'by':'关于'
'func':'帮助'
"""

def by():
    """
    关于
    """
    print('LrsLib作者：刘镕硕\n刘镕硕版权所有')
def func(fun='all'):
    """
    帮助
    :param fun: 需要帮助的函数
    """
    function = {'tkin.Window':'对Tk()进行优化的适合中国人的一个类',
                'tools.pront':'一个一个地打印文本',
                'tools.show_image':'显示图片在pygame窗口中',
                'all':'''全部函数：
'tkin.Window':'对Tk()进行优化的适合中国人的一个类',
'tools.pront':'一个一个地打印文本',
'tools.show_image':'显示图片在pygame窗口中'
'by':'关于'
'func':'帮助'
'''
                }
    print(function[fun])
