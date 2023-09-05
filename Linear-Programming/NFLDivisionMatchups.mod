set CONFERENCES;
set DIVISION{CONFERENCES};
set DIVISIONS := union{i in CONFERENCES} DIVISION[i];

param expectedWins{d in DIVISIONS};
param maxWins{d in DIVISIONS};
param minWins{d in DIVISIONS};
param conference{d in DIVISIONS};
param order{d in DIVISIONS};

var matchups{d1 in DIVISIONS, d2 in DIVISIONS} binary;

minimize blowouts: sum{d1 in DIVISIONS, d2 in DIVISIONS}matchups[d1, d2] * abs(expectedWins[d1] - expectedWins[d2]);

#8 total division matchups, don't allow divisions to play themselves
subject to eightMatchupsConstraints: 16 <= sum{d1 in DIVISIONS, d2 in DIVISIONS: d1 != d2}matchups[d1,d2] <= 16;

#Limit each conference to 2 total inter-conference matchups
subject to 2InConferenceConstraints1{d1 in DIVISION["NFC"]}: 1 <= sum{d2 in DIVISION["NFC"]}matchups[d1, d2] <= 1;
subject to 2InConferenceConstraints3{d1 in DIVISION["AFC"]}: 1 <= sum{d2 in DIVISION["AFC"]}matchups[d1, d2] <= 1;

#Limit each conference to 4 cross conference matchups
subject to 4CrossConferenceConstraints1: 4 <= sum{d1 in DIVISION["NFC"], d2 in DIVISION["AFC"]}matchups[d1,d2] <= 4;

#Limit each division to 2 matchups
subject to twoEachConstraints1{d2 in DIVISIONS}: 2 <= sum{d1 in DIVISIONS}matchups[d1,d2] <= 2;

#Force symmetry (if Afc east plays the afc west then the afc west must play the afc east)
subject to symmetricConstraints{d1 in DIVISIONS, d2 in DIVISIONS}: matchups[d1, d2] = matchups[d2, d1];


data;
set CONFERENCES := NFC, AFC;
set DIVISION[NFC] := NNORTH, NSOUTH, NEAST, NWEST;
set DIVISION[AFC] := ANORTH, ASOUTH, AEAST, AWEST;

param expectedWins :=
NNORTH 33
NSOUTH 32
NEAST 36
NWEST 33
ANORTH 39
ASOUTH 30
AEAST 37
AWEST 37;

param maxWins :=
NNORTH 9.5
NSOUTH 8
NEAST 11
NWEST 11.5
ANORTH 11
ASOUTH 9
AEAST 11.5
AWEST 11.5;

param minWins :=
NNORTH 7.5
NSOUTH 7.5
NEAST 8
NWEST 5
ANORTH 8
ASOUTH 5
AEAST 8
AWEST 8.5;

