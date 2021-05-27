import math
from PIL import Image


def ntype_edges_weight(pix1, pix2, sigma):
    if pix1 > pix2:
        return int(math.exp(-(pix1 - pix2) ** 2 / (2 * sigma ** 2)))  # / np.linalg.norm(pix1 - pix2))
    return 1


def get_histogram_distribution(pixels_x, pixels_y, image, lambda_=1.0):
    pixels_number = len(pixels_x)
    groups_number = 40
    groups = [0 for i in range(groups_number)]
    mult = groups_number / 256
    for i in range(0, pixels_number):
        intensity = image[pixels_x[i], pixels_y[i]]
        groups[math.floor(intensity * mult)] += 1

    for i in range(groups_number):
        if groups[i] != 0:
            groups[i] = math.floor(- lambda_ * math.log(groups[i] / pixels_number))
        else:
            groups[i] = -1

    def distribution(intensity):
        """Closure function of probabilistic distribution."""

        nonlocal groups
        nonlocal mult

        intensity = math.floor(intensity * mult)
        return groups[intensity]

    return distribution


def k_edge(table_x, table_y, table_capacity, num, width):
    max = 0
    for i in range(len(table_x)):
        if table_x[i] == num and (
                table_y[i] == num - 1 or table_y[i] == num + 1 or table_y[i] == num + width or table_y[
                i] == num - width):
            if table_capacity[i] > max:
                max = table_capacity[i]
    return max + 1


