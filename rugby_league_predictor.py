# -*- coding: utf-8 -*-

DEFAULT_LEAGUE_FILENAME = "SL_26"

import shelve
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
import numpy as np


########################| -V- DEFAULT SETTINGS -V-|############################

# https://www.bbc.co.uk/sport/rugby-league/

class Settings:
    def __init__(self): # loading default settings
        self.ROUND = 0
        self.ALPHABETICALLY_ORDER_TEAMS = True
        self.LEAGUE_FILENAME = DEFAULT_LEAGUE_FILENAME
        self.BYES = False # If a team is not present in a round's fixtures, behave as if they were given a bye.

        self.WINNING_POINTS = 2
        self.DRAWING_POINTS = 1

        self.LOSING_POINTS_AWARDED = False # Super XIII
        self.LOSING_POINTS_MAX_MARGIN = 12
        self.LOSING_POINTS = 1

        self.GENERAL_POINTS_DIVISOR = 2.4
        self.FORM_RUN_LENGTH = 5
        self.DEFAULT_FORM_SCORE = 2.5
        self.FORM_SCORE_DIVISOR = self.FORM_RUN_LENGTH # caps max form score for a prediction to 1 point
        self.RESULT_POINTS = 3
        self.DERBY_FACTOR_POINTS = 1
        self.MARGIN_LIMITS = np.array([2, 8, 12, 16, 22])
        self.MARGIN_POINTS = [1.5, 1, 0.5, 0.3, 0.2, 0.1]
        self.MARGIN_IGNORES_RESULT = False
        self.MIDPOINT_LIMITS = np.array([6, 8, 12, 18, 26])
        self.MIDPOINT_POINTS = np.array([1, 0.8, 0.6, 0.4, 0.2, 0.1])
        self.team_id_table = ["saints", "fc", "wakey", "hudd", "cas", "leigh", "bradford", "kr", "catalans", "leeds", "wire", "wigan", "york", "toulouse"]
        self.team_desc_table = ["St Helens", "Hull FC", "Wakefield Trinity", "Huddersfield Giants",\
                           "Castleford Tigers", "Leigh Leopards", "Bradford Bulls", "Hull KR",\
                               "Catalans Dragons", "Leeds Rhinos", "Warrington Wolves", "Wigan Warriors",\
                                   "York Knights", "Toulouse Olympique"]
        self.derby_factor_pairs = [["saints", "wigan"], ["fc", "kr"], ["bradford", "leeds"], ["toulouse", "catalans"], ["wakey", "cas"]]
        self.players = ["player1", "player2", "player3", "player4"]
    def create_settings_dict(self):
        # create default settings
        self.settings_dict = {
        "ALPHABETICALLY_ORDER_TEAMS" : self.ALPHABETICALLY_ORDER_TEAMS,
        "LEAGUE_FILENAME" : self.LEAGUE_FILENAME,
        "BYES" : self.BYES,
        "WINNING_POINTS" : self.WINNING_POINTS,
        "DRAWING_POINTS" : self.DRAWING_POINTS,
        "LOSING_POINTS_AWARDED" : self.LOSING_POINTS_AWARDED,
        "LOSING_POINTS_MAX_MARGIN" : self.LOSING_POINTS_MAX_MARGIN,
        "LOSING_POINTS" : self.LOSING_POINTS,
        "GENERAL_POINTS_DIVISOR" : self.GENERAL_POINTS_DIVISOR,
        "FORM_RUN_LENGTH" : self.FORM_RUN_LENGTH,
        "DEFAULT_FORM_SCORE" : self.DEFAULT_FORM_SCORE,
        "FORM_SCORE_DIVISOR" : self.FORM_SCORE_DIVISOR,
        "RESULT_POINTS" : self.RESULT_POINTS,
        "DERBY_FACTOR_POINTS" : self.DERBY_FACTOR_POINTS,
        "MARGIN_LIMITS" : self.MARGIN_LIMITS,
        "MARGIN_POINTS" : self.MARGIN_POINTS,
        "MARGIN_IGNORES_RESULT" : self.MARGIN_IGNORES_RESULT,
        "MIDPOINT_LIMITS" : self.MIDPOINT_LIMITS,
        "MIDPOINT_POINTS" : self.MIDPOINT_POINTS,
        "team_id_table" : self.team_id_table,
        "team_desc_table" : self.team_desc_table,
        "derby_factor_pairs" : self.derby_factor_pairs,
        "players" : self.players,
        "NUMBER_OF_PLAYERS" : len(self.players),
        "NUMBER_OF_TEAMS" : len(self.team_id_table),
        "NUMBER_OF_ROUNDS" : 50,
        "MAX_NUMBER_OF_MATCHES_PER_ROUND" : ((len(self.team_id_table)) // 2)
        }
        for key, value in zip(self.settings_dict.keys(), self.settings_dict.values()):
            eval_value = str(value)
            exec(f"{key} = eval_value")
        return self.settings_dict
    def update_secondary_settings(self): # for settings whose value depends on another setting
        self.settings_dict["NUMBER_OF_PLAYERS"] = len(self.settings_dict["players"])
        self.settings_dict["NUMBER_OF_TEAMS"] = len(self.settings_dict["team_id_table"])
        self.settings_dict["MAX_NUMBER_OF_MATCHES_PER_ROUND"] = len(self.settings_dict["team_id_table"]) // 2
        return
    def update_settings(self, update_dict):
        for key, value in zip(update_dict.keys(), update_dict.values()):
            self.settings_dict[key] = value
        """global ALPHABETICALLY_ORDER_TEAMS
        global LEAGUE_FILENAME
        global BYES
        global WINNING_POINTS
        global DRAWING_POINTS
        global LOSING_POINTS
        global LOSING_POINTS_AWARDED
        global LOSING_POINTS_MAX_MARGIN
        global GENERAL_POINTS_DIVISOR
        global FORM_RUN_LENGTH
        global DEFAULT_FORM_SCORE
        global FORM_SCORE_DIVISOR
        global RESULT_POINTS
        global DERBY_FACTOR_POINTS
        global MARGIN_LIMITS
        global MARGIN_POINTS
        global MARGIN_IGNORES_RESULT
        global MIDPOINT_LIMITS
        global MIDPOINT_POINTS
        global team_id_table
        global team_desc_table
        global derby_factor_pairs
        global players"""
        for key, value in zip(self.settings_dict.keys(), self.settings_dict.values()):
            eval_value = str(value)
            exec(f"{key} = eval_value")
        self.update_secondary_settings()
        return self.settings_dict
    def save_settings(self, silent=False):
        try:
            shelve_file = shelve.open(settings["LEAGUE_FILENAME"])
            shelve_file["settings"] = self.settings_dict
            shelve_file.close()
            if not silent:
                do_message("League setting(s) saved successfully")
        except:
            do_error_message("Failed to save league settings")
        return
def load_settings(filename=DEFAULT_LEAGUE_FILENAME):
    global settings_instance
    global settings
    print("League filename: " + filename)
    try:
        league_file = shelve.open(filename)
        imported_settings = league_file["settings"]
        settings_instance = Settings()
        settings = settings_instance.create_settings_dict()
        settings = settings_instance.update_settings(imported_settings)
        print(f"Successfully loaded settings (filename: {filename} | {settings['LEAGUE_FILENAME']})")
        league_file.close()
        try:
            settings["ROUND"]
        except KeyError:
            settings["ROUND"] = 1
    except OSError:
        print("Creating default settings")
        settings_instance = Settings()
        settings = settings_instance.create_settings_dict()
    
load_settings()

ROUND = 0

########################| -^- SETTINGS -^-|####################################

###############################################################################


if settings["ALPHABETICALLY_ORDER_TEAMS"]:
    settings["team_id_table"] = np.array(settings["team_id_table"])
    settings["team_desc_table"] = np.array(settings["team_desc_table"])
    sort_guide = np.argsort(settings["team_desc_table"])
    settings["team_desc_table"] = settings["team_desc_table"][sort_guide]
    settings["team_id_table"] = settings["team_id_table"][sort_guide]
    settings["team_id_table"] = (settings["team_id_table"]).tolist()
    settings["team_desc_table"] = (settings["team_desc_table"]).tolist()    

settings["derby_factor_table"] = np.zeros((len(settings["team_id_table"]), len(settings["team_id_table"])))
for a, b in settings["derby_factor_pairs"]:
    row = settings["team_id_table"].index(a)
    column = settings["team_id_table"].index(b)
    settings["derby_factor_table"][row][column] = 1
    settings["derby_factor_table"][column][row] = 1

m = Tk()
lb1 = Listbox(m, width = 75, height = 20)
#####################  ------  INTERNAL FUNCTIONS  ------  ####################
def do_nothing():
    return
def try_open_data(_type, filename):
    print(f"Opening '{_type}' in '{filename}'")
    invalid_data = False
    no_data = False
    try:
        shelve_file = shelve.open(filename)
        data = shelve_file[_type]
        invalid_data = False
        shelve_file.close()
    except KeyError: # File exists but key doesn't
        no_data = True
        shelve_file.close()
        return 2
    except: # Unknown
        invalid_data = True
        shelve_file.close()
        return 3
    if data.any() != 0: 
        no_data = False
        shelve_file.close()
        return data
    no_data = True # Else: file exists and key exists but is blank
    shelve_file.close()
    return 1
def do_error_message(message):
    win = Toplevel()
    win.wm_title("Error")
    errormsg = Label(win, text=message)
    errormsg.grid(row=0, column=0)
    ok_button = ttk.Button(win, text="OK", command=win.destroy)
    ok_button.grid(row=1, column=0)
def do_message(message):
    win = Toplevel()
    win.wm_title("RL Predictor")
    msg = Label(win, text=message)
    msg.grid(row=0, column=0)
    ok_button = ttk.Button(win, text="OK", command=win.destroy)
    ok_button.grid(row=1, column=0)
###############################################################################
class Team:
    def __init__(self, team_id, team_desc, pld=0, pts=0, pd=0, pf=0, pa=0, wins=0, losses=0, draws=0):
        self.team_id = team_id
        self.team_desc = team_desc
        self.run = np.array([self.team_id, False, False, False])
        self.pld = pld
        self.pts = pts
        self.pd = pd
        self.place = 0
        self.pf = pf
        self.pa = pa
        self.wins = wins
        self.losses = losses
        self.draws = draws
    def get_place(self, table):
        place = settings["NUMBER_OF_TEAMS"] - table.index(self.team_id)
        return place
    def update_place(self, place):
        self.place = place
    def update_run(self, _round):
        self.run = np.vstack((self.run, _round))
    def reset_run(self):
        self.run = np.array([self.team_id, False, False, False])
    def get_form_score(self):
        form_score = 0
        if len(self.run) < (settings["FORM_RUN_LENGTH"] + 1):
            return settings["DEFAULT_FORM_SCORE"]
        
        for i in range (1,(settings["FORM_RUN_LENGTH"] + 1),1): #for last 5 matches
            if isinstance(self.run[-1 * i][0], np.str_):
                return settings["DEFAULT_FORM_SCORE"]
            if self.run[-1 * i][0] < 0: # If this team lost this match
                form_score += 1
        return form_score
    def get_form_score_at_round(self):
        _round = settings['ROUND']
        form_score = 0
        if len(self.run) > settings["FORM_RUN_LENGTH"]:
            run_slice = self.run[_round-5:_round]
        else:
            return DEFAULT_FORM_SCORE
        for i in range (0,(settings["FORM_RUN_LENGTH"]),1):
            if run_slice[-1 * i][0] is True:
                form_score += 1
        return form_score
    
def get_team_instance_from_id(_id):
    for t in team_stack:
        if t.team_id == _id:
            return t
        if t.team_desc == _id:
            return t
    do_error_message("get_team_instance_from_id couldn't find a team object!\n Input: " + _id)

###################### -V- LEAGUE HANDLING FUNCTIONS -V- ######################
def initialise_league(team_ids=settings["team_id_table"], team_desc=settings["team_desc_table"]):
    team_stack = []
    for t_index, t in enumerate(settings["team_id_table"]):
        current_team = Team(t, settings["team_desc_table"][t_index], 0, 0)
        team_stack.append(current_team)
    # declare all team instances
    # return array of class instances for each team in same order as id table
    return team_stack
def save_league():
    do_message("This feature is redundant as leagues auto-save any changes")
def load_league(filename=settings["LEAGUE_FILENAME"]):
    load_settings(filename)
    league_file = shelve.open(filename)
    league_file.close()
    return initialise_league(settings["team_id_table"], settings["team_desc_table"])
def clear_league(filename):
    league_file = shelve.open(filename)
    league_file.clear()
    league_file.close()
    
if os.path.isfile(settings["LEAGUE_FILENAME"]):
    team_stack = load_league()
else:
    team_stack = initialise_league()

def save_league_as(filename):
    shelve_file_1 = shelve.open(settings["LEAGUE_FILENAME"])
    shelve_file_2 = shelve.open(filename)
    shelve_file_2.clear()
    for key, value in zip(list(shelve_file_1.keys()), list(shelve_file_1.values())):
        shelve_file_2[key] = value
    shelve_file_1.close()
    shelve_file_2.close()
    do_message("League saved as {0}.".format(filename))
###################### -^- LEAGUE HANDLING FUNCTIONS -^- ######################
    
############################## -V- VIEW FUNCTIONS -V- #########################
def identify_winner(scores):
    result = []
    if scores[0] > scores[1]:
        result = 0
    elif scores[1] > scores[0]:
        result = 1
    else:
        result = 2
    return result
def compare_prediction(team_1, team_2, prediction, real):
    if isinstance(team_1, str):
        team_1 = get_team_instance_from_id(team_1)
        team_2 = get_team_instance_from_id(team_2)
        
    points = 0
    try:
        real = np.array(real, dtype=int)
        prediction = np.array(prediction, dtype=int)
    except ValueError: # prediction empty or invalid
        return 0
    real = np.array(real, dtype=int)
    r_score_owner = real[0]
    r_score_other = real[1]
    r_score_midpoint = np.average((r_score_owner, r_score_other)) 
    r_margin = r_score_owner - r_score_other
    
    p_score_owner = prediction[0]
    p_score_other = prediction[1]
    p_score_midpoint = np.average((p_score_owner, p_score_other))
    p_margin = p_score_owner - p_score_other
    
    d_score_owner = r_score_owner - p_score_owner
    d_score_other = r_score_other - p_score_other
    d_score_midpoint = r_score_midpoint - p_score_midpoint
    d_margin = r_margin - p_margin
    
    # 0 for home, 1 for away, 2 for draw
    p_winner = identify_winner(prediction)
    r_winner = identify_winner(real)
    if p_winner == r_winner:
        points += settings["RESULT_POINTS"]
        if settings["derby_factor_table"][settings["team_id_table"].index(team_1.team_id)][settings["team_id_table"].index(team_2.team_id)]\
        or settings["derby_factor_table"][settings["team_id_table"].index(team_2.team_id)][settings["team_id_table"].index(team_1.team_id)]  is True:
            
            points += settings["DERBY_FACTOR_POINTS"]
        
        if p_winner == 0:
            form_score = team_1.get_form_score()
        if p_winner == 1:
            form_score = team_2.get_form_score()
        else:
            form_score = settings["FORM_SCORE_DIVISOR"] #form score becomes a bonus for predicting a draw I guess
        form_points = form_score / settings["FORM_SCORE_DIVISOR"]
        points += form_points
    else:
        d_margin = d_margin * ((settings["MARGIN_IGNORES_RESULT"] * -2) + 1) # invert delta margin (This means you get points specifically for good margin regardless of winner)
    for m_index, m in enumerate(settings["MARGIN_LIMITS"]):
        if d_margin < m:
            points += settings["MARGIN_POINTS"][m_index]
            break
    for m_index, m in enumerate(settings["MIDPOINT_LIMITS"]):
        if d_score_midpoint < m:
            points += settings["MIDPOINT_POINTS"][m_index]
            break
    return points
def allocate_team_stats(results):
    for team in team_stack:
        team.reset_run()
        team.pld = 0
        team.pts = 0
        team.pf = 0
        team.pa = 0
        team.pd = 0
        team.wins = 0
        team.losses = 0
        team.draws = 0
    for current_round in results:
        for current_game in current_round:
            if current_game[0] != '':
                team_1 = get_team_instance_from_id(current_game[0])
                team_2 = get_team_instance_from_id(current_game[1])
                team_1_score = int(current_game[2])
                team_2_score = int(current_game[3])
                margin = int(team_1_score) - int(team_2_score)
                if settings["LOSING_POINTS_AWARDED"]:
                    if margin == 0:
                        team_1.pts += settings["DRAWING_POINTS"]
                        team_2.pts += settings["DRAWING_POINTS"]
                        team_1.draws += 1
                        team_2.draws += 1
                    if margin < 0:
                        team_2.pts += settings["WINNING_POINTS"]
                        team_2.wins += 1
                        team_1.losses += 1
                        if (-1 * margin) < int(settings["LOSING_POINTS_MAX_MARGIN"]):
                            team_1.pts += settings["LOSING_POINTS"]
                    if margin > 0:
                        team_1.pts += settings["WINNING_POINTS"]
                        team_1.wins += 1
                        team_2.losses += 1
                        if margin < int(settings["LOSING_POINTS_MAX_MARGIN"]):
                            team_2.pts += settings["LOSING_POINTS"]
                else:
                    if margin == 0:
                        team_1.pts += settings["DRAWING_POINTS"]
                        team_2.pts += settings["DRAWING_POINTS"]
                        team_1.draws += 1
                        team_2.draws += 1
                    if margin < 0:
                        team_2.pts += settings["WINNING_POINTS"]
                        team_2.wins += 1
                        team_1.losses += 1
                    if margin > 0:
                        team_1.pts += settings["WINNING_POINTS"]
                        team_1.wins += 1
                        team_2.losses += 1
                team_1.pf += team_1_score
                team_2.pf += team_2_score
                team_1.pa += team_2_score
                team_2.pa += team_1_score
                team_1.pd += (team_1_score - team_2_score)
                team_2.pd += (team_2_score - team_1_score)
                team_1.update_run([margin, team_2.team_id, team_1_score, team_2_score])
                team_2.update_run( [(-1 * margin) , team_1.team_id, team_2_score, team_1_score])
                # Maybe I'll add a "number of byes" stat to tables in the future. So I'll keep some of this commented for now.
    number_of_matches_array = []
    # number_of_byes_array = []
    for team in team_stack:
        if team.run.ndim == 2:
            team.pld = len(team.run) - 1
            number_of_matches_array.append((team.pld))
        else:
            team.pld = 0
            number_of_matches_array.append(team.pld)
    max_matches = max(number_of_matches_array)
    if settings["BYES"]:
        for i_team, team in enumerate(team_stack):
            # number_of_byes_array.append(max_matches - number_of_matches_array[i_team])
            team.pts += settings["WINNING_POINTS"] * (max_matches - number_of_matches_array[i_team])
def update_table(teams):
    """
    Updates a team_stack to be ordered by place (points and points difference) of each team.
    
    Parameters
    ----------
    teams : Array of "team", typically team_stack

    Returns
    -------
    ordered_table : Array
        League table in team_stack, ordered by place, from lowest to highest.

    """
    points_array = []
    pd_array = []
    ordered_table = []
    points_range = (0, (settings["NUMBER_OF_ROUNDS"] * 2) + 1)
    for i in range (*points_range):
        points_array.append([])
        pd_array.append([])
    for p in range (*points_range):
        for t in teams:
            if t.pts == p:
                points_array[p].append(t)
                pd_array[p].append(t.pd)
    for i_b, brane in enumerate(pd_array):
        solution = np.argsort(brane)
        points_array[i_b] = np.array(points_array[i_b], dtype=object) # Numpy does not like dtype=object ndarrays
        points_array[i_b] = points_array[i_b][(solution)]
    for b in points_array:
        for t in b:
            t.update_place((settings["NUMBER_OF_TEAMS"] - len(ordered_table)))
            ordered_table.append(t)
    shelve_file = shelve.open("league")
    shelve_file["league_table"] = ordered_table
    shelve_file.close()
    return ordered_table
def ui_render_league_box(lb=lb1):
    results = try_open_data("results", settings["LEAGUE_FILENAME"]) # bad call
    if isinstance(results, int):
        pass
    else:
        allocate_team_stats(results)
    ordered = np.flip(update_table(team_stack))
    lb1.delete(0, END)
    for t_i, c_team in enumerate(ordered):
        cur_string = "{0} : {1} | Pld: {2} | W: {3} | D: {4} | L: {5} | Pts : {6} | PF : {7} | PA : {8} | PD : {9}"\
            .format(c_team.place, c_team.team_desc, c_team.pld, c_team.wins, c_team.draws, c_team.losses, c_team.pts, c_team.pf, c_team.pa, c_team.pd)
        lb1.insert(t_i, cur_string)
    lb1.pack()
def view_fixtures():
    round_num = settings['ROUND']
    round_index = int(round_num) - 1
    fixtures = try_open_data("fixtures", settings["LEAGUE_FILENAME"])
    win = Toplevel()
    win.wm_title(f"Round fixtures for round {ROUND}")
    if isinstance(fixtures, int):
        if fixtures == -1:
            do_error_message(f"ERROR: Fixtures for this round are not entered (round {settings['ROUND']})")
            win.destroy()
            return
        do_error_message(f"ERROR: Invalid fixtures were read for this round (round {settings['ROUND']})")
        win.destroy()
        return
    fixtures = fixtures[round_index]
    team_1_box = []
    space = []
    team_2_box = []
    
    round_header = Label(win, text=f"Round : {settings['ROUND']}")
    round_header.grid(row=0, column=0)
    
    score_header_1 = Label(win, text="Team 1")
    score_header_1.grid(row=1, column=0)
    
    score_header_2 = Label(win, text="Team 2")
    score_header_2.grid(row=1, column=2)
    
    header_space = Label(win, text="------------------")
    header_space.grid(row=2, column=1)
    
    ui_index = 0
    for i_teams, teams in enumerate(fixtures):
        
        ui_index = (2 * i_teams + 2)
        
        team_1_box.append(Label(win, text=teams[0]))
        team_1_box[-1].grid(row=(ui_index + 1), column=0)
        
        space.append(Label(win, anchor="c", text=" vs. "))
        space[-1].grid(row=(ui_index + 1), column=1)
        
        team_2_box.append(Label(win, text=teams[1]))
        team_2_box[-1].grid(row=(ui_index + 1), column=2)
    
    confirm_button = ttk.Button(win, text="OK", command=win.destroy)
    confirm_button.grid(row=(ui_index + 2), column=1)
    return
def view_predictions():
    player_select_win = Toplevel()
    player_select_win.wm_title("Select player")
    msg = Label(player_select_win, text=f"Select a player...")
    msg.grid(row=0, column=0)
    player_header = Label(player_select_win, text="Player :")
    player_header.grid(row=1,column=0)
    player_dropdown = ttk.Combobox(player_select_win, state="readonly")
    player_dropdown["values"] = settings["players"]
    player_dropdown.grid(row=1,column=1)
    def send_player():
        try:
            player_index = settings["players"].index(player_dropdown.get())
        except ValueError:
            do_message("You must select a player first.")
            return -1
        show_predictions(player_index)
    ok_button = ttk.Button(player_select_win, text="Select", command=lambda : send_player())
    ok_button.grid(row=1, column=0)
    def show_predictions(player_index):
        player_selected = settings["players"][player_index]
        round_num = settings['ROUND']
        round_index = int(round_num) - 1
        predictions = try_open_data("predictions", settings["LEAGUE_FILENAME"])
        win = Toplevel()
        win.wm_title(f'Round predictions for round {settings['ROUND']} for player "{player_selected}"')
        if isinstance(predictions, int):
            if predictions == -1:
                do_error_message(f"ERROR: Fixtures for this round are not entered (round {settings['ROUND']})")
                return
            do_error_message(f"ERROR: Invalid fixtures were read for this round (round {settings['ROUND']})")
            return
        predictions = predictions[player_index][round_index]
        team_1_box = []
        team_1_score = []
        space = []
        team_2_score = []
        team_2_box = []
        
        round_header = Label(win, text=f"ROUND : {settings['ROUND']}")
        round_header.grid(row=0, column=0)
        
        score_header_1 = Label(win, text="Team 1")
        score_header_1.grid(row=2, column=0)
        
        score_header_2 = Label(win, text="Team 2")
        score_header_2.grid(row=2, column=4)
        
        ui_index = 0
        for i_teams, teams in enumerate(predictions):
            
            ui_index = (2 * i_teams + 2)
            
            team_1_box.append(Label(win, text=teams[0]))
            team_1_box[-1].grid(row=(ui_index + 1), column=0)
            
            team_1_score.append(Label(win, text=f"[{teams[2]}]"))
            team_1_score[-1].grid(row=(ui_index + 1), column=1)
            
            space.append(Label(win, anchor="c", text=" - "))
            space[-1].grid(row=(ui_index + 1), column=2)
            
            team_2_score.append(Label(win, text=f"[{teams[3]}]"))
            team_2_score[-1].grid(row=(ui_index + 1), column=3)
            
            team_2_box.append(Label(win, text=teams[1]))
            team_2_box[-1].grid(row=(ui_index + 1), column=4)
        
        confirm_button = ttk.Button(win, text="OK", command=win.destroy)
        confirm_button.grid(row=(ui_index + 2), column=0)
    return
def view_results():
    round_num = settings['ROUND']
    round_index = int(round_num) - 1
    results = try_open_data("results", settings["LEAGUE_FILENAME"])
    win = Toplevel()
    win.wm_title(f"Round results for round {settings['ROUND']}")
    if isinstance(results, int):
        if results == -1:
            do_error_message(f"ERROR: Results for this round are not entered (round {settings['ROUND']})")
            win.destroy()
            return
        do_error_message(f"ERROR: Invalid results were read for this round (round {settings['ROUND']}) (Code {results})")
        win.destroy()
        return
    results = results[round_index]
    team_1_box = []
    team_1_score = []
    space = []
    team_2_score = []
    team_2_box = []
    
    round_header = Label(win, text=f"ROUND : {settings['ROUND']}")
    round_header.grid(row=0, column=0)
    
    score_header_1 = Label(win, text="Team 1")
    score_header_1.grid(row=2, column=0)
    
    score_header_2 = Label(win, text="Team 2")
    score_header_2.grid(row=2, column=4)
    
    ui_index = 0
    for i_teams, teams in enumerate(results):
        
        ui_index = (2 * i_teams + 2)
        
        team_1_box.append(Label(win, text=teams[0]))
        team_1_box[-1].grid(row=(ui_index + 1), column=0)
        
        team_1_score.append(Label(win, text=f"[{teams[2]}]"))
        team_1_score[-1].grid(row=(ui_index + 1), column=1)
        
        space.append(Label(win, anchor="c", text=" - "))
        space[-1].grid(row=(ui_index + 1), column=2)
        
        team_2_score.append(Label(win, text=f"[{teams[3]}]"))
        team_2_score[-1].grid(row=(ui_index + 1), column=3)
        
        team_2_box.append(Label(win, text=teams[1]))
        team_2_box[-1].grid(row=(ui_index + 1), column=4)
    
    confirm_button = ttk.Button(win, text="OK", command=win.destroy)
    confirm_button.grid(row=(ui_index + 2), column=0)
    return
############################## -^- VIEW FUNCTIONS -^- #########################

############################# -V- LEAGUE FUNCTIONS -V- ########################
def prompt_add_round_fixtures():
    win = Toplevel()
    win.wm_title("Add Round fixtures...")
    
    team_1_input = []
    space = []
    team_2_input = []
    
    round_header = Label(win, text="ROUND :")
    round_header.grid(row=0, column=0)
    round_value = Text(win, height=1, width=4)
    round_value.grid(row=0, column=1)
    
    ui_index = 0
    
    for i_teams in range (settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"]):
        
        ui_index = (2 * i_teams + 2)
        
        team_1_input.append(ttk.Combobox(win, state="readonly"))
        team_1_input[-1]["values"] = settings["team_desc_table"]
        team_1_input[-1].grid(row=(ui_index + 1),column=1)
        
        space.append(Label(win, anchor="c", text="vs"))
        space[-1].grid(row=(ui_index + 1), column=2)
        
        team_2_input.append(ttk.Combobox(win, state="readonly"))
        team_2_input[-1]["values"] = settings["team_desc_table"]
        team_2_input[-1].grid(row=(ui_index + 1),column=3)
        
    def send_fixtures():
        round_num = round_value.get("1.0", "end-1c")
        if round_num == '':
            round_num = settings['ROUND']
        round_index = int(round_num) - 1 # number -> index
        shelve_file = shelve.open(settings["LEAGUE_FILENAME"])
        try:
            fixtures = shelve_file["fixtures"]
        except KeyError:
            fixtures = np.zeros((settings["NUMBER_OF_ROUNDS"], settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 2), dtype="<U32")
        cur_fixtures = fixtures
        blank_fixtures = np.zeros((settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 2), dtype="<U32")
        
        for fixture in range (len(blank_fixtures)):
            team_1_id = team_1_input[fixture].get()
            team_2_id = team_2_input[fixture].get()
            blank_fixtures[fixture] = [team_1_id, team_2_id]
            
        cur_fixtures[round_index] = blank_fixtures
        shelve_file["fixtures"] = cur_fixtures
        shelve_file.close()
        win.destroy()
        return
    
    confirm_button = ttk.Button(win, text="Confirm", command=lambda:send_fixtures())
    confirm_button.grid(row=(ui_index + 2), column=1)
    
    cancel_button = ttk.Button(win, text="Cancel", command=win.destroy)
    cancel_button.grid(row=(ui_index + 2), column=3)
    return
def prompt_add_prediction():
    round_num = settings['ROUND']
    round_index = int(round_num) - 1
    fixtures_file = try_open_data("fixtures", settings["LEAGUE_FILENAME"])
    if isinstance(fixtures_file, int):
        do_error_message(f"There are no fixtures for this round ({settings['ROUND']})")
        return
    else:
        fixtures = fixtures_file[round_index]
    win = Toplevel()
    win.wm_title("Add Round predictions...")
    if isinstance(fixtures, int):
        if fixtures == -1:
            do_error_message(f"ERROR: Fixtures for this round are not entered (round {settings['ROUND']})")
            return
        else:
            do_error_message(f"ERROR: Invalid fixtures were read for this round (round {settings['ROUND']})")
            return

    team_1_box = []
    team_1_score_input = []
    space = []
    team_2_score_input = []
    team_2_box = []
    
    player_header = Label(win, text="Player :")
    player_header.grid(row=0,column=0)
    player_dropdown = ttk.Combobox(win, state="readonly")
    player_dropdown["values"] = settings["players"]
    player_dropdown.grid(row=0,column=1)
    top_space = Label(win, text="|")
    top_space.grid(row=0,column=2)
    round_header = Label(win, text="ROUND :")
    round_header.grid(row=0, column=3)
    round_value = Label(win, text=str(round_num))
    round_value.grid(row=0, column=4)
    
    team_header_1 = Label(win, text="Home team")
    team_header_1.grid(row=1, column=1)
    
    team_header_2 = Label(win, text="Away team")
    team_header_2.grid(row=1, column=3)
    
    ui_index = 0
    
    for i_teams, teams in enumerate(fixtures):
        ui_index = (2 * i_teams + 2)
        
        team_1_box.append(Label(win, text=teams[0]))
        team_1_box[-1].grid(row=(ui_index + 1), column=0)
        
        team_1_score_input.append(Text(win, height=1, width = 6))
        team_1_score_input[-1].grid(row=(ui_index + 1), column=1)
        
        space.append(Label(win, anchor="c", text="-"))
        space[-1].grid(row=(ui_index + 1), column=2)
        
        team_2_score_input.append(Text(win, height=1, width = 6))
        team_2_score_input[-1].grid(row=(ui_index + 1), column=3)
        
        team_2_box.append(Label(win, text=teams[1]))
        team_2_box[-1].grid(row=(ui_index + 1), column=4)

    def send_prediction():
        def confirm_overwrite(): 
            def confirmed_overwrite(): # Surely there is a better way to do this, but I do not know tkinter well enough.
                blank_predictions = np.zeros((settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 4), dtype="<U32")
                for prediction in range (settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"]):
                    team_1_score = team_1_score_input[prediction].get("1.0", "end-1c")
                    team_2_score = team_2_score_input[prediction].get("1.0", "end-1c")
                    
                    # I'm not sure if this will always be the right shape if there's more than 1 round. 
                    blank_predictions[prediction] = \
                    np.array([*round_fixtures[prediction], team_1_score, team_2_score], dtype="<U32")
                cur_predictions[player_index][round_index] = blank_predictions
                shelve_file["predictions"] = cur_predictions
                shelve_file.close()
                warning_win.destroy()
                current_player = settings["players"][player_index]
                do_message("Predictions for {current_player} saved successfully.")
            warning_win = Toplevel()
            warning_win.wm_title("Warning")
            current_player = settings["players"][player_index]
            msg = Label(warning_win, text=f"You are about to overwrite existing predictions for {current_player} for this round (Round {settings['ROUND']}). Are you sure?")
            msg.grid(row=0, column=0)
            ok_button = ttk.Button(warning_win, text="Overwrite", command=((lambda : do_nothing()) and (lambda: confirmed_overwrite())))
            ok_button.grid(row=1, column=0)
            cancel_button = ttk.Button(warning_win, text="Cancel", command=lambda : warning_win.destroy())
            cancel_button.grid(row=2, column=0)
        def overwrite():
            blank_predictions = np.zeros((settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 4), dtype="<U32")
            for prediction in range (settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"]):
                team_1_score = team_1_score_input[prediction].get("1.0", "end-1c")
                team_2_score = team_2_score_input[prediction].get("1.0", "end-1c")
                
                # I'm not sure if this will always be the right shape if there's more than 1 round. 
                blank_predictions[prediction] = \
                np.array([*round_fixtures[prediction], team_1_score, team_2_score], dtype="<U32")
            cur_predictions[player_index][round_index] = blank_predictions
            shelve_file["predictions"] = cur_predictions
            shelve_file.close()
            do_message("Predictions for {current_player} saved successfully.")
        try:
            player_index = settings["players"].index(player_dropdown.get())
        except ValueError:
            do_message("You must select a player first.")
            return
        shelve_file = shelve.open(settings["LEAGUE_FILENAME"])
        fixtures = shelve_file["fixtures"]
        round_fixtures = fixtures[round_index]
        try:
            cur_predictions = shelve_file["predictions"]
            #cur_predictions = cur_predictions.astype("<U32")
            #cur_predictions = np.zeros((NUMBER_OF_PLAYERS, NUMBER_OF_ROUNDS, MAX_NUMBER_OF_MATCHES_PER_ROUND, 4), dtype="<U32")
        except:
            league_filename = settings["LEAGUE_FILENAME"]
            print(f"Could not open predictions for {league_filename}, creating a default one.")
            cur_predictions = np.zeros((settings["NUMBER_OF_PLAYERS"], settings["NUMBER_OF_ROUNDS"], settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 4), dtype="<U32")
        if cur_predictions[player_index][round_index].any() != 0:
            confirm_overwrite()
        else:
            overwrite()
        return
    confirm_button = ttk.Button(win, text="Confirm", command=lambda:send_prediction())
    confirm_button.grid(row=(ui_index + 2), column=1)
    
    cancel_button = ttk.Button(win, text="Cancel", command=win.destroy)
    cancel_button.grid(row=(ui_index + 2), column=3)
    return
def prompt_add_round_results():
    """WIP"""
    round_num = ROUND
    round_index = int(round_num) - 1
    fixtures = try_open_data("fixtures", settings["LEAGUE_FILENAME"])
    fixtures = fixtures[round_index]
    win = Toplevel()
    win.wm_title("Add Round results...")
    if isinstance(fixtures, int):
        if fixtures == -1:
            do_error_message(f"ERROR: Fixtures for this round are not entered (round {settings['ROUND']})")
            return
        do_error_message(f"ERROR: Invalid fixtures were read for this round (round {settings['ROUND']})")
        return
    team_1_box = []
    team_1_score_input = []
    space = []
    team_2_score_input = []
    team_2_box = []
    
    round_header = Label(win, text="ROUND :")
    round_header.grid(row=0, column=0)
    round_value = Label(win, text=str(settings['ROUND']))
    round_value.grid(row=0, column=1)
    
    score_header_1 = Label(win, text="Score")
    score_header_1.grid(row=2, column=1)
    
    score_header_2 = Label(win, text="Score")
    score_header_2.grid(row=2, column=3)
    
    ui_index = 0
    for i_teams, teams in enumerate(fixtures):
        
        ui_index = (2 * i_teams + 2)
        
        team_1_box.append(Label(win, text=teams[0]))
        team_1_box[-1].grid(row=(ui_index + 1), column=0)
        
        team_1_score_input.append(Text(win, height=1, width = 6))
        team_1_score_input[-1].grid(row=(ui_index + 1), column=1)
        
        space.append(Label(win, anchor="c", text="-   "))
        space[-1].grid(row=(ui_index + 1), column=2)
        
        team_2_score_input.append(Text(win, height=1, width = 6))
        team_2_score_input[-1].grid(row=(ui_index + 1), column=3)
        
        team_2_box.append(Label(win, text=teams[1]))
        team_2_box[-1].grid(row=(ui_index + 1), column=4)

    def send_round():
        cur_results = try_open_data("results", settings["LEAGUE_FILENAME"])
        cur_fixtures = fixtures
        blank_results = np.zeros((settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 4), dtype="<U32")
        if isinstance(cur_results, int): # If it does not exist/is invalid create a new one
            cur_results = np.zeros((settings["NUMBER_OF_ROUNDS"], settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 4), dtype="<U32")
        for result in range (settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"]):
            team_1 = cur_fixtures[result][0]
            team_2 = cur_fixtures[result][1]
            team_1_score = team_1_score_input[result].get("1.0", "end-1c")
            team_2_score = team_2_score_input[result].get("1.0", "end-1c")

            blank_results[result] = \
            np.array([team_1, team_2, team_1_score, team_2_score])
        
        cur_results[round_index] = blank_results
        shelve_file = shelve.open(settings["LEAGUE_FILENAME"])
        shelve_file["results"] = cur_results
        shelve_file.close()
        win.destroy()
    
    confirm_button = ttk.Button(win, text="Confirm", command=lambda:send_round())
    confirm_button.grid(row=(ui_index + 2), column=0)
    
    cancel_button = ttk.Button(win, text="Cancel", command=win.destroy)
    cancel_button.grid(row=(ui_index + 2), column=1)
def prompt_set_round():
    win = Toplevel()
    win.wm_title("Set round...")
    
    round_set_box = Label(win, text="The round will be set to :")
    round_set_box.grid(row=0, column=0)
    round_set_input = Text(win, height=1, width=4)
    round_set_input.grid(row=0, column=1)
    round_current_box = Label(win, text=f"(Current round: {settings['ROUND']})")
    round_current_box.grid(row=1, column=0)
    def set_round():
        global settings
        try:
            settings['ROUND'] = int(round_set_input.get("1.0", "end-1c"))
        except ValueError:
            settings['ROUND'] = 1 # Don't need to use update_settings because we're only changing 1 value
        settings_instance.save_settings(True)
        win.destroy()
    set_button = ttk.Button(win, text="Set", command=lambda:set_round())
    set_button.grid(row=2, column=0)
    
    cancel_button = ttk.Button(win, text="Cancel", command=win.destroy)
    cancel_button.grid(row=2, column=1)
    return
############################# -^- LEAGUE FUNCTIONS -^- ########################

############################# -V- SCORING FUNCTIONS -V- #######################
def get_total_scores_all_rounds():
    total_scores = []
    for player in settings["players"]:
        player_score = 0
        for _round in range (settings["NUMBER_OF_ROUNDS"]):
            current_score = get_player_score_for_round(player, _round)
            if current_score > 0:
                player_score += current_score
        total_scores.append(player_score)
    return total_scores
def get_player_score_for_round(player, _round, display=True):
    round_index = int(_round) - 1
    player_index = settings["players"].index(player)
    predictions = try_open_data("predictions", settings["LEAGUE_FILENAME"])
    if isinstance(predictions, int):
        print("No predictions found for get_player_score_for_round()")
        return 0
    results = try_open_data("results", settings["LEAGUE_FILENAME"])
    if isinstance(results, int):
        print("No results found for get_player_score_for_round()")
        return 0
    round_predictions = predictions[player_index][round_index]
    round_results = results[round_index]
    round_points = 0
    for game in range (settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"]):
        teams = round_predictions[game][0:2]
        predicted_scores = round_predictions[game][2:]
        real_scores = round_results[game][2:]
        if teams[0] != np.str_(''):
            points = compare_prediction(*teams, predicted_scores, real_scores)
            round_points += points
            if display:
                print(f"Points for {player} for match {game} ({teams[0]} vs {teams[1]}): {points}")
        else:
            points = 0
    return round_points
def show_player_scores():
    win = Toplevel()
    win.wm_title("Player scores")
    player_scores = get_total_scores_all_rounds()
    for i_p, p in enumerate(settings["players"]):
        player_score = player_scores[i_p]
        score_text = Label(win, text=f"{p} : {player_score:.2f}")
        score_text.grid(row=i_p, column=0)
    ok_button = ttk.Button(win, text="OK", command=win.destroy)
    ok_button.grid(row=(len(settings["players"]) + 1), column=0)
def show_player_scores_at_round():
    win = Toplevel()
    win.wm_title(f"Player scores for round {settings['ROUND']}")
    player_scores = []
    round_text = Label(win, text=f"ROUND : {settings['ROUND']}")
    round_text.grid(row=0, column=0)
    for i_p, p in enumerate(settings["players"]):
        player_scores.append(get_player_score_for_round(p, settings['ROUND']))
        player_score = player_scores[i_p]
        score_text = Label(win, text=f"{p} : {player_score:.2f}")
        score_text.grid(row=(i_p+1), column=0)
    ok_button = ttk.Button(win, text="OK", command=win.destroy)
    ok_button.grid(row=(i_p + 2), column=0)
############################# -^- SCORING FUNCTIONS -^- #######################

############################# -V- OPTIONS FUNCTIONS -V- #######################
def create_yn_box(window):
    yn_box = ttk.Combobox(window, state="readonly", width=5)
    yn_box["values"] = ["Yes", "No"]
    return yn_box
def create_number_box(window):
    number_box = Text(window, height=1, width=4)
    return number_box
def create_space_box(window):
    space_box = Label(window, text="---------")
    return space_box
def create_list_box(window, length): 
    box_list = []
    for i in range (length):
        box_list.append(Text(window, height=1, width=4))
    return box_list
def get_box_value(box, box_type): 
    if box_type == "yn":
        value = box.get()
        if value == "Yes":
            value = True
        else:
            value = False
    elif box_type == "number":
        value = box.get("1.0", "end-1c")
    elif box_type[:4] == "list":
        value = box.get("1.0", "end-1c")
    else:
        value = "space"
    return value
def format_option_types(option_types):
    formatted_option_types = []
    unformatted_counter = 0
    formatted_counter = 0
    while unformatted_counter < len(option_types): # ["list3"] -> "["list3", "list3", "list3"]
        if option_types[unformatted_counter][:-1] == "list":
            list_length = int(option_types[unformatted_counter][4:])
            for i in range(list_length):
                formatted_option_types.append(option_types[unformatted_counter])
            formatted_counter += list_length
            unformatted_counter += 1
        else:
            formatted_option_types.append(option_types[unformatted_counter])
            formatted_counter += 1
            unformatted_counter += 1
    return formatted_option_types
def format_options(option_types, option_vars):
    formatted_option_types = []
    formatted_option_vars = []
    unformatted_counter = 0
    formatted_counter = 0
    while unformatted_counter < len(option_types): # ["list3"] -> "["list3", "list3", "list3"]
        if option_types[unformatted_counter][:-1] == "list":
            list_length = int(option_types[unformatted_counter][4:])
            for i in range(list_length):
                formatted_option_types.append(option_types[unformatted_counter])
                formatted_option_vars.append(option_vars[unformatted_counter])
            formatted_counter += list_length
            unformatted_counter += 1
        else:
            formatted_option_types.append(option_types[unformatted_counter])
            formatted_option_vars.append(option_vars[unformatted_counter])
            formatted_counter += 1
            unformatted_counter += 1
    return (formatted_option_types, formatted_option_vars)
def league_settings_menu():
    win = Toplevel()
    win.wm_title("League settings")
    display_keys = []
    display_keyval_space = []
    display_values = []
    option_vars = (("BYES", "WINNING_POINTS", "DRAWING_POINTS",\
                    "spaceholder", "LOSING_POINTS_AWARDED", "LOSING_POINTS", "LOSING_POINTS_MAX_MARGIN"))
    option_keys = ["Teams have bye-rounds", "Points for winning", "Points for drawing", "",\
                   "Loser can be awarded points?", "Points for losing", "Maximum losing margin"]
    option_values = np.array((settings["BYES"], settings["WINNING_POINTS"], settings["DRAWING_POINTS"], \
                              "space", settings["LOSING_POINTS_AWARDED"], settings["LOSING_POINTS"]\
                                  , settings["LOSING_POINTS_MAX_MARGIN"]), dtype="<U32")
    option_types = ["yn", "number", "number", "space", "yn", "number", "number"]
    ui_index = 0
    num_elements = 7
    for i in range (num_elements):
        display_keys.append(Label(win, text=option_keys[i]))
        display_keys[-1].grid(row=(i + 1), column=0)
        current_type = option_types[i]
        if current_type == "yn":
            display_values.append(create_yn_box(win))
            if option_values[i] == "True":
                display_values[-1].set("Yes")
            if option_values[i] == "False":
                display_values[-1].set("No")
            display_values[-1].grid(row=(i + 1), column=2)
            display_keyval_space.append(Label(win, text="|"))
            display_keyval_space[-1].grid(row = (i+1), column=1)
        elif current_type == "space":
            display_values.append(create_space_box(win))
            display_values[-1].grid(row=(i + 1), column=2)
        else:
            display_values.append(create_number_box(win))
            display_values[-1].insert(END, option_values[i])
            display_values[-1].grid(row=(i + 1), column=2)
            display_keyval_space.append(Label(win, text="|"))
            display_keyval_space[-1].grid(row = (i+1), column=1)
    def send_settings():
        global settings
        new_settings = {}
        box_values = []
        for i_box, box in enumerate(display_values):
            box_values.append(get_box_value(box, option_types[i_box]))
        for i_var, var in enumerate(option_vars):
            if option_types[i_var] == "number":
                new_settings[var] = float(box_values[i_var])
            if option_types[i_var] == "yn":
                new_settings[var] = box_values[i_var]
        settings = settings_instance.update_settings(new_settings)
        settings_instance.save_settings()
        win.destroy()
        return
    confirm_button = ttk.Button(win, text="Confirm", command=lambda: send_settings())
    confirm_button.grid(row=(i + 3), column = 0)
    cancel_button = ttk.Button(win, text="Cancel", command=win.destroy)
    cancel_button.grid(row=(i + 3), column = 1)
    return
def teams_settings_menu():
    return
def scoring_settings_menu():
    win = Toplevel()
    win.wm_title("Scoring settings")
    display_keys = []
    display_keyval_space = []
    display_values = []
    option_vars = (("RESULT_POINTS", "DERBY_FACTOR_POINTS", "FORM_SCORE_DIVISOR",\
                    "spaceholder", "MARGIN_POINTS", "MARGIN_LIMITS", "MIDPOINT_POINTS", "MIDPOINT_LIMITS"))
    option_keys = ["Points for predicting correct result", "Derby result bonus", "Form score divisor", "",\
                   "Margin accuracy points", "Margin accuracy limits", "Total score accuracy points", "Total score accuracy limits"]
    option_values = [settings["RESULT_POINTS"], settings["DERBY_FACTOR_POINTS"], settings["FORM_SCORE_DIVISOR"], \
                              "space", settings["MARGIN_POINTS"], settings["MARGIN_LIMITS"]\
                                  , settings["MIDPOINT_POINTS"], settings["MIDPOINT_LIMITS"]]
    option_types = ["number", "number", "number", "space", "list6", "list5", "list6", "list5"] # list = list of numbers
    
    formatted_option_types, formatted_option_vars = format_options(option_types, option_vars)
    ui_index = 0
    num_elements = len(option_vars)
    for i in range (num_elements):
        display_keys.append(Label(win, text=option_keys[i]))
        display_keys[-1].grid(row=(i + 1), column=0)
        current_type = option_types[i]
        if current_type == "yn":
            display_keyval_space.append(Label(win, text="|"))
            display_keyval_space[-1].grid(row = (i+1), column=1)
            display_values.append(create_yn_box(win))
            display_values[-1].set(option_values[i])
            display_values[-1].grid(row=(i + 1), column=2)
        elif current_type == "space":
            display_values.append(create_space_box(win))
            display_values[-1].grid(row=(i + 1), column=2)
        elif current_type[:4] == "list":
            display_keyval_space.append(Label(win, text="|"))
            display_keyval_space[-1].grid(row = (i+1), column=1)
            for i_v, value in enumerate(option_values[i]):
                display_values.append(create_number_box(win))
                display_values[-1].insert(END, option_values[i][i_v])
                display_values[-1].grid(row=(i + 1), column=i_v+2)
        else:
            display_values.append(create_number_box(win))
            display_values[-1].insert(END, option_values[i])
            display_values[-1].grid(row=(i + 1), column=2)
            display_keyval_space.append(Label(win, text="|"))
            display_keyval_space[-1].grid(row = (i+1), column=1)
    def send_settings():
        global settings
        list_begin = -1
        list_length = 0
        new_settings = {}
        box_values = []
        for i_box, box in enumerate(display_values):
            box_values.append(get_box_value(box, formatted_option_types[i_box]))
        """
        for i_var, var in enumerate(option_vars):
            print(list_begin+list_length)
            print(i_var)
            if i_var >= list_begin + list_length:
                if option_types[i_var] == "number":
                    new_settings[var] = float(box_values[i_var])
                if option_types[i_var] == "yn":
                    new_settings[var] = bool(box_values[i_var])
                if option_types[i_var][:4] == "list":
                    list_begin = i_var
                    list_length = int(option_types[i_var][4:])
                    new_settings[var] = [0] * list_length
                    for k in range (list_length):
                        new_settings[var][k] = float(box_values[i_var+k])
                    print(new_settings)
        """
        for i_var, var in enumerate(formatted_option_vars):
            print(list_begin+list_length)
            print(i_var)
            if i_var >= list_begin + list_length:
                if formatted_option_types[i_var] == "number":
                    new_settings[var] = float(box_values[i_var])
                if formatted_option_types[i_var] == "yn":
                    new_settings[var] = bool(box_values[i_var])
                if formatted_option_types[i_var][:4] == "list":
                    list_begin = i_var
                    list_length = int(formatted_option_types[i_var][4:])
                    new_settings[var] = [0] * list_length
                    for k in range (list_length):
                        new_settings[var][k] = float(box_values[i_var+k])
                    print(new_settings)
        settings = settings_instance.update_settings(new_settings)
        win.destroy()
        return
    confirm_button = ttk.Button(win, text="Confirm", command=lambda: send_settings())
    confirm_button.grid(row=(i + 3), column = 0)
    cancel_button = ttk.Button(win, text="Cancel", command=win.destroy)
    cancel_button.grid(row=(i + 3), column = 1)
    return
############################# -^- OPTIONS FUNCTIONS -^- #######################

def prompt_save_league_as():
    f = asksaveasfilename(initialdir = os.getcwd())
    if f is None or f == '': # asksaveasfile return `None` if dialog closed with cancel or X.
        return
    save_league_as(f)
def prompt_import_league():
    global team_stack
    f = askopenfilename(initialdir = os.getcwd())
    try:
        if f.find(".") == -1: # asksaveasfile return `None` if dialog closed with "cancel".
            return
    except AttributeError:
        return
    f = f[:-4]
    team_stack = load_league(f)
    ui_render_league_box(lb1)
def prompt_refresh_league():
    global team_stack
    team_stack = initialise_league()
    ui_render_league_box(lb1)
def option_save_settings():
    settings_instance.save_settings()
    return

def create_team_set_menu():
    win = Toplevel()
    win.wm_title("Create team set")
    lb_create = Listbox(win, width = 84, height = 10)
    lb_create.grid(row = 0, column = 2)
    team_table = []
    def add_team():
        win_add = Toplevel()
        win_add.wm_title("Add team")
        team_label = Label(win_add, text="Name of team")
        team_label.grid(row = 0, column = 0)
        team_name_box = Text(win_add, height=1, width=50)
        team_name_box.grid(row = 1, column = 0)
        def create_team():
            text_box = team_name_box.get("1.0",END)[:-1]
            if text_box == "\n":
                do_message("Please enter a team name")
            else:
                new_team = Team(text_box, text_box)
                team_table.append(new_team)
                cur_string = "{0} : {1} | Pld: {2} | W: {3} | D: {4} | L: {5} | Pts : {6} | PF : {7} | PA : {8} | PD : {9}"\
                    .format(new_team.place, new_team.team_desc, new_team.pld, new_team.wins, new_team.draws, new_team.losses, new_team.pts, new_team.pf, new_team.pa, new_team.pd)
                lb_create.insert(len(team_table), cur_string)
            return   
        add_button = ttk.Button(win_add, text="Add", command=lambda: create_team())
        add_button.grid(row = 2, column = 0)
    add_menu_button = ttk.Button(win, text="Add Team", command=lambda: add_team())
    add_menu_button.grid(row = 0, column = 0)
    def remove_team():
        line = lb_create.curselection()
        if line == ():
            do_message("Please select a team first.")
        else:
            for index in line:
                lb_create.delete(index)
                team_table.pop(index)
    remove_button = ttk.Button(win, text="Remove selected team", command=lambda: remove_team())
    remove_button.grid(row = 0, column = 3)
    def prompt_clear():
        warning_win = Toplevel()
        warning_win.wm_title("Clear all teams")
        msg = Label(warning_win, text="Are you sure you want to clear the table and remove all teams?")
        msg.grid(row=0, column=1)
        def clear_table():
            lb_create.delete(0, lb_create.size())
            warning_win.destroy()
        ok_button = ttk.Button(warning_win, text="Clear", command=((lambda : do_nothing()) and (lambda: clear_table())))
        ok_button.grid(row=1, column=0)
        cancel_button = ttk.Button(warning_win, text="Cancel", command=lambda : warning_win.destroy())
        cancel_button.grid(row=1, column=2)
    clear_button = ttk.Button(win, text="Clear table", command=lambda: prompt_clear())
    clear_button.grid(row = 2, column = 3)
    def edit_team():
        if lb_create.curselection() == ():
            do_message("Select a team first.")
            return
        win_add = Toplevel()
        win_add.wm_title("Edit selected team")
        selected_team_index = lb_create.curselection()[0] #If multiple selected just do the first one
        selected_team = team_table[selected_team_index].team_desc
        team_label = Label(win_add, text=f"Name of team (Selected team: {selected_team})")
        team_label.grid(row = 0, column = 0)
        team_name_box = Text(win_add, height=1, width=50)
        team_name_box.insert("1.0", selected_team)
        team_name_box.grid(row = 1, column = 0)
        def confirm_edit_team():
            text_box = team_name_box.get("1.0",END)[:-1]
            if text_box == "\n":
                do_message("Please enter a team name")
            else:
                lb_create.delete(selected_team_index)
                team_table.pop(selected_team_index)
                new_team = Team(text_box, text_box)
                team_table.append(new_team)
                cur_string = "{0} : {1} | Pld: {2} | W: {3} | D: {4} | L: {5} | Pts : {6} | PF : {7} | PA : {8} | PD : {9}"\
                    .format(new_team.place, new_team.team_desc, new_team.pld, new_team.wins, new_team.draws, new_team.losses, new_team.pts, new_team.pf, new_team.pa, new_team.pd)
                lb_create.insert(len(team_table), cur_string)
            return   
        confirm_button = ttk.Button(win_add, text="Confirm", command=lambda: confirm_edit_team())
        confirm_button.grid(row = 2, column = 0)
    edit_button = ttk.Button(win, text="Edit selected team", command=lambda: edit_team())
    edit_button.grid(row = 2, column = 0)
    def prompt_save_table_as_league():
        def save_table_as_league(filename):
            shelve_file_1 = shelve.open(settings["LEAGUE_FILENAME"])
            shelve_file_2 = shelve.open(filename)
            shelve_file_2.clear()
            exported_team_id_table = []
            exported_team_desc_table = []
            exported_league_filename = filename
            exported_dict = {}
            exported_dict["settings"] = {}
            for team in team_table:
                exported_team_id_table.append(team.team_id)
                exported_team_desc_table.append(team.team_desc)
            for key, value in zip(list(shelve_file_1.keys()), list(shelve_file_1.values())):
                exported_dict[key] = value
            exported_dict["settings"]["team_id_table"] = exported_team_id_table
            exported_dict["settings"]["team_desc_table"] = exported_team_desc_table
            exported_dict["settings"]["LEAGUE_FILENAME"] = filename
            if "fixtures" in exported_dict:
                exported_dict.pop("fixtures")
            if "predictions" in exported_dict:
                exported_dict.pop("predictions")
            if "results" in exported_dict:
                exported_dict.pop("results")
            for key, value in zip(list(exported_dict.keys()), list(exported_dict.values())):
                shelve_file_2[key] = value
            do_message(f"League saved as {filename}.")
            print(f"League saved as {filename} | {shelve_file_2['settings']['LEAGUE_FILENAME']}.")
            shelve_file_1.close()
            shelve_file_2.close()
        f = asksaveasfilename(initialdir = os.getcwd())
        if f is None or f == '': # asksaveasfile return `None` if dialog closed with cancel or X.
            return
        save_table_as_league(f)
        return
    save_button = ttk.Button(win, text="Save as league", command=lambda: prompt_save_table_as_league())
    save_button.grid(row = 1, column = 2)
    return
"""
    def send_settings():
        global settings
        new_settings = {}
        box_values = []
        for i_box, box in enumerate(display_values):
            box_values.append(get_box_value(box, option_types[i_box]))
        for i_var, var in enumerate(option_vars):
            if option_types[i_var] == "number":
                new_settings[var] = float(box_values[i_var])
            if option_types[i_var] == "yn":
                new_settings[var] = bool(box_values[i_var])
        settings = settings_instance.update_settings(new_settings)
        win.destroy()
        return
"""
def players_menu():
    global settings
    win = Toplevel()
    win.wm_title("Players")
    lb_player = Listbox(win, width = 84, height = 10)
    lb_player.grid(row = 0, column = 2)
    
    def update_table():
        global settings
        lb_player.delete(0, lb_player.size())
        for i_p, p in enumerate(settings["players"]):
            lb_player.insert(i_p, p)
    
    update_table()
    
    def add_player():
        win_add = Toplevel()
        win_add.wm_title("Player list")
        player_label = Label(win_add, text="Name of player")
        player_label.grid(row = 0, column = 0)
        player_name_box = Text(win_add, height=1, width=50)
        player_name_box.grid(row = 1, column = 0)
        def create_player():
            global settings
            text_box = player_name_box.get("1.0",END)[:-1]
            if text_box == "\n":
                do_message("Please enter a player name")
            else:
                new_settings = {}
                new_player_name = text_box
                new_player_list = settings["players"]
                new_player_list.append(new_player_name)
                new_settings["players"] = new_player_list
                settings = settings_instance.update_settings(new_settings)
                old_predictions = try_open_data("predictions", settings["LEAGUE_FILENAME"])
                if isinstance(old_predictions, int):
                    settings_instance.save_settings()
                    update_table()
                    win_add.destroy()
                    return
                blank_player_predictions = np.zeros((1, settings["NUMBER_OF_ROUNDS"], settings["MAX_NUMBER_OF_MATCHES_PER_ROUND"], 4), dtype="<U32")
                new_predictions = np.concatenate((old_predictions, blank_player_predictions), axis=0)
                league_file = shelve.open(settings["LEAGUE_FILENAME"])
                league_file["predictions"] = new_predictions
                league_file.close()
                settings_instance.save_settings()
                update_table()
                win_add.destroy()
            return   
        add_button = ttk.Button(win_add, text="Add", command=lambda: create_player())
        add_button.grid(row = 2, column = 0)
    add_menu_button = ttk.Button(win, text="Add player", command=lambda: add_player())
    add_menu_button.grid(row = 0, column = 0)
    def confirm_remove_player():
        global settings
        def remove_player(index):
            global settings
            selection = lb_player.curselection()
            if selection == ():
                do_message("Please select a player first.")
            else:
                selected_player_index = selection[0]
                new_settings = {}
                player_list = settings["players"]
                new_player_list = player_list
                new_player_list.pop(selected_player_index)
                new_settings["players"] = new_player_list
                settings = settings_instance.update_settings(new_settings)
                old_predictions = try_open_data("predictions", settings["LEAGUE_FILENAME"])
                if isinstance(old_predictions, int):
                    settings_instance.save_settings()
                    update_table()
                    return
                new_predictions = np.delete(old_predictions, selected_player_index, 0)
                league_file = shelve.open(settings["LEAGUE_FILENAME"])
                league_file["predictions"] = new_predictions
                league_file.close()
                settings_instance.save_settings()
                update_table()
        selected_player_index = lb_player.curselection()[0]
        warning_win = Toplevel()
        warning_win.wm_title("Warning")
        current_player = settings["players"][selected_player_index]
        msg = Label(warning_win, text=f"You are about to remove the player '{current_player}' from the game, which will permanently erase ALL of their points and predictions. Are you sure?")
        msg.grid(row=0, column=0)
        ok_button = ttk.Button(warning_win, text="Remove", command=((lambda : do_nothing()) and (lambda: remove_player(selected_player_index))))
        ok_button.grid(row=1, column=0)
        cancel_button = ttk.Button(warning_win, text="Cancel", command=lambda : warning_win.destroy())
        cancel_button.grid(row=2, column=0)
    remove_button = ttk.Button(win, text="Remove selected player", command=lambda: confirm_remove_player())
    remove_button.grid(row = 0, column = 3)
    def edit_player():
        if lb_player.curselection() == ():
            do_message("Select a player first.")
            return
        win_edit = Toplevel()
        win_edit.wm_title("Edit selected player")
        selected_player_index = lb_player.curselection()[0] # If multiple selected just do the first one
        selected_player = settings["players"][selected_player_index]
        team_label = Label(win_edit, text=f"Name of player (Selected player: {selected_player})")
        team_label.grid(row = 0, column = 0)
        team_name_box = Text(win_edit, height=1, width=50)
        team_name_box.insert("1.0", selected_player)
        team_name_box.grid(row = 1, column = 0)
        def confirm_edit_player():
            new_settings_dict = {}
            text_box = team_name_box.get("1.0",END)[:-1]
            if text_box == "\n":
                do_message("Please enter a player name")
            else:
                old_players = settings["players"]
                new_players = old_players
                new_players[selected_player_index] = text_box
                new_settings_dict["players"] = new_players
                settings_instance.update_settings(new_settings_dict)
                settings_instance.save_settings()
                update_table()
                win_edit.destroy()
            return   
        confirm_button = ttk.Button(win_edit, text="Confirm", command=(lambda: confirm_edit_player()))
        confirm_button.grid(row = 2, column = 0)
    edit_button = ttk.Button(win, text="Change player name", command=lambda: edit_player())
    edit_button.grid(row = 1, column = 0)
    return
def derby_settings_menu():
    win = Toplevel()
    win.wm_title("Derbies")
    lb_derby = Listbox(win, width = 84, height = 10)
    lb_derby.grid(row=0, column = 1)
    def update_derby_table():
        global settings
        lb_derby.delete(0, lb_derby.size())
        for i_p, p in enumerate(settings["derby_factor_pairs"]):
            formatted_string = (get_team_instance_from_id(p[0]).team_desc) + " vs " + (get_team_instance_from_id(p[1]).team_desc)
            lb_derby.insert(i_p, formatted_string)
            
    update_derby_table()
    
    def add_derby_fixture():
        win_add = Toplevel()
        win_add.wm_title("Add derby fixture...")
        
        
        team_1_input = ttk.Combobox(win_add, state="readonly")
        team_1_input["values"] = settings["team_desc_table"]
        team_1_input.grid(row=1,column=0)
        
        space = Label(win_add, anchor="c", text="vs")
        space.grid(row=1, column=1)
        
        team_2_input = ttk.Combobox(win_add, state="readonly")
        team_2_input["values"] = settings["team_desc_table"]
        team_2_input.grid(row=1,column=2)

        def save_derby_fixture():
            global settings
            team_1_desc = team_1_input.get()
            team_2_desc = team_2_input.get()
            team_1_id = get_team_instance_from_id(team_1_desc).team_id
            team_2_id = get_team_instance_from_id(team_2_desc).team_id
            settings["derby_factor_pairs"].append([team_1_id, team_2_id])
            settings_instance.save_settings(True)
            update_derby_table()
            return
        add_button = ttk.Button(win_add, text="Confirm", command=(lambda: save_derby_fixture()))
        add_button.grid(row = 2, column = 1)
        return
    add_button = ttk.Button(win, text="Add", command=(lambda: add_derby_fixture()))
    add_button.grid(row = 2, column = 0)
    def remove_selected_derby_fixture():
        fixture_index = lb_derby.curselection()
        if len(fixture_index) >= 1:
            fixture_index = fixture_index[0]
        else:
            do_message("You must select a fixture first.")
            return
        settings["derby_factor_pairs"].pop(fixture_index)
        settings_instance.save_settings(True)
        update_derby_table()
        return
    remove_button = ttk.Button(win, text="Remove selected", command=(lambda: remove_selected_derby_fixture()))
    remove_button.grid(row = 2, column = 1)
    def edit_derby_fixture():
        win_edit = Toplevel()
        win_edit.wm_title("Edit derby fixture...")
        
        fixture_index = lb_derby.curselection()
        if len(fixture_index) >= 1:
            fixture_index = fixture_index[0]
        else:
            do_message("You must select a fixture first.")
            return
        
        team_1_input = ttk.Combobox(win_edit, state="readonly")
        team_1_input["values"] = settings["team_desc_table"]
        team_1_input.current(team_1_input["values"].index(get_team_instance_from_id(settings["derby_factor_pairs"][fixture_index][0]).team_desc))
        team_1_input.grid(row=1,column=0)
        
        space = Label(win_edit, anchor="c", text="vs")
        space.grid(row=1, column=1)
        
        team_2_input = ttk.Combobox(win_edit, state="readonly")
        team_2_input["values"] = settings["team_desc_table"]
        team_2_input.current(team_2_input["values"].index(get_team_instance_from_id(settings["derby_factor_pairs"][fixture_index][1]).team_desc))
        team_2_input.grid(row=1,column=2)

        def save_edited_derby_fixture():
            global settings
            team_1_desc = team_1_input.get()
            team_2_desc = team_2_input.get()
            team_1_id = get_team_instance_from_id(team_1_desc).team_id
            team_2_id = get_team_instance_from_id(team_2_desc).team_id
            settings["derby_factor_pairs"][fixture_index] = [team_1_id, team_2_id]
            settings_instance.save_settings(True)
            update_derby_table()
            win_edit.destroy()
            return
        confirm_edit_button = ttk.Button(win_edit, text="Confirm", command=(lambda: save_edited_derby_fixture()))
        confirm_edit_button.grid(row = 2, column = 1)
        return
    edit_button = ttk.Button(win, text="Edit selected", command=(lambda: edit_derby_fixture()))
    edit_button.grid(row = 2, column = 2)
    return
update_table(team_stack)
m.title('RL Prediction League')
menu = Menu(m)
m.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
#filemenu.add_command(label='Refresh League', command=lambda:prompt_refresh_league())
filemenu.add_command(label='Import League', command=lambda:prompt_import_league())
filemenu.add_command(label='Save League settings', command=lambda:option_save_settings())
filemenu.add_command(label='Save League as...', command=lambda:prompt_save_league_as())

viewmenu = Menu(menu)
menu.add_cascade(label='View', menu=viewmenu)
viewmenu.add_command(label='View Fixtures', command=lambda:view_fixtures())
viewmenu.add_command(label='View Predictions', command=lambda:view_predictions())
viewmenu.add_command(label='View Results', command=lambda:view_results())
viewmenu.add_command(label='Refresh Table', command=lambda:ui_render_league_box(lb1))

leaguemenu = Menu(menu)
menu.add_cascade(label='League', menu=leaguemenu)
leaguemenu.add_command(label='Set Round', command=lambda:prompt_set_round())
leaguemenu.add_command(label='Add Fixtures', command=lambda:prompt_add_round_fixtures())
leaguemenu.add_command(label='Add Round Results', command=lambda:prompt_add_round_results())
leaguemenu.add_command(label='Add Round Predictions', command=lambda:prompt_add_prediction())

scoremenu = Menu(menu)
menu.add_cascade(label='Scoring', menu=scoremenu)
scoremenu.add_command(label='Show player scores', command=lambda:show_player_scores())
scoremenu.add_command(label='Show player scores for this round', command=lambda:show_player_scores_at_round())

optionsmenu = Menu(menu)
menu.add_cascade(label='Options', menu=optionsmenu)
optionsmenu.add_command(label='League settings', command=lambda:league_settings_menu())
optionsmenu.add_command(label='Scoring settings', command=lambda:scoring_settings_menu())
optionsmenu.add_command(label='Manage derby fixtures', command=lambda:derby_settings_menu())

teamsmenu = Menu(menu)
menu.add_cascade(label='Teams', menu=teamsmenu)
teamsmenu.add_command(label='Create new team set', command=lambda:create_team_set_menu())

playersmenu = Menu(menu)
menu.add_cascade(label='Players', menu=playersmenu)
playersmenu.add_command(label="Manage players", command = lambda:players_menu())

ui_render_league_box(lb1)
m.mainloop()
