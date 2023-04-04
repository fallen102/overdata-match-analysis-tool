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

frame = customtkinter.CTkFrame(master=root, bg_color="#ffffff", fg_color="#ffffff")
frame.pack(side="right", pady=50, padx=60, fill="both", expand=True)

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

match_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="MATCH SUMMARY", command=MatchPage, width=140,font=customtkinter.CTkFont(family="BankSansEFCY-RegCon", size=14))
match_button.place(y=10)

data_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="PLAYER COMPARISON", command=DataPage, width=140,font=customtkinter.CTkFont(family="BankSansEFCY-RegCon", size=14))
data_button.place(y=45)

data_button = customtkinter.CTkButton(master=left_sidebar_frame, text_color='#ffffff', text="DATA BANK", command=DataPage, width=140, font=customtkinter.CTkFont(family="BankSansEFCY-RegCon", size=14))
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
                            "Number Of Living Players Team 1": list(), "Number Of Living Players Team 2": list(),
                            "Array Of Living Players Team 1": list(), "Array Of Living Players Team 2": list(),
                            "Array Of Dead Players Team 1": list(), "Array Of Dead Players Team 2": list(),
                            "Team Score Team 1": list(), "Team Score Team 2": list(), "Gamemode": "",
                            "Time Elapsed": list(), "Control Mode Score Percentage Team 1": list(),
                            "Control Mode Score Percentage Team 2": list(), "Is Control Point Locked?": list(),
                            "Control Mode Scoring Team": list(), "Number Of Players On Control Point": list(),
                            "Is Team 1 Attacking?": list(),
                            "Payload Progress Percentage": list(), "Objective Index": list(),
                            "Point Capture Percentage": list(), "Push Bot X Position": list(),
                            "Push Bot Y Position": list(), "Push Bot Z Position": list(),
                            "Push Percentage": list(), "Match Time Elapsed": list()}
        # ^ Push Percentage is yet to be implemented

        # Determining the map for a given file passed in
        self.modified = []
        self.file = open("Logs/" + file, "r")
        self.read = self.file.readlines()

        for line in self.read:
            if line[-1] == '\n':
                self.modified.append(line[11:])
            self.match_stats["Map"] = self.modified[0]
            for index, char in enumerate(self.match_stats["Map"]):
                if char == ",":
                    len_of_mapline = len(self.match_stats["Map"])
                    index_of_end_map = index
                    self.match_stats["Map"] = self.match_stats["Map"][:-(len_of_mapline - index)]
                    break

        # Determing gamemode info from gamemode logs (one of the two non-player logs)
        for index, line in enumerate(self.read):
            split = line.split(",")
            if line.__contains__("INFORMATION LOG"):
                # Logic for information log
                self.match_stats["Match Round"].append(split[0].split(" ")[1])
                self.match_stats["Number Of Living Players Team 1"].append(split[1])
                self.match_stats["Number Of Living Players Team 2"].append(split[2])
                self.match_stats["Array Of Living Players Team 1"].append(split[3])
                self.match_stats["Array Of Living Players Team 2"].append(split[4])
                self.match_stats["Array Of Dead Players Team 1"].append(split[5])
                self.match_stats["Array Of Dead Players Team 2"].append(split[6])
                self.match_stats["Team Score Team 1"].append(split[7])
                self.match_stats["Team Score Team 2"].append(split[8])
            elif not line.__contains__("PLAYER LOG") and index > 1:
                # Logic for game mode log
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
        players_line_split = self.read[1].split(",")
        self.team1player1 = Player(players_line_split[0].split(" ")[1])
        self.team1player2 = Player(players_line_split[1])
        self.team1player3 = Player(players_line_split[2])
        self.team1player4 = Player(players_line_split[3])
        self.team1player5 = Player(players_line_split[4])

        self.team2player1 = Player(players_line_split[6])
        self.team2player2 = Player(players_line_split[7])
        self.team2player3 = Player(players_line_split[8])
        self.team2player4 = Player(players_line_split[9])
        self.team2player5 = Player(players_line_split[10])

        self.players = [self.team1player1, self.team1player2, self.team1player3, self.team1player4, self.team1player5,
                        self.team2player1, self.team2player2, self.team2player3, self.team2player4, self.team2player5]

        # Determining which lines need to be logged and the relevant player object to log them under
        for index, line in enumerate(self.read):
            if line.__contains__("PLAYER LOG"):
                split_player_var_log = line.split(",")
                for player in self.players:
                    if split_player_var_log[1] == player.player_stats["Player Name"]:
                        player.AddLog(line)


