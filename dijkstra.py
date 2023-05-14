import heapq
import numpy as np
import helpers
import vertexClass


def find_shortest_path(img, src, dst):
    pq = []  # min-heap priority queue
    source_x = src[0]
    source_y = src[1]
    dest_x = dst[0]
    dest_y = dst[1]
    imagerows, imagecols = img.shape[0], img.shape[1]
    # access by matrix[row][col]
    matrix = np.full((imagerows, imagecols), None)
    for r in range(imagerows):
        for c in range(imagecols):
            matrix[r][c] = vertexClass.Vertex(c, r)
            matrix[r][c].index_in_queue = len(pq)
            pq.append(matrix[r][c])
    matrix[source_y][source_x].d = 0
    pq = helpers.bubble_up(pq, matrix[source_y][source_x].index_in_queue)
    while len(pq) > 0:
        u = pq[0]
        u.processed = True
        pq[0] = pq[-1]
        pq[0].index_in_queue = 0
        pq.pop()
        pq = helpers.bubble_down(pq, 0)
        neighbors = helpers.get_neighbors(matrix, u.y, u.x)
        for v in neighbors:
            dist = helpers.get_distance(img, (u.y, u.x), (v.y, v.x))
            if u.d + dist < v.d:
                v.d = u.d + dist
                v.parent_x = u.x
                v.parent_y = u.y
                idx = v.index_in_queue
                pq = helpers.bubble_down(pq, idx)
                pq = helpers.bubble_up(pq, idx)

    path = []
    iter_v = matrix[dest_y][dest_x]
    path.append((dest_x, dest_y))
    while (iter_v.y != source_y or iter_v.x != source_x):
        path.append((iter_v.x, iter_v.y))
        iter_v = matrix[iter_v.parent_y][iter_v.parent_x]

    path.append((source_x, source_y))
    return path
