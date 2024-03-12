import random

def generate_quiz():
    operator = random.choice(['+', '-', '*', '/'])
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    
    # Ensure division yields integer result
    if operator == '/':
        num1 *= num2
    
    question = f"{num1} {operator} {num2} = ?"
    answer = eval(str(num1) + operator + str(num2))
    if str(answer).endswith('.0'):
        return [question, int(answer)]
    else:
        return [question, answer]