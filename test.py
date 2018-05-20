import editdistance
import sys

str1 = 'appll'
str2 = 'An apple in the tree'
str3 = 'wild animal'

print()
print('我们用编辑距离来衡量相似度，编辑距离越小相似度越大\n假设有关键词word，需要对比的语句有str1和str2')
print('word: appll')
print('str1: An apple in the tree')
print('str2: wild animal')
print()
print('假如直接用word跟两条语句进行对比，得到的编辑距离如下：')
print('word与str1: ' + str(editdistance.eval(str1, str2)))
print('word与str2: ' + str(editdistance.eval(str1, str3)))
print()
print('出于直觉，appll和str1中的apple更接近，但是考虑到整条语\n句的长度，word与str2的编辑距离更小,'
      '为了更加贴合我们的需\n求，可以把语句切割成一个个单词和word求编辑距离，取其中最\n小的作为编辑距离')


dis = sys.maxsize
for word in str2.split():
    tmp = editdistance.eval(str1, word)
    if tmp < dis:
        dis = tmp
print('\n根据新的算法，得到的编辑距离如下：')
print('word与str1: ' + str(dis))

dis = sys.maxsize
for word in str3.split():
    tmp = editdistance.eval(str1, word)
    if tmp < dis:
        dis = tmp
print('word与str2: ' + str(dis))
print()