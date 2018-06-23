# -*- coding:utf-8 -*-
import os
import upyun

# 定义项目附件根路径
basePath = '###Your base File Path'

#实例化upyun
up = upyun.UpYun('###Your serverName', '###Your account', '###Your password', timeout=60, endpoint=upyun.ED_AUTO)

#定义文件上传头部
headers = { 'x-gmkerl-rotate': '180' }

#定义遍历方式
def visit(arg, dirname, names):
	filename = 'errLogs'
	with open(filename,'w') as f:
		for name in names:
			tempName = dirname + '/' + name
			#判断该path是文件
			if os.path.isfile(tempName):
				#尝试读取云端文件，判断文件是否存在
				try:
					up.getinfo('/' + name)
				except upyun.modules.exception.UpYunServiceException, err:
					if err[1] == '404':
						#文件不存在则上传
						try:
							with open(tempName, 'rb') as uploadThis:
    							up.put(name, uploadThis, checksum=True, headers=headers)
    					except Exception:
    						f.write(name + '	文件上传异常 \n')
				else:
					#其他异常则记录
					f.write(name + '	文件获取未知异常 \n')

#执行遍历
os.path.walk(basePath, visit, '')
print '完事，详情请查看errLog'