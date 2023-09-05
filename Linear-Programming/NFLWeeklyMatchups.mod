set CONFERENCES;
set DIVISION{CONFERENCES};
set DIVISIONS := union{i in CONFERENCES} DIVISION[i];
set TEAM{DIVISIONS};
set TEAMS := union{d in DIVISIONS} TEAM[d];

set WEEKS ordered;

param matchups{TEAMS, TEAMS};
param expectedWins{TEAMS};

var wMatchups{ht in TEAMS, at in TEAMS, WEEKS: ht != at and matchups[ht, at] > 0} binary;

#we want good matchups every week so we would like to minimize the difference in total expected wins across every week (add one to the home team since playing at home offers slight advantage)
minimize parity{w in WEEKS}: sum{ht in TEAMS, at in TEAMS: ht != at and matchups[ht, at] > 0}wMatchups[ht, at, w]*abs(expectedWins[ht]+1-expectedWins[at]);

#every team can only play 1 week
s.t. weeklyConstraints{ht in TEAMS, w in WEEKS}: 0 <= sum{at in TEAMS: ht != at and matchups[ht, at] >0}(wMatchups[ht, at, w] + wMatchups[at, ht, w]) <= 1;

#schedule every matchup
s.t. fulfillMatchupsConstraint{ht in TEAMS, at in TEAMS: ht != at and matchups[ht,at] > 0}: sum{w in WEEKS}(wMatchups[ht, at, w] + wMatchups[at, ht, w]) = matchups[ht, at];

#Only allow bye weeks on weeks 6 through 14
#s.t. byeWeekConstraint{ht in TEAMS, w in WEEKS}: 6<= sum{at in TEAMS: ht != at and matchups[ht, at] > 0} (abs(wMatchups[ht, at, w]/*+wMatchups[at, ht, w]*/ - 1)*w + abs(wMatchups[ht, at,w] /*+ wMatchups[at,ht,w]*/)*8) <= 14 ;
s.t. byeWeekConstraint{ht in TEAMS, w in WEEKS: w < 6 or w > 14}: sum{at in TEAMS: ht != at and matchups[ht, at] >0}(wMatchups[ht, at, w] + wMatchups[at, ht, w]) = 1;

#Prevent two concurrent away games
s.t. no_three_away_games_in_a_row{at in TEAMS, w in WEEKS: w <= 16}:sum{ht in TEAMS: ht != at and matchups[ht, at] > 0}(wMatchups[ht, at, w] + wMatchups[ht, at, w+1] + wMatchups[ht, at, w+2] ) <= 2;

#Restrict each team to at most 9 home/away games
s.t. homeGameConstraint{ht in TEAMS}:  8 <= sum{at in TEAMS, w in WEEKS: ht != at and matchups[ht, at] > 0}wMatchups[ht, at, w] <= 9;

#Force one home and one away within the division
s.t. divisionalHomeAndAway{d in DIVISIONS, ht in TEAM[d], at in TEAM[d]: ht != at}: sum{w in WEEKS} wMatchups[ht,at,w] <=1;

#Force 6 home games within the conference
s.t. sixHomeConfGames{c in CONFERENCES, d1 in DIVISION[c], ht in TEAM[d1]}: sum{d2 in DIVISION[c], at in TEAM[d2], w in WEEKS:ht != at and d1 != d2 and matchups[ht, at] > 0} wMatchups[ht, at, w] = 3;
#s.t. 2DivisionalMatchupHomeGames{d1 in DIVISION['NFC'], d2 in DIVISION['NFC'], ht in TEAM[d1], at in TEAM[d2]

data;

set CONFERENCES := NFC, AFC;

set DIVISION[NFC] := NNORTH, NSOUTH, NEAST, NWEST;
set DIVISION[AFC] := ANORTH, ASOUTH, AEAST, AWEST;

set TEAM[NNORTH] := CHI, GB, DET, MIN;
set TEAM[NSOUTH] := NO, TB, ATL, CAR;
set TEAM[NEAST] := DAL, PHI, WAS, NYG;
set TEAM[NWEST] := LAR, SEA, SF, ARI;

set TEAM[ANORTH] := CIN, CLE, BAL, PIT;
set TEAM[ASOUTH] := HOU, TEN, IND, JAX;
set TEAM[AEAST] := BUF, NE, NYJ, MIA;
set TEAM[AWEST] := KC, LAC, DEN, LV;

set WEEKS := 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18;

param expectedWins :=
ARI 5.5
ATL 8.5
BAL 9.5
BUF 10.5
CAR 7.5
CHI 7.5
CIN 11.5
CLE 9.5
DAL 9.5
DEN 8.5
DET 9.5
GB 7.5
HOU 5.5
IND 6.5
JAX 10.5
KC 11.5
LAC 9.5
LAR 7.5
LV 7.5
MIA 9.5
MIN 8.5
NE 7.5
NO 9.5
NYG 8.5
NYJ 9.5
PHI 10.5
PIT 8.5
SEA 8.5
SF 11.5
TB 6.5
TEN 7.5
WAS 7.5
; 

