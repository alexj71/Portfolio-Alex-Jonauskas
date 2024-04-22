import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.tree import plot_tree
from sklearn.model_selection import StratifiedKFold
import numpy as np
from collections import defaultdict
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import make_scorer, f1_score


# Import Data, fix errors, and transform UDFA to 8th round draft pick
QBData = pd.read_csv('C:/Users/alexj/OneDrive/Documents/FantasyFootballData/cDataQB.csv')
nflData = pd.read_csv('C:/Users/alexj/OneDrive/Documents/FantasyFootballData/nflData2023.csv')
nflData['PPG (PPR)'] = pd.to_numeric(nflData['PPG (PPR)'], errors='coerce')
nflData.loc[nflData['DR'] == 'UDFA', 'DR'] = 8
QBData.loc[QBData['DR'] == 'UDFA', 'DR'] = 8

# Filter nfl data to qb seasons where the qb played at least 12 games
qb_data = nflData[(nflData['Pos'] == 'QB') & (nflData['GMs'] >= 12)]
years = range(2000, 2023)  # Update the end year as needed

# Find the 10th scoring and 5th scoring qbs overall by year
top_10_qb_per_year = []
top_5_qb_per_year = []
for year in years:
    # Filter data for the specific year
    data_for_year = qb_data[qb_data['Year'] == year]
    # Sort by 'PPR/G' in descending order and get the 10th highest
    top_10_qb = data_for_year.nlargest(10, 'PPG (PPR)').iloc[9]['PPG (PPR)']
    top_5_qb = data_for_year.nlargest(5, 'PPG (PPR)').iloc[4]['PPG (PPR)']
    # Append the 10th highest to the new DataFrame
    top_10_qb_per_year.append(top_10_qb)
    top_5_qb_per_year.append(top_5_qb)

# Find the line of best fit for 10th and 5th overall seasons by year
a, b = np.polyfit(years, top_10_qb_per_year, 1)
averagesTen = []
for year in years:
    averagesTen.append(a*year + b)
print(averagesTen)
averages_dict_ten = dict(zip(years, averagesTen))

c, d = np.polyfit(years, top_5_qb_per_year, 1)
averagesFive = []
for year in years:
    averagesFive.append(c*year + d)
print(averagesFive)
averages_dict_five = dict(zip(years, averagesFive))

#Plot a line graph of the 10th and 5th best seasons with lines of best fit
plt.figure(figsize=(12, 6))
plt.plot(years, top_10_qb_per_year, label='10th Best')
plt.plot(years, top_5_qb_per_year, label='5th Best')
plt.plot(years, a*years+b)
plt.plot(years, c*years+d)
plt.grid(True)
plt.title('The 5th and 10th Best QB\'s PPR/G Since 2000')
plt.xlabel('Year')
plt.ylabel('PPG (PPR)')
plt.show()

# Filter Players that were above the top 10 and top 5 thresholds by year (whether or not they are above the line of best fit
top10 = qb_data['CFB ID'][(qb_data['CFB ID'] != 'UNK') & (qb_data['PPG (PPR)'] >= qb_data['Year'].map(averages_dict_ten))]
top5 = qb_data['CFB ID'][(qb_data['CFB ID'] != 'UNK') & (qb_data['PPG (PPR)'] >= qb_data['Year'].map(averages_dict_five))]

id_list = top10

# Use a defaultdict to count occurrences in the top 10 list
id_counts = defaultdict(int)
for id in id_list:
    id_counts[id] += 1

# Print player IDs with their counts
for id, count in id_counts.items():
    print(f"ID: {id}, Count: {count}")

# Any player in the top 10 list twice or top 5 list once is appended to list of hits
hits = []
for t in top10.unique().tolist():
    if t in top5.tolist() or id_counts[t] > 1:
        hits.append(t)
print(hits)

# Print the qbs with 1 top 10 season
'''for t in top10.unique().tolist():
    if t not in hits:
        print(t, ",", end =" ")'''

# Add the hit/bust column to the college dataframe to use for training data
for id in QBData['cfb_id']:
    if id in hits:
        QBData.loc[QBData['cfb_id'] == id, 'Hit/Bust'] = 1
    else:
        QBData.loc[QBData['cfb_id'] == id, 'Hit/Bust'] = 0

''' Add additional features not in dataset, fix any remaining problems with data, and filter to players who played 
    before 2020 to train model '''
