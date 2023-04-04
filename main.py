import customtkinter
from PIL import ImageTk, Image, ImageEnhance
import math

customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

def MatchPage():
    print("match page")


def DataPage():
    print("data page wooh!")


root = customtkinter.CTk()
root.attributes('-fullscreen', True)

topframe = customtkinter.CTkFrame(master=root, bg_color="#4D6394", fg_color="#4D6394", height=90)
topframe.pack(side="top", fill="both", expand=True)

frame = customtkinter.CTkFrame(master=root)
frame.pack(side="right", pady=50, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=topframe, text="OVERSTAT V2.1",
                               font=customtkinter.CTkFont(family="BankSansEFCY-Bol", size=29), text_color='#ffffff')
label.place(x=(1920 / 2) - 120, y=30)

left_sidebar_frame = customtkinter.CTkFrame(master=root, bg_color='#3f9ae0', fg_color='#3f9ae0')
left_sidebar_frame.pack(side="left", fill="both")
left_sidebar_frame.configure(width=140, height=1200)

match_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="Match Summary",
                                       command=MatchPage, width=140)
match_button.place(y=10)

data_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="Player Comparison",
                                      command=DataPage, width=140)
data_button.place(y=45)

data_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="Data Bank",
                                      command=DataPage, width=140)
data_button.place(y=80)

def FetchHeroIcon(heroName, crop_x_left, crop_x_right, crop_y_top, crop_y_bottom, sizex=50, sizey=50):
    portrait3d = Image.open("3d icons/Icon-" + heroName + ".png")
    portrait3d = portrait3d.resize((sizex, sizey), Image.LANCZOS)
    filter = ImageEnhance.Contrast(portrait3d)
    portrait3d = filter.enhance(0.9)
    cropped = portrait3d.crop(
        [(sizex * crop_x_left), (sizey * crop_y_top), sizex - (sizex * crop_x_right), sizey - (sizey * crop_y_bottom)])
    portrait3d_photoimage = ImageTk.PhotoImage(cropped)
    return (portrait3d_photoimage)


class Match:

    def __init__(self, file):
        self.players = []

        # Information log params
        self.match_round = []
        self.num_living_players_t1 = []
        self.num_living_players_t2 = []
        self.array_living_players_t1 = []
        self.array_living_players_t2 = []
        self.array_dead_players_t1 = []
        self.array_dead_players_t2 = []
        self.team_score_t1 = []
        self.team_score_t2 = []

        # Game mode log params (paragraph break for different per-gm functions)
        self.game_mode = ""
        self.time_elapsed = []
        self.control_mode_score_percent_t1 = []
        self.control_mode_score_percent_t2 = []
        self.is_control_point_locked = []
        self.control_mode_scoring_team = []
        self.num_players_on_control_point = []

        self.is_team_1_attacking = []
        self.payload_progress_percent = []
        self.objective_index = []

        self.point_capture_percent = []

        self.push_payload_pos_x = []
        self.push_payload_pos_y = []
        self.push_payload_pos_z = []
        # This will be based off a read graph as described in notepad 'push' and will go from -100% to 100% (or just
        # -1 to 1)
        self.push_percent = []

        # Determining the map for a given file passed in
        self.modified = []
        self.file = open(file, "r")
        self.read = self.file.readlines()

        for line in self.read:
            if line[-1] == '\n':
                self.modified.append(line[11:])

            self.map = self.modified[0]
            for index, char in enumerate(self.map):

                if char == ",":
                    len_of_mapline = len(self.map)
                    index_of_end_map = index
                    self.map = self.map[:-(len_of_mapline - index)]
                    break

        # Determing gamemode info from gamemode logs (one of the two non-player logs)
        for index, line in enumerate(self.read):
            split = line.split(",")
            if line.__contains__("INFORMATION LOG"):
                # Logic for information log
                self.match_round.append(split[0].split(" ")[1])
                self.num_living_players_t1.append(split[1])
                self.num_living_players_t2.append(split[2])
                self.array_living_players_t1.append(split[3])
                self.array_living_players_t2.append(split[4])
                self.array_dead_players_t1.append(split[5])
                self.array_dead_players_t2.append(split[6])
                self.team_score_t1.append(split[7])
                self.team_score_t2.append(split[8])
            elif not line.__contains__("PLAYER LOG") and index > 1:
                # Logic for game mode log
                self.game_mode = split[0].split(" ")[1]
                self.time_elapsed.append(split[1])
                if self.game_mode == "Control":
                    self.control_mode_score_percent_t1.append(split[2])
                    self.control_mode_score_percent_t2.append(split[3])
                    self.is_control_point_locked.append(split[4])
                    self.control_mode_scoring_team.append(split[5])
                    self.num_players_on_control_point.append(split[6])
                elif self.game_mode == "Escort":
                    self.is_team_1_attacking.append(split[2])
                    self.payload_progress_percent.append(split[3])
                    self.objective_index.append(split[4])
                elif self.game_mode == "Assault":
                    self.is_team_1_attacking.append(split[2])
                    self.point_capture_percent.append(split[3])
                    self.objective_index.append(split[4])
                elif self.game_mode == "Hybrid":
                    self.is_team_1_attacking.append(split[2])
                    self.point_capture_percent.append(split[3])
                    self.payload_progress_percent.append(split[4])
                    self.objective_index.append(split[5])
                elif self.game_mode == "Push":
                    self.push_payload_pos_x.append(split[2][1:-1])
                    self.push_payload_pos_y.append(split[3][1:])
                    self.push_payload_pos_z.append(split[4][1:-3])

        # Creating each player object for the match based on username from the second log line
        players_line_split = self.read[1].split(",")
        self.team1player1 = Player(players_line_split[0].split(" ")[1], self.players)
        self.team1player2 = Player(players_line_split[1], self.players)
        self.team1player3 = Player(players_line_split[2], self.players)
        self.team1player4 = Player(players_line_split[3], self.players)
        self.team1player5 = Player(players_line_split[4], self.players)

        self.team2player1 = Player(players_line_split[6], self.players)
        self.team2player2 = Player(players_line_split[7], self.players)
        self.team2player3 = Player(players_line_split[8], self.players)
        self.team2player4 = Player(players_line_split[9], self.players)
        self.team2player5 = Player(players_line_split[10], self.players)

        # Determining which lines need to be logged and the relevant player object to log them under
        for index, line in enumerate(self.read):
            if line.__contains__("PLAYER LOG"):
                split_player_var_log = line.split(",")
                for player in self.players:
                    if split_player_var_log[1] == player.playername:
                        player.AddLog(line)


