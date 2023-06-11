from itertools import combinations, product
from bs4 import BeautifulSoup
import argparse
import requests
from colorama import init as colorama_init, Fore, Style


CATEGORIES = ['steganography', 'cryptanalysis', 'forensic', 'programming', 'cracking', 'realist', 'web-server', 'app-system', 'app-script', 'web-client', 'network']


def get_page(pseudo):
    s = requests.Session()
    r = s.get(f"https://www.root-me.org/{pseudo}?inc=score&lang=en")
    if r.status_code == 200:
        return BeautifulSoup(r.text, 'html.parser')
    else:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Invalid username")
        exit()


def get_challenges(page):
	links = page.find_all("a", class_="rouge")
	todos = []
	for link in links:
		category = link.get("href").split("/")[2].lower()
		name = link.text.strip().replace("x\xa0", "")
		points = int(link.get("title").split()[0])
		todos.append( (category, name, points) )
	return todos


def get_points(page):
	points = int(page.find_all("h3")[5].text)
	return points


def filter_by_categories(challenges, add_categories, remove_categories):
    global CATEGORIES
    if add_categories == None and remove_categories == None:
        return challenges
    
    c = []
    if add_categories == None:
        c = [e for e in CATEGORIES if e not in remove_categories]
    elif remove_categories == None:
        c = add_categories

    return [challenge for challenge in challenges if challenge[0] in c]
    

def parse_categories(raw):
	# add mechanisme to recognise the intended category and fix it
    if raw == None:
        return None
    return list(map(lambda x: x.strip().lower(), raw.split(",")))


def compute_combinations(challenges, points, goal, depth):
    valid_combinations = []
    find_combinations(challenges, points, goal, depth, [], valid_combinations, set())
    valid_combinations.sort(key=lambda x: sum(challenge[2] for challenge in x))
    return valid_combinations


def find_combinations(challenges, points, goal, depth, current_combination, valid_combinations, used_challenges):
    if points == goal:
        sorted_combination = sorted(current_combination, key=lambda x: x[2])
        if sorted_combination not in valid_combinations:
            valid_combinations.append(sorted_combination)
    elif points < goal and depth > 0:
        for challenge in challenges:
            category, name, point_value = challenge
            if challenge not in used_challenges:
                new_points = points + point_value
                new_depth = depth - 1
                new_combination = current_combination + [challenge]
                new_used_challenges = used_challenges.copy()
                new_used_challenges.add(challenge)
                find_combinations(challenges, new_points, goal, new_depth, new_combination, valid_combinations, new_used_challenges)
                find_combinations(challenges, points, goal, new_depth, current_combination, valid_combinations, used_challenges)

def display_results(username, points, goal, combinations):
    pass


def parse_args():
    parser = argparse.ArgumentParser(description='Offers rootme challenges combinations to reach a goal')
    parser.add_argument('username', type=str, help='The rootme username. You can find it in your profile\'s URL')
    parser.add_argument('goal', type=int, help='The goal to reach')
    parser.add_argument('-d', '--depth', type=int, metavar='', default=3, help='The maximum number of challenges to combine. Default is 3, higher than 4 may take a long time')
    category_group = parser.add_mutually_exclusive_group(required=False)
    category_group.add_argument('-a', '--add-categories', type=str, metavar='', default=None, help='The categories to include, separated by commas. Default is all categories')
    category_group.add_argument('-e', '--exclude-categories', type=str, metavar='',default=None, help='The categories to exclude, separated by commas. Default is all categories')
    args = parser.parse_args()
    return args.username, args.goal, args.depth, parse_categories(args.add_categories), parse_categories(args.exclude_categories)


def main():
    colorama_init()

    username, goal, depth, add_categories, exclude_categories = parse_args()

    page = get_page(username)
    challenges = get_challenges(page)
    points = get_points(page)

    if goal <= points:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} Your {goal} goal is greater or equal than your current {points} score") # TODO
        exit()

    challenges = filter_by_categories(challenges, add_categories, exclude_categories)

    cmb = compute_combinations(challenges, points, goal, depth)
    
    display_results(username, points, goal, cmb)


if __name__ == "__main__":
	main()