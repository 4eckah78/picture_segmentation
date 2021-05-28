import graph_maker


class Graph:

    def __init__(self, table_x, table_y, table_capacity, height, width, image, k_edge):
        self.maxflow = 0
        self.file = image
        self.k_edge = k_edge
        self.image = self.file.load()
        self.V = height * width + 2
        self.width = width
        self.height = height
        self.E = len(table_x)
        self.table_x = table_x
        self.table_y = table_y
        self.table_capacity = table_capacity
        edges = list(zip(table_x, table_y, table_capacity))
        self.list = {i: [] for i in range(self.V)}
        for i in edges:
            self.list[i[0]].append([i[1], i[2], 0])
        self.levels = []

    def recompute_list(self, obj_pix, bck_pix, bck_prob_func, obj_prob_func):
        print(self.list)
        for j in obj_pix:
            for k in self.list[0]:
                if k[0] == j:
                    k[1] += self.k_edge
                    k[1] += obj_prob_func(self.image[(j - 1) // self.file.size[1], (j - 1) % self.file.size[1]], self.k_edge)
            for k in self.list[j]:
                if k[0] == self.E - 1:
                    k[1] += bck_prob_func(self.image[(j - 1) // self.file.size[1], (j - 1) % self.file.size[1]], self.k_edge)
        for j in bck_pix:
            for k in self.list[0]:
                if k[0] == j:
                    print(k)
                    k[1] += self.k_edge
                    k[1] += obj_prob_func(self.image[(j - 1) // self.file.size[1], (j - 1) % self.file.size[1]], self.k_edge)
                    print(k)
            for k in self.list[j]:
                if k[0] == self.E - 1:
                    print(k)
                    k[1] += bck_prob_func(self.image[(j - 1) // self.file.size[1], (j - 1) % self.file.size[1]], self.k_edge)
                    # k[1] += self.k_edge
                    print(k)

    def bfs_with_levels(self):
        self.levels = [-1] * self.V
        self.levels[0] = 0
        to_visit = [0]
        visited = set()
        layered_list = {}
        layered_list = layered_list.copy()
        layered_reverse_list = {i: [] for i in range(self.V)}
        print("BFS in progress")
        while to_visit:
            current = to_visit.pop(0)
            layered_list[current] = [v for v in self.list[current] if v[1] - v[2] > 0 and (
                        self.levels[v[0]] < 0 or self.levels[v[0]] - self.levels[current] == 1)]
            for i in layered_list[current]:
                self.levels[i[0]] = self.levels[current] + 1
                layered_reverse_list[i[0]].append([current, i[1], i[2]])
                if i[0] not in visited:
                    to_visit.append(i[0])
                visited.add(current)
                visited.add(i[0])
        layered_reverse_list = {k: v for k, v in layered_reverse_list.items() if v != []}
        return layered_list, layered_reverse_list

    def right_clean(self, layered_list, layered_reverse_list, right_check_points):
        while right_check_points:
            i = right_check_points.pop()
            if i in layered_list:
                if len(layered_list[i]) == 0:
                    for j in layered_reverse_list[i]:
                        layered_list[j[0]].remove([i, j[1], j[2]])  # удаление всех исходящих в удаленную вершину ребер
                        right_check_points.append(j[0])
                    del layered_list[i]
                    del layered_reverse_list[i]
        return layered_list, layered_reverse_list

    def left_clean(self, layered_list, layered_reverse_list, left_check_points):
        while left_check_points:
            i = left_check_points.pop()
            if i in layered_reverse_list:
                if len(layered_reverse_list[i]) == 0:
                    for j in layered_list[i]:
                        layered_reverse_list[j[0]].remove([i, j[1], j[2]])
                        left_check_points.append(j[0])
                    del layered_list[i]
                    del layered_reverse_list[i]
        return layered_list, layered_reverse_list

    def dinitz_alg(self):
        while True:  # фаза
            layered_list, layered_reversed_list = self.bfs_with_levels()
            if self.levels[self.V - 1] == -1:  # в сток не попасть
                break
            while self.V - 1 in layered_reversed_list:  # поиск всех дополняющих путей (итерации)
                path = [self.V - 1]
                current_flow = float('inf')
                current = self.V - 1
                left_clean_points = []
                right_clean_points = []
                while current != 0:  # поиск 1-го конкретного пути
                    for i in layered_reversed_list[current]:
                        if i[1] - i[2] <= current_flow:
                            right_clean_points.append(i[0])  # проверяем тупики
                            left_clean_points.append(current)
                            if i[1] - i[2] < current_flow:
                                current_flow = i[1] - i[2]
                                right_clean_points = [i[0]]
                                left_clean_points = [current]
                        path.append(i[0])
                        current = i[0]
                        break
                print(path)
                for k in layered_reversed_list[path[len(path) - 2]]:
                    if k[0] == path[len(path) - 1]:
                        k[2] += current_flow
                        if k[1] - k[2] <= 0:
                            layered_reversed_list[path[len(path) - 2]].remove(k)
                        break
                for j in self.list[path[len(path) - 1]]:
                    if j[0] == path[len(path) - 2]:
                        j[2] += current_flow
                        break
                for j in layered_list[path[len(path) - 1]]:
                    if j[0] == path[len(path) - 2] and j[1] - j[2] <= 0:
                        layered_list[path[len(path) - 1]].remove(j)
                        break
                for j in self.list[path[1]]:
                    if j[0] == path[0]:
                        j[2] += current_flow
                        break
                for j in layered_list[path[1]]:
                    if j[0] == path[0] and j[1] - j[2] <= 0:
                        layered_list[path[1]].remove(j)
                        break
                for k in layered_reversed_list[path[0]]:
                    if k[0] == path[1]:
                        k[2] += current_flow
                        if k[1] - k[2] <= 0:
                            layered_reversed_list[path[0]].remove(k)
                        break
                for i in range(1, len(path) - 2):
                    for j in self.list[path[i + 1]]:
                        if j[0] == path[i]:
                            j[2] += current_flow
                            break
                    for j in layered_list[path[i + 1]]:
                        if j[0] == path[i] and j[1] - j[2] <= 0:
                            layered_list[path[i + 1]].remove(j)
                            break
                    for k in self.list[path[i]]:
                        if k[0] == path[i + 1]:
                            k[2] -= current_flow
                            break
                    for c in layered_reversed_list[path[i]]:
                        if c[0] == path[i + 1]:
                            c[2] += current_flow
                            if c[1] - c[2] <= 0:
                                layered_reversed_list[path[i]].remove(c)
                            break
                    for l in layered_reversed_list[path[i + 1]]:
                        if l[0] == path[i]:
                            l[2] -= current_flow
                            break
                layered_list, layered_reversed_list = self.right_clean(layered_list, layered_reversed_list,
                                                                       right_clean_points)
                layered_list, layered_reversed_list = self.left_clean(layered_list, layered_reversed_list,
                                                                      left_clean_points)
                self.maxflow += current_flow
