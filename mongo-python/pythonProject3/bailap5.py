# import
from xmlrpc.client import DateTime

from pymongo import MongoClient
from datetime import datetime
# b1: ket noi den MongoDb
client = MongoClient('localhost', 27017)
client.drop_database('facebookData1')
db = client['facebookData1']

# b2: Tap cac collections
users_collection = db['user']
posts_collection = db['post']
comments_collection = db['comments']

# b3: Them giu lieu nguoi dung
users_data = [
    { 'user_id': 1, 'name': "Nguyen Van A", 'email': "a@gmail.com", 'age': 25 },
    { 'user_id': 2, 'name': "Tran Thi B", 'email': "b@gmail.com", 'age': 30 },
    { 'user_id': 3, 'name': "Le Van C", 'email': "c@gmail.com", 'age': 22 }
]
users_collection.insert_many(users_data) # Thêm dữ liệu người dùng
# Bước 4: Thêm dữ liệu posts
posts_data=[{ 'post_id': 1, 'user_id': 1, 'content': "Hôm nay thật đẹp trời!", 'created_at': datetime(2024,10,1) },
    { 'post_id': 2, 'user_id': 2, 'content': "Mình vừa xem một bộ phim hay!", 'created_at': datetime(2024,10,2) },
    { 'post_id': 3, 'user_id': 1, 'content': "Chúc mọi người một ngày tốt lành!", 'created_at': datetime(2024,10,3) }]
posts_collection.insert_many(posts_data)  # Thêm dữ liệu
# b3: Them giu lieu comments
comments_data=[{ 'comment_id': 1, 'post_id': 1, 'user_id': 2, 'content': "Thật tuyệt vời!", 'created_at': datetime(2024,10,1) },
    { 'comment_id': 2, 'post_id': 2, 'user_id': 3, 'content': "Mình cũng muốn xem bộ phim này!", 'created_at': datetime(2024,10,2) },
    { 'comment_id': 3, 'post_id': 3, 'user_id': 1, 'content': "Cảm ơn bạn!", 'created_at': datetime(2024,10,3)}]
comments_collection.insert_many(comments_data)

# b5: truy van du lieu
# xem tat ca nguoi dung
print(" Tất Cả Người Dùng ")
for user in users_data:
    print(user)
# xem tat ca bai dang cua user_id = 1
print(" Tất Cả Bài Đăng Của user_id:1 ")
post_user1 = posts_collection.find({'user_id': 1})
for post in post_user1:
    print(post)
#  Truy vấn người dùng có độ tuổi trên 25
print(" Người dùng có tuổi trên 25  ")
user_age25=users_collection.find({'age': {'$gt':25}})
for user in user_age25:
    print(user)
# Truy vấn tất cả bài đăng được tạo trong tháng 10
print("  Truy vấn tất cả bài đăng được tạo trong tháng 10 ")
post_in_10=posts_collection.find({'created_at': {'$gte':datetime(2024,10,1),'$lt':datetime(2024,11,1)}})
for post in post_in_10:
    print(post)
#Bước 6: Cập Nhật và Xóa Dữ Liệu
#Cập nhật nội dung bài đăng của người dùng với post_id = 1
posts_collection.update_one({'post_id':1},{'$set':{"content":'Hôm nay thời tiết thật đẹp!'}})
print(" Nội dung post mới ")
for post in posts_collection.find():
    print(post)
# Xóa bình luận với comment_id = 2
print(" Xóa commnet ")
comments_collection.delete_one({'comment_id':2})
for comment in comments_collection.find():
    print(comment)
# Xem lại dữ liệu sau khi cập nhật và xóa
print(" xem lại tất cả bài đăng")
for post in posts_collection.find():
    print(post)
print(" xem lại tất cả các bình luận ")
for comment in comments_collection.find():
    print(comment)
# Đóng kết nối
client.close()
