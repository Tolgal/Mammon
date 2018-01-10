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


def random_roll(rr_number, rr_die):
    """
    Generates rr_number random numbers between 0 and the value of rr_die.
    """
    rr_numbers = []
    for x in range(rr_number):
        rr_numbers.append(random.randint(1, rr_die))
    return rr_numbers


def cleanup_roll(words):
    replaced = multireplace(words, {' ': '', '\n': '', '\r': '', '\t':'', "+":"," ,"-":",-"})
    lowercase = replaced.lower()
    new_list = lowercase.split(',')
    new_list = list(filter(None, new_list))
    return new_list


def create_die(cd_die):
    if '-' in cd_die:
        cd_die = cd_die.replace('-', '')
        rolls, limit = map(int, cd_die.split('d'))
        temp_list = random_roll(rolls, limit)
        neg_temp_list = [ -x for x in temp_list]
        return neg_temp_list
    else:
        rolls, limit = map(int, cd_die.split('d'))
        return random_roll(rolls, limit)


def create_roll_answer(cra_dice, cra_results):
    total = 0
    for i in cra_results:
        total += sum(i)
    cra_answer = '\n**Result:**'
    for i in range(len(cra_dice)):
        if i != range(len(cra_dice))[-1]:
            if cra_dice[i].replace("-", "").isdigit() == True:
                cra_answer = cra_answer + ' ' + cra_dice[i] + ' +'
            else:
                cra_answer = cra_answer + ' ' + cra_dice[i] + '(' + ','.join(str(k) for k in cra_results[i]) + ') +'
        else:
            if cra_dice[i].replace("-", "").isdigit() == True:
                cra_answer = cra_answer + ' ' + cra_dice[i]
            else:
                cra_answer = cra_answer + ' ' + cra_dice[i] + '(' + ','.join(str(k) for k in cra_results[i]) + ')'
    cra_answer = cra_answer + '\n**Total**: ' + str(total)
    return cra_answer