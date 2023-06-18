import sys
import ddddocr
import os
import time

jpgStr = []
resultList = []
start = time.perf_counter()
for filepath, dirnames, filenames in os.walk(
        r'C:\Users\Administrator\PycharmProjects\TensorFlowTest\datasets\training'):
    for filename in filenames:
        jpgStr.append(os.path.join(filepath, filename))
print(jpgStr)
ocr = ddddocr.DdddOcr()
for i in range(len(jpgStr)):
    with open(jpgStr[i], 'rb') as f:
        img_bytes = f.read()
        result = ocr.classification(img_bytes)
        resultList.append(result)

baifenbi = 0
for i in range(len(filenames)):
    if filenames[i].replace('.jpg', '') == resultList[i]:
        baifenbi = baifenbi + 1

end = time.perf_counter()
print('耗时：{:.4f}s'.format(end - start))
print(baifenbi)

sys.exit()
