from math import *

# def sub_function_1(value):
#     return value * 2

# def sub_function_2(value):
#     return value + 10

# def sub_function_3(value):
#     return value - 5

# def sub_function_4(value):
#     return value ** 2

# def condition_example(value):
#     return value > 20  # Điều kiện: giá trị lớn hơn 20
# # def main_function(value, condition):
# def main_function():
#     """
#     Xử lý lần lượt 4 hàm con.
#     Nếu giá trị sau khi xử lý thỏa mãn điều kiện, trả về kết quả và kết thúc.
#     Nếu không, tiếp tục xử lý hàm con tiếp theo.
#     """
#     print("Chương trình đã bắt đầu.")  
#     input_value = float(input("Nhập giá trị ban đầu: "))
#     for sub_function in [sub_function_1, sub_function_2, sub_function_3, sub_function_4]:
#         result = sub_function(input_value)
#         print(f"Giá trị sau khi xử lý: {result}")
#         if condition_example(result):
#             print("Điều kiện thỏa mãn, trả về giá trị:", result)
#             return result
#     print("Không có giá trị nào thỏa mãn điều kiện.")
#     return None


# Gọi hàm
# if __name__ == "__main__":
    # input_value = float(input("Nhập giá trị ban đầu: "))
    # main_function(input_value, condition_example)
def test_1(l1,l2,l3):
    x = l1+l2+l3
def test_2(l1,l2,l3):
    y = l1+l2
    z = l1+l3
    test_1(l1,l2,l3)
    print("ham test 1: x1 =",x)
    print("ham test 2: x2 =",y)
if __name__ == "__main__":
    test_2(1,2,3)