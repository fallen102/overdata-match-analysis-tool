import os
import threading
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import customtkinter
from PIL import ImageTk, Image, ImageEnhance
import math
import seaborn as sns


def MatchPage():
    data_frame.pack_forget()
    player_comparison_frame.pack_forget()
    frame.pack(side="right", pady=50, padx=60, fill="both", expand=True)


def DataPage():
    frame.pack_forget()
    player_comparison_frame.pack_forget()
    data_frame.pack(side="right", pady=50, padx=60, fill="both", expand=True)


def PlayerComparisonPage():
    frame.pack_forget()
    data_frame.pack_forget()
    player_comparison_frame.pack(side="right", pady=50, padx=60, fill="both", expand=True)


hero_colour_dict = {"Ana": "7484B5", "Ashe": "D5D9DA", "Baptiste": "189B89", "Bastion": "88A14E", "Brigitte": "B47317", "Cassidy": "873128", "D.Va": "DC60BD", "Doomfist": "5B3C28", "Echo": "74C3FC", "Genji": "B4F902",
                    "Hanzo": "5E697F", "Junker Queen": "376CB2", "Junkrat": "DEDC93", "Kiriko": "216B5E", "Lucio": "58C633", "Mei": "4FA2FF", "Mercy": "F9F8CA", "Moira": "DB4216", "Orisa": "CAD701", "Pharah": "2A63B0",
                    "Ramattra": "6844DA", "Reaper": "970707", "Reinhardt": "B4BDBE", "Roadhog": "E78E00", "Sigma": "24DADE", "Sojourn": "EE1B00", "Soldier": "334C8E", "Sombra": "B105BB",
                    "Symmetra": "00B7F0", "Torbjorn": "F3543E", "Tracer": "FFA31E", "Widowmaker": "7857C0", "Winston": "444051", "Wrecking Ball": "C48C2D", "Zarya": "F160AD", "Zenyatta": "98892E"}


customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.attributes('-fullscreen', True)

topframe = customtkinter.CTkFrame(master=root, bg_color="#4D6394", fg_color="#4D6394", height=90)
topframe.pack(side="top", fill="both", expand=True)

frame = customtkinter.CTkFrame(master=root, bg_color="#ffffff", fg_color="#ffffff")
frame.pack(side="right", pady=50, padx=60, fill="both", expand=True)

player_comparison_frame = customtkinter.CTkFrame(master=root, bg_color="#ffffff", fg_color="#ffffff")

data_frame = customtkinter.CTkFrame(master=root, bg_color="#ffffff", fg_color="#ffffff")

# Temporary exit icon to close app
exit_icon = Image.open("Button Icons/Exit.png")
exit_icon = exit_icon.resize((30, 30), Image.LANCZOS)
exit_icon_pi = ImageTk.PhotoImage(exit_icon)
exit_button = customtkinter.CTkButton(master=topframe, text="", image=exit_icon_pi, width=30, height=90, command=exit, bg_color='#3f9ae0', fg_color='#3f9ae0')
exit_button.pack(side="top", anchor="ne")

title = customtkinter.CTkLabel(master=topframe, text="OVERDATA V2.1", font=customtkinter.CTkFont(family="BankSansEFCY-Bol", size=29), text_color='#ffffff')
title.place(x=(1920 / 2) - 120, y=30)

left_sidebar_frame = customtkinter.CTkFrame(master=root, bg_color='#3f9ae0', fg_color='#3f9ae0')
left_sidebar_frame.pack(side="left", fill="both")
left_sidebar_frame.configure(width=140, height=1200)

match_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="MATCH SUMMARY", command=MatchPage, width=140)
match_button.place(y=10)

data_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="PLAYER COMPARISON", command=DataPage, width=140)
data_button.place(y=45)

data_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="DATA BANK", command=DataPage, width=140)
data_button.place(y=80)


