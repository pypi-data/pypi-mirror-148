COSTACK_MAIN_ML = """import json
import pickle
import numpy as np

classifier = None
with open('./model/model.pkl', 'rb') as f:
    classifier = pickle.load(f)

def handler(event, context):
    if "body" not in event:
        X = np.array(json.loads(event)["data"])
    else:
        X = np.array(json.loads(event["body"])["data"])
    result = classifier.predict(X)
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "result": result.tolist()
    }
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }

"""



TRAIN_CONTENT = """from sklearn import svm
from sklearn import datasets
import pickle

iris = datasets.load_iris()
X, y = iris.data, iris.target

clf = svm.SVC()
clf.fit(X, y)

with open('./model/model.pkl','wb') as f:
    pickle.dump(clf,f)
"""

