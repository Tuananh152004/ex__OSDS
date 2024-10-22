

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title("Hệ thống quản lý địa chỉ")
root.geometry("600x800")

# # Kết nối tới db
# conn = sqlite3.connect('address_book.db')
# c = conn.cursor()

# # Tao bang de luu tru
# c.execute('''
#     CREATE TABLE addresses(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         first_name text,
#         last_name text,
#         address text,
#         city text,
#         state text,
#         zipcode interger
#     )
# '''
# )

def them():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    # Lấy dữ liệu đã nhập
    name_value =f_name.get()
    lastName_value = l_name.get()
    address_value = address.get()
    city_value = city.get()
    state_value = state.get()
    zipcode_value = zipcode.get()
    # Thực hiện câu lệnh để thêm
    c.execute('''   
        INSERT INTO 
        addresses (first_name, last_name, address, city, state, zipcode)
        VALUES 
        (:name, :last_name, :address,:city, :state, :zipcode)
    ''',{
        'name' : name_value,
        'last_name' : lastName_value,
        'address': address_value,
        'city': city_value,
        'state': state_value,
        'zipcode': zipcode_value,
      }
    )
    conn.commit()
    conn.close()

    # Reset form
    f_name.delete(0, END)
    l_name.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

def xoa():
    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    # Lấy ID từ ô nhập liệu
    id_value = delete_box.get()
    # Kiểm tra xem ID có tồn tại hay không
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id': id_value})
    record = c.fetchone()

    if record is None:
        # Nếu không tìm thấy bản ghi nào với ID đó, hiện thông báo lỗi
        messagebox.showerror("Lỗi", "ID không tồn tại!")
    else:
# Nếu tìm thấy bản ghi, tiến hành xóa
        c.execute('''DELETE FROM
                            addresses 
                          WHERE id:id''',
                  {'id':id_value})
# Hiên thi thong bao
        messagebox.showinfo("Thông báo", "Đã xóa!")
    delete_box.delete(0, END)
    conn.commit()

    conn.close()

    # Hiển thị lại dữ liệu
    truy_van()


def truy_van():
    # Xóa đi các dữ liệu trong TreeView
    for row in tree.get_children():
        tree.delete(row)

    # Kết nối và lấy dữ liệu
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    c.execute("SELECT * FROM addresses")
    records = c.fetchall()

    # Hien thi du lieu
    for r in records:
        tree.insert("", END, values=(r[0], r[1], r[2]))

    # Ngat ket noi
    conn.close()


def chinh_sua():
    global editor
    editor = Tk()
    editor.title('Cập nhật bản ghi')
    editor.geometry("400x300")

    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = delete_box.get()
    c.execute("SELECT * FROM addresses WHERE id=:id", {'id':record_id})
    records = c.fetchall()

    global f_id_editor, f_name_editor, l_name_editor, address_editor, city_editor, state_editor, zipcode_editor

    f_id_editor = Entry(editor, width=30)
    f_id_editor.grid(row=0, column=1, padx=20, pady=(10, 0))
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=1, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=2, column=1)
    address_editor = Entry(editor, width=30)
    address_editor.grid(row=3, column=1)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=4, column=1)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=5, column=1)
    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=6, column=1)

    f_id_label = Label(editor, text="ID")
    f_id_label.grid(row=0, column=0, pady=(10, 0))
    f_name_label = Label(editor, text="Họ")
    f_name_label.grid(row=1, column=0)
    l_name_label = Label(editor, text="Tên")
    l_name_label.grid(row=2, column=0)
    address_label = Label(editor, text="Địa chỉ")
    address_label.grid(row=3, column=0)
    city_label = Label(editor, text="Thành phố")
    city_label.grid(row=4, column=0)
    state_label = Label(editor, text="Tỉnh/Thành")
    state_label.grid(row=5, column=0)
    zipcode_label = Label(editor, text="Mã bưu chính")
    zipcode_label.grid(row=6, column=0)

    for record in records:
        f_id_editor.insert(0, record[0])
        f_name_editor.insert(0, record[1])
        l_name_editor.insert(0, record[2])
        address_editor.insert(0, record[3])
        city_editor.insert(0, record[4])
        state_editor.insert(0, record[5])
        zipcode_editor.insert(0, record[6])

    edit_btn = Button(editor, text="Lưu bản ghi", command=cap_nhat)
    edit_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