def FetchHeroIcon(heroName, crop_x_left, crop_x_right, crop_y_top, crop_y_bottom, icon_type, sizex=50, sizey=50):
    portrait3d = Image.open(icon_type + "_Hero_Icons/Icon-" + heroName + ".png")
    portrait3d = portrait3d.resize((sizex, sizey), Image.LANCZOS)
    filter = ImageEnhance.Contrast(portrait3d)
    portrait3d = filter.enhance(0.9)
    cropped = portrait3d.crop(
        [(sizex * crop_x_left), (sizey * crop_y_top), sizex - (sizex * crop_x_right), sizey - (sizey * crop_y_bottom)])
    portrait3d_photoimage = ImageTk.PhotoImage(cropped)
    return (portrait3d_photoimage)


# Somewhat copy-paste of FetchHeroIcon but its only two functions for now and very little code so whatever. I'll make modular later if need be, otherwise this feels like the best solution
def FetchHeroColour(heroName, sizex=50, sizey=15):
    colourimage = Image.open("Hero_Colours/" + heroName + ".PNG")
    colourimage = colourimage.resize((sizex, sizey), Image.LANCZOS)
    colourimage_photoimage = ImageTk.PhotoImage(colourimage)
    return colourimage_photoimage


class Match:

    def __init__(self, file):

        self.match_stats = {"Map": "", "Players": list(), "Match Round": list(),
                            "Array Of Living Players Team 1": list(), "Array Of Living Players Team 2": list(),
                            "Array Of Dead Players Team 1": list(), "Array Of Dead Players Team 2": list(),
                            "Number Of Living Players Team 1": list(), "Number Of Living Players Team 2": list(),
                            "Team Score Team 1": list(), "Team Score Team 2": list(), "Gamemode": "",
                            "Time Elapsed": list(), "Control Mode Score Percentage Team 1": list(),
                            "Control Mode Score Percentage Team 2": list(), "Is Control Point Locked?": list(),
                            "Control Mode Scoring Team": list(), "Number Of Players On Control Point": list(),
                            "Is Team 1 Attacking?": list(),
                            "Payload Progress Percentage": list(), "Objective Index": list(),
                            "Point Capture Percentage": list(), "Push Bot X Position": list(),
                            "Push Bot Y Position": list(), "Push Bot Z Position": list(),
                            "Push Percentage": list(), "Match Time Elapsed": list(),
                            "Time Between Global Logs": 2, "Time Between T1P1 Player Log": 1,
                            "Team 1 Name": "", "Team 2 Name": ""}
        # ^ Push Percentage is yet to be implemented

        self.modified = []
        self.file = open("Logs/" + file, "r")
        self.read = self.file.readlines()

        split = self.read[0].split(",")
        self.match_stats["Map"] = split[0]
        self.match_stats["Team 1 Name"] = split[1]
        self.match_stats["Team 2 Name"] = split[2]
        self.match_stats["Time Between Global Logs"] = split[3]
        self.match_stats["Time Between T1P1 Player Log"] = split[4]

        for index, line in enumerate(self.read):
            split = line.split(",")
            if line.__contains__("Information Log"):
                # "Minimum" gamemode logging setting
                if split[0].split(" ")[1] == 0:
                    self.match_stats["Match Round"].append(split[1])
                    self.match_stats["Team Score Team 1"].append(split[2])
                    self.match_stats["Team Score Team 2"].append(split[3])
                # "Performance" gamemode logging setting
                elif split[0].split(" ")[1] == 1:
                    self.match_stats["Match Round"].append(split[1])
                    self.match_stats["Number Of Living Players Team 1"].append(split[2])
                    self.match_stats["Number Of Living Players Team 2"].append(split[3])
                    self.match_stats["Team Score Team 1"].append(split[4])
                    self.match_stats["Team Score Team 2"].append(split[5])
                elif split[0].split(" ")[1] == 2:
                # "Maximum" gamemode logging setting
                    self.match_stats["Match Round"].append(split[1])
                    # These array entries will need to be reconfigured a bit here once you have a working log to test with, because the individual items of the array will be comma-separated
                    self.match_stats["Array Of Living Players Team 1"].append(split[2])
                    self.match_stats["Array Of Living Players Team 2"].append(split[3])
                    self.match_stats["Array Of Dead Players Team 1"].append(split[4])
                    self.match_stats["Array Of Dead Players Team 2"].append(split[5])
                    self.match_stats["Team Score Team 1"].append(split[6])
                    self.match_stats["Team Score Team 2"].append(split[7])
            elif line.__contains__("MG Log"):
            # This also needs to be adjusted because it will include logs for final blows and resurrects and whatnot, those should be a given a tag to check for here like "Event Log" or gm can be given "Gamemode Log"
                # Logic for map & game mode log
                self.match_stats["Gamemode"] = split[0].split(" ")[1]
                self.match_stats["Match Time Elapsed"].append(split[1])
                if self.match_stats["Gamemode"] == "Control":
                    self.match_stats["Control Mode Score Percentage Team 1"].append(split[2])
                    self.match_stats["Control Mode Score Percentage Team 2"].append(split[3])
                    self.match_stats["Is Control Point Locked?"].append(split[4])
                    self.match_stats["Control Mode Scoring Team"].append(split[5])
                    self.match_stats["Number Of Players On Control Point"].append(split[6])
                elif self.match_stats["Gamemode"] == "Escort":
                    self.match_stats["Is Team 1 Attacking?"].append(split[2])
                    self.match_stats["Payload Progress Percentage"].append(split[3])
                    self.match_stats["Objective Index"].append(split[4])
                elif self.match_stats["Gamemode"] == "Assault":
                    self.match_stats["Is Team 1 Attacking?"].append(split[2])
                    self.match_stats["Point Capture Percentage"].append(split[3])
                    self.match_stats["Objective Index"].append(split[4])
                elif self.match_stats["Gamemode"] == "Hybrid":
                    self.match_stats["Is Team 1 Attacking?"].append(split[2])
                    self.match_stats["Point Capture Percentage"].append(split[3])
                    self.match_stats["Payload Progress Percentage"].append(split[4])
                    self.match_stats["Objective Index"].append(split[5])
                elif self.match_stats["Gamemode"] == "Push":
                    self.match_stats["Push Bot X Position"].append(split[2][1:-1])
                    self.match_stats["Push Bot Y Position"].append(split[3][1:])
                    self.match_stats["Push Bot Z Position"].append(split[4][1:-3])

        # Creating each player object for the match based on username from the second log line
        self.new_line = self.read[1].replace("0", "")
        players_line_split = self.new_line.split(",")
        self.team1player1 = Player(players_line_split[0].split(" ")[1], self.match_stats["Time Between T1P1 Player Log"])
        self.team1player2 = Player(players_line_split[1], self.match_stats["Time Between T1P1 Player Log"])
        self.team1player3 = Player(players_line_split[2], self.match_stats["Time Between T1P1 Player Log"])
        self.team1player4 = Player(players_line_split[3], self.match_stats["Time Between T1P1 Player Log"])
        self.team1player5 = Player(players_line_split[4], self.match_stats["Time Between T1P1 Player Log"])

        self.team2player1 = Player(players_line_split[6], self.match_stats["Time Between T1P1 Player Log"])
        self.team2player2 = Player(players_line_split[7], self.match_stats["Time Between T1P1 Player Log"])
        self.team2player3 = Player(players_line_split[8], self.match_stats["Time Between T1P1 Player Log"])
        self.team2player4 = Player(players_line_split[9], self.match_stats["Time Between T1P1 Player Log"])
        self.team2player5 = Player(players_line_split[10], self.match_stats["Time Between T1P1 Player Log"])

        self.players = [self.team1player1, self.team1player2, self.team1player3, self.team1player4, self.team1player5,
                        self.team2player1, self.team2player2, self.team2player3, self.team2player4, self.team2player5]

        # Determining which lines need to be logged and the relevant player object to log them under
        for index, line in enumerate(self.read):
            if line.__contains__("Player Log"):
                split_player_var_log = line.split(",")
                for player in self.players:
                    if split_player_var_log[1] == player.player_stats["Player Name"]:
                        player.AddLog(line)