class Player:

    def __init__(self, playername, players):
        self.match_time_elapsed = []
        self.hero = []
        self.h_dmg_dealt = []
        self.b_dmg_dealt = []
        self.dmg_mitigated = []
        self.dmg_taken = []
        self.deaths = []
        self.eliminations = []
        self.final_blows = []
        self.environmental_deaths = []
        self.environmental_kills = []
        self.healing_dealt = []
        self.objective_kills = []
        self.solo_kills = []
        self.ultimates_earned = []
        self.ultimates_used = []
        self.healing_received = []
        self.ult_charge_percent = []
        self.player_closest_to_reticle = []
        self.x_pos = []
        self.y_pos = []
        self.z_pos = []
        self.team = []
        self.ability_1_cd = []
        self.ability_2_cd = []
        self.health = []
        self.max_health = []
        self.health_type_health = []
        self.health_type_armour = []
        self.health_type_shields = []

        self.logs_count = 0

        self.playername = playername

        players.append(self)

    def AddLog(self, line):
        self.logs_count += 1
        split_player_log = line.split(",")
        self.match_time_elapsed.append(split_player_log[0].split(" ")[1])
        if split_player_log[2] == "LÃºcio" or split_player_log[2] == "Lúcio" or split_player_log[2] == "Lucio":
            self.hero.append("Lucio")
        else:
            self.hero.append(split_player_log[2])
            self.h_dmg_dealt.append(split_player_log[3])
            self.b_dmg_dealt.append(split_player_log[4])
            self.dmg_mitigated.append(split_player_log[5])
            self.dmg_taken.append(split_player_log[6])
            self.deaths.append(split_player_log[7])
            self.eliminations.append(split_player_log[8])
            self.final_blows.append(split_player_log[9])
            self.environmental_deaths.append(split_player_log[10])
            self.environmental_kills.append(split_player_log[11])
            self.healing_dealt.append(split_player_log[12])
            self.objective_kills.append(split_player_log[13])
            self.solo_kills.append(split_player_log[14])
            self.ultimates_earned.append(split_player_log[15])
            self.ultimates_used.append(split_player_log[16])
            self.healing_received.append(split_player_log[17])
            self.ult_charge_percent.append(split_player_log[18])
            self.player_closest_to_reticle.append(split_player_log[19])
            self.x_pos.append(split_player_log[20][1:])
            self.y_pos.append(split_player_log[21])
            self.z_pos.append(split_player_log[22][:-1])
            self.team.append(split_player_log[23])
            self.ability_1_cd.append(split_player_log[24])
            self.ability_2_cd.append(split_player_log[25])
            self.health.append(split_player_log[26])
            self.max_health.append(split_player_log[27])
            self.health_type_health.append(split_player_log[28])
            self.health_type_armour.append(split_player_log[29])
            self.health_type_shields.append(split_player_log[30])


def CreatePlayerNameAndIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName, heroName, weighting, hero2Name, weighting2, hero3Name, weighting3):
    # i.e. if all three 'most played hero' slots are populated
    icon = customtkinter.CTkLabel(master=frame,
                                  image=FetchHeroIcon(heroName, 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
                                  text="")
    if left_align:
        icon.place(x=0 + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))
    else:
        icon.place(x=1660 - icon_size_x + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))

    icon2 = customtkinter.CTkLabel(master=frame,
                                   image=FetchHeroIcon(hero2Name, 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
                                   text="")
    if left_align:
        icon2.place(x=0 + starting_x + icon_size_x, y=0 + starting_y + (vertical_slot * icon_size_y))
    else:
        icon2.place(x=1660 - (icon_size_x * 2) + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))

    icon3 = customtkinter.CTkLabel(master=frame,
                                   image=FetchHeroIcon(hero3Name, 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
                                   text="")
    if left_align:
        icon3.place(x=0 + starting_x + (2 * icon_size_x), y=0 + starting_y + (vertical_slot * icon_size_y))
    else:
        icon3.place(x=1660 - (icon_size_x * 3) + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))

    fontsize = round(0.9 + icon_size_y / 2.75)
    name = customtkinter.CTkLabel(master=frame, text=playerName.upper(),
                                  font=customtkinter.CTkFont(family="BankSansEFCY-Reg", size=fontsize),
                                  text_color='#383235')
    if left_align:
        name.place(x=9 + (3.5 * icon_size_x) + starting_x,
                   y=(0.2 * icon_size_y) + starting_y + (vertical_slot * icon_size_y))
    else:
        name.place(x=1559 - (3.5 * icon_size_x) + starting_x,
                   y=(0.25 * icon_size_y) + starting_y + (vertical_slot * icon_size_y))


def ParseHeroPlaytimeDataForMatch(playerName, match):
    timeplayed_hero_dict = {}

    for player in match.players:
        if player.playername == playerName:
            for log in range(player.logs_count - 1):
                if player.hero[log] in timeplayed_hero_dict:
                    timeplayed_hero_dict[player.hero[log]] += 1
                else:
                    timeplayed_hero_dict[player.hero[log]] = 1

    return timeplayed_hero_dict


def ParseHeroPlaytimeDataForMatchCollection(playerName, matchCollection):
    timeplayed_hero_dict = {}

    for match in matchCollection:
        for key, value in ParseHeroPlaytimeDataForMatch(playerName, match).items():
            if key in timeplayed_hero_dict.keys():
                timeplayed_hero_dict[key] += value
            else:
                timeplayed_hero_dict[key] = value

    return timeplayed_hero_dict


def FindTop3(parsedHeroPlaytimeData):
    highest_h_count = 0
    second_highest_h_count = 0
    third_highest_h_count = 0
    most_played = ""
    second_most_played = ""
    third_most_played = ""
    proportion_of_first = 0
    proportion_of_second = 0
    proportion_of_third = 0

    total_playtime = sum(parsedHeroPlaytimeData.values())

    top3list = sorted(parsedHeroPlaytimeData, key=parsedHeroPlaytimeData.get, reverse=True)[:3]
    # print(top3list)

    returnlist = ["" for i in range(6)]
    for index, hero in enumerate(top3list):
        returnlist[index*2] = hero
        returnlist[index*2+1] = parsedHeroPlaytimeData[hero]/total_playtime

    return returnlist



match1 = Match("Log-2023-04-02-17-27-33.txt")
match2 = Match("Log-2023-04-02-16-02-30.txt")
match3 = Match("Log-2023-04-03-15-25-56.txt")

some_data_collection = [match1, match2]



t1p1_hero = FindTop3(ParseHeroPlaytimeDataForMatch("morning", match3))
t2p1_hero = FindTop3(ParseHeroPlaytimeDataForMatchCollection("Coronet", some_data_collection))

CreatePlayerNameAndIconGUI(60, 60, 0, 0, True, 0, match3.team1player1.playername, t1p1_hero[0], t1p1_hero[1], t1p1_hero[2], t1p1_hero[3], t1p1_hero[4], t1p1_hero[5])
CreatePlayerNameAndIconGUI(60, 60, 0, 0, False, 0, match1.team2player1.playername, t2p1_hero[0], t2p1_hero[1], t2p1_hero[2], t2p1_hero[3], t2p1_hero[4], t2p1_hero[5])

# CreatePlayerNameAndIconGUI(60, 60, 0, 0, True, 1, "Bob", "Reinhardt", 1)

# CreatePlayerNameAndIconGUI(60, 60, 0, 0, False, 1, "Stewart", "Zarya", 1)

root.mainloop()

# FIND A WAY TO GET THE SPECIFIC MAP I.E. ICEBREAKER OR LABS OR SUB LEVEL BY NAME (NO EASILY FOUND WAY TO DO THIS BUT
# U CAN DO IT I KNOW YOU CAN, EVEN IF IT MEANS SELECTING THE MAPS IN A PSEUDO-RANDOM ORDER RATHER THAN LETTING THE
# GAME HANDLE IT)

# Add events for sources of elms / damages / deaths like who the attacker is, what ability/ult/primary/secondary did
# it, etc

# ur rounding method for the icons could be reviewed and made much smarter, rn it kinda sucks

# MAKE IT WORK WITH LEAVERS

# ok push is implemented, so it won't crash but now unfortunately to know is pushing I think you'll need arrays of both
# teams of who is on payload / bot and u need ur in/out graph / spline thing as well for distance, also forward
# spawn appears not to affect obj index so that has to be manual as well

# also find a way to log zar and sym energy

# ^ to do this ill have to recreate the system by decaying their number per patch notes and adding it based on h + b
# damage
