import enum
from random import sample, choice, randint
from timeit import default_timer
from copy import deepcopy
from tkinter import N


def u_hamilton(n, nasycenie):
    nasycenie = nasycenie*((n*(n-1))/2)
    graf = [[0 for _ in range(n)] for _ in range(n)]
    #print(*graf, sep="\n")
    wierzch = [i for i in range(1, n)]
    poprzedni = 0
    krawedzie = 0
    krawedz = None
    for i in range(1, n):
        krawedz = choice(wierzch)
        wierzch.remove(krawedz)
        graf[poprzedni][krawedz] = 1
        graf[krawedz][poprzedni] = 1
        poprzedni = krawedz
        krawedzie += 1
    graf[0][krawedz] = 1
    graf[krawedz][0] = 1
    #print(*graf, sep="\n", end="\n\n")

    wierzch = [i for i in range(1, n)]
    while krawedzie < nasycenie:
        temp = sample(wierzch, k=3)
        if graf[temp[0]][temp[1]] == 0 and graf[temp[1]][temp[2]] == 0 and graf[temp[0]][temp[2]] == 0:
            graf[temp[0]][temp[1]] = 1
            graf[temp[1]][temp[0]] = 1
            graf[temp[1]][temp[2]] = 1
            graf[temp[2]][temp[1]] = 1
            graf[temp[0]][temp[2]] = 1
            graf[temp[2]][temp[0]] = 1
            krawedzie += 3

    return graf


def u_nie_hamilton(n, nasycenie):
    graf = u_hamilton(n, nasycenie)
    nasycenie = nasycenie*((n*(n-1))/2)
    odizolowany = randint(0, n-1)
    for i in range(n):
        graf[i][odizolowany] = 0
        graf[odizolowany][i] = 0
    return graf


def lista_nastepnikow(sasiedztwo, n):
    nastepnicy = [[] for _ in range(n)]
    for y, row in enumerate(sasiedztwo):
        for x, element in enumerate(row):
            if element != 0:
                nastepnicy[y].append(x)
    return nastepnicy


def sprawdzanie_hamilton(graf, n):
    seq = [0]
    if hamilton_util(graf, n, seq):
        print(*seq)
        return seq
    else:
        print("Cykl hamiltona nie istnieje.")
        return False


def hamilton_util(graf, n, seq):
    if len(seq) == n:
        if graf[seq[-1]][0] == 1:
            return True
        else:
            return False
    for v in range(1, n):
        if graf[seq[-1]][v] == 1 and v not in seq:
            seq.append(v)
            if hamilton_util(graf, n, seq) == True:
                return True
            # print(seq)
            seq.pop(len(seq)-1)
    return False


def sprawdzanie_euler(graf, n):
    # Ilosc wierzcholkow o nieparzystym stopniu
    odd = 0
    # Ilosc wierzcholkow majacych znaczenie dla cyklu eulera (degree != 0)
    non_zero = 0
    for row in graf:
        degree = 0
        for element in row:
            if element == 1:
                degree += 1
        if degree > 0:
            non_zero += 1
        if degree % 2 != 0:
            odd += 1

    s = None
    for id, row in enumerate(graf):
        for element in row:
            if element == 1:
                s = id
                break
        if s:
            break
    if bfs(graf, n, s) != non_zero:
        return False
    if odd != 0:
        return False
    return True


def bfs(graf, n, s):
    visited = [False] * n
    visited[s] = True
    queue = [s]
    res = 0

    while queue:
        s = queue.pop(0)
        res += 1
        for id, element in enumerate(graf[s]):
            if visited[id] == False and element == 1:
                queue.append(id)
                visited[id] = True
    return res


def bfs_nastepnicy(graf, n, s):
    visited = [False] * n
    visited[s] = True
    queue = [s]
    res = 0

    while queue:
        s = queue.pop(0)
        res += 1
        for x in graf[s]:
            if visited[x] == False:
                queue.append(x)
                visited[x] = True
    return res


def usun_krawedz(graf, v, u):
    for id, element in enumerate(graf[u]):
        if element == v:
            graf[u].pop(id)
    for id, element in enumerate(graf[v]):
        if element == u:
            graf[v].pop(id)


def is_valid(graf, v, u, n):
    if len(graf[v]) == 1:
        return True
    else:
        reachable = bfs_nastepnicy(graf, n, v)
        usun_krawedz(graf, v, u)
        reachable2 = bfs_nastepnicy(graf, n, v)

        graf[v].append(u)
        graf[u].append(v)

        if reachable > reachable2:
            return False
        return True


def wypisz_euler(temp_graf, n):
    if sprawdzanie_euler(temp_graf, n) == False:
        print("Cykl eulera nie istnieje.")
        return False
    graf = lista_nastepnikow(temp_graf, n)
    # Znajdz wierzcholek startowy
    for id, v in enumerate(graf):
        if len(v) > 0:
            s = id
            break
    cykl_eulera(graf, n, s)


def cykl_eulera(graf, n, v):
    for next in graf[v]:
        if is_valid(graf, v, next, n):
            print(v, next, sep=" -> "),
            usun_krawedz(graf, next, v)
            cykl_eulera(graf, n, next)


def main():
    while True:
        try:
            n = int(input("Podaj ilosc krawedzi w grafie: "))
            nasycenie = float(input("Podaj nasycenie grafu: "))
            break
        except ValueError:
            print("Podaj wartosc typu int, a nastepnie typu float")

    graf_hamilton = u_hamilton(n, nasycenie)
    graf_nie_hamilton = u_nie_hamilton(n, nasycenie)
    print(*graf_hamilton, sep="\n")

    while (inp := input("\n1. Znajdz cykl Eulera\n2. Znajdz cykl Hamiltona\n")) != ("q" or "0"):
        if inp == "1":
            if (g := input("    1. Graf hamiltonowski\n    2. Graf nie-hamiltonowski\n")):
                if g == "1":
                    wypisz_euler(graf_hamilton, n)
                if g == "2":
                    wypisz_euler(graf_nie_hamilton, n)
        if inp == "2":
            if (g := input("    1. Graf hamiltonowski\n    2. Graf nie-hamiltonowski\n")):
                if g == "1":
                    sprawdzanie_hamilton(graf_hamilton, n)
                if g == "2":
                    sprawdzanie_hamilton(graf_nie_hamilton, n)

        input()


if __name__ == '__main__':
    main()