class Player:

    def __init__(self, playername, time_between_player_logs):
        self.player_stats = {"Match Time Elapsed": list(), "Hero": list(), "Hero Damage Dealt": list(),
                             "Barrier Damage Dealt": list(), "Damage Mitigated": list(), "Damage Taken": list(),
                             "Deaths": list(), "Eliminations": list(),
                             "Final Blows": list(), "Environmental Deaths": list(), "Environmental Kills": list(),
                             "Healing Dealt": list(), "Objective Kills": list(), "Solo Kills": list(),
                             "Ultimates Earned": list(), "Ultimates Used": list(),
                             "Healing Received": list(), "Ultimate Charge Percentage": list(),
                             "Ability 1 Cooldown": list(), "Ability 2 Cooldown": list(), "Total Health": list(),
                             "Max Health": list(), "Logs Count": 0, "Player Name": playername, "Time Between Player Logs": time_between_player_logs}

    def AddLog(self, line):

        self.player_stats["Logs Count"] += 1
        split_player_log = line.split(",")

        self.player_stats["Match Time Elapsed"].append(split_player_log[0].split(" ")[1])

        if split_player_log[2] == "LÃºcio" or split_player_log[2] == "Lúcio" or split_player_log[2] == "Lucio":
            self.player_stats["Hero"].append("Lucio")
        elif split_player_log[2] == "Soldier: 76":
            self.player_stats["Hero"].append("Soldier")
        else:
            self.player_stats["Hero"].append(split_player_log[2])

        self.player_stats["Hero Damage Dealt"].append(split_player_log[3])
        self.player_stats["Barrier Damage Dealt"].append(split_player_log[4])
        self.player_stats["Damage Mitigated"].append(split_player_log[5])
        self.player_stats["Damage Taken"].append(split_player_log[6])
        self.player_stats["Deaths"].append(split_player_log[7])
        self.player_stats["Eliminations"].append(split_player_log[8])
        self.player_stats["Final Blows"].append(split_player_log[9])
        self.player_stats["Environmental Deaths"].append(split_player_log[10])
        self.player_stats["Environmental Kills"].append(split_player_log[11])
        self.player_stats["Healing Dealt"].append(split_player_log[12])
        self.player_stats["Objective Kills"].append(split_player_log[13])
        self.player_stats["Solo Kills"].append(split_player_log[14])
        self.player_stats["Ultimates Earned"].append(split_player_log[15])
        self.player_stats["Ultimates Used"].append(split_player_log[16])
        self.player_stats["Ultimate Charge Percentage"].append(split_player_log[17])
        self.player_stats["Healing Received"].append(split_player_log[18])
        self.player_stats["Ability 1 Cooldown"].append(split_player_log[19])
        self.player_stats["Ability 2 Cooldown"].append(split_player_log[20])
        self.player_stats["Total Health"].append(split_player_log[21])
        self.player_stats["Max Health"].append(split_player_log[22])


def CreatePlayerIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerObject, heroes, displayPlaytimeBar, icon_type, displayed_stats, display_team_name, displayPlaytimeTextAswell):
    top3 = FindTop3(heroes)

    if len(top3) < 3:
        for i in range(3-len(top3)):
            top3.append("")

    index = 0
    playtimeBarPadding = 1
    if displayPlaytimeBar:
        playtimeBarPadding = 1.2
        if displayPlaytimeTextAswell:
            playtimeBarPadding = 1.4

    for hero in top3:
        icon = customtkinter.CTkLabel(master=frame, image=FetchHeroIcon(hero, 0, 0, 0, 0, icon_type, sizex=icon_size_x, sizey=icon_size_y), text="")
        if left_align:
            icon_x_pos = 0 + starting_x + (index * icon_size_x)
            icon_y_pos = 0 + starting_y + (vertical_slot * icon_size_y * playtimeBarPadding)
            icon.place(x=icon_x_pos, y=icon_y_pos)
        else:
            icon_x_pos = 1660 - icon_size_x - (index * icon_size_x) + starting_x
            icon_y_pos = 0 + starting_y + (vertical_slot * icon_size_y * playtimeBarPadding)
            icon.place(x=icon_x_pos, y=icon_y_pos)

        if displayPlaytimeBar and hero != "":
            proportion_of_hero_played = ProportionOfHeroPlayed(heroes, hero)
            round_proportion = round(proportion_of_hero_played * icon_size_x)
            if round_proportion < 1:
                round_proportion = 1
            playtimeBar = customtkinter.CTkLabel(master=frame, text="", image=FetchHeroColour(hero, round_proportion, 10), height=10, width=round_proportion)
            playtimeBar.place(x=icon_x_pos, y=icon_y_pos + icon_size_y)
            if displayPlaytimeTextAswell:
                minutes_played = math.ceil(proportion_of_hero_played * int(playerObject.player_stats["Logs Count"]) * int(playerObject.player_stats["Time Between Player Logs"]) / 60)
                playtimeText = customtkinter.CTkLabel(master=frame, text=str(minutes_played) + " MINS", font=customtkinter.CTkFont(family="BankSansEFCY-Bol", size=12), text_color="#"+hero_colour_dict[hero])
                playtimeText.place(x=icon_x_pos, y=icon_y_pos + icon_size_y + 10)
        index += 1

    multiplier = 8
    length_of_prev = multiplier
    # This should be altered so that the spacing (what _index is multiplied by) is dependent on the length of the previous string
    for _index, stat in enumerate(displayed_stats):
        stat_label = customtkinter.CTkLabel(master=frame, text=stat.upper(), font=customtkinter.CTkFont(family="BankSansEFCY-Bol", size=14), text_color='#424366')
        length_of_prev_spacing_multiplier = (length_of_prev * 4)+85
        if left_align:
            label_x = 10 + starting_x + ((index) * icon_size_x) + (_index*length_of_prev_spacing_multiplier)
            label_y = 0 + starting_y + (vertical_slot * icon_size_y * playtimeBarPadding) + icon_size_y/3
            stat_label.place(x=label_x, y=label_y)
        else:
            label_x = 1560 - ((index) * icon_size_x) + starting_x - (_index*length_of_prev_spacing_multiplier)
            label_y = 0 + starting_y + (vertical_slot * icon_size_y * playtimeBarPadding) + icon_size_y/3
            stat_label.place(x=label_x, y=label_y)
        length_of_prev = len(str(stat))


