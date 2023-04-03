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
            if line.__contains__("INFORMATION LOG"):
                # Logic for information log
                self.match_round.append(line.split(",")[0].split(" ")[1])
                self.num_living_players_t1.append(line.split(",")[1])
                self.num_living_players_t2.append(line.split(",")[2])
                self.array_living_players_t1.append(line.split(",")[3])
                self.array_living_players_t2.append(line.split(",")[4])
                self.array_dead_players_t1.append(line.split(",")[5])
                self.array_dead_players_t2.append(line.split(",")[6])
                self.team_score_t1.append(line.split(",")[7])
                self.team_score_t2.append(line.split(",")[8])
            elif not line.__contains__("PLAYER LOG") and index > 1:
                # Logic for game mode log
                self.game_mode = line.split(",")[0].split(" ")[1]
                self.time_elapsed.append(line.split(",")[1])
                if self.game_mode == "Control":
                    self.control_mode_score_percent_t1.append(line.split(",")[2])
                    self.control_mode_score_percent_t2.append(line.split(",")[3])
                    self.is_control_point_locked.append(line.split(",")[4])
                    self.control_mode_scoring_team.append(line.split(",")[5])
                    self.num_players_on_control_point.append(line.split(",")[6])
                elif self.game_mode == "Escort":
                    self.is_team_1_attacking.append(line.split(",")[2])
                    self.payload_progress_percent.append(line.split(",")[3])
                    self.objective_index.append(line.split(",")[4])
                elif self.game_mode == "Assault":
                    self.is_team_1_attacking.append(line.split(",")[2])
                    self.point_capture_percent.append(line.split(",")[3])
                    self.objective_index.append(line.split(",")[4])
                elif self.game_mode == "Hybrid":
                    self.is_team_1_attacking.append(line.split(",")[2])
                    self.point_capture_percent.append(line.split(",")[3])
                    self.payload_progress_percent.append(line.split(",")[4])
                    self.objective_index.append(line.split(",")[5])
                elif self.game_mode == "Push":
                    self.push_payload_pos_x.append(line.split(",")[2][1:-1])
                    self.push_payload_pos_y.append(line.split(",")[3][1:])
                    self.push_payload_pos_z.append(line.split(",")[4][1:-3])

        # Creating each player object for the match based on username from the second log line
        self.team1player1 = Player(self.read[1].split(",")[0].split(" ")[1], self.players)
        self.team1player2 = Player(self.read[1].split(",")[1], self.players)
        self.team1player3 = Player(self.read[1].split(",")[2], self.players)
        self.team1player4 = Player(self.read[1].split(",")[3], self.players)
        self.team1player5 = Player(self.read[1].split(",")[4], self.players)

        self.team2player1 = Player(self.read[1].split(",")[6], self.players)
        self.team2player2 = Player(self.read[1].split(",")[7], self.players)
        self.team2player3 = Player(self.read[1].split(",")[8], self.players)
        self.team2player4 = Player(self.read[1].split(",")[9], self.players)
        self.team2player5 = Player(self.read[1].split(",")[10], self.players)

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


def CreatePlayerNameAndIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName,heroName, weighting=None,hero2Name=None, weighting2=None, hero3Name=None, weighting3=None):
    # If there is only one hero played
    if hero2Name is None:

        icon = customtkinter.CTkLabel(master=frame,
                                      image=FetchHeroIcon(heroName, 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
                                      text="")
        if left_align:
            icon.place(x=0 + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))
        else:
            icon.place(x=1660 - icon_size_x + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))

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

        icon2 = customtkinter.CTkLabel(master=frame,
                                      image=FetchHeroIcon("EMPTY", 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
                                      text="")
        if left_align:
            icon2.place(x=0 + starting_x + icon_size_x, y=0 + starting_y + (vertical_slot * icon_size_y))
        else:
            icon2.place(x=1660 - (icon_size_x*2) + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))

        icon3 = customtkinter.CTkLabel(master=frame,
                                       image=FetchHeroIcon("EMPTY", 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
                                       text="")
        if left_align:
            icon3.place(x=0 + starting_x + (2* icon_size_x), y=0 + starting_y + (vertical_slot * icon_size_y))
        else:
            icon3.place(x=1660 - (icon_size_x * 3) + starting_x, y=0 + starting_y + (vertical_slot * icon_size_y))

    # i.e. if there are exactly two heroes played
    elif hero2Name is not None and hero3Name is None:
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
                                       image=FetchHeroIcon("EMPTY", 0, 0, 0, 0, sizex=icon_size_x, sizey=icon_size_y),
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
    # i.e. if all three 'most played hero' slots are populated
    elif hero3Name is not None:
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


def TryCreatePlayerNameAndIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName, item_0, item_1, item_2, item_3, item_4, item_5):
    try:
        CreatePlayerNameAndIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName, item_0, item_1, item_2, item_3, item_4, item_5)
    except:
        try:
            CreatePlayerNameAndIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName, item_0, item_1, item_2, item_3)
        except:
            CreatePlayerNameAndIconGUI(icon_size_x, icon_size_y, starting_x, starting_y, left_align, vertical_slot, playerName, item_0, item_1)


