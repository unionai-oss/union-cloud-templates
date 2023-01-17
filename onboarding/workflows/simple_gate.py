import typing

import numpy
from flytekit import task, workflow
from sklearn import svm
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


@task
def get_data() -> typing.Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    data = load_digits()
    X = data.images.reshape(len(data.images), -1)
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    print(f"\nSplit data sizes:\nX_train {X_train.shape}, X_test {X_test.shape}, y_train {y_train.shape}, y_test {y_test.shape}")
    return X_train, X_test, y_train, y_test


@task
def get_models(X_train: numpy.ndarray, y_train: numpy.ndarray) -> typing.Tuple[svm.SVC, LogisticRegression]:
    svc = svm.SVC(gamma=0.001, C=100)
    svc.fit(X_train, y_train)

    # y_pred = svc.predict(X_test[0:20])
    # print(y_pred)

    lr = LogisticRegression(C=2, max_iter=20000)
    lr.fit(X_train, y_train)
    return svc, lr


@task
def preds(m1: svm.SVC, m2: LogisticRegression, X_test: numpy.ndarray):
    pred_1 = m1.predict(X_test[0:20])
    pred_2 = m2.predict(X_test[0:20])
    print(f"Pred 1: {pred_1}")
    print(f"Pred 2: {pred_2}")
# pred2 = lr.predict(X_test[0:20])
# print(pred2)
# print(y_test[0:20])


@workflow
def wf():
    X_train, X_test, y_train, y_test = get_data()
    m1, m2 = get_models(X_train=X_train, y_train=y_train)
    preds(m1=m1, m2=m2, X_test=X_test)


if __name__ == "__main__":
    wf()
