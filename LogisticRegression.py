import numpy as n
import diffprivlib.models as dp
import numpy as np
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import matplotlib.pyplot as plt
import time


def train_and_test(filepath="static/uploaded/logReg.txt", epsilon=0.1, split_ratio=1, x_fields_list, y_field_name, **unused_args):
    '''
    returns the train and test accuracy in %
    @Split_ratio = train:(test+train) should be in (0,1]
    '''
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())

    headers = list(df)
    y_index = headers.index(y_field_name)
    x_indices = [headers.index(field[0]) for field in x_fields_list]
    
    X = df.iloc[:, x_indices].values  # features, np array
    Y = df.iloc[:, y_index].values  # labels, np array
    print("splitting at ")
    split_index = int(X.shape[0]*split_ratio)
    print("Split_index =", split_index)
    X_train, X_test = X[:split_index], X[split_index:]
    Y_train, Y_test = Y[:split_index], Y[split_index:]
    # bounds=None will throw warning; no Priors
    
    dp_clf = Pipeline([
        ('scaler', MinMaxScaler()),
        ('clf', dp.LogisticRegression(epsilon=epsilon))
    ])
    dp_clf.fit(X_train, Y_train)
    test_accuracy = (dp_clf.predict(X_test) == Y_test).sum() / \
        Y_test.shape[0] * 100
    train_accuracy = (dp_clf.predict(X_train) ==
                      Y_train).sum() / Y_train.shape[0] * 100
    print("ACCURACIES:", test_accuracy, train_accuracy)
    params = dp_clf.sigma_
    print("params", params)
    x_list = [e[0] for e in x_fields_list]
    return (train_accuracy, test_accuracy, params, x_list)


def make_and_save_graph(filepath="static/uploaded/logReg.txt", split_ratio=1, x_fields_list, y_field_name,  **unused_args):
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())

    headers = list(df)
    y_index = headers.index(y_field_name)
    x_indices = [headers.index(field[0]) for field in x_fields_list]
    
    X = df.iloc[:, x_indices].values  # features, np array
    Y = df.iloc[:, y_index].values  # labels, np array

    split_index = int(X.shape[0]*split_ratio)
    print("splitting at ", split_index, "for arrays of size ", X.shape, Y.shape)
    X_train, X_test = X[:split_index], X[split_index:]
    Y_train, Y_test = Y[:split_index], Y[split_index:]
    if split_ratio == 1:
        X_test, Y_test = X_train, Y_train
        print("Split ratio 1; Testing on Train data")
    print("shapes:", X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)
    epsilons = np.logspace(-2, 2, 50)
    accuracy = list()

    for epsilon in epsilons:
        clf = Pipeline([
        ('scaler', MinMaxScaler()),
        ('clf', dp.LogisticRegression(epsilon=epsilon))
        ])
        clf.fit(X_train, Y_train)

        accuracy.append(
            (clf.predict(X_test) == Y_test).sum() / Y_test.shape[0])

    plt.semilogx(epsilons, accuracy)
    plt.title("Differentially private Regression accuracy")
    plt.xlabel("epsilon")
    plt.ylabel("Accuracy")
    name = 'static/images/LogisticRegression'+str(time.time())+'.png'
    plt.savefig(name)
    plt.close()
    return name
