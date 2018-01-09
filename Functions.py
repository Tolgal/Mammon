import random
import re

def random_numbers(number, die, addition):
	 #Generates numbers and adds them to each other
	numbers = []
	for i in range(number):
		numbers.append(random.randint(1,die))
	total = sum(numbers)
	string = ', '.join(str(k)for k in numbers)
	answer = '```**Result**: ' + str(number) + 'D' + str(die)
	if addition != 0:
		total += addition
		if addition > 0:
		    answer = answer + '+' + str(addition)
		if addition < 0:
		    answer = answer + str(addition)
	answer =  answer + ' (' + string + ') ' + str(addition) + '\n**Total**: ' + str(total) + '```'
	return answer


def multireplace(string, replacements):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :rtype: str
    """
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)