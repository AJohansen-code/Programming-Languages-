NB. J mini assignment - tasks.ijs

NB. Task 2: Three verbs 

NB. Average or 'avg' is the fork that complutes the average of a list (+ / % #). 
NB. The sum is divided by the count
avg =: + / % #

NB. Range is the explicit verb that computes the range if a list. 
NB. Finding the max vaul while using max-insert (>./) and subtracts (-) the miniumal vaule by using min-insert(<./)
range =: 3 : '(>./y) - (<./y)'

NB. Even is a verb that is a filters an array to only keep even numbers. 
NB. It generates an array from 0 to N-1 using i., checks which elements have a 0 remainder when divided by 2 (0 = 2 | y), and uses that boolean mask with copy (#) to keep only the matching items.
evens =: 3 : '(0 = 2 | y) # y'