QBData['DP'] = pd.to_numeric(QBData['DP'], errors='coerce')
QBData['Y/RA'] = QBData['Rush Yards']/QBData['Rush Attempts']
QBData['Comp %'] = QBData['Comp']/QBData['Pass Attempts']
QBData['Y/A'] = (QBData['Rush Yards'] + QBData['Pass Yards'])/(QBData['Rush Attempts']+QBData['Pass Attempts'])
QBData['Y/PA'] = QBData['Pass Yards']/QBData['Pass Attempts']
QBData['Comp% * Y/PA'] = QBData['Comp %'] * QBData['Y/PA']
QBData['INT %'] = QBData['INT']/QBData['Pass Attempts']
QBData['Snaps'] = QBData['Pass Attempts'] + QBData['Rush Attempts']
#QBData[(QBData['DP'] > 13.5) & (QBData['DP'] > 35.5) & (QBData['Comp% * Y/PA'] > 4.739)][['cfb_id', 'DP', 'Comp% * Y/PA', 'Hit/Bust']].to_csv('C:/Users/alexj/OneDrive/Documents/FantasyFootballData/temp.csv')
QBData = QBData[(QBData['DY'] < 2020)]

# Train data
X = QBData[['Pass Attempts', 'Rush Attempts', 'Pass Yards', 'Rush Yards', 'Pass TDs', 'Rush TDs', 'Comp', 'PPR/G',
            'Best PPG', 'INT', 'DR', 'DP', 'Gs', 'Comp %', 'Y/PA', 'Y/RA', 'Y/A', 'Comp% * Y/PA', 'INT %', 'Snaps']]
y = QBData['Hit/Bust']
clf = tree.DecisionTreeClassifier(criterion="gini")

# Perform k-fold cross-validation at varying depths
depths = range(1, 15)
for depth in depths:
    clf.set_params(min_samples_leaf=5, max_depth=depth)

    # Use stratified 5-fold cross-validation
    stratified_kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)

    # Calculate cross-validated accuracy scores
    scores = cross_val_score(clf, X, y, cv=stratified_kfold)
    f1_scorer = make_scorer(f1_score, average='weighted')
    f1_scores = cross_val_score(clf, X, y, cv=stratified_kfold, scoring=f1_scorer)

    # Print the mean accuracy and standard deviation for each depth
    print(f"Depth {depth}: Mean Accuracy = {np.mean(scores):.4f}, Std Dev = {np.std(scores):.4f}")
    print(f"Mean F1-score across folds: {np.mean(f1_scores)}")
    print(f"Standard deviation of F1-scores: {np.std(f1_scores)}\n")

# Fit the model
clf = tree.DecisionTreeClassifier(min_samples_leaf=5, max_depth=4)
clf.fit(X, y)

# Plot the decision tree
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=['Pass Attempts', 'Rush Attempts', 'Pass Yards', 'Rush Yards', 'Pass TDs', 'Rush TDs', 'Comp',
            'PPR/G', 'Best PPG', 'INT', 'DR', 'DP', 'Gs', 'Comp %', 'Y/PA', 'Y/RA', 'Y/A', 'Comp% * Y/PA', 'INT %', 'Snaps']
          , class_names=['Bust', 'Hit'], filled=True, rounded=True)
plt.show()

# Code for checking other spliting options when a split is deemed overfitted
'''tempX = QBData[(QBData['DP'] > 13.5) & (QBData['DP'] > 35.5) & (QBData['Comp% * Y/PA'] > 4.739)][['Pass Attempts', 'Rush Attempts', 'Pass Yards', 'Rush Yards', 'Pass TDs', 'Rush TDs', 'Comp', 'PPR/G',
            'Best PPG', 'INT', 'DR', 'DP', 'Gs', 'Y/RA', 'Y/A', 'INT %', 'Snaps']]
tempY = QBData[(QBData['DP'] > 13.5) & (QBData['DP'] > 35.5) & (QBData['Comp% * Y/PA'] > 4.739)]['Hit/Bust']
tempclf = tree.DecisionTreeClassifier(max_depth=2)
tempclf.fit(tempX,tempY)
plt.figure(figsize=(12, 8))
plot_tree(tempclf, feature_names=['Pass Attempts', 'Rush Attempts', 'Pass Yards', 'Rush Yards', 'Pass TDs', 'Rush TDs', 'Comp',
            'PPR/G', 'Best PPG', 'INT', 'DR', 'DP', 'Gs', 'Y/RA', 'Y/A', 'INT %', 'Snaps']
          , class_names=['Bust', 'Hit'], filled=True, rounded=True)
plt.show()'''

# Get the decision tree
tree = clf.tree_
paths = []
def print_tree_path(node, path=""):
    if tree.feature[node] != -2:  # If it's not a leaf node
        feature_name = X.columns[tree.feature[node]]
        threshold = tree.threshold[node]
        path += f"{feature_name} <= {threshold} --> "
        print_tree_path(tree.children_left[node], path)
        print_tree_path(tree.children_right[node], path)
    else:
        class_label = clf.classes_[tree.value[node].argmax()]
        path += f"Class: {class_label}"
        #print(path)
        paths.append(path)
    return paths




