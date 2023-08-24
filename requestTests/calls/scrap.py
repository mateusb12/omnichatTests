import itertools

aux = [i for i in filter(lambda x: x % 5, itertools.islice(itertools.count(5), 10))]
print(aux)