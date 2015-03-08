#!/usr/bin/env python

from pprint import pformat


class DiGraph(object):
    def __init__(self):
        self.vertices = set()
        self.edges = set()
    def add_vertex(self, vertex):
        self.vertices.add(vertex)
    def add_edge(self, vertex_1, vertex_2, weight):
        self.add_vertex(vertex_1)
        self.add_vertex(vertex_2)
        self.edges.add((vertex_1, vertex_2, weight))
    def neighbors(self, target):
        return [{'name': v[1], 'weight': v[2]} for v in filter(lambda x: x[0] == target, self.edges)]
    def bfi(self, start):
        visited = [start]
        i = 0
        while i < len(visited):
            neighbors = self.neighbors(visited[i])
            visited += [v['name'] for v in sorted(neighbors, key=lambda x: x['weight']) if v['name'] not in visited]
            yield visited[i]
            i += 1
    def dfi(self, start):
        visited = []
        stack = [start]
        while stack:
            current = stack[-1]
            neighbors = self.neighbors(current)
            new = [v['name'] for v in sorted(neighbors, key=lambda x: x['weight']) if v['name'] not in visited and v['name'] not in stack]
            if new:
                stack.append(new[0])
            else:
                stack.pop(-1)
            if current not in visited:
                visited.append(current)
                yield current
    def bfs(self, start, finish):
        if start == finish:
            # self-connected verticies
            return 0
        for i, current in enumerate(graph.bfi(start)):
            if current == finish:
                return i
        return -1
    def dfs(self, start, finish):
        if start == finish:
            # self-connected verticies
            return 0
        for i, current in enumerate(graph.dfi(start)):
            if current == finish:
                return i
        return -1
    def dijkstra(self, start, finish):
        dist_map = {vertex: {'weight': float('inf'), 'path': [], 'done': False} for vertex in self.vertices}
        dist_map[start]['weight'] = 0
        while not dist_map[finish]['done']:
            current = sorted([[k, v] for k, v in dist_map.iteritems() if not v['done']], key=lambda x: x[1]['weight'])[0][0]
            dist_map[current]['done'] = True
            neighbors = sorted(self.neighbors(current), key=lambda x: x['weight'])
            for vertex in neighbors:
                if dist_map[current]['weight'] + vertex['weight'] < dist_map[vertex['name']]['weight']:
                    dist_map[vertex['name']]['weight'] = dist_map[current]['weight'] + vertex['weight']
                    dist_map[vertex['name']]['path'] = dist_map[current]['path'] + [current]
        dist_map[finish]['path'].append(finish)
        dist_map[finish]['hops'] = len(dist_map[finish]['path'])
        del(dist_map[finish]['done'])
        return dist_map[finish]
    def __str__(self):
        return pformat(self.__dict__(), indent=2)
    def __dict__(self):
        output = {}
        for vertex in self.vertices:
            output[vertex] = [(v[1], v[2]) for v in filter(lambda x: x[0] == vertex, self.edges)]
        return output


if __name__ == '__main__':
    graph = DiGraph()

    # load data
    with open('distances.raw') as f:
        data = f.read()
    headers = []
    for line in data.split('\n'):
        if line.startswith('|'):
            headers = line.split('|')[1:]
            continue
        city = line.split('|')[0].split(',')[0]
        distances = line.split('|')[1:]
        for i, value in enumerate(distances):
            try:
                int_value = int(value.replace(',', ''))
            except ValueError:
                continue
            # 626 is lowest converge-able value -- but it chops a few vertices
            if int_value < 900 and city and headers[i]:
                graph.add_edge(city, headers[i], int_value)
                graph.add_edge(headers[i], city, int_value)

    cities = list(graph.vertices)
    runs = []
    for i, city_1 in enumerate(cities):
        for city_2 in cities[i+1:]:
            runs.append(graph.dijkstra(city_1, city_2))

    print 'bfi Los Angeles', list(graph.bfi('Los Angeles'))
    print 'dfi Los Angeles', list(graph.dfi('Los Angeles'))
    print 'bfs Los Angeles --> Boston', graph.bfs('Los Angeles', 'Boston')
    print 'dfs Los Angeles --> Boston', graph.dfs('Los Angeles', 'Boston')
    print 'Dijkstra:'
    print '\n'.join([str(v) for v in sorted(runs, key=lambda x: x['weight'])][-30:])
