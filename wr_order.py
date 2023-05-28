import json

def write_order(data, file="order_num"):
    with open(file, "w") as fp:
        json.dump(data, fp)

def read_order(file="order_num"):
    with open(file) as fp:
        num = json.load(fp)["track"]
        return num