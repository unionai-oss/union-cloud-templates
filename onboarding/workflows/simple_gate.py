import typing

import numpy
from datetime import timedelta
from flytekit import task, workflow, wait_for_input, conditional
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

    lr = LogisticRegression(C=2, max_iter=20000)
    lr.fit(X_train, y_train)
    return svc, lr


@task
def preds(m1: svm.SVC, m2: LogisticRegression, X_test: numpy.ndarray) -> typing.Tuple[numpy.ndarray, numpy.ndarray]:
    pred_1 = m1.predict(X_test[0:20])
    pred_2 = m2.predict(X_test[0:20])
    print(f"Pred 1: {pred_1}")
    print(f"Pred 2: {pred_2}")
    return pred_1, pred_2


# @task
# def run_preds(m: typing.Union[svm.SVC, LogisticRegression], X_test: numpy.ndarray) -> numpy.ndarray:
#     p = m.predict(X_test)
#     print(p)
#     return p


@task
def run_pred_1(m: svm.SVC, X_test: numpy.ndarray) -> numpy.ndarray:
    p = m.predict(X_test)
    return p


@task
def run_pred_2(m: LogisticRegression, X_test: numpy.ndarray) -> numpy.ndarray:
    p = m.predict(X_test)
    return p


@workflow
def wf() -> typing.Tuple[numpy.ndarray, numpy.ndarray]:
    X_train, X_test, y_train, y_test = get_data()
    m1, m2 = get_models(X_train=X_train, y_train=y_train)
    sample_pred_1, _ = preds(m1=m1, m2=m2, X_test=X_test)
    choice = wait_for_input("model-choice", timeout=timedelta(hours=1), expected_type=int)
    sample_pred_1 >> choice
    return conditional("predictbymodel").if_(choice == 1).then(run_pred_1(m=m1, X_test=X_test)).else_().then(run_pred_2(m=m2, X_test=X_test)), y_test


if __name__ == "__main__":
    predictions, y_test = wf()
    print(f"Predictions:\n{predictions}")
    print(f"y_test:\n{y_test}")
