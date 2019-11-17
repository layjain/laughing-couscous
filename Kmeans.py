import numpy as np
import diffprivlib.models as dp
import numpy as np
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import matplotlib.pyplot as plt
import time


def train_and_test(filepath="static/uploaded/logReg.txt", epsilon=0.1, bounds=(1e-7, 1e7), split_ratio=1, n_clusters=8, **unused_args):
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())
    X = df.iloc[:, :-1].values  # features, np array
    Y = df.iloc[:, -1].values  # labels, np array
    print("splitting")
    split_index = int(X.shape[0]*split_ratio)
    X_train, X_test = X[:split_index], X[split_index:]
    Y_train, Y_test = Y[:split_index], Y[split_index:]

    dp_clf = dp.KMeans(epsilon=epsilon, bounds=[
                       bounds]*X.shape[1], n_clusters=n_clusters)
    dp_clf.fit(X_train, Y_train)
    test_accuracy = (dp_clf.predict(X_test) == Y_test).sum() / \
        Y_test.shape[0] * 100
    train_accuracy = (dp_clf.predict(X_train) ==
                      Y_train).sum() / Y_train.shape[0] * 100
    return (train_accuracy, test_accuracy)


def make_and_save_graph(filepath="static/uploaded/logReg.txt", split_ratio=1, bounds=(1e-7, 1e7), n_clusters=8, **unused_args):
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())
    X = df.iloc[:, :-1].values  # features, np array
    Y = df.iloc[:, -1].values  # labels, np array
    print("splitting")

    split_index = int(X.shape[0]*split_ratio)
    X_train, X_test = X[:split_index], X[split_index:]
    Y_train, Y_test = Y[:split_index], Y[split_index:]

    epsilons = np.logspace(-2, 2, 50)
    accuracy = list()

    for epsilon in epsilons:
        clf = dp.KMeans(epsilon=epsilon, bounds=[
                        bounds]*X.shape[1], n_clusters=n_clusters)
        clf.fit(X_train, Y_train)

        accuracy.append(
            (clf.predict(X_test) == Y_test).sum() / Y_test.shape[0])

    plt.semilogx(epsilons, accuracy)
    plt.title("Differentially private kMeans accuracy")
    plt.xlabel("epsilon")
    plt.ylabel("Accuracy")
    name = 'static/images/NaiveBayes'+str(time.time())+'.png'
    plt.savefig(name)
    plt.close()
    return name