def CreateMatchGUI(icon_size_x, icon_size_y, starting_x, starting_y, match, displayPlaytimeBar, icon_type, displayed_stats, display_team_name, displayPlaytimeTextAswell):

    # Create team name
    t1_label = customtkinter.CTkLabel(master=frame, text=match.match_stats["Team 1 Name"],font=customtkinter.CTkFont(family="BankSansEFCY-Bol", size=20),text_color='#424366')
    t2_label = customtkinter.CTkLabel(master=frame, text=match.match_stats["Team 2 Name"],font=customtkinter.CTkFont(family="BankSansEFCY-Bol", size=20),text_color='#424366')

    t1_label.place(x=200, y=25)
    t2_label.place(x=1200, y=25)

    if display_team_name:
        index = 0
        add_index = 1
    else:
        index = 0

    for player in match.players:
        if player.player_stats["Player Name"] != "":
            return_stats = []
            if index < 5:
                left_align = True
                vertical_slot = index + add_index
            else:
                left_align = False
                vertical_slot = index+add_index-5
            for item in displayed_stats:
                if type(player.player_stats[item]) is not str:
                    return_stats.append(player.player_stats[item][player.player_stats["Logs Count"]-1])
                else:
                    return_stats.append(player.player_stats[item])
            CreatePlayerIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, player, ParseHeroPlaytimeData(player), displayPlaytimeBar, icon_type, return_stats, display_team_name, displayPlaytimeTextAswell)
        index += 1


