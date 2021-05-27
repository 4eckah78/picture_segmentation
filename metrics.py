from PIL import Image


def metric_1(path1, path2):
    file1 = Image.open(path1)
    file2 = Image.open(path2)
    height, width = file1.size
    image1 = file1.load()
    image2 = file2.load()
    file1.close()
    file2.close()
    correct = 0
    for i in range(0, height):
        for j in range(0, width):
            if image1[i, j] == image2[i, j]:
                correct += 1
    return correct / (height * width)


def jackar(path1, path2):
    file1 = Image.open(path1)
    file2 = Image.open(path2)
    height, width = file1.size
    image1 = file1.load()
    image2 = file2.load()
    file1.close()
    file2.close()
    correct = 0
    all_pix = 0
    for i in range(0, height):
        for j in range(0, width):
            if image1[i, j] == image2[i, j] == (255, 255, 255):
                correct += 1
                all_pix += 1
            elif image1[i, j] == (255, 255, 255) or image2 == (255, 255, 255):
                all_pix += 1
    return correct/all_pix


print(metric_1("result_image6.jpg", "C:/Users/yuryp/Desktop/Готовые сегментации/bool-320.jpg"))
print(jackar("result_image6.jpg", "C:/Users/yuryp/Desktop/Готовые сегментации/bool-320.jpg"))