def Top3HeroesPlayedProportionallyMatch(playerName, match):
    ana = 0
    ashe = 0
    baptiste = 0
    bastion = 0
    brigitte = 0
    cassidy = 0
    doomfist = 0
    dva = 0
    echo = 0
    genji = 0
    hanzo = 0
    junkerqueen = 0
    junkrat = 0
    kiriko = 0
    lucio = 0
    mei = 0
    mercy = 0
    moira = 0
    orisa = 0
    pharah = 0
    ramattra = 0
    reaper = 0
    reinhardt = 0
    roadhog = 0
    sigma = 0
    sojourn = 0
    soldier76 = 0
    sombra = 0
    symmetra = 0
    torbjorn = 0
    tracer = 0
    widowmaker = 0
    winston = 0
    wreckingball = 0
    zarya = 0
    zenyatta = 0

    for player in match.players:
        if player.playername == playerName:
            for log in range(player.logs_count - 1):
                # You need to ensure the log file deals with spacing the same way as the strings in the below match/case statement, i.e. Junkerqueen or Junker Queen or Junker queen
                match player.hero[log]:
                    case "Ana":
                        ana += 1
                        continue
                    case "Ashe":
                        ashe += 1
                        continue
                    case "Baptiste":
                        baptiste += 1
                        continue
                    case "Bastion":
                        bastion += 1
                        continue
                    case "Brigitte":
                        brigitte += 1
                        continue
                    case "D.Va":
                        dva += 1
                        continue
                    case "Doomfist":
                        doomfist += 1
                        continue
                    case "Echo":
                        echo += 1
                        continue
                    case "Genji":
                        genji += 1
                        continue
                    case "Hanzo":
                        hanzo += 1
                        continue
                    case "Junkrat":
                        junkrat += 1
                        continue
                    case "Lucio":
                        lucio += 1
                        continue
                    case "Cassidy":
                        cassidy += 1
                        continue
                    case "Mei":
                        mei += 1
                        continue
                    case "Mercy":
                        mercy += 1
                        continue
                    case "Moira":
                        moira += 1
                        continue
                    case "Orisa":
                        orisa += 1
                        continue
                    case "Pharah":
                        pharah += 1
                        continue
                    case "Reaper":
                        reaper += 1
                        continue
                    case "Reinhardt":
                        reinhardt += 1
                        continue
                    case "Roadhog":
                        roadhog += 1
                        continue
                    case "Sigma":
                        sigma += 1
                        continue
                    case "Soldier: 76":
                        soldier76 += 1
                        continue
                    case "Sombra":
                        sombra += 1
                        continue
                    case "Symmetra":
                        symmetra += 1
                        continue
                    case "Torbjorn":
                        torbjorn += 1
                        continue
                    case "Tracer":
                        tracer += 1
                        continue
                    case "Widowmaker":
                        widowmaker += 1
                        continue
                    case "Winston":
                        winston += 1
                        continue
                    case "Wrecking Ball":
                        wreckingball += 1
                        continue
                    case "Zarya":
                        zarya += 1
                        continue
                    case "Zenyatta":
                        zenyatta += 1
                        continue
                    case "Junkerqueen":
                        junkerqueen += 1
                        continue
                    case "Sojourn":
                        sojourn += 1
                        continue
                    case "Kiriko":
                        kiriko += 1
                        continue
                    case "Ramattra":
                        ramattra += 1
                        continue
            heroes = [ana, ashe, baptiste, bastion, brigitte, dva, doomfist, echo, genji, hanzo, junkrat, lucio,
                      cassidy,
                      mei, mercy, moira, orisa, pharah, reaper, reinhardt, roadhog, sigma, soldier76, sombra, symmetra,
                      torbjorn, tracer, widowmaker, winston, wreckingball, zarya, zenyatta, ramattra, sojourn, kiriko,
                      junkerqueen]
            heroes_string = ["Ana", "Ashe", "Baptiste", "Bastion", "Brigitte", "D.Va", "Doomfist", "Echo", "Genji",
                             "Hanzo",
                             "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Moira", "Orisa", "Pharah", "Reaper",
                             "Reinhardt",
                             "Roadhog", "Sigma", "Soldier76", "Sombra", "Symmetra", "Torbjorn", "Tracer", "Widowmaker",
                             "Winston", "Wrecking Ball", "Zarya", "Zenyatta", "Ramattra", "Sojourn", "Kiriko",
                             "Junkerqueen"]

            highest_h_count = 0
            second_highest_h_count = 0
            third_highest_h_count = 0
            most_played = ""
            second_most_played = ""
            third_most_played = ""
            for index, hero in enumerate(heroes):
                # If a new "most played hero" is identified
                if hero > highest_h_count:
                    # If #1 does not exist
                    if most_played == "":
                        highest_h_count = hero
                        most_played = heroes_string[index]
                        proportion_of_first = math.floor(1000 * hero / player.logs_count) / 1000
                    else:
                        if second_most_played == "":
                            # If #1 already exists but #2 does not
                            second_highest_h_count = highest_h_count
                            second_most_played = most_played
                            proportion_of_second = proportion_of_first
                            highest_h_count = hero
                            most_played = heroes_string[index]
                            proportion_of_first = math.floor(1000 * hero / player.logs_count) / 1000
                        else:
                            # If #1 and #2 both already exist
                            third_most_played = second_most_played
                            third_highest_h_count = second_highest_h_count
                            proportion_of_third = proportion_of_second
                            second_most_played = most_played
                            second_highest_h_count = highest_h_count
                            proportion_of_second = proportion_of_first
                            highest_h_count = hero
                            most_played = heroes_string[index]
                            proportion_of_first = math.floor(1000 * hero / player.logs_count) / 1000
                    del heroes[index]
                    del heroes_string[index]
            for index, hero in enumerate(heroes):
                # If a new "second most played hero" is identified
                if hero > second_highest_h_count:
                    if second_most_played == "":
                        # If #2 does not exist yet
                        second_highest_h_count = hero
                        second_most_played = heroes_string[index]
                        proportion_of_second = math.floor(1000 * hero / player.logs_count) / 1000
                    else:
                        # If #2 already exists
                        third_most_played = second_most_played
                        third_highest_h_count = second_highest_h_count
                        proportion_of_third = proportion_of_second
                        second_most_played = heroes_string[index]
                        second_highest_h_count = hero
                        proportion_of_second = math.floor(1000 * hero / player.logs_count) / 1000
                    del heroes[index]
                    del heroes_string[index]
            for index, hero in enumerate(heroes):
                if hero > third_highest_h_count:
                    third_highest_h_count = hero
                    third_most_played = heroes_string[index]
                    proportion_of_third = math.floor(1000 * hero / player.logs_count) / 1000

    try:
        returnlist = [most_played, proportion_of_first, second_most_played, proportion_of_second, third_most_played,
                      proportion_of_third]
        return returnlist
    except:
        print("Only one/two heroes played")
    try:
        returnlist = [most_played, proportion_of_first, second_most_played, proportion_of_second, "", ""]
        return returnlist
    except:
        print("Only one hero played")

    returnlist = [most_played, proportion_of_first, "", "", "", ""]
    return returnlist