param matchups
:   ARI ATL BAL BUF CAR CHI CIN CLE DAL DEN DET  GB HOU IND JAX  KC LAC LAR  LV :=
ARI   .   0   0   1   0   1   0   0   1   0   0   0   1   0   0   0   0   2   0
ATL   0   .   0   0   2   1   0   0   0   1   1   1   1   1   1   0   0   0   0
BAL   0   0   .   0   0   0   2   2   1   0   1   0   1   1   1   0   1   0   0
BUF   1   0   0   .   0   0   1   0   0   1   0   0   0   0   1   1   1   1   1
CAR   0   2   0   0   .   1   0   0   0   0   1   1   1   1   1   0   0   1   0
CHI   1   1   0   0   1   .   0   0   0   1   2   2   0   1   0   1   1   0   0
CIN   0   0   2   1   0   0   .   2   1   0   0   0   1   1   1   1   0   0   0
CLE   0   0   2   0   0   0   2   .   0   0   1   0   1   1   1   0   1   0   0
DAL   1   0   1   0   0   0   1   0   .   0   0   0   0   0   0   0   1   1   0
DEN   0   1   0   1   0   1   0   0   0   .   0   1   1   1   0   2   2   0   2
DET   0   1   1   0   1   2   0   1   0   0   .   2   0   0   0   1   1   0   0
GB    0   1   0   0   1   2   0   0   0   1   2   .   0   0   0   1   1   1   1
HOU   1   1   1   0   1   0   1   1   0   1   0   0   .   2   2   0   0   0   1
IND   0   1   1   0   1   1   1   1   0   1   0   0   2   .   2   0   0   0   0
JAX   0   1   1   1   1   0   1   1   0   0   0   0   2   2   .   1   0   0   0
KC    0   0   0   1   0   1   1   0   0   2   1   1   0   0   1   .   2   0   2
LAC   0   0   1   1   0   1   0   1   1   2   1   1   0   0   0   2   .   0   2
LAR   2   0   0   1   1   0   0   0   1   0   0   1   0   0   0   0   0   .   1
LV    0   0   0   1   0   0   0   0   0   2   0   1   1   0   0   2   2   1   .
MIA   1   0   0   2   0   0   0   1   1   1   0   0   0   0   0   1   1   1   1
MIN   0   1   0   0   1   2   0   0   1   1   2   2   0   0   0   1   1   0   1
NE    1   0   0   2   1   1   0   0   0   1   0   0   0   1   0   1   1   0   1
NO    0   2   1   0   2   1   0   1   1   0   1   1   1   1   1   0   0   0   0
NYG   1   1   1   0   0   0   1   1   2   1   0   1   0   0   0   0   0   1   0
NYJ   1   0   1   2   0   0   0   0   1   1   1   0   0   0   0   1   1   1   1
PHI   1   0   0   1   0   0   1   1   2   0   1   0   0   0   1   0   0   1   0
PIT   0   1   2   0   0   0   2   2   0   0   0   0   1   1   1   0   0   0   0
SEA   2   1   0   1   0   0   0   0   1   0   0   0   0   0   0   0   0   2   0
SF    2   0   0   1   0   0   1   0   1   0   1   0   0   0   0   1   0   2   0
TB    1   2   0   0   2   1   0   0   0   0   1   1   1   1   1   0   0   0   1
TEN   0   0   1   0   1   0   1   1   0   0   0   1   2   2   2   0   0   1   1
WAS   1   0   1   0   1   1   1   1   2   0   0   0   0   0   0   0   0   1   1

:   MIA MIN  NE  NO NYG NYJ PHI PIT SEA  SF  TB TEN WAS    :=
ARI   1   0   1   0   1   1   1   0   2   2   1   0   1
ATL   0   1   0   2   1   0   0   1   1   0   2   0   0
BAL   0   0   0   1   1   1   0   2   0   0   0   1   1
BUF   2   0   2   0   0   2   1   0   1   1   0   0   0
CAR   0   1   1   2   0   0   0   0   0   0   2   1   1
CHI   0   2   1   1   0   0   0   0   0   0   1   0   1
CIN   0   0   0   0   1   0   1   2   0   1   0   1   1
CLE   1   0   0   1   1   0   1   2   0   0   0   1   1
DAL   1   1   0   1   2   1   2   0   1   1   0   0   2
DEN   1   1   1   0   1   1   0   0   0   0   0   0   0
DET   0   2   0   1   0   1   1   0   0   1   1   0   0
GB    0   2   0   1   1   0   0   0   0   0   1   1   0
HOU   0   0   0   1   0   0   0   1   0   0   1   2   0
IND   0   0   1   1   0   0   0   1   0   0   1   2   0
JAX   0   0   0   1   0   0   1   1   0   0   1   2   0
KC    1   1   1   0   0   1   0   0   0   1   0   0   0
LAC   1   1   1   0   0   1   0   0   0   0   0   0   0
LAR   1   0   0   0   1   1   1   0   2   2   0   1   1
LV    1   1   1   0   0   1   0   0   0   0   1   1   1
MIA   .   0   2   0   0   2   0   1   1   1   0   0   0
MIN   0   .   0   1   0   0   1   1   0   0   1   0   0
NE    2   0   .   0   0   2   0   0   1   1   0   1   0
NO    0   1   0   .   0   0   0   0   0   1   2   0   0
NYG   0   0   0   0   .   0   2   1   1   1   0   0   2
NYJ   2   0   2   0   0   .   0   1   1   0   0   0   0
PHI   0   1   0   0   2   0   .   1   1   1   0   0   2
PIT   1   1   0   0   1   1   1   .   1   0   0   1   0
SEA   1   0   1   0   1   1   1   1   .   2   1   0   1
SF    1   0   1   1   1   0   1   0   2   .   0   0   1
TB    0   1   0   2   0   0   0   0   1   0   .   1   0
TEN   0   0   1   0   0   0   0   1   0   0   1   .   1
WAS   0   0   0   0   2   0   2   0   1   1   0   1   .
;