def ProportionOfHeroPlayed(heroes, hero):
    total_playtime = sum(heroes.values())
    return heroes[hero] / total_playtime


def ParseHeroPlaytimeData(playerObject):
    timeplayed_hero_dict = {}

    for log in range(playerObject.player_stats["Logs Count"] - 1):
        if playerObject.player_stats["Hero"][log] in timeplayed_hero_dict:
            timeplayed_hero_dict[playerObject.player_stats["Hero"][log]] += 1
        else:
            timeplayed_hero_dict[playerObject.player_stats["Hero"][log]] = 1

    return timeplayed_hero_dict


def CreateNewPlayerDataObjectFromMatchCollection(playerName, matchCollection):
    collection_player_objects = []
    for match in matchCollection:
        for player in match.players:
            if player.player_stats["Player Name"] == playerName:
                collection_player_objects.append(player)

    return_player = Player(playerName)

    for index, player in enumerate(collection_player_objects):
        return_player.player_stats["Hero"] += player.player_stats["Hero"]
        return_player.player_stats["Hero Damage Dealt"] += player.player_stats["Hero Damage Dealt"]
        return_player.player_stats["Barrier Damage Dealt"] += player.player_stats["Barrier Damage Dealt"]
        return_player.player_stats["Damage Mitigated"] += player.player_stats["Damage Mitigated"]
        return_player.player_stats["Damage Taken"] += player.player_stats["Damage Taken"]
        return_player.player_stats["Deaths"] += player.player_stats["Deaths"]
        return_player.player_stats["Eliminations"] += player.player_stats["Eliminations"]
        return_player.player_stats["Final Blows"] += player.player_stats["Final Blows"]
        return_player.player_stats["Environmental Deaths"] += player.player_stats["Environmental Deaths"]
        return_player.player_stats["Environmental Kills"] += player.player_stats["Environmental Kills"]
        return_player.player_stats["Healing Dealt"] += player.player_stats["Healing Dealt"]
        return_player.player_stats["Objective Kills"] += player.player_stats["Objective Kills"]
        return_player.player_stats["Solo Kills"] += player.player_stats["Solo Kills"]
        return_player.player_stats["Ultimates Earned"] += player.player_stats["Ultimates Earned"]
        return_player.player_stats["Ultimates Used"] += player.player_stats["Ultimates Used"]
        return_player.player_stats["Healing Received"] += player.player_stats["Healing Received"]
        return_player.player_stats["Ultimate Charge Percentage"] += player.player_stats["Ultimate Charge Percentage"]
        return_player.player_stats["Ability 1 Cooldown"] += player.player_stats["Ability 1 Cooldown"]
        return_player.player_stats["Ability 2 Cooldown"] += player.player_stats["Ability 2 Cooldown"]
        return_player.player_stats["Total Health"] += player.player_stats["Total Health"]
        return_player.player_stats["Logs Count"] += player.player_stats["Logs Count"]

    return return_player


def FindTop3(parsedHeroPlaytimeData):
    top3list = sorted(parsedHeroPlaytimeData, key=parsedHeroPlaytimeData.get, reverse=True)[:3]
    return top3list


match1 = Match("Log-2023-04-11-14-50-34.txt")

#some_data_collection = [match1, match2]

#morning_combined_player_object = CreateNewPlayerDataObjectFromMatchCollection("morning", some_data_collection)
#coronet_combined_player_object = CreateNewPlayerDataObjectFromMatchCollection("Coronet", some_data_collection)

