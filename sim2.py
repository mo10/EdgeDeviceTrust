import math
import numpy as np

# <summary>
# 求熵
# </summary>
# <param name="vs">数据集合</param>
# <param name="cols">列数</param>
# <param name="rows">行数</param>
# <returns>Ei</returns>
def CalcShang(matrix,cols,rows):
    H = []
    K = math.log(rows)
    fs = []
    print("K = %f "%(K))
    for i in range(0,cols):
        temp = 0.00
        for j in range(0,rows):
            tr = np.transpose(matrix) #转置数组
            f = matrix[j][i] / np.sum(tr[i])
            if f > 0:
                temp = temp + f * math.log(f)
        H.append((-K)*temp)

    sum_E = np.sum(H) # 计算熵

    W = []
    for x in range(0,cols):
        w = (1.0 - H[x]) / (cols - sum_E)
        W.append(w)
    # 计算F to D feedback trust
    DW = np.zeros((rows, cols))
    for i in range(0,rows):
        for j in range(0,cols):
            DW[i][j] = matrix[i][j] * W[j]
    Fbk = []
    for x in range(0,cols):
        Fbk.append(np.sum(np.transpose(DW)[x]))
    return Fbk

test = [
    [0.4922, 0.4516, 0.5159, 0.1294, 0.6565, 0.3395, 0.1083, 0.6306, 0.2860],
    [0.4442, 0.3552, 0.6315, 0.1410, 0.5303, 0.6156, 0.2567, 0.5291, 0.6142],
    [0.5078, 0.0088, 0.1901, 0.5485, 0.2547, 0.1209, 0.3843, 0.1162, 0.0270],
    [0.1814, 0.2505, 0.2671, 0.2392, 0.3224, 0.1732, 0.1350, 0.3689, 0.1894],
    [0.3020, 0.5002, 0.3686, 0.4515, 0.3435, 0.2784, 0.0015, 0.3694, 0.3858],
    [0.2170, 0.5484, 0.3217, 0.4128, 0.2662, 0.3844, 0.6157, 0.3063, 0.3520],
]

print(CalcShang(test,9,6))