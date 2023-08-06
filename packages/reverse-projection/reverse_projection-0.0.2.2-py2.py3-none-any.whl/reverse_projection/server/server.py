from flask import Flask, render_template, jsonify, request
import platform, json, os
from pathlib import PurePath
from flask_cors import CORS
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from cachelib import SimpleCache
from ..search import ReverseProjection
import numpy as np

cache = SimpleCache()

sys_spliter = "\\" if platform.system() == "Windows" else "/"
filepath = PurePath(__file__).parent
filepath = str(filepath)+sys_spliter
app = Flask(__name__, template_folder= filepath + "template", 
            static_folder=filepath + "static")
CORS(app)
app.config["SECRET_KEY"] = "luktian"
app.jinja_env.variable_start_string = "{{{"
app.jinja_env.variable_end_string = "}}}"

@app.route('/')
def main():
    return render_template("main.html")

# 0列为number，1列为label，2列以后为feature
# 0行为feature_name
@app.route("/test", methods=["POST"])
def test():
    file = request.files.get("file")
    ext = os.path.splitext(file.filename)[-1]
    if ext == ".xlsx" or ext == ".xls":
        try:
            data = pd.read_excel(file)
            fnames = data.iloc[:, 2:].columns.tolist()
            numbers = data.iloc[:, 0].values
            labels = data.iloc[:, 1].values
            X = data.iloc[:, 2:].values
        except Exception as e:
            print(e)
            return jsonify(msg="文件读取失败")
        try:
            scaler = StandardScaler().fit(X)
            scaled_X = scaler.transform(X)
            transformer = PCA().fit(scaled_X)
            transformed_X = transformer.transform(scaled_X)[:, :2]
            print(transformed_X)
            cache.set("scaler", scaler)
            cache.set("transformer", transformer)
            cache.set("fvalues", scaled_X)
        except Exception as e:
            print(e)
            return jsonify(msg="文件处理失败")
        pro_xs = []
        label_sets = []
        numberss = []
        for label in set(labels.tolist()):
            pro_x = transformed_X[labels==float(label)].tolist()
            pro_xs.append(pro_x)
            number = numbers[labels==float(label)].tolist()
            numberss.append(number)
            label_sets.append(label)
        return jsonify(msg="文件处理成功", pro_x=pro_xs, fnames=fnames, labels=label_sets, numbers=numberss)
    return jsonify(message="请用xlsx上传")

@app.route("/rp", methods=["POST"])
def rp():
    points = request.form.get("points")
    points = json.loads(points)
    points = np.array(points).astype(float)
    scaler = cache.get("scaler")
    transformer = cache.get("transformer")
    fvalues = cache.get("fvalues")
    if scaler is not None and transformer is not None:
        result = ReverseProjection(feature_values=fvalues, transformer=transformer, verbose=True, criterion=0.00001).search(points)
        spoint = result["points"]
        sfeatures = result["features"]
        sfeatures = scaler.inverse_transform(np.array(sfeatures).reshape(1, -1))
        return jsonify(message="计算成功", result=sfeatures.tolist()[0], spoint=spoint)

    return jsonify(message="失败了")

if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)

