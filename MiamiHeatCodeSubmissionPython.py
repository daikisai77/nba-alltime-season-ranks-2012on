import pandas as pd
import numpy as np

#Loading the Dataset
player_stat_path = r"C:\Users\dsai3\Downloads\archive\PlayerStatistics.csv"
ps_df = pd.read_csv(player_stat_path)
ps_df['gameDate'] = pd.to_datetime(ps_df['gameDate'], errors = 'coerce')
print(ps_df.shape)
#print(ps_df.head())
#print(ps_df.info)

#Cleaning up irrelevant data
ps_df = ps_df[(ps_df['gameDate'] >= '2010-10-03') & (ps_df['gameType'] == 'Regular Season')]
print(ps_df.shape)
#print(ps_df.head())

#Making a new column for the specific season
season = np.where(ps_df['gameDate'].dt.month >= 10, ps_df['gameDate'].dt.year, ps_df['gameDate'].dt.year - 1)
ps_df['Season'] = season
print(ps_df.shape)
print(ps_df.sample(10))

from scipy.stats import zscore
#Making a new Dataframe that looks at stats per player per season
season_totals_df = (ps_df.groupby(['Season', 'personId'], as_index = False).agg({
    "gameId" : "nunique",
    "numMinutes":"sum",
    "points":"sum",
    "assists":"sum",
    "reboundsDefensive":"sum",
    "reboundsOffensive":"sum",
    "reboundsTotal":"sum",
    "blocks":"sum",
    "steals":"sum",
    "fieldGoalsAttempted":"sum",
    "fieldGoalsMade":"sum",
    "threePointersAttempted":"sum",
    "threePointersMade":"sum",
    "freeThrowsAttempted":"sum",
    "freeThrowsMade":"sum",
    "foulsPersonal":"sum",
    "turnovers":"sum",
    "plusMinusPoints":"sum"})
            )    
season_totals_df = season_totals_df.rename(columns = {"gameId" : "GP"})

#To get the names of each player I will now merge this data with the players file
player_path = r"C:\Users\dsai3\Downloads\archive\Players.csv"
p_df = pd.read_csv(player_path)

season_totals_with_names_df = season_totals_df.merge(
    p_df[["personId", "firstName", "lastName"]],
    on = "personId",
    how = "left"
)
#print(season_totals_with_names_df)

#Now I will make a season average dataframe
season_avg_df = season_totals_with_names_df.copy()
stats_columns = [s for s in season_totals_with_names_df.columns if s not in ['Season', 'personId', 'firstName', 'lastName', 'GP', 'plusMinusPoints']]
for s in stats_columns:
    season_avg_df[f"{s}_per_game"] = season_avg_df[s] / season_avg_df['GP']
season_avg_df["fieldGoals_percentage_per_game"] = season_avg_df["fieldGoalsMade_per_game"] / season_avg_df["fieldGoalsAttempted_per_game"]
season_avg_df["threePointers_percentage_per_game"] = season_avg_df["threePointersMade_per_game"] / season_avg_df["threePointersAttempted_per_game"]
season_avg_df["freeThrows_percentage_per_game"] = season_avg_df["freeThrowsMade_per_game"] / season_avg_df["freeThrowsAttempted_per_game"]

#Creating a ranking metric
season_avg_df["PM_per_min"] = season_avg_df['plusMinusPoints']/season_avg_df['numMinutes']
season_avg_df["PM_per_game"] = season_avg_df['plusMinusPoints']/season_avg_df['GP']
season_avg_df["PM_per_36"] = season_avg_df["PM_per_min"]*36
season_avg_df['Impact_Score'] = (
    season_avg_df['points_per_game']
    + season_avg_df['assists_per_game']
    + season_avg_df['reboundsTotal_per_game'] * 0.7
    + season_avg_df['blocks_per_game']
    + season_avg_df['steals_per_game']
    - season_avg_df['turnovers_per_game']
)


#Reordering some colums
id_cols = ['Season', 'personId', 'firstName', 'lastName', 'GP']
other_cols = [c for c in season_avg_df.columns if c not in id_cols]
season_avg_df = season_avg_df[id_cols + other_cols]
#print(season_avg_df.head())
print(len(season_avg_df))

season_avg_500 = season_avg_df[season_avg_df['numMinutes'] >= 500].reset_index(drop = True)

#Combining the metrics for one cohesive metric
season_avg_500["Impact_Score_z"] = zscore(season_avg_500["Impact_Score"])
season_avg_500["PM_per_36_z"] = zscore(season_avg_500["PM_per_36"])
season_avg_500["CombinedScore"] = (
    0.55 * season_avg_500["Impact_Score_z"] + 0.45 * season_avg_500["PM_per_36_z"]
)
print(len(season_avg_500))
with pd.option_context("display.max_columns", None):
    print(season_avg_500.sample(10))
#Plus Minus Results
#Best
best = season_avg_500.sort_values("PM_per_36", ascending=False).head(10)
print('Best PM per 36')
print(best[["personId","firstName", "lastName", "Season","PM_per_36"]])

#Worst
print('Worst PM per 36')
worst = season_avg_500.sort_values("PM_per_36", ascending=True).head(10)
print(worst[["personId","firstName", "lastName", "Season","PM_per_36"]])

#Average
print('Average PM per 36')
sorted_avg = season_avg_500.sort_values("PM_per_36", ascending=True)
n = len(sorted_avg)
middle_start = n//2 - 5
middle_end = n//2 + 5
middle_10 = sorted_avg.iloc[middle_start:middle_end]

print(middle_10[["personId","firstName", "lastName","Season","PM_per_36"]])

print('------------------------------------------------------------------------')
#Impact Results
#Best
best = season_avg_500.sort_values('Impact_Score', ascending=False).head(10)
print('Best Impact')
print(best[["personId","firstName", "lastName", "Season","Impact_Score"]])

#Worst
print('Worst Impact')
worst = season_avg_500.sort_values('Impact_Score', ascending=True).head(10)
print(worst[["personId","firstName", "lastName", "Season","Impact_Score"]])

#Average
print('Average Impact')
sorted_avg = season_avg_500.sort_values('Impact_Score', ascending=True)
n = len(sorted_avg)
middle_start = n//2 - 5
middle_end = n//2 + 5
middle_10 = sorted_avg.iloc[middle_start:middle_end]
print(middle_10[["personId","firstName", "lastName","Season","Impact_Score"]])

print('------------------------------------------------------------------------')
#Combined Results
#Best
best = season_avg_500.sort_values('CombinedScore', ascending=False).head(10)
print('Best Combined')
print(best[["personId","firstName", "lastName", "Season","CombinedScore"]])

#Worst
print('Worst Combined')
worst = season_avg_500.sort_values('CombinedScore', ascending=True).head(10)
print(worst[["personId","firstName", "lastName", "Season","CombinedScore"]])

#Average
print('Average Combined')
sorted_avg = season_avg_500.sort_values('CombinedScore', ascending=True)
n = len(sorted_avg)
middle_start = n//2 - 5
middle_end = n//2 + 5
middle_10 = sorted_avg.iloc[middle_start:middle_end]
print(middle_10[["personId","firstName", "lastName","Season","CombinedScore"]])
