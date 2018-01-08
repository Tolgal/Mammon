import random

def random_numbers(number, die, addition):
	 #Generates numbers and adds them to each other
	numbers = []
	for i in range(number):
		numbers.append(random.randint(1,die))
	total = sum(numbers)
	string = ', '.join(str(k)for k in numbers)
	answer = 'Result: ' + str(number) + 'D' + str(die)
	if addition != 0:
		total += addition
		string += ', ' + str(addition)
		answer = answer + '+' + str(addition)
	answer =  answer + ' (' + string + ')\nTotal: ' + str(total)
	return answer
