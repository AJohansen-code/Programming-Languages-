# J Mini Assignment

## Environment

## Task 1: Prediction and Results 

|Expression | Prediction | Results | Notes/ Rules tested |
|---|---|---|---|
| '2 * 3 + 4' | 14 |  |  |
| '10 - 4 - 3' | 9 |  |  |
| '(10 - 4) - 3' | 3 |  |  |
| '2 ^ 3 ^ 2' | 512 |  |  |  |
| '# 3 1 4 1 5' | 5 |  |  |
| '2 # 3 1 4' | 3 3 1 1 4 4 |  |  |  | 
| '+/ 3 1 4 1 5' | 14 |  |  |  |


## Reflection

### 1. What surprised you about J? 

### 2. Which Sebesta criterion (readability, writability, reliability, cost) does it favor, and what does it give up?

### 3. How would you write above in a language you know, and what would be different?
I would write 'above' in Python. The reason for choosing is due to how similar the written using a list of comprehensions and/ or standard loops.
Here is a written example:

'''python 
def above(scores):
    avg_sum = sum(scores) / len(score)
    return sum(1 for s in scores if s > avg)
    
