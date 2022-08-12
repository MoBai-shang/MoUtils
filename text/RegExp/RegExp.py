import re

'''
如果你要多行匹配，那么需要加上re.S和re.M标志. 加上re.S后, .将会匹配换行符，
默认.不会匹配换行符. 代码如下:
'''
s="a23b\na34b"
print('\n多行匹配：')
print(re.findall(r"a(\d+)b.+a(\d+)b", s, re.S))
print('非多行匹配：')
print(re.findall(r"a(\d+)b.+a(\d+)b", s))
print('加上re.M后,^$标志将会匹配每一行，默认^和$只会匹配第一行')
print(re.findall(r"^a(\d+)b", s))#输出['23']
print(re.findall(r"^a(\d+)b", s, re.M))#输出['23', '34']

print('\n指定匹配某字符次数')
p = re.compile(r'\d{3}-\d{6,8}')
print(p.findall('010-628888789'))

print('\n匹配IP')
p=re.compile(r"(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5])")
print(p.search(".192.168.1.251").group())

s="a123b456b"
print('\n贪婪 提取ab之间的值: 匹配a和最后一个b之间的所有值')
print(re.findall(r"a(.+?)b",s))
print('非贪婪 匹配ab之间的值: a和第一个出现的b之间的值')
print(re.findall(r"a(.+)b", s))

'''
2. 连续多个位置的字符串提取
这种情况我们可以使用(?P<name>…)这个正则表达式来提取. 举例,如果我们有一行
webserver的access日志:'192.168.0.1 25/Oct/2012:14:46:34 "GET /api HTTP/1.1"
200 44 "http://abc.com/search" "Mozilla/5.0"',我们想提取这行日志里面所有的内容,
可以写多个(?P<name>expr)来提取,其中name可以更改为你为该位置字符串命名的变量,
expr改成提取位置的正则即可. 代码如下:
'''
line ='192.168.0.1 25/Oct/2012:14:46:34 "GET /api HTTP/1.1" 200 44 "http://abc.com/search" "Mozilla/5.0"'
print('\n提取关键词:')
reg = re.compile('^(?P<remote_ip>[^ ]*) (?P<date>[^ ]*) "(?P<request>[^"]*)" (?P<status>[^ ]*) (?P<size>[^ ]*) "(?P<referrer>[^"]*)" "(?P<user_agent>[^"]*)"')
regMatch = reg.match(line)
linebits = regMatch.groupdict()
for k, v in linebits.items():
    print(k+": "+v)

print('中文 匹配规则必须含有u,可以没有r[\u4e00-\u9fa5]')
context='4月企业销售前瞻指数73.4（图表3）'
pattern=re.compile(u"(企业销售前瞻指数.{0,4}?\d+\.?\d+)",re.S)
print(pattern.findall(context))




