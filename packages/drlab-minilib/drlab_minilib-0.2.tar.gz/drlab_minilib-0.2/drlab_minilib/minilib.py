"""
This is a miniature library for educational purposes only. It only implements some simple methods to make learning of AI/ML easier for managers / rookies.
There are 3 training use cases in this library:
1. HR Department: in this case there are datasets with CVs and future employees` evaluations. Students should train classifier to support future CV selection decisions.
2. ...
3. ...

>> DATASETS NOT INCLUDED HERE! They are distributed during training day.

Libraries used:
pandas
sklearn

Author: 
Rafal Labedzki Ph.D.
rlabed@sgh.waw.pl

"""
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt



def open(file):
    return pd.read_csv(file, sep=";")

def show(data):
    print(pd.DataFrame(data).head())

def classifier_decision_tree(data):
    X = data[["programowanie","zarządzanie","wykształcenie","języki","doświadczenie"]]
    y = data["OCENA"]
    decision_tree = tree.DecisionTreeClassifier(random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    decision_tree.fit(X_train,y_train)
    print(f"AI model ready. Decision tree precision: {decision_tree.score(X_test,y_test)*100}%")
    plt.figure(dpi=300)
    tree.plot_tree(
        decision_tree=decision_tree,
        feature_names=X.columns,
        class_names=["SLABY", "DOBRY"],
        impurity=False
        )



    