import tabs as tb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
test_data = ROOT / "datasets" / "test_data.csv"
null_data = ROOT / "datasets" / "null.csv"
dota_data = ROOT / "datasets" / "dota_data.csv"
mine_data = ROOT / "datasets" / "minecraft.csv"

minecraft_teams = tb.load_csv(mine_data, autotyping=False) # изначально значения записаны через ","
minecraft_teams.print_table()                                     # дальше мы их по приколу запишем через ";"
print(minecraft_teams.types) # все значения - строки

tb.save_csv(minecraft_teams, "team", "saved_test_files/", 7, delimiter=";")

print("\n", "="*100, "\n", "="*100, "\n")

saved_files = ROOT / "tests" / "saved_test_files"
team2 = saved_files / "team_2.csv"
team3 = saved_files / "team_3.csv"

teams_without_team1 = tb.load_csv(team2, team3, delimiter=";") # соединяем две команды
teams_without_team1.print_table()
print(teams_without_team1.types) # разные типы столбцов в зависимости от значений в них