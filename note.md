### Adminpwd:

### 📄 **Markdown Tổng Hợp Lệnh Quản Lý Odoo & Backup**

---

# 🚀 Docker Compose Lệnh Quản Lý Odoo + Backup

## 1. Khởi động, dừng hệ thống Odoo

# 🚀 Khởi động Odoo + PostgreSQL
docker compose up -d

# 🛑 Dừng các container Odoo + PostgreSQL
docker compose down

# 🛑 Dừng mà KHÔNG xóa volume (giữ dữ liệu)
docker compose stop

# ❌ Dừng và XÓA hết cả volume (cẩn thận!)
docker compose down -v

---

## 2. Xem log Odoo & PostgreSQL

# 🔍 Xem log real-time
docker compose logs -f

# 🔍 Xem log riêng service Odoo
docker compose logs -f odoo

# 🔍 Xem log PostgreSQL
docker compose logs -f db

---

## 3. Quản lý module Odoo

# 🔄 Cập nhật lại Odoo module (migrate)
docker compose exec odoo odoo -u all -d <ten_database> --stop-after-init

---

## 4. Truy cập vào container

# 🐚 Vào bên trong container Odoo
docker compose exec odoo bash

# 🐚 Vào bên trong container PostgreSQL
docker compose exec db bash

---

## 5. Backup thủ công & Cleanup

# 🗃 Backup dữ liệu thủ công (tạo file .tar.gz)
docker compose run --rm backup

# 🗑️ Xóa backup và chỉ giữ lại 10 file mới nhất
ls -1t ./backups/backup_*.tar.gz | tail -n +11 | xargs -r rm -- && echo "Đã giữ lại 10 bản backup mới nhất."

# 🗃 Backup mới và 🗑️ cleanup ngay sau đó (giữ lại 10 bản)
docker compose run --rm backup && \
ls -1t ./backups/backup_*.tar.gz | tail -n +11 | xargs -r rm -- && \
echo "Backup xong, đã giữ lại 10 bản backup mới nhất."

---

## 6. Kiểm tra backup và dung lượng

# 📂 Hiển thị các file backup
ls -lh ./backups/backup_*.tar.gz

# 📦 Xem dung lượng thư mục backups
du -sh ./backups

---

## 7. Xem nội dung file backup

# 🔍 Liệt kê file bên trong backup
tar tzf ./backups/backup_YYYYMMDD_HHMMSS.tar.gz

---

## 8. Đổi tên file backup quan trọng

# 📅 Đổi tên backup theo ghi chú
mv ./backups/backup_20250429_021500.tar.gz ./backups/projectA_before_update.tar.gz

---

## 9. Cập nhật backup "mới nhất" và xóa bản cũ cùng tên

# 🔄 Tạo backup mới, cập nhật thành latest_backup.tar.gz
rm -f ./backups/latest_backup.tar.gz && \
docker compose run --rm backup && \
mv ./backups/backup_*.tar.gz ./backups/latest_backup.tar.gz && \
echo "Backup mới nhất đã được cập nhật."

---

# ✅ Lưu ý:
- Thay <ten_database> bằng tên database thực tế.
- Dùng chmod +x nếu tạo script file .sh.
