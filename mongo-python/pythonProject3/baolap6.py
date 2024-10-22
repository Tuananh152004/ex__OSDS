# import
from xmlrpc.client import DateTime

from pymongo import MongoClient
from datetime import datetime
# b1: ket noi den MongoDb
client = MongoClient('localhost', 27017)
client.drop_database('driveManagemnet1')
db = client['driveManagemnet1']
# b2: Tap cac collections
files_collection = db['file']
# b3: Them giu lieu nguoi dung
file_data=[{ 'file_id': 1, 'name': "Report.pdf", 'size': 2048, 'owner': "Nguyen Van A", 'created_at': datetime(2024,1,10), 'shared': 'false' },
    { 'file_id': 2, 'name': "Presentation.pptx", 'size': 5120, 'owner': "Tran Thi B", 'created_at': datetime(2024,1,15), 'shared': 'true' },
    { 'file_id': 3, 'name': "Image.png", 'size': 1024, 'owner': "Le Van C", 'created_at': datetime(2024,1,20), 'shared': 'false' },
    { 'file_id': 4, 'name': "Spreadsheet.xlsx", 'size': 3072, 'owner': "Pham Van D", 'created_at':datetime(2024,1,25), 'shared': 'true' },
    { 'file_id': 5, 'name': "Notes.txt", 'size': 512, 'owner': "Nguyen Thi E", 'created_at': datetime(2024,1,30), 'share': 'false' }]
files_collection.insert_many(file_data)
# Bước 3: Thực hiện các truy vấn để quản lý tệp
# 3.1: Xem tất cả tệp trong bộ sưu tập 'files'
print(" Tất Cả file ")
for file in file_data:
    print(file)

# 3.2: Tìm tệp có kích thước lớn hơn 2000KB
print(" tệp có kích thước lớn hơn 2000KB ")
file_gt2000kb=files_collection.find({'size':{"$gt":2000}})
for file in file_gt2000kb:
    print(file)

# 3.3: Đếm tổng số tệp
file_count=files_collection.count_documents({})
print(f'\nĐếm tổng số tệp:{file_count}')

# 3.4: Tìm tất cả tệp được chia sẻ
file_shared=files_collection.find({'shared':'true'})
print("tất cả tệp được chia sẻ")
for file in file_shared:
    print(file)
# 3.5: Thống kê số lượng tệp theo chủ sở hữu
print(" Thống kê số lượng tệp theo chủ sở hữu ")
owner_file=files_collection.aggregate([{ "$group": { "_id": "$owner", "count": { '$sum': 1 } } }])
for file in owner_file:
    print(file)
# Bước 4: Cập nhật và xóa thông tin tệp
# 4.1: Cập nhật trạng thái chia sẻ của tệp với file_id = 1 thành true
files_collection.update_one({ "file_id": 1 }, { "$set": { "shared": "true" } })
print('Cập nhật trạng thái chia sẻ của tệp với file_id = 1 thành true')
for file in files_collection.find():
    print(file)
 # 4.2: Xóa tệp với file_id = 3
files_collection.delete_one({ "file_id": 3 })
print(" Xóa tệp với file_id = 3 ")
for file in files_collection.find():
     print(file)

# Buớc 5: Xem lại dữ liệu sau khi cập nhật và xóa
print("Xem lại dữ liệu sau khi cập nhật và xóa")
for file in files_collection.find():
    print(file)
# Kiểm tra lại tất cả tệp trong bộ sưu tập
print("  Kiểm tra lại Tất Cả file ")
for file in file_data:
    print(file)
# Câu hỏi 1: Tìm tất cả tệp của người dùng có tên là "Nguyen Van A".
print("tất cả tệp của người dùng có tên là 'Nguyen Van A'")
for file in files_collection.find({'owner': "Nguyen Van A"}):
    print(file)
# Câu hỏi 2: Tìm tệp lớn nhất trong bộ sưu tập.
print("tệp lớn nhất trong bộ sưu tập")
for file in files_collection.find().sort("size",-1).limit(1):
    print(file)
# Câu hỏi 3: Tìm số lượng tệp có kích thước nhỏ hơn 1000KB.
print("tệp có kích thước nhỏ hơn 1000KB")
for file in files_collection.find({'size':{"$lt":1000}}):
    print(file)
#Câu hỏi 4: Tìm tất cả tệp được tạo trong tháng 1 năm 2024.
print("tệp được tạo trong tháng 1 năm 2024")
file_in_1=files_collection.find({"created_at": {"$gte":datetime(2024,1,1),"$lt":datetime(2024,2,1)}})
for file in file_in_1:
    print(file)
#Câu hỏi 5: Cập nhật tên tệp với `file_id` là 4 thành "New Spreadsheet.xlsx".
print("Cập nhật tên tệp với `file_id` là 4 thành 'New Spreadsheet.xlsx'")
files_collection.update_one({"file_id": 4}, {"$set": {"name":"New Spreadsheet.xlsx"}})
for file in files_collection.find():
    print(file)
# Câu hỏi 6: Xóa tất cả tệp có kích thước nhỏ hơn 1000KB.
print("Xóa tất cả tệp có kích thước nhỏ hơn 1000KB")
files_collection.delete_one({ "size":{"$lt":1000}})
for file in files_collection.find():
    print(file)

# Đóng kết nối
client.close()