def Top3HeroesPlayedProportionallyMatchCollection(playerName, matchCollection):
    ana = 0
    ashe = 0
    baptiste = 0
    bastion = 0
    brigitte = 0
    cassidy = 0
    doomfist = 0
    dva = 0
    echo = 0
    genji = 0
    hanzo = 0
    junkerqueen = 0
    junkrat = 0
    kiriko = 0
    lucio = 0
    mei = 0
    mercy = 0
    moira = 0
    orisa = 0
    pharah = 0
    ramattra = 0
    reaper = 0
    reinhardt = 0
    roadhog = 0
    sigma = 0
    sojourn = 0
    soldier76 = 0
    sombra = 0
    symmetra = 0
    torbjorn = 0
    tracer = 0
    widowmaker = 0
    winston = 0
    wreckingball = 0
    zarya = 0
    zenyatta = 0
    for match in matchCollection:
        for player in match.players:
            if player.playername == playerName:
                for log in range(player.logs_count - 1):
                    # You need to ensure the log file deals with spacing the same way as the strings in the below match/case statement, i.e. Junkerqueen or Junker Queen or Junker queen
                    match player.hero[log]:
                        case "Ana":
                            ana += 1
                            continue
                        case "Ashe":
                            ashe += 1
                            continue
                        case "Baptiste":
                            baptiste += 1
                            continue
                        case "Bastion":
                            bastion += 1
                            continue
                        case "Brigitte":
                            brigitte += 1
                            continue
                        case "D.Va":
                            dva += 1
                            continue
                        case "Doomfist":
                            doomfist += 1
                            continue
                        case "Echo":
                            echo += 1
                            continue
                        case "Genji":
                            genji += 1
                            continue
                        case "Hanzo":
                            hanzo += 1
                            continue
                        case "Junkrat":
                            junkrat += 1
                            continue
                        case "Lucio":
                            lucio += 1
                            continue
                        case "Cassidy":
                            cassidy += 1
                            continue
                        case "Mei":
                            mei += 1
                            continue
                        case "Mercy":
                            mercy += 1
                            continue
                        case "Moira":
                            moira += 1
                            continue
                        case "Orisa":
                            orisa += 1
                            continue
                        case "Pharah":
                            pharah += 1
                            continue
                        case "Reaper":
                            reaper += 1
                            continue
                        case "Reinhardt":
                            reinhardt += 1
                            continue
                        case "Roadhog":
                            roadhog += 1
                            continue
                        case "Sigma":
                            sigma += 1
                            continue
                        case "Soldier: 76":
                            soldier76 += 1
                            continue
                        case "Sombra":
                            sombra += 1
                            continue
                        case "Symmetra":
                            symmetra += 1
                            continue
                        case "Torbjorn":
                            torbjorn += 1
                            continue
                        case "Tracer":
                            tracer += 1
                            continue
                        case "Widowmaker":
                            widowmaker += 1
                            continue
                        case "Winston":
                            winston += 1
                            continue
                        case "Wrecking Ball":
                            wreckingball += 1
                            continue
                        case "Zarya":
                            zarya += 1
                            continue
                        case "Zenyatta":
                            zenyatta += 1
                            continue
                        case "Junkerqueen":
                            junkerqueen += 1
                            continue
                        case "Sojourn":
                            sojourn += 1
                            continue
                        case "Kiriko":
                            kiriko += 1
                            continue
                        case "Ramattra":
                            ramattra += 1
                            continue
    heroes = [ana, ashe, baptiste, bastion, brigitte, dva, doomfist, echo, genji, hanzo, junkrat, lucio,
              cassidy,
              mei, mercy, moira, orisa, pharah, reaper, reinhardt, roadhog, sigma, soldier76, sombra,
              symmetra,
              torbjorn, tracer, widowmaker, winston, wreckingball, zarya, zenyatta, ramattra, sojourn,
              kiriko, junkerqueen]
    heroes_string = ["Ana", "Ashe", "Baptiste", "Bastion", "Brigitte", "D.Va", "Doomfist", "Echo", "Genji",
                     "Hanzo",
                     "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Moira", "Orisa", "Pharah", "Reaper",
                     "Reinhardt",
                     "Roadhog", "Sigma", "Soldier76", "Sombra", "Symmetra", "Torbjorn", "Tracer",
                     "Widowmaker",
                     "Winston", "Wrecking Ball", "Zarya", "Zenyatta", "Ramattra", "Sojourn", "Kiriko",
                     "Junkerqueen"]

    highest_h_count = 0
    second_highest_h_count = 0
    third_highest_h_count = 0

    total_logs = 0

    for match in matchCollection:
        for player in match.players:
            if player.playername == playerName:
                total_logs += player.logs_count

    for index, hero in enumerate(heroes):
        if hero > highest_h_count:
            highest_h_count = hero
            most_played = heroes_string[index]
            proportion_of_first = math.ceil(10 * hero / total_logs) / 10
            del heroes[index]
            del heroes_string[index]
    for index, hero in enumerate(heroes):
        if hero > second_highest_h_count:
            second_highest_h_count = hero
            second_most_played = heroes_string[index]
            proportion_of_second = math.ceil(10 * hero / total_logs) / 10
            del heroes[index]
            del heroes_string[index]
    for index, hero in enumerate(heroes):
        if hero > third_highest_h_count:
            third_highest_h_count = hero
            third_most_played = heroes_string[index]
            proportion_of_third = math.ceil(10 * hero / total_logs) / 10

    try:
        returnlist = [most_played, proportion_of_first, second_most_played, proportion_of_second, third_most_played,
                      proportion_of_third]
        return returnlist
    except:
        print("Only one/two heroes played")

    try:
        returnlist = [most_played, proportion_of_first, second_most_played, proportion_of_second, "", ""]
        return returnlist
    except:
        print("Only one hero played")

    returnlist = [most_played, proportion_of_first, "", "", "", ""]
    return returnlist


match1 = Match("Log-2023-04-02-17-27-33.txt")
match2 = Match("Log-2023-04-02-16-02-30.txt")
match3 = Match("Log-2023-04-03-15-25-56.txt")

some_data_collection = [match1, match2]

t1p1_hero = Top3HeroesPlayedProportionallyMatch("morning", match3)
t2p1_hero = Top3HeroesPlayedProportionallyMatch("Coronet", match3)

TryCreatePlayerNameAndIconGUI(60, 60, 0, 0, True, 0, match3.team1player1.playername, t1p1_hero[0], t1p1_hero[1], t1p1_hero[2], t1p1_hero[3], t1p1_hero[4], t1p1_hero[5])
TryCreatePlayerNameAndIconGUI(60, 60, 0, 0, False, 0, match1.team2player1.playername, t2p1_hero[0], t2p1_hero[1], t2p1_hero[2], t2p1_hero[3], t2p1_hero[4], t2p1_hero[5])

# CreatePlayerNameAndIconGUI(40, 40, 0, 0, True, 1, "Bob", "Reinhardt", 1)

# CreatePlayerNameAndIconGUI(110, 110, 0, 0, True, 1, "Stewart", "Zarya", 1)

# root.mainloop()

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