def make_graph(path, selected_bck_pixls_x, selected_bck_pixls_y, selected_obj_pixls_x, selected_obj_pixls_y, lmbda=1,
               sigma=1):
    file = Image.open(path)
    image = file.load()
    height, width = file.size

    bck_prob_func = get_histogram_distribution(selected_bck_pixls_x, selected_bck_pixls_y, image, lmbda)
    obj_prob_func = get_histogram_distribution(selected_obj_pixls_x, selected_obj_pixls_y, image, lmbda)
    file.close()
    table_x = []
    table_y = []
    table_capacity = []
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            # ребра из центрального пикселя в левый
            table_x.append(i * width + j + 1)
            table_y.append(i * width + j)
            table_capacity.append(ntype_edges_weight(image[i, j], image[i, j - 1], sigma))

            # ребра из центрального пикселя в правый
            table_x.append(i * width + j + 1)
            table_y.append(i * width + j + 2)
            table_capacity.append(ntype_edges_weight(image[i, j], image[i, j + 1], sigma))

            # ребра из центрального пикселя в верхний
            table_x.append(i * width + j + 1)
            table_y.append((i - 1) * width + j + 1)
            table_capacity.append(ntype_edges_weight(image[i, j], image[i - 1, j], sigma))

            # ребра из центрального пикселя в нижний
            table_x.append(i * width + j + 1)
            table_y.append((i + 1) * width + j + 1)
            table_capacity.append(ntype_edges_weight(image[i, j], image[i + 1, j], sigma))

        # итерируемся по горизонтальным границам, где каждый пискель имеет 3 соседа
    for i in range(1, width - 1):
        # ребра из центрального пикселя верхней границы в левый
        table_x.append(i + 1)
        table_y.append(i)
        table_capacity.append(ntype_edges_weight(image[0, i], image[0, i - 1], sigma))
        # ребра из центрального пикселя верхней границы в правый
        table_x.append(i + 1)
        table_y.append(i + 2)
        table_capacity.append(ntype_edges_weight(image[0, i], image[0, i + 1], sigma))
        # ребра из центрального пикселя верхней границы в нижний
        table_x.append(i + 1)
        table_y.append(width + i + 1)
        table_capacity.append(ntype_edges_weight(image[0, i], image[1, i], sigma))
        # ребра из центрального пикселя нижней границы в левый
        table_x.append(width * (height - 1) + i + 1)
        table_y.append(width * (height - 1) + i)
        table_capacity.append(ntype_edges_weight(image[height - 1, i], image[height - 1, i - 1], sigma))
        # ребра из центрального пикселя нижней границыв правый

        table_x.append(width * (height - 1) + i + 1)
        table_y.append(width * (height - 1) + i + 2)
        table_capacity.append(ntype_edges_weight(image[height - 1, i], image[height - 1, i + 1], sigma))
        # ребра из центрального пикселя нижней границы в верхний
        table_x.append(width * (height - 1) + i + 1)
        table_y.append(width * (height - 2) + i + 1)
        table_capacity.append(ntype_edges_weight(image[height - 1, i], image[height - 2, i], sigma))

        # итерируемся по вертикальным границам, где каждый пискель имеет 3 соседа
    for i in range(1, height - 1):
        # ребра из центрального пикселя левой границы в верхний
        table_x.append(width * i + 1)
        table_y.append(width * (i - 1) + 1)
        table_capacity.append(ntype_edges_weight(image[i, 0], image[i - 1, 0], sigma))
        # ребра из центрального пикселя левой границы в нижний
        table_x.append(width * i + 1)
        table_y.append(width * (i + 1) + 1)
        table_capacity.append(ntype_edges_weight(image[i, 0], image[i + 1, 0], sigma))
        # ребра из центрального пикселя левой границы в правый
        table_x.append(width * i + 1)
        table_y.append(width * i + 2)
        table_capacity.append(ntype_edges_weight(image[i, 0], image[i, 1], sigma))
        # ребра из центрального пикселя правой границы в верхний
        table_x.append(width * (i + 1))
        table_y.append(width * i)
        table_capacity.append(ntype_edges_weight(image[i, width - 1], image[i - 1, width - 1], sigma))
        # ребра из центрального пикселя правой границы в нижний
        table_x.append(width * (i + 1))
        table_y.append(width * (i + 2))
        table_capacity.append(ntype_edges_weight(image[i, width - 1], image[i + 1, width - 1], sigma))
        # ребра из центрального пикселя нправой границы в левый
        table_x.append(width * (i + 1))
        table_y.append(width * (i + 1) - 1)
        table_capacity.append(ntype_edges_weight(image[i, width - 1], image[i + 1, width - 1], sigma))

    # верхний левый угловой пискель
    table_x.append(1)
    table_y.append(2)
    table_capacity.append(ntype_edges_weight(image[0, 0], image[0, 1], sigma))
    table_x.append(1)
    table_y.append(width + 1)
    table_capacity.append(ntype_edges_weight(image[0, 0], image[1, 0], sigma))

    # верхний правый угловой пискель
    table_x.append(width)
    table_y.append(width - 1)
    table_capacity.append(ntype_edges_weight(image[0, width - 1], image[0, width - 2], sigma))
    table_x.append(width)
    table_y.append(2 * width)
    table_capacity.append(ntype_edges_weight(image[0, width - 1], image[1, width - 1], sigma))

    # нижний левый угловой пискель
    table_x.append(width * (height - 1) + 1)
    table_y.append(width * (height - 2) + 1)
    table_capacity.append(ntype_edges_weight(image[height - 1, 0], image[height - 2, 0], sigma))
    table_x.append(width * (height - 1) + 1)
    table_y.append(width * (height - 1) + 2)
    table_capacity.append(ntype_edges_weight(image[height - 1, 0], image[height - 1, 1], sigma))

    # нижний правый угловой пискель
    table_x.append(width * height)
    table_y.append(width * height - 1)
    table_capacity.append(ntype_edges_weight(image[height - 1, width - 1], image[height - 1, width - 2], sigma))
    table_x.append(width * height)
    table_y.append(width * (height - 1))
    table_capacity.append(ntype_edges_weight(image[height - 1, width - 1], image[height - 2, width - 1], sigma))

    for i in range(height):  # задали все t-связи
        for j in range(width):
            if (i + 1, j+1) in zip(selected_bck_pixls_x, selected_bck_pixls_y):
                table_x.append(0)
                table_y.append(i * width + j + 1)
                table_capacity.append(0)
                table_capacity.append(k_edge(table_x, table_y, table_capacity, i * width + j + 1, width))
                table_x.append(i * width + j + 1)
                table_y.append(width * height + 1)
            elif (i + 1, j+1) in zip(selected_obj_pixls_x, selected_obj_pixls_y):
                table_capacity.append(k_edge(table_x, table_y, table_capacity, i * width + j + 1, width))
                table_x.append(0)
                table_y.append(i * width + j + 1)
                table_x.append(i * width + j + 1)
                table_y.append(width * height + 1)
                table_capacity.append(0)
            else:
                table_x.append(0)
                table_y.append(i * width + j + 1)
                table_capacity.append(obj_prob_func(image[i, j]))
                table_x.append(i * width + j + 1)
                table_y.append(width * height + 1)
                table_capacity.append(bck_prob_func(image[i, j]))

    return table_x, table_y, table_capacity, height, width


def get_bwimage(w_pixels, width, height):
    image = Image.new(mode="RGB", size=(width, height))
    for i in w_pixels:
        image.putpixel(((i - 1) % width, (i - 1) // width), (255, 255, 255))
    im_flipped = image.transpose(method=Image.TRANSPOSE)
    return im_flipped
