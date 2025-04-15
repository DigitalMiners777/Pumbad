from datetime import datetime
import time
import random
import cloudscraper
import os
import pyfiglet
from requests.exceptions import RequestException
from colorama import Fore, Style


# Define custom ANSI colors
Ab = '\033[1;92m'
aB = '\033[1;91m'
AB = '\033[1;96m'
aBbs = '\033[1;93m'
AbBs = '\033[1;95m'
A_bSa = '\033[1;31m'
a_bSa = '\033[1;32m'
faB_s = '\033[2;32m'
a_aB_s = '\033[2;39m'
Ba_bS = '\033[2;36m'
Ya_Bs = '\033[1;34m'
S_aBs = '\033[1;33m'


class Pumpad:
    def __init__(self) -> None:
        self.scraper = cloudscraper.create_scraper()
        self.headers = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[{datetime.now().strftime('%x %X %Z')}]"
            f"{Style.RESET_ALL} {Fore.WHITE + Style.BRIGHT}|{Style.RESET_ALL} {message}",
            flush=True,
        )

    def welcome(self):
        # Add the custom banner with pyfiglet
        ab = pyfiglet.figlet_format("Digital Miners")
        print(a_bSa + ab)  # Print the custom banner with color

        print(Fore.GREEN + " PUMPAD SCRIPT BOT ")
        print(Fore.RED + f"TELEGRAM GROUP {Fore.GREEN}@DigitalMiners777")
        print(Fore.YELLOW + " DEVELOPED BY @Anaik123 ")
        print(f"{Fore.WHITE}~" * 60)

    def user_information(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/tg/user/information'
        self.headers.update({'Authorization': f'tma {query}'})
        response = self.scraper.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def get_lottery(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/lottery'
        self.headers.update({'Authorization': f'tma {query}'})
        response = self.scraper.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def post_lottery(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/lottery'
        self.headers.update({'Authorization': f'tma {query}'})
        response = self.scraper.post(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def get_missions(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/tg/missions'
        self.headers.update({'Authorization': f'tma {query}'})
        response = self.scraper.get(url, headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def post_missions(self, query: str, mission_id: int):
        url = f'https://tg.pumpad.io/referral/api/v1/tg/missions/check/{mission_id}'
        self.headers.update({'Authorization': f'tma {query}'})
        response = self.scraper.post(url, headers=self.headers, json={})
        return response.json() if response.status_code == 200 else None

    def checkin(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/tg/raffle/checkin'
        self.headers.update({'Authorization': f'tma {query}'})
        response = self.scraper.post(url, headers=self.headers)
        if response.status_code == 200:
            self.log(Fore.GREEN + 'Checkin successful! ✅')
        else:
            self.log(Fore.RED + 'Failed checkin or already checked in today ❌')

    def raffle(self, query: str):
        url = 'https://tg.pumpad.io/referral/api/v1/tg/raffle/bets'
        self.headers.update({'Authorization': f'tma {query}'})
        remain_count = 1
        while remain_count > 0:
            response = self.scraper.post(url, headers=self.headers)
            remain_count = response.json().get('remain_count', 0)
            self.log(Fore.YELLOW + f"You have {Fore.WHITE}{remain_count}{Fore.YELLOW} remaining tickets 🎫")
            time.sleep(1)

        url = 'https://tg.pumpad.io/referral/api/v1/tg/raffle/numbers?raffle_id=8'
        response = self.scraper.get(url, headers=self.headers)
        self.log(Fore.GREEN + f"You have total {Fore.WHITE}{len(response.json())}{Fore.GREEN} tickets 🎟️")

    def process_query(self, query: str):
        try:
            user = self.user_information(query)
            if user:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{user['user_name']}{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]"
                )

            missions = self.get_missions(query)
            if missions and 'mission_list' in missions:
                for mission in missions['mission_list']:
                    mission_id = mission['mission']['id']
                    mission_name = mission['mission']['name']
                    mission_reward = mission['mission']['reward']
                    done_time = mission['done_time']

                    if mission_id == 38:
                        self.log(f"{Fore.YELLOW}Skipping mission {mission_name} 🚫")
                        continue

                    if done_time == 0:
                        complete = self.post_missions(query, mission_id)
                        if complete:
                            self.log(f"{Fore.GREEN}Mission {mission_name} completed ✅. Reward: + {mission_reward} Draw Count 🎯")
                        else:
                            self.log(f"{Fore.RED}Mission {mission_name} not completed ❌")
                    else:
                        self.log(f"{Fore.YELLOW}Mission {mission_name} already completed ✅")
            else:
                self.log(f"{Fore.GREEN}No missions available 🔍")

            draw = self.post_lottery(query)
            if draw:
                if 'reward' in draw:
                    self.log(f"{Fore.GREEN}Draw successful: {draw['reward']['name']} 🎉")
                else:
                    self.log(f"{Fore.RED}Draw not successful ❌")

            lottery = self.get_lottery(query)
            if lottery:
                count = lottery['draw_count']
                while count > 0:
                    draw = self.post_lottery(query)
                    if draw and 'reward' in draw:
                        self.log(f"{Fore.GREEN}Draw successful: {draw['reward']['name']} 🎉")
                    count -= 1
                if count == 0:
                    self.log(f"{Fore.YELLOW}No draw count remaining ⏳")
            else:
                self.log(f"{Fore.RED}Failed to get lottery data ❌")

            self.checkin(query)
            self.raffle(query)

        except RequestException:
            self.log(f"{Fore.RED}[ Blocked by Cloudflare ] Try running again 🔄")

    def login(self):
        expected_key = "Digitalminers"  # The key that must be entered to start
        user_key = input(f"{Fore.YELLOW}Enter the login key: {Style.RESET_ALL}")
        if user_key != expected_key:
            self.log(Fore.RED + "Invalid key! Exiting the script... 🚫")
            exit()
        else:
            self.log(Fore.GREEN + "Login successful! 🚀")

    def main(self):
        try:
            self.login()  # Prompt for login before continuing

            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            for i, query in enumerate(queries):
                query = query.strip()
                if query:
                    self.log(
                        f"{Fore.GREEN + Style.BRIGHT}Processing Account {i + 1}/{len(queries)} ➡️{Style.RESET_ALL}"
                    )
                    self.process_query(query)
                    self.log(f"{Fore.CYAN + Style.BRIGHT}- {Style.RESET_ALL}" * 75)
                    time.sleep(random.randint(1, 3))  # Short delay between accounts

        except KeyboardInterrupt:
            self.log(f"{Fore.RED}[ EXIT ] Pumpad - BOT 🛑")
        except Exception as e:
            self.log(f"{Fore.RED}An error occurred: {e} ⚠️")


if __name__ == "__main__":
    pumpad = Pumpad()
    pumpad.clear_terminal()
    pumpad.welcome()
    pumpad.main()