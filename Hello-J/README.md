# J Mini Assignment

## Environment
This program is ran using VS Code, As I had to download the J Software due to GitHub issues (which is no issues as this made sure the languages was working correctly). Software is in J 9.7 version with VS Code J extensions.
The scrip are verified in the editor VS Code play button and directly via `.devcontainer/run-j.sh tasks.ijs`. Interactive predictions were evaluated in `jconsole`.

## Task 1: Prediction and Results 

|Expression | Prediction | Results | Notes/ Rules tested |
|---|---|---|---|
| '2 * 3 + 4' | 14 | 14 | It evaluates the number set from right to left, just like in math '2 * (3+4) = 14' |
| '10 - 4 - 3' | 9 | 9 | same as the previous question it follows number set right to left '(10-4) - 3 = 9' |
| '(25 - 4) - 3' | 18 | 18 | The parentheses explicit groups forces overrides the right to left order '(25 - 4) = 21' resulting it to be '21 - 3 = 18' |
| '2 ^ 3 ^ 2' | 512 | 512 | It evaluates the order of exponenties from right to left '2 ^ 3 = 9' then becomes '2 ^ 9 = 512' |
| '# 2 5 9 7 8 1 0 3 ' | 8 | 8 | the '#' tally counts all the numbers in the list |
| '3 # 4 2 0' | 0 | 4 4 4 2 2 2 0 0 0 | the '#' dyadic replicates each of the number on the list from the right to left 3 times. I made the misunderstood and assumed it was identifying the number placement in the list | 
| '+/ 3 1 4 1 5' | 14 | 14 | the adverb '/' that insert '+' between the numbers list makes the order a sum which is where we get '3 + 1 + 4 + 1 + 5 = 14'  |


## Reflection

### 1. What surprised you about J? 
I had a hard time trying to wrap my head around this language as first. The biggest issues I had was that it did not use operator precedence, like not using standard loops of 'for' or 'while' and it had to read everything right to left. However, it was interesting how it dealt with math operations, it worked everything on a entire array without having to use extra code. For example, in expression '10 - 4 - 3' the solution turn into '9' and not '3' making it not rely on typical math rules. Besides these different changes/ understanding, the symbols change their meaning depending on if they have one or two inputs (maybe more), the patterns like forks (+ - / # %) can allow you to write code without the need to name a single variable.   

### 2. Which Sebesta criterion (readability, writability, reliability, cost) does it favor, and what does it give up?
*Favors Writability. 
- The J language maximizes its writability for array manipulations very easy to write. While other languages usually uses loops, counters and an index tracking, J language takes just a few characters, For example ; in the seventh expression '+/ 3 1 4 1 5', it is adding up the numbers. You can easily do tasks like averaging numbers or filtering data in just 3 to 7 characters without declaring variables or setting up iterators.
    
*Gives up Readability.
- The negative side from being easy to write is that it difficult to read J language. The reason is due to have heavily relies on short punctuation characters, hidden arguments, and strict reading from right to left in math. Unless you are familiar with the way array is structured, it is very difficult to read the code. 

### 3. How would you write above in a language you know, and what would be different?
I would write 'above' in Python. The reason for choosing is due to how similar the written using a list of comprehensions and/ or standard loops.
Here is a written example:

'''python 
def above(scores):
    avg_sum = sum(scores) / len(score)
    return sum(1 for s in scores if s > avg)
    
