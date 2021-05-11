import numpy as np
import time


class Graph:
    def __init__(self, path=""):
        with open(path, 'r') as file:
            self.data = file.read().split('\n')
        self.V = int(self.data[0].split(' ')[0])
        self.E = int(self.data[0].split(' ')[1])
        self.capacity_matrix = np.zeros((self.V, self.V))
        self.flow = np.zeros((self.V, self.V))
        self.max_flow = 0
        self.data.pop(0)
        self.data.pop()
        self.levels = []
        for i in self.data:
            self.capacity_matrix[int(i.split(' ')[0]) - 1, int(i.split(' ')[1]) - 1] = int(i.split(' ')[2])

    def bfs_with_levels(self):
        self.levels = [-1] * self.V
        self.levels[0] = 0

        to_visit = [self.levels[0]]

        while to_visit:
            current = to_visit.pop(0)
            for i in range(self.V):
                if self.capacity_matrix[current, i] - self.flow[current, i] > 0 and self.levels[i] < 0:
                    self.levels[i] = self.levels[current] + 1
                    to_visit.append(i)

    def find_augmenting_path(self, origin=0, max_flow=float('inf')):
        if origin == self.V - 1:
            return max_flow
        for i in range(self.V):
            if self.capacity_matrix[origin, i] - self.flow[origin, i] > 0 and self.levels[origin] + 1 == self.levels[i]:
                current_flow = min(max_flow, self.capacity_matrix[origin, i] - self.flow[origin, i])
                path_flow = self.find_augmenting_path(i, current_flow)
                if path_flow > 0:
                    self.flow[origin, i] += path_flow
                    self.flow[i, origin] -= path_flow
                    return path_flow
        return 0

    def alg_Dinitz(self):
        self.max_flow = 0
        while True:
            self.bfs_with_levels()
            if self.levels[self.V - 1] < 0:
                return self.max_flow
            while True:
                path_flow = self.find_augmenting_path()
                if path_flow == 0:
                    break
                self.max_flow += path_flow


# # for i in range(1, 7):
# #     graph = Graph("C:/Users/yuryp/Downloads/test_" + str(i) + ".txt")
# #     start_time = time.time()
# #     graph.alg_Dinitz()
# #     print("test N ", i)
# #     print("Work time = ", time.time() - start_time, "\n")
# #     print("max flow = ", graph.max_flow)
#
# # for i in range(5, 6):
# #     graph = Graph("C:/Users/yuryp/Downloads/test_d" + str(i) + ".txt")
# #     start_time = time.time()
# #     graph.alg_Dinitz()
# #     print("test d N ", i)
# #     print("Work time = ", time.time() - start_time, "\n")
# #     print("max flow = ", graph.max_flow)
# #
# # for i in range(1, 8):
# #     graph = Graph("C:/Users/yuryp/Downloads/test_rd0" + str(i) + ".txt")
# #     start_time = time.time()
# #     graph.alg_Dinitz()
# #     print("test rd N ", i)
# #     print("Work time = ", time.time() - start_time, "\n")
# #     print("max flow = ", graph.max_flow)
#
# for i in range(1, 8):
#     graph = Graph("C:/Users/yuryp/Downloads/test_rl0" + str(i) + ".txt")
#     start_time = time.time()
#     graph.alg_Dinitz()
#     print("test rl N ", i)
#     print("Work time = ", time.time() - start_time, "\n")
#     print("max flow = ", graph.max_flow)
#
# graph = Graph("C:/Users/yuryp/Downloads/test_rl10.txt")
# start_time = time.time()
# graph.alg_Dinitz()
# print("test rl N 10", )
# print("Work time = ", time.time() - start_time, "\n")
# print("max flow = ", graph.max_flow)
