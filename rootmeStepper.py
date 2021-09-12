## === Library imports === ###
import requests
import sys
from bs4 import BeautifulSoup
from itertools import combinations, product


## === Variable decleration === ##
URL = ["https://www.root-me.org/", "?inc=score&lang=en"]


## === Functions === ##
def display_welcome():
	print()
	print(" ----------------------------------")
	print("| ==== Rootme Step Calculator ==== |")
	print(" ---------------------- By Log_s --")
	print()

def display_results(pseudo, goal, points, possibilities):			
	print(f" - User   : {pseudo}")
	print(f" - Points : {points}")
	print(f" - Goal   : {goal}")
	print()
	if (len(possibilities) > 0):
		print(f"Found {len(possibilities)} possibilities :")
		print()
		for possibility in possibilities:
			print(possibility)
	else:
		print("Sorry, but there is no way of reaching that goal with currently available challenges")
		print("You'll have to skip that goal, or wait for new challenges to be released")

def display_error(msg, show_help):
	print("[!] An error has occured :")
	print(f"\t{msg}")
	print()
	if show_help:
		display_help()
	exit(0)

def display_help():
	print("Usage : python3 rootmeStepper.py <username> <goal> [<depth>]")
	print("\tusername : The user you want to search for. Make sure he is unique (use the username that appear in the URL when checking his profile")
	print("\tgoal : The number you want to reach (example : 8000)")
	print("\tdepth : The maximum amount of challenges to reach the goal. Default is 3. If you choose more than 4, the calculation time may be extensive")
	print()
	print("Examples :")
	print("\tpython3 rootmeStepper.py Log_s 7000 3")
	print("\tpython3 rootmeStepper.py Log_s 8000")

def parse_args():
	if len(sys.argv) == 3:
		pseudo = sys.argv[1]
		try:
			goal = int(sys.argv[2])
		except:
			display_error("Goal argument must be a Integer", False)
		return pseudo, goal, 3
	elif len(sys.argv) == 4:
		pseudo = sys.argv[1]
		try:
			goal = int(sys.argv[2])
		except:
			display_error("Goal argument must be a Integer", False)
		try:
			depth = int(sys.argv[3])
		except:
			display_error("Depth argument must be a Integer", False)
		return pseudo, goal, depth
	else:
		display_error("Wrong number of arguments", True)

def get_page(pseudo):
	global URL
	s = requests.Session()
	r = s.get(URL[0] + pseudo + URL[1])
	if r.status_code == 200:
		return r.text
	else:
		display_error("Couldn't find user", False)

def get_challenges(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = soup.find_all("a", class_="rouge")
	todos = []
	for link in links:
		parsed = str(link).split('"')
		category = parsed[3].split("/")[2]
		name = parsed[6].split("\xa0")[1].split("</a>")[0]
		points = parsed[5].split()[0]
		todos.append( (category, name, points) )
	return todos

def get_points(page):
	soup = BeautifulSoup(page, 'html.parser')
	points = int(soup.find_all("h3")[4].text.strip())
	return points

def get_combinations(challenges, goal, depth):
	numbers = [int(challenge[2]) for challenge in challenges]
	final = []
	for n in range(depth+1):
		tmp = [comb for comb in combinations(numbers, n) if sum(comb) == goal]
		final += tmp
	final = [t for t in (set(tuple(i) for i in final))]
	filtered = list(set( [ tuple(sorted(i)) for i in final]))
	filtered.sort(key=lambda t: len(t))
	return filtered

def get_possibilities(challenges, combinations):
	possibilities = []
	for i, combination in enumerate(combinations):
		possibilities.append([])
		for j, element in enumerate(combination):
			possibilities[i].append([])
			for challenge in challenges:
				if int(challenge[2]) == int(element):
					possibilities[i][j].append(challenge)
	final = []
	for possibility in possibilities:
		for combination in list(product(*possibility)):
			current = ""
			for chall in combination:
				current += f"\t{chall[2]} : {chall[0]}/{chall[1]} \n"
			final.append(current)
	return final

## === Main Program === ###
def main():
	pseudo, goal, depth = parse_args()
	display_welcome()
	page = get_page(pseudo)
	challenges = get_challenges(page)
	points = get_points(page)
	combinations = get_combinations(challenges, goal - points, depth)
	possibilities = get_possibilities(challenges, combinations)
	display_results(pseudo, goal, points, possibilities)

if __name__ == "__main__":
	main()