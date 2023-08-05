import os
from PIL import Image, ImageDraw
from colorthief import ColorThief



class NbaBattle:
    TeamAbb = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MIA', 'MIL', 'MIN',
               'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET', 'CHA']

    def __init__(self, teamA, teamB):
        self.teamA = self._is_valid_team(teamA)
        self.teamB = self._is_valid_team(teamB)

    def _is_valid_team(self, team):
        if team not in self.TeamAbb:
            raise ValueError("Team's abbreviation is wrong.")
        return team

    def home_team_logo(self):
        return self.generate_team_picture(self.teamA)

    def guest_team_logo(self):
        return self.generate_team_picture(self.teamB)

    def generate_team_picture(self, team):
        dirname = os.path.dirname(__file__)
        logo_path = os.path.join(dirname, f"./teams/{team}.png")
        team_logo = Image.open(logo_path)
        w, h = team_logo.size
        w_s = int(w/1.3)
        w_h = int(h/1.3)
        team_logo = team_logo.resize((w_s, w_h), Image.ANTIALIAS)
        color_thief = ColorThief(logo_path)
        color_code =  color_thief.get_color(quality=1)
        background_image = Image.new("RGB", (285, 400), color_code)
        team_logo = team_logo.convert("RGBA")
        background_image = background_image.convert("RGBA")
        width = (background_image.width - team_logo.width) // 2
        height = (background_image.height - team_logo.height) // 2
        background_image.paste(team_logo, (width, height), team_logo)
        return {
            "image" : background_image,
            "rgb" : color_code,
        }

    def create_battle_image(self):
        teamA = self.home_team_logo()["image"]
        teamA_color = self.home_team_logo()["rgb"]
        teamB = self.guest_team_logo()["image"]
        teamB_color = self.guest_team_logo()["rgb"]
        teamA_size = teamA.size
        battle_image = Image.new('RGB',(2*teamA_size[0] + 30, teamA_size[1]), (250,250,250))
        battle_image.paste(teamA,(0,0))
        battle_image.paste(teamB,(teamA_size[0] + 30,0))
        draw = ImageDraw.Draw(battle_image)
        draw.polygon([(teamA_size[0], 0), (teamA_size[0] + 29, 0), (teamA_size[0], teamA_size[1])], teamA_color)
        draw.polygon([(teamA_size[0], teamA_size[1]), (teamA_size[0] + 29, teamA_size[1]), (teamA_size[0] + 29, 0)], teamB_color)
        return battle_image

