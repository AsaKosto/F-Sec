# F-Sec
The Minefield
Asa Kosto

Approach and Strategy:
	The first step I took to form a strategy for the challenge was to inspect the source code of the page. I could see that the information about the minefield was organized in a table that could be easily parsed. I decided the most straightforward strategy would involve three parts:
Download the source code from the page so I could manipulate it locally
Parse the source code for the minefield and organize it into some kind of data structure
Search or traverse the data structure to find a safe path from the start point to the flag

Step 1: Downloading the Source Code
In my first attempt to download the source code, I used the requests library (https://docs.python-requests.org/en/latest/) to read the website source into a file. I printed the file to confirm that I had the right source code, and everything was the same except the minefield itself. This was because the request to the server from the terminal window I was using was using the same session as the browser, and since the specific layout of the minefield is tied to the session, I was seeing two different minefields. 
	In my first attempt to get the terminal session to match the browser session, I used the BurpSuite application to intercept the GET request that was sent upon refreshing the page. The software allows you to see the exact formatting of all requests that go through your browser using a proxy. I copied the session cookie, along with all the other request headers, and hardcoded them into a dictionary, which I passed as a parameter into the requests.get() function. This did not work. I could see in BurpSuite that the requests I was sending from the terminal were not formatted properly.
	I did a bit of searching, and I found this page: https://stackoverflow.com/questions/26018944/use-existing-authenticated-session-from-browser-to-perform-https-request-on-pyth , which describes how to use your existing browser session to access files. The code snippet I used is in the response given by @amgaera (9/24/14, 14:16). It uses a library called pycookiecheat (https://pypi.org/project/pycookiecheat/). I used the pycookiecheat.chrome_cookies() function to access the same session I was using in the browser and download the HTML. I printed it and confirmed that the minefield in my terminal matched the one in the browser. I also read through the data and read it into a two dimensional list that I could print in order to visually verify that the minefields were the same. 

(Note: the lines that initialize and print this array can be commented out to increase efficiency without affecting the functionality of the script)

Step 2: Organize the Data
	Now that I had all the necessary information about the layout of the minefield, I had to figure out how to safely pass through it. I decided a graph would be the best way to organize the minefield data so it could be easily traversed later. In the same loop that created the visual representation, I read all the data into a one dimensional list, with each index representing a square. 0 is the first square in the first row, 1 is the second square in the first row, 22 is the first square in the second row, and so on until 483, which is the bottom right square containing the flag. I then looped through that array and read each entry into a dictionary with the index of the square as the key and a list containing the adjacent squares as the value. ({... index : [up, down, left, right]...}) If the square was on a corner or an edge, I assigned the appropriate value in the adjacency list to “None.” For example, the first and third entries in the adjacency list for index 0 are both “None”, because there are no squares above or to the left of the leftmost square in the top row. I used simple mathematical expressions in the loop to decide if squares were on the edge of the minefield. For instance, if a square is in the first row, its index will be less than 22, or if it is in the first column, its index mod 22 will be 0, and so on. At the end, I printed the dictionary and looked it over to make sure all the values had been assigned correctly.

Step 3: Finding a Path
	Once data was organized into a graph, all I had to do was perform a depth-first search on it and print out the path once I found the flag. I used a slightly unconventional implementation for the search algorithm. My specific implementation is a modified version of this algorithm: https://www.geeksforgeeks.org/find-paths-given-source-destination/ , which is used to find all the paths from a source node to a target node. I changed the function so it returned as soon as it found a single path, so it didn’t display every possible path from the start square to the flag. (For some minefields, there are quite a few!) I also had to modify the path description to include moves, instead of the indices of the nodes. I like using this algorithm because it is very versatile. If you just return as soon as you find a path, it works like a regular depth-first search. However, if you want to find a specific path, such as the shortest, the longest, or a path that hits specific nodes, you only need to change the implementation a little bit. 
	I also chose the specific order in which the search visited adjacent squares. The algorithm always searches down, to the right, to the left, then up. Since the start square is in the top left, and the flag is in the bottom right, it makes sense that moving down and to the right first is more likely to get you closer to the flag. I also noticed throughout testing that most of the minefield layouts could be traversed safely by moving only down and to the right. The search will never call the search function on a square to the left of the current square unless it cannot go down or to the right. Since this situation rarely arose, it seemed most efficient to search down and to the right first. It also obviously does not travel to a square if it contains a bomb, represented by an ‘@’ in the appropriate index of the original list.
	I ran the script a few times and manually traced through the minefield to make sure the paths were in fact reliable. Once I was convinced the script did in fact work, I refreshed the page, ran the script, copied the answer from the terminal and pasted it into the browser. The token I received upon successful submission of a path was “keyring-heremit56”

Potential Improvements and Bugs:
	The script can be optimized beyond the final version that reliably found a safe path. As stated in Step 2, the code that prints the array in a two dimensional list can be commented out to improve space efficiency. It is likely that reading the response into a file and reading line by line through the file is unnecessary, and that one can probably create the list that contains the locations of the bombs directly from the response object. However, I did not search thoroughly for a way to do this. It is also likely that the walk() function that performs the depth-first search can be further optimized. 
	There is one potential bug that is immediately apparent in the script: the limits on the iteration through the lines of the file containing the website source code. The script is hardcoded to search through lines 36 to 1400. Throughout every test, the formatted table that laid out the minefield always started at line 36, but for some reason the line at which the table ended was never consistent. It was usually between 1300 and 1310, so I chose 1400 and added a condition that the loop should stop when it saw the string ‘end’ marking the end of the table formatting. It is unlikely, although possible, that the table formatting could go beyond line 1400, and then the list representation of the minefield would be incomplete. 
	The script could have been further improved by adding a few lines at the end to send the safe path directly to the website instead of copying and pasting it into the browser. This would have been useful if the time limit was shorter or if there were a large number of minefields that had to be traversed. 
