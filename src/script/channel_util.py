from shutil import SameFileError
import zipfile
import sys
import subprocess
import os
import shutil
import log_utils
from xml.etree import ElementTree

# 查看当前apk的comment字段信息
def checkApkComment(signedApk):

    log_utils.getLogger().info('do checkApkComment')

    info,tag = readComment(signedApk)
    if info:
        if tag == 'comment':
            log_utils.getLogger().info('apkComment result: ' + info)
            commentDict = eval(info)
            if 'channelId' in commentDict.keys():
                print('channelId:' + commentDict['channelId'])
            else:
                return '该apk不包含渠道id信息，读取失败'
        else:
            log_utils.getLogger().info('channelId result: ' + info)
            print('channelId:' + info)
    else:
        return '该apk不包含渠道id信息，读取失败'


def readComment(signedApk):
    with zipfile.ZipFile(signedApk,'r',zipfile.ZIP_DEFLATED) as myzip:
        tag = 'comment'
        info = str(myzip.comment,encoding = "utf-8")
        if not info: # 不存在comment字段，读meta-inf文件下空渠道信息
            fileList = myzip.namelist()
            for f in fileList:
                if f.startswith('META-INF/channelId'):
                    info = f.split('_',1)[1]
                    tag = 'empty_file'

        return info,tag

# 用作本地生成多个渠道包
def changeNativeChannel(signedApk,*InfoList):
    originPath = os.path.split(signedApk)[0]
    symbols = InfoList[0]
    extra = InfoList[1]
    out_dir = InfoList[2]
    commentDict = {}
    result = ''

    if out_dir is None:
        print("out_dir is None,make out_dir named temps")
        out_dir = os.path.join(originPath,'temps')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            print("make out_dir success." )

    if extra == '':
       print("extra_info is None")
       extra = ""

    symbolList = symbols.split(',')
    originName = os.path.split(signedApk)[1]

    for symbol in symbolList:
        try:
            shutil.copy(signedApk, out_dir)
        except SameFileError as error:
            result = format(error)
            return result
        except FileNotFoundError as error:
            result = format(error)
            return result
        tempApk = os.path.join(out_dir,originName)
        commentDict['channelId'] = symbol
        if extra:
            commentDict['extra'] = extra

        with zipfile.ZipFile(tempApk,'a',zipfile.ZIP_DEFLATED) as myzip:

            log_utils.getLogger().debug('do insert empty_channel_file.....')
            # 遍历META-INF目录下文件，如果本来就存有渠道空文件，返回提示不能生成渠道包
            fileList = myzip.namelist()
            for f in fileList:
                if f.startswith('META-INF/channelId'):
                    log_utils.getLogger().info('channel file has exists: ' + f)
                    return ('Failed ! channel file has exists: ' + f)

            # 添加以渠道id命令的空文件到META-INF/文件下
            channel_file = "META-INF/channelId_{channel}".format(channel=symbol)

            if not os.path.exists("empty_file.txt"):
                log_utils.getLogger().debug('empty_file.txt is not exists..')
                return ('Failed ! empty_file.txt is not exists..')

            myzip.write("empty_file.txt", channel_file)

            log_utils.getLogger().debug('do change EOCD comment.....')
            myzip.comment = str(commentDict).encode('utf-8') # 修改comment字段
            myzip.close()
            targetName = os.path.join(out_dir,originName.split(".")[0] + '(' + symbol + ').apk')
            shutil.move(tempApk,targetName)

            if not myzip.comment.strip(): # 修改字段失败
                result = 'APK comment modify failed.'
                raise Exception('APK comment modify failed.')

    print('changeApkChannel success!')
    return result