def cap_nhat():
    conn = sqlite3.connect('address_book.db')
    c = conn.cursor()
    record_id = f_id_editor.get()

    c.execute("""UPDATE addresses SET
           first_name = :first,
           last_name = :last,
           address = :address,
           city = :city,
           state = :state,
           zipcode = :zipcode
           WHERE id = :id""",
              {
                  'first': f_name_editor.get(),
                  'last': l_name_editor.get(),
                  'address': address_editor.get(),
                  'city': city_editor.get(),
                  'state': state_editor.get(),
                  'zipcode': zipcode_editor.get(),
                  'id': record_id
              })

    conn.commit()
    conn.close()
    editor.destroy()

    # Cập nhật lại danh sách bản ghi sau khi chỉnh sửa
    truy_van()
def on_tree_select(event):
    # Lấy item được chọn trong Treeview
    selected_item = tree.selection()
    if selected_item:
        # Lấy giá trị của ID từ item được chọn
        item = tree.item(selected_item)
        id_value = item['values'][0]  # Giả sử cột đầu tiên chứa ID
        delete_box.delete(0, END)     # Xóa nội dung ô nhập liệu hiện tại
        delete_box.insert(0, id_value) # Chèn ID vào ô nhập liệu

# Khung cho các ô nhập liệu
input_frame = Frame(root)
input_frame.pack(pady=10)

# Các ô nhập liệu cho cửa sổ chính
f_name = Entry(input_frame, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))
l_name = Entry(input_frame, width=30)
l_name.grid(row=1, column=1)
address = Entry(input_frame, width=30)
address.grid(row=2, column=1)
city = Entry(input_frame, width=30)
city.grid(row=3, column=1)
state = Entry(input_frame, width=30)
state.grid(row=4, column=1)
zipcode = Entry(input_frame, width=30)
zipcode.grid(row=5, column=1)

# Các nhãn
f_name_label = Label(input_frame, text="Họ")
f_name_label.grid(row=0, column=0, pady=(10, 0))
l_name_label = Label(input_frame, text="Tên")
l_name_label.grid(row=1, column=0)
address_label = Label(input_frame, text="Địa chỉ")
address_label.grid(row=2, column=0)
city_label = Label(input_frame, text="Thành phố")
city_label.grid(row=3, column=0)
state_label = Label(input_frame, text="Tỉnh/Thành")
state_label.grid(row=4, column=0)
zipcode_label = Label(input_frame, text="Mã bưu chính")
zipcode_label.grid(row=5, column=0)

# Khung cho các nút chức năng
button_frame = Frame(root)
button_frame.pack(pady=10)

# Các nút chức năng
submit_btn = Button(button_frame, text="Thêm bản ghi", command=them)
submit_btn.grid(row=0, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
query_btn = Button(button_frame, text="Hiển thị bản ghi", command=truy_van)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=137)
delete_box_label = Label(button_frame, text="Chọn ID")
delete_box_label.grid(row=2, column=0, pady=5)
delete_box = Entry(button_frame, width=30)
delete_box.grid(row=2, column=1, pady=5)
delete_btn = Button(button_frame, text="Xóa bản ghi", command=xoa)
delete_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=136)
edit_btn = Button(button_frame, text="Chỉnh sửa bản ghi", command=chinh_sua)
edit_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Khung cho Treeview
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Treeview để hiển thị bản ghi
columns = ("ID", "Họ", "Tên")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
for column in columns:
    tree.column(column, anchor=CENTER) # This will center text in rows
    tree.heading(column, text=column)
tree.pack()

# Định nghĩa tiêu đề cho các cột
for col in columns:
    tree.heading(col, text=col)
# Kết nối sự kiện nhấp chuột với hàm on_tree_select
tree.bind("<ButtonRelease-1>", on_tree_select)
# Gọi hàm truy vấn để hiển thị bản ghi khi khởi động
truy_van()

root.mainloop()