# morning
#t1p1_heroes = ParseHeroPlaytimeData(morning_combined_player_object)

# Coronet
# t2p1_heroes = ParseHeroPlaytimeData(match3.team2player1)
# Above it automatically parses the data for THAT MATCH (match 3), since each match has its own of this player object and match3.player is a unique playerObject which is passed in
#t2p1_heroes = ParseHeroPlaytimeData(coronet_combined_player_object)

# CreatePlayerIconGUI(60, 60, 0, 0, True, 0, match3.team1player1.player_stats["Player Name"], t1p1_heroes, True, "Silhouette")
# CreatePlayerIconGUI(60, 60, 0, 0, False, 0, match1.team2player1.player_stats["Player Name"], t2p1_heroes, True, "Silhouette")

drop_down_frame = customtkinter.CTkFrame(master=topframe, bg_color="#4D6394", fg_color="#4D6394", height=30, width=900)
drop_down_frame.place(x=0,y=0)

selectable_stat = customtkinter.StringVar(frame)
selectable_stat.set("Player Name")
drop_down_options = ["Player Name", "Hero Damage Dealt"]
drop_down_1 = customtkinter.CTkOptionMenu(master=topframe, variable=selectable_stat, values=drop_down_options, width=160)
drop_down_1.place(x=385,y=58)

selectable_logs = customtkinter.StringVar(frame)
log_options = os.listdir('Logs/')
selectable_logs.set(log_options[0])
log_drop_down = customtkinter.CTkOptionMenu(master=topframe, variable=selectable_logs, values=log_options, width=160)
log_drop_down.place(x=0,y=58)


def DoStuff():
    CreateMatchGUI(60, 60, 0, 0, Match(selectable_logs.get()), True, "Silhouette", displayed_stats, True, True)


displayed_stats = ["Player Name", "Hero Damage Dealt", "Healing Dealt"]
submit_log_button = customtkinter.CTkButton(master=topframe, command=DoStuff, text="Submit")
submit_log_button.place(x=220, y=58)


def CreateGraph(player, stat_key, team_1_aligned):
    graph_frame = customtkinter.CTkFrame(master=frame, bg_color="#C9C9C9", fg_color="#C9C9C9",width=600)

    if team_1_aligned:
        graph_frame.place(x=140, y=-140)
    else:
        graph_frame.place(x=840, y=-140)

    x = np.arange(0,player.player_stats["Logs Count"],1)
    y = player.player_stats[stat_key]

    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.355, right=1.2)
    plt.plot(x, y)
    # plt.ylim(0, 90)
    # _min = min(y)
    _max = 0

    for data_point in range(player.player_stats["Logs Count"]):
        float_var = float(player.player_stats[stat_key][data_point])
        int_var = int(float_var)
        if int_var > _max:
            _max = math.floor(int_var)

    # plt.locator_params(axis='y', nbins=4)
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))
    # plt.ylim(ymax=10)
    # plt.yticks(np.linspace(0, _max, 10))
    plt.fill_between(x,y)
    


    canvas = FigureCanvasTkAgg(figure=fig, master=graph_frame)
    canvas.get_tk_widget().pack()






# CreateGraph(match4.team1player1, "Hero Damage Dealt", True)
# CreateGraph(match4.team2player1, "Hero Damage Dealt", False)

# displayed_stats = ["Player Name", "Hero Damage Dealt", "Healing Dealt"]



# CreateMatchGUI(60, 60, 0, 0, Match("Log-2023-04-11-14-50-34.txt"), True, "Silhouette", displayed_stats, True, True)

root.mainloop()





# t1p2_heroes = {"Reinhardt":90}
# CreatePlayerNameAndIconGUI(60, 60, 0, 0, True, 1, "Bob", t1p2_heroes, True)

# CreatePlayerNameAndIconGUI(60, 60, 0, 0, False, 1, "Stewart", "Zarya", 1)


