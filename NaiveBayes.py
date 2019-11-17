import numpy as np
import diffprivlib.models as dp
import numpy as np
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import matplotlib.pyplot as plt
import time


def train_and_test(filepath="static/uploaded/logReg.txt", epsilon=0.1, bounds=(1e-7, 1e7), split_ratio=1, **unused_args):
    '''
    returns the train and test accuracy in %
    @Split_ratio = train:(test+train) should be in (0,1]
    '''
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())
    X = df.iloc[:, :-1].values  # features, np array
    Y = df.iloc[:, -1].values  # labels, np array
    print("splitting at ")
    split_index = int(X.shape[0]*split_ratio)
    print("Split_index =", split_index)
    X_train, X_test = X[:split_index], X[split_index:]
    Y_train, Y_test = Y[:split_index], Y[split_index:]
    # bounds=None will throw warning; no Priors
    dp_clf = dp.GaussianNB(epsilon=epsilon, bounds=[bounds]*X.shape[1])
    dp_clf.fit(X_train, Y_train)
    test_accuracy = (dp_clf.predict(X_test) == Y_test).sum() / \
        Y_test.shape[0] * 100
    train_accuracy = (dp_clf.predict(X_train) ==
                      Y_train).sum() / Y_train.shape[0] * 100
    print("ACCURACIES:", test_accuracy, train_accuracy)
    params = dp_clf.sigma_
    print("params", params)
    return (train_accuracy, test_accuracy, params)


def make_and_save_graph(filepath="static/uploaded/logReg.txt", split_ratio=1, bounds=(1e-7, 1e7),  **unused_args):
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())
    X = df.iloc[:, :-1].values  # features, np array
    Y = df.iloc[:, -1].values  # labels, np array
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
        clf = dp.GaussianNB(epsilon=epsilon, bounds=[bounds]*X.shape[1])
        clf.fit(X_train, Y_train)

        accuracy.append(
            (clf.predict(X_test) == Y_test).sum() / Y_test.shape[0])

    plt.semilogx(epsilons, accuracy)
    plt.title("Differentially private Naive Bayes accuracy")
    plt.xlabel("epsilon")
    plt.ylabel("Accuracy")
    name = 'static/images/NaiveBayes'+str(time.time())+'.png'
    plt.savefig(name)
    plt.close()
    return name
