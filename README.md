# nba-alltime-season-ranks-2012on
Ranking the greatest NBA seasons since 2012 using a transparent “combined score” that blends impact, efficiency, team context, and availability. Reproducible Python pipeline with data cleaning, feature engineering, and weights you can tweak.

# Greatest NBA Seasons Since 2012 (Custom Ranking)

This project ranks the greatest NBA seasons since 2012 using a **Combined Score** built from two complementary measures:  
1. **Impact Score (box score–based)**  
2. **Per-36 Plus/Minus (team impact–based)**  

By blending these two perspectives, the rankings highlight which players had the strongest balance of individual production and on-court team impact.

---

## Methodology

1. **Aggregate game logs**  
   - Used `PlayerStatistics` raw game logs.  
   - Aggregated to season-level stats for each player (minutes, games played, points, assists, rebounds, blocks, steals, turnovers, plus/minus).  

2. **Derive season averages**  
   - Calculated per-game stats (PPG, APG, RPG, BPG, SPG, TOVPG).  

3. **Create custom metrics**  
   - **Per-36 Plus/Minus** = `(season plus/minus ÷ total minutes) × 36`.  
     - Normalizes players with different playing times.  
   - **Impact Score** = `PPG + APG + (RPG × 0.7) + BPG + SPG – TOVPG`.  
     - Captures individual box score contributions while penalizing turnovers.  

4. **Combine into one score**  
   - Standardized both metrics (z-scores).  
   - Applied weights:  
     - **0.55 × Impact Score**  
     - **0.45 × Plus/Minus Score**  
   - Ensures fairness so neither metric dominates due to raw value differences.  

5. **Rankings**  
   - Players with ≥500 minutes qualified.  
   - Grouped into:  
     - **Top 10 best seasons**  
     - **10 most “average” seasons** (closest to league mean)  
     - **Bottom 10 worst seasons**

---

## Why This Approach?

- **Box score stats alone** (e.g., triple-doubles from Westbrook, Jokic, Harden) can exaggerate individual impact while ignoring team outcomes.  
- **Plus/minus alone** can reward role players in limited minutes (e.g., JaVale McGee).  
- By combining both, this ranking balances **individual dominance** with **team impact**.  

---

## Results

### 🏆 Best 10 Seasons
1. Giannis Antetokounmpo (2019–2020)  
2. Nikola Jokic (2024–2025)  
3. Shai Gilgeous-Alexander (2024–2025)  
4. Stephen Curry (2015–2016)  
5. Nikola Jokic (2022–2023)  
6. Nikola Jokic (2023–2024)  
7. Luka Doncic (2023–2024)  
8. Joel Embiid (2023–2024)  
9. Stephen Curry (2016–2017)  
10. James Harden (2018–2019)  

### ⚖️ Most Average 10 Seasons
1. Michael Kidd-Gilchrist (2017–2018)  
2. Georges Niang (2022–2023)  
3. Davion Mitchell (2024–2025)  
4. Ish Smith (2019–2020)  
5. Allen Crabbe (2018–2019)  
6. Shane Battier (2013–2014)  
7. Jerami Grant (2023–2024)  
8. Jaxson Hayes (2024–2025)  
9. Derek Fisher (2012–2013)  
10. Dwight Powell (2020–2021)  

### ❌ Worst 10 Seasons
1. Greg Brown III (2021–2022)  
2. Kevin Seraphin (2010–2011)  
3. Keon Johnson (2021–2022)  
4. Ignas Brazdeikis (2021–2022)  
5. DeAndre Liggins (2017–2018)  
6. Dennis Schröder (2013–2014)  
7. Earl Clark (2011–2012)  
8. Timothe Luwawu-Cabarrot (2018–2019)  
9. John Lucas III (2013–2014)  
10. Stephen Graham (2010–2011)  
