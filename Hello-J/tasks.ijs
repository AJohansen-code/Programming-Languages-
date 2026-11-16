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

NB. Task 3: Above Average 

NB. above: count items strickly greater that the list average. 
NB. (y > avg y) generates boolean vector (1 if item is > mean, 0 otherwise).
NB. +/ sums that boolean vector to count qualifying items without loops. 
above =: 3 : '+/y > avg y'

NB. test dataset of at least 6 numbers
scores = =: 72 88 64 95 81 90 58

NB. Output Script

smoutput ' ==Task 2 calls== '

smoutput ' avg 70 85 90 95:  ', ": avg 70 85 90 95
smoutput ' range 3 9 4 1:    ', ": range 3 9 4 1
smoutput ' evens i. 10:       ', ": evens i. 10
smoutput ''

smoutput ' ==Task 3: Above Average== '
smoutput ' scores list:        ', ": scores
smoutput ' avg scores:         ', ": avg scores
smoutput ' above scores:       '. ": above scores


