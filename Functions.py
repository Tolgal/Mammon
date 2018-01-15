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
        return [ -x for x in temp_list]
    else:
        rolls, limit = map(int, cd_die.split('d'))
        return random_roll(rolls, limit)


def create_roll_answer(cra_dice, cra_results):
    total = 0
    for i in cra_results:
        total += sum(i)
    cra_answer = '\n**Result:**'
    for i in range(len(cra_dice[:-1])):
        if cra_dice[i].replace("-", "").isdigit() == True:
            cra_answer = cra_answer + ' ' + cra_dice[i] + ' +'
        else:
            cra_answer = cra_answer + ' ' + cra_dice[i] + '(' + ','.join(str(k) for k in cra_results[i]) + ') +'
    if cra_dice[-1].replace("-", "").isdigit() == True:
        cra_answer = cra_answer + ' ' + cra_dice[-1]
    else:
        cra_answer = cra_answer + ' ' + cra_dice[-1] + '(' + ','.join(str(k) for k in cra_results[-1]) + ')'
    cra_answer = cra_answer + '\n**Total**: ' + str(total)
    return cra_answer


def check_mention(cm_string):
    member, words = '', '' 
    for word in cm_string.split():
        match = re.search("<@[0-9]*>", cm_string)
        if match != None:
            member = member + match.group(0) + ' '
            cm_string = cm_string.replace(match.group(0), '')
        else:
            words += word
    if not member:
        member = None
    return words, member


def create_server_dict(csd_botservers):
	servers = {}
	for server in csd_botservers:
		servers[server] = {}
		servers[server]['channels'], servers[server]['roles'], servers[server]['members'] = [], [], []
		for channel in server.channels:
			servers[server]['channels'].append(channel.id)
		for role in server.roles:
			servers[server]['roles'].append(role.id)
		for member in server.members:
			servers[server]['members'].append(member.id)
	print(servers)
	create_servers_files(servers)
	return


def create_servers_files(csf_servers):
	for server in csf_servers:
		file = open('%s.txt' % server, 'w')
		string = ','.join(csf_servers[server]['channels']) + '\n' + ','.join(csf_servers[server]['roles']) + '\n' + ','.join(csf_servers[server]['members'])
		file.write(string)
		file.close()
	return



if __name__ == "__main__":
    print(check_mention("peanut"))
