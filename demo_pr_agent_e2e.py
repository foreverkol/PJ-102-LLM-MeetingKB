"""PR-Agent E2E 演示补丁: 故意包含 3 类可评审问题"""


def calc_score(values, weights=None):
    # 问题1: 无输入校验(除零风险)
    total = 0
    for v in values:
        total += v
    if weights:
        # 问题2: 长度不校验就 zip
        return sum(v * w for v, w in zip(values, weights)) / len(weights)
    return total / len(values)


def load_config(path):
    # 问题3: 裸 except 吞异常
    try:
        with open(path) as f:
            return f.read()
    except:
        return None


if __name__ == "__main__":
    print(calc_score([1, 2, 3], [0.5, 0.5]))
