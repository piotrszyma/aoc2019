import collections

relations = collections.defaultdict(set)

with open('input', 'r') as f:
    for line in (l.strip() for l in f):
        planet1, planet2 = line.split(')')
        relations[planet1].add(planet2)
        relations[planet2].add(planet1)

queue = collections.deque()
queue.extend((relation, []) for relation in relations['YOU'])
visited = {'YOU'}

while queue:
    local_root, path = queue.popleft()

    if local_root == 'SAN':
        print(len(path) - 1)
        break

    for neighbour in relations[local_root]:

        if neighbour in visited:
            continue
        visited.add(neighbour)
        queue.extend((relation, [*path, local_root, neighbour])
                     for relation in relations[neighbour]
                     if relation not in visited)
