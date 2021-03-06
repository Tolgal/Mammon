#import modules needed for the functions
import random
import re
import os
from tempfile import mkstemp
from shutil import move


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



def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with os.fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    os.remove(file_path)
    #Move new file
    move(abs_path, file_path)


def open_file(of_filename):
	with open(of_filename) as file:
		lines = file.readlines()
	return lines


def write_file(wf_filename, wf_data):
	with open(wf_filename, 'w+') as file:
		for i in wf_data:
			if i not in file.read():
				file.write(i + '\n')


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
	create_servers_files(servers)


def create_servers_files(csf_servers):
	for server in csf_servers:
		file = open('Data\\%s.txt' % server, 'w')
		string = ','.join(csf_servers[server]['channels']) + '\n' + ','.join(csf_servers[server]['roles']) + '\n' + ','.join(csf_servers[server]['members'])
		file.write(string)
		file.close()


def edit_host_message(host_dict : dict):
	final_message = '**Mission Board:** '
	for a in host_dict:
		final_message = '{0}\n{1}'.format(final_message, host_dict[a])
	return final_message


def create_dirs(cd_dirlist):
    for directory in cd_dirlist:
        if not os.path.exists(directory):
            os.makedirs(directory)

def create_files(cf_files):
	for file in cf_files:
		try:
			file = open(file, 'r')
		except IOError:
			file = open(file, 'w')
		file.close()


def check_allowed(ca_message):
	with open('Data\\allowed_users') as allowed:
		if ca_message.author.id not in allowed.read():
			if ca_message.content.lower() == 'mammon is my god':
				return ca_message.author.id, True
			return False, False
		return False, True


def get_stats():
	users = []
	stats = open_file('Data\\rps')
	stats = [x.strip() for x in stats]
	stats = [x.split(',') for x in stats]
	for user in stats[1:]:
		users.append(user[0])
	return stats, users


def check_choices(cc_bchoice, cc_pchoice, cc_answer, cc_user_stats):
	rpsdict = {'rock':'scissors', 'paper':'rock', 'scissors':'paper'}
	try:
		if cc_bchoice == cc_pchoice.lower():
			cc_answer = cc_answer + '**It\'s a tie**'
			cc_user_stats[2] = str(int(cc_user_stats[2])+ 1)
			cc_user_stats[5] = '0'
		elif rpsdict[cc_pchoice.lower()] == cc_bchoice:
			cc_answer = cc_answer + '**You won :frowning:**'
			cc_user_stats[1] = str(int(cc_user_stats[1])+ 1)
			cc_user_stats[5] = str(int(cc_user_stats[5])+ 1)
			if int(cc_user_stats[5]) > int(cc_user_stats[4]):
				cc_user_stats[4] = cc_user_stats[5]
		elif rpsdict[cc_bchoice.lower()] == cc_pchoice:
			cc_answer = cc_answer + '**I won :smile:**'
			cc_user_stats[3] = str(int(cc_user_stats[3])+ 1)
			cc_user_stats[5] = '0'
		else:
			cc_answer = False
	except:
		cc_answer = False
	return cc_answer, cc_user_stats


if __name__ == "__main__":
	print(check_mention("peanut"))