class Player:

    def __init__(self, playername):
        self.player_stats = {"Match Time Elapsed": list(), "Hero": list(), "Hero Damage Dealt": list(),
                             "Barrier Damage Dealt": list(), "Damage Mitigated": list(), "Damage Taken": list(),
                             "Deaths": list(), "Eliminations": list(),
                             "Final Blows": list(), "Environmental Deaths": list(), "Environmental Kills": list(),
                             "Healing Dealt": list(), "Objective Kills": list(), "Solo Kills": list(),
                             "Ultimates Earned": list(), "Ultimates Used": list(),
                             "Healing Received": list(), "Ultimate Charge Percentage": list(),
                             "Player Closest To Reticle": list(), "X Position": list(), "Y Position": list(),
                             "Z Position": list(), "Team": list(), "Ability 1 Cooldown": list(),
                             "Ability 2 Cooldown": list(), "Total Health": list(), "Max Health": list(),
                             "Active Health": list(), "Active Armour": list(), "Active Shields": list(),
                             "Logs Count": 0,
                             "Player Name": playername}

    def AddLog(self, line):

        self.player_stats["Logs Count"] += 1
        split_player_log = line.split(",")

        self.player_stats["Match Time Elapsed"].append(split_player_log[0].split(" ")[1])

        if split_player_log[2] == "LÃºcio" or split_player_log[2] == "Lúcio" or split_player_log[2] == "Lucio":
            self.player_stats["Hero"].append("Lucio")
        elif split_player_log[2] == "Soldier:76":
            self.player_stats["Hero"].append("Soldier 76")
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
        self.player_stats["Healing Received"].append(split_player_log[17])
        self.player_stats["Ultimate Charge Percentage"].append(split_player_log[18])
        self.player_stats["Player Closest To Reticle"].append(split_player_log[19])
        self.player_stats["X Position"].append(split_player_log[20][1:])
        self.player_stats["Y Position"].append(split_player_log[21])
        self.player_stats["Z Position"].append(split_player_log[22][:-1])
        self.player_stats["Team"].append(split_player_log[23])
        self.player_stats["Ability 1 Cooldown"].append(split_player_log[24])
        self.player_stats["Ability 2 Cooldown"].append(split_player_log[25])
        self.player_stats["Total Health"].append(split_player_log[26])
        self.player_stats["Max Health"].append(split_player_log[27])
        self.player_stats["Active Health"].append(split_player_log[28])
        self.player_stats["Active Armour"].append(split_player_log[29])
        self.player_stats["Active Shields"].append(split_player_log[30])


def CreatePlayerIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName, heroes, displayPlaytimeBar, icon_type):
    top3 = FindTop3(heroes)
    index = 0
    playtimeBarPadding = 1
    if displayPlaytimeBar:
        playtimeBarPadding = 1.2

    for hero in top3:
        icon = customtkinter.CTkLabel(master=frame, image=FetchHeroIcon(hero, 0, 0, 0, 0, icon_type, sizex=icon_size_x,
                                                                        sizey=icon_size_y), text="")
        if left_align:
            icon_x_pos = 0 + starting_x + (index * icon_size_x)
            icon_y_pos = 0 + starting_y + (vertical_slot * icon_size_y * playtimeBarPadding)
            icon.place(x=icon_x_pos, y=icon_y_pos)
        else:
            icon_x_pos = 1660 - icon_size_x - (index * icon_size_x) + starting_x
            icon_y_pos = 0 + starting_y + (vertical_slot * icon_size_y * playtimeBarPadding)
            icon.place(x=icon_x_pos, y=icon_y_pos)

        if displayPlaytimeBar:
            proportion_of_hero_played = ProportionOfHeroPlayed(heroes, hero)
            round_proportion = round(proportion_of_hero_played * icon_size_x)
            if round_proportion < 1:
                round_proportion = 1
            playtimeBar = customtkinter.CTkLabel(master=frame, text="",
                                                 image=FetchHeroColour(hero, round_proportion, 10), height=10,
                                                 width=round_proportion)
            playtimeBar.place(x=icon_x_pos, y=icon_y_pos + icon_size_y)
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
        return_player.player_stats["Player Closest To Reticle"] += player.player_stats["Player Closest To Reticle"]
        return_player.player_stats["X Position"] += player.player_stats["X Position"]
        return_player.player_stats["Y Position"] += player.player_stats["Y Position"]
        return_player.player_stats["Z Position"] += player.player_stats["Z Position"]
        return_player.player_stats["Team"] += player.player_stats["Team"]
        return_player.player_stats["Ability 1 Cooldown"] += player.player_stats["Ability 1 Cooldown"]
        return_player.player_stats["Ability 2 Cooldown"] += player.player_stats["Ability 2 Cooldown"]
        return_player.player_stats["Total Health"] += player.player_stats["Total Health"]
        return_player.player_stats["Max Health"] += player.player_stats["Max Health"]
        return_player.player_stats["Active Health"] += player.player_stats["Active Health"]
        return_player.player_stats["Active Armour"] += player.player_stats["Active Armour"]
        return_player.player_stats["Active Shields"] += player.player_stats["Active Shields"]
        return_player.player_stats["Logs Count"] += player.player_stats["Logs Count"]

    return return_player


def FindTop3(parsedHeroPlaytimeData):
    top3list = sorted(parsedHeroPlaytimeData, key=parsedHeroPlaytimeData.get, reverse=True)[:3]
    return top3list


match1 = Match("Log-2023-04-02-17-27-33.txt")
match2 = Match("Log-2023-04-02-16-02-30.txt")
match3 = Match("Log-2023-04-03-15-25-56.txt")

some_data_collection = [match1, match2]

morning_combined_player_object = CreateNewPlayerDataObjectFromMatchCollection("morning", some_data_collection)
coronet_combined_player_object = CreateNewPlayerDataObjectFromMatchCollection("Coronet", some_data_collection)

# morning
t1p1_heroes = ParseHeroPlaytimeData(morning_combined_player_object)

# Coronet
# t2p1_heroes = ParseHeroPlaytimeData(match3.team2player1)
# Above it automatically parses the data for THAT MATCH (match 3), since each match has its own of this player object and match3.player is a unique playerObject which is passed in
t2p1_heroes = ParseHeroPlaytimeData(coronet_combined_player_object)

CreatePlayerIconGUI(60, 60, 0, 0, True, 0, match3.team1player1.player_stats["Player Name"], t1p1_heroes, True, "Silhouette")
CreatePlayerIconGUI(60, 60, 0, 0, False, 0, match1.team2player1.player_stats["Player Name"], t2p1_heroes, True, "Silhouette")

# t1p2_heroes = {"Reinhardt":90}
# CreatePlayerNameAndIconGUI(60, 60, 0, 0, True, 1, "Bob", t1p2_heroes, True)

# CreatePlayerNameAndIconGUI(60, 60, 0, 0, False, 1, "Stewart", "Zarya", 1)

root.mainloop()
