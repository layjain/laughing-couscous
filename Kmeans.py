import numpy as np
import diffprivlib.models as dp
import numpy as np
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import matplotlib.pyplot as plt
import time


def train_and_test(filepath="static/uploaded/logReg.txt", epsilon=0.1, split_ratio=1, n_clusters=8, x_fiels_list, y_field_name, **unused_args):
    print("making pandas dataframe")
    df = pd.read_csv(filepath, header=None)
    print("head:", df.head())

    headers = list(df)
    x_indices = [headers.index(field[0]) for field in x_fields_list]
    
    X = df.iloc[:, x_indices].values  # features, np array

    print("splitting")
    split_index = int(X.shape[0]*split_ratio)
    X_train, X_test = X[:split_index], X[split_index:]

    dp_clf = dp.KMeans(epsilon=epsilon, n_clusters=n_clusters)
    dp_clf.fit(X_train)

    params = dp_clf.cluster_centers_

    x_list = [e[0] for e in x_indices]
    y_list = ["Cluster "+str(i+1) for i in range(n_clusters)]

    return (train_accuracy, test_accuracy, params, x_list, y_list)


def make_and_save_graph(filepath="static/uploaded/logReg.txt", split_ratio=1, n_clusters=8, x_fiels_list, y_field_name, **unused_args):
    '''
    This function is not called for now
    '''
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
        clf = dp.KMeans(epsilon=epsilon, n_clusters=n_clusters)
        clf.fit(X_train, Y_train)

        accuracy.append(
            (clf.predict(X_test) == Y_test).sum() / Y_test.shape[0])

    plt.semilogx(epsilons, accuracy)
    plt.title("Differentially private Naive Bayes accuracy")
    plt.xlabel("epsilon")
    plt.ylabel("Accuracy")
    name = 'static/images/KMeans'+str(time.time())+'.png'
    plt.savefig(name)
    plt.close()
    return name