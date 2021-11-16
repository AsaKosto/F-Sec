#program to find a safe path through a minefield

import urllib.request
import requests
import pycookiecheat

#this code snippet is from https://stackoverflow.com/questions/26018944/use-existing-authenticated-session-from-browser-to-perform-https-request-on-pyth
#thanks @amgaera
#read the source code from the website into a file
url = "https://pg-0451682683.fs-playground.com"
s = requests.Session()
cookies = pycookiecheat.chrome_cookies(url)
myfile = s.get(url, cookies = cookies)

open("webpage", "wb").write(myfile.content)

fp = open("webpage", "r")
lines = fp.readlines()

#a section to print the minefield for testing
#arrs is structly used for testing to see if the source code in the file matches the website
#it can be commented out to make the program more efficient
arrs = [[] for i in range(22)]
r = 0
c = 0

#create the array that will be used for the adjecency dict
mines = []
#read through the source in the file and mark indices of mines as clear (' ') or dangerous ('@')
for i in range(36, 1400):
    if 'empty' in lines[i]:
        arrs[r].append(' ')
        mines.append(' ')
        c += 1
    if 'full' in lines[i]:
        arrs[r].append('@')
        mines.append('@')
        c += 1
    if c == 22:
        c = 0
        r += 1
    #the line at which the table formatting the minefield ended was inconsistent
    #the loop is formatted to always go at least to the end of the file and break as soon as all the sections of the minefield have been parsed
    if r == 22: 
        break
    if 'end' in lines[i]:
        break

#mark the last section in the minefield as the flag
arrs[21][21] = 'F'
mines.pop()
mines.append('F')

#print to ensure consistency with the minefield in the browser
for row in arrs:
    print(row)
print('\n')
#print(mines)

#create a adjecency disctionary in order to "traverse" the minefield
d = {}

n = len(mines)
i = 0

while i < n:
    adj = []
    #up
    if i < 22: #first row
        adj.append(None)
    else:
        adj.append(i - 22)
    #down
    if ((n - 22) < i < n): #last row
        adj.append(None)
    else:
        adj.append(i + 22)
    #left
    if (i % 22) == 0: #first column
        adj.append(None)
    else:
        adj.append(i-1)
    #right
    if ((i + 1) % 22) == 0: #last column
        adj.append(None)
    else:
        adj.append(i+1)

    d[i] = adj
    i += 1

#print(d)

#define a search function to find the safe route from start to finish
visited = set()
path = []
wtw = []

#this algorithm is a modified version of the one found here: https://www.geeksforgeeks.org/find-paths-given-source-destination/
#this algorithm finds all available paths from a source to a destination, and can be used to find the shortest path
#with small adjustments, this function can be modified to show the shortest path through the minefield, or all available paths
def walk(visited, graph, node):
    visited.add(node)
    path.append(node)
    
    up = graph[node][0]
    down = graph[node][1]
    left = graph[node][2]
    right = graph[node][3]
    
    adj = [down, right, left, up]

    if node == 483:
        #print(path)
        s = ''
        print(s.join(wtw))
        return
    else:
        for i in range(0,4):
            q = adj[i]
            if q != None:
                if q not in visited:
                    if mines[q] != '@':
                        if i == 0:
                            wtw.append('D')
                        if i == 1:
                            wtw.append('R')
                        if i == 2:
                            wtw.append('L')
                        if i == 3:
                            wtw.append('U')
                        walk(visited, graph, q)
    wtw.pop()
    path.pop()
    visited.remove(node)


walk(visited, d, 0)


















