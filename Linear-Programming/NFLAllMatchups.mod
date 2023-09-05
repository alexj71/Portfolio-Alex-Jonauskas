set CONFERENCES;
set DIVISION{CONFERENCES};
set DIVISIONS := union{i in CONFERENCES} DIVISION[i];

set TEAM{DIVISIONS};
set TEAMS := union{d in DIVISIONS} TEAM[d];

param DivMatchups{DIVISIONS, DIVISIONS};
param TeamDivMatchups{i in TEAMS, j in TEAMS} := 
if (exists {d1 in DIVISIONS, d2 in DIVISIONS} DivMatchups[d1, d2]==1 and i in TEAM[d1] and j in TEAM[d2]) 
		or (exists {d in DIVISIONS} i in TEAM[d] and j in TEAM[d] and i != j)
then 1 else 0; 
param expectedWins{TEAMS};

var matchups{i in TEAMS, j in TEAMS : i != j /*and TeamDivMatchups[i,j] = 0*/} >= 0, <=2;

minimize blowouts: sum{t1 in TEAMS, t2 in TEAMS: t1 != t2 and TeamDivMatchups[t1,t2] = 0}matchups[t1, t2] * abs(expectedWins[t1] - expectedWins[t2]);

#Force symmetry (if bears plays the packers then the packers must play the bears)
subject to symmetricConstraints{t1 in TEAMS, t2 in TEAMS: t1 != t2 /*and TeamDivMatchups[t1,t2] = 0*/}: matchups[t1, t2] = matchups[t2, t1];

#each team plays 17 games
subject to 17GamesConstraints{t1 in TEAMS}: sum{t2 in TEAMS: t1 != t2 /*and TeamDivMatchups[t1, t2] = 0*/}matchups[t1, t2] = 17;

#schedule the extra additional 2 inter conference matchups
subject to 2ExtraGamesInNFC{d1 in DIVISION["NFC"], t1 in TEAM[d1]}: sum{d2 in DIVISION["NFC"], t2 in TEAM[d2]: d2 != d1 and DivMatchups[d1,d2]=0}matchups[t1,t2] = 2;
subject to 2ExtraGamesInAFC{d1 in DIVISION["AFC"], t1 in TEAM[d1]}: sum{d2 in DIVISION["AFC"], t2 in TEAM[d2]: d2 != d1 and DivMatchups[d1,d2]=0}matchups[t1,t2] = 2;

#schedule the 4 matchups between divisions that are playing each other
subject to NFCDivMatches{d1 in DIVISION["NFC"], t1 in TEAM[d1]}: sum{d2 in DIVISION["NFC"], t2 in TEAM[d2]: d2 != d1 and DivMatchups[d1, d2]=1}matchups[t1,t2] = 4;
subject to AFCDivMatches{d1 in DIVISION["AFC"], t1 in TEAM[d1]}: sum{d2 in DIVISION["AFC"], t2 in TEAM[d2]: d2 != d1 and DivMatchups[d1, d2]=1}matchups[t1,t2] = 4;

#schedule the intra division matchups
subject to intraDivisionMatches{d in DIVISIONS, t1 in TEAM[d], t2 in TEAM[d]: t1 != t2}: matchups[t1, t2] = 2;

#only allow intra division matchups to have 2
subject to 2GamesVsEachDivMate{d1 in DIVISIONS, d2 in DIVISIONS, t1 in TEAM[d1], t2 in TEAM[d2]: DivMatchups[d1,d2] = 1}: matchups[t1, t2]<= 1;

s.t. noOtherDoubleMatchups{d1 in DIVISIONS, d2 in DIVISIONS, t1 in TEAM[d1], t2 in TEAM[d2]: d1 != d2}: matchups[t1, t2] <=1;

#base on the expected wins in the new year or base on the previous wins?
#subject to fairnessConstraint{d1 in DIVISIONS, t1 in TEAM[d1]}: sum{d2 in DIVISION, t2 in TEAM[d2]}matchups[t1, t2]*expectedWins[t2] <= 

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

param DivMatchups
:      AEAST ANORTH ASOUTH AWEST NEAST NNORTH NSOUTH NWEST    :=
AEAST     0     0      0      1     0     0      0      1
ANORTH    0     0      1      0     1     0      0      0
ASOUTH    0     1      0      0     0     0      1      0
AWEST     1     0      0      0     0     1      0      0
NEAST     0     1      0      0     0     0      0      1
NNORTH    0     0      0      1     0     0      1      0
NSOUTH    0     0      1      0     0     1      0      0
NWEST     1     0      0      0     1     0      0      0
;

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