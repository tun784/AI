import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Phần 1: Trộn 2 mảng một chiều
a = [3, 9, 1, 4]
b = [2, 7, 4, 3, 2, 8]
result = []

for i in range(min(len(a), len(b))):
    result.append(min(a[i], b[i]))

if len(a) > len(b):
    result.extend(a[len(b):])
else:
    result.extend(b[len(a):])

print("Mang ket qua:", result)

# Phần 2: Làm việc với ma trận 2 chiều
a_matrix = np.array([[1, 2, -3], [-4, 5, 6], [7, 8, 9]])
n = a_matrix.shape[0]

# a. Tính tổng tam giác trên của đường chéo phụ
sum_upper_triangle = sum(a_matrix[i, j] for i in range(n) for j in range(n) if i + j < n - 1)
print("Tong tam giac tren cua duong cheo phu:", sum_upper_triangle)

# b. Chuyển các phần tử âm thành trị tuyệt đối
a_matrix = np.abs(a_matrix)
print("Ma tran sau khi chuyen phan tu am thanh tri tuyet doi:\n", a_matrix)

# c. Thay các phần tử chẵn trong a bằng số nguyên x
x = 10
a_matrix[a_matrix % 2 == 0] = x
print("Ma tran sau khi thay phan tu chan bang x:\n", a_matrix)

# d. Kiểm tra ma trận có toàn chẵn không
all_even = np.all(a_matrix % 2 == 0)
print("Ma tran co toan chan khong:", all_even)

# e. Kiểm tra ma trận có đối xứng không
is_symmetric = np.array_equal(a_matrix, a_matrix.T)
print("Ma tran co doi xung khong:", is_symmetric)

# f. Kiểm tra đường chéo chính tăng dần không
is_main_diag_increasing = all(a_matrix[i, i] < a_matrix[i+1, i+1] for i in range(n-1))
print("Duong cheo chinh co tang dan khong:", is_main_diag_increasing)

# g. Xuất các phần tử thuộc tam giác dưới của đường chéo phụ
lower_triangle = [a_matrix[i, j] for i in range(n) for j in range(n) if i + j >= n - 1]
print("Tam giac duoi cua duong cheo phu:", lower_triangle)

# h. Kiểm tra đường chéo phụ giảm dần không
is_secondary_diag_decreasing = all(a_matrix[i, n-1-i] > a_matrix[i+1, n-2-i] for i in range(n-1))
print("Duong cheo phu co giam dan khong:", is_secondary_diag_decreasing)

# Phần 3: Tạo dictionary chứa 3 dictionaries
dicts = {
    'dict1': {'a': 1, 'b': 2},
    'dict2': {'c': 3, 'd': 4},
    'dict3': {'e': 5, 'f': 6}
}
print("Dictionary:", dicts)

# Phần 4: Đọc và xuất file
file_path = "output.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write("Du lieu ma tran:\n" + str(a_matrix))

with open(file_path, "r", encoding="utf-8") as f:
    print("Noi dung file:")
    print(f.read())

# Phần 5: Tìm hiểu Pandas và Matplotlib
# Pandas: Tạo DataFrame từ dữ liệu dictionary
data = {'Name': ['An', 'Binh', 'Chi'], 'Age': [20, 21, 19], 'Score': [85, 90, 88]}
df = pd.DataFrame(data)
print("DataFrame:\n", df)

# Matplotlib: Vẽ biểu đồ điểm số của học sinh
plt.plot(df['Name'], df['Score'], marker='o')
plt.title("Diem so cua hoc sinh")
plt.xlabel("Ten hoc sinh")
plt.ylabel("Diem so")
plt.show()