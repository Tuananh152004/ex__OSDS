# import
from pymongo import MongoClient
from datetime import datetime
# b1: ket noi den MongoDb
client = MongoClient('localhost', 27017)
client.drop_database('tiktokABC')
db = client['tiktokABC']

# b2: Tap cac collections
users_collection = db['user']
videos_collection = db['video']

# b3: Them giu lieu nguoi dung
users_data = [
    { 'user_id': 1, 'username': 'user1', 'full_name': 'Nguyen Van A', 'followers': 1500, 'following': 200 },
    { 'user_id': 2, 'username': 'user2', 'full_name': 'Tran Thi B', 'followers': 2000, 'following': 300 },
    { 'user_id': 3, 'username': 'user3', 'full_name': 'Le Van C', 'followers': 500, 'following': 100 }
]
users_collection.insert_many(users_data)  # Thêm dữ liệu người dùng
# Bước 4: Thêm dữ liệu video
videos_data = [
    { 'video_id': 1, 'user_id': 1, 'title': 'Video 1', 'views': 10000, 'likes': 500, 'created_at': datetime(2024, 1, 1) },
    { 'video_id': 2, 'user_id': 2, 'title': 'Video 2', 'views': 20000, 'likes': 1500, 'created_at': datetime(2024, 1, 5) },
    { 'video_id': 3, 'user_id': 3, 'title': 'Video 3', 'views': 5000, 'likes': 200, 'created_at': datetime(2024, 1, 10) }
]
videos_collection.insert_many(videos_data)  # Thêm dữ liệu video

# b5: Truy van du lieu
#5.1: Xem tat ca nguoi dung
print(" Tất Cả Người Dùng")
for user in users_collection.find():
    print(user)
#5.2 Tìm video có nhiều view nhất
print(" Tìm videos Có Nhiều Người Xem Nhất")
most_viewed_video = videos_collection.find().sort('views', -1).limit(1)
for video in most_viewed_video:
    print(video)
#5.3 Tìm tất cả video của người dùng có username là user1
print("\n Tất cả video của người dùng 'user1': ")
user_video = videos_collection.find_one({'user_id': 1})
for video in user_video:
    print(video)
# B6: Cập nhật dữ liệu
# Cập nhật số người theo dõi của người dùng với 'user_id' là 1 lên 2000
users_collection.update_one({'user_id': 1}, {'$set': {'followers': 2000}})
# Bước 7: Xóa video có `video_id` là 3
videos_collection.delete_one({'video_id': 3})
# Bước 8: Xem lại dữ liệu sau khi cập nhật và xóa
print("\nDữ liệu người dùng sau khi cập nhật:")
for user in users_collection.find():
    print(user)

print("\nDữ liệu video sau khi xóa:")
for video in videos_collection.find():
    print(video)

# Đóng kết nối
client.close()