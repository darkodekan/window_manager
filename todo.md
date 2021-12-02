# TODO LIST

1. fix ghost window
- catch configure request
- different events?
2. resize window feature
3. bar support
4. child window dont configure
5. move window
6. make script to test it with automatically
7. bottom border [x]
8. custom bar 
9. standardize config file
10. generate new window
- idea:
splitting from focused one(depending on width/height)
and when it is deleted it previous window should regain space
if previous window is deleted the child window should regain its space
(it's not that simple it seems, there are few special cases to consider)
regain space newest one ?
11. fix pixel rounding
12. fix focus window
13. remove window
14. workspaces
15. multimonitor support


another idea:
if child dies without children, its parent regains space
if parent dies, newest child(and its children) should regain space
and it becomes parent of siblings
if older child dies, parents and siblings should regain space


#cases
1. only parent, full screen
2. parent and one child
child dies parent regains space
parent does child regains space
3. parent and multiple children
parent dies, newest child regains space
newest child without children dies, parent reains space
older child without children dies, parent and siblings regain space

any child with children dies, see 2. or 3.




resizing
parent gets larger, newest child moves also(along its children)




#MOVING TO THE SIDE!!! some windows height remains constant
# when moving to the side calculate DISPLAY WIDTH -width_win