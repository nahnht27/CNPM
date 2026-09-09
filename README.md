# Platform Connecting the Film Photography Community with Darkroom and Studio Services

Nền tảng kết nối cộng đồng nhiếp ảnh phim với các dịch vụ phòng tối, studio và thiết bị nhiếp ảnh.

## I. Tổng quan dự án

### Mục tiêu

Mục tiêu của dự án là xây dựng một nền tảng hỗ trợ cộng đồng nhiếp ảnh phim trong việc tìm kiếm, đặt chỗ và sử dụng các dịch vụ sáng tạo như darkroom, studio và thiết bị nhiếp ảnh.

Hệ thống cung cấp các chức năng quản lý cho Photographer, Service Provider và Administrator, bao gồm tìm kiếm không gian sáng tạo, đặt chỗ, thanh toán, quản lý tài nguyên, workshop và quản lý người dùng.

### Phạm vi

Phạm vi dự án bao gồm các chức năng chính:

* Đăng ký, đăng nhập và quản lý tài khoản người dùng
* Quản lý hồ sơ Photographer và Service Provider
* Tìm kiếm và xem thông tin chi tiết về Creative Space
* Đặt chỗ Creative Space và thuê thiết bị
* Quản lý và theo dõi Booking
* Hủy Booking và thanh toán
* Xem hóa đơn và lịch sử Booking
* Xem và đăng ký Workshop
* Quản lý Creative Space, Equipment và Service Package
* Quản lý Workshop và danh sách người đăng ký
* Quản lý người dùng và Service Provider
* Phê duyệt Service Provider
* Quản lý thông báo và thông tin thanh toán

## II. Các main-flow chính

* Đăng ký / đăng nhập người dùng
* Quản lý hồ sơ cá nhân
* Tìm kiếm và xem chi tiết Creative Space
* Đặt chỗ Creative Space và thuê thiết bị
* Quản lý, xác nhận và từ chối Booking
* Hủy Booking và thực hiện thanh toán
* Xem hóa đơn và lịch sử Booking
* Xem và đăng ký Workshop
* Quản lý Creative Space, Equipment và Service Package
* Quản lý Workshop và người đăng ký
* Quản lý người dùng và Service Provider
* Phê duyệt Service Provider
* Quản lý thông báo và thông tin thanh toán

## III. Công nghệ triển khai

### Frontend

* HTML
* CSS
* JavaScript
* Fetch API

### Backend

* Python
* Flask
* Clean Architecture
* SQLAlchemy
* Repository Pattern

### Database

* PostgreSQL
* Supabase

### Development Tools

* Visual Studio Code
* Git
* GitHub

## IV. Các tasks chính

* Phân tích yêu cầu hệ thống và xác định các nghiệp vụ chính
* Xây dựng Feature Decomposition Diagram (FDD), Use Case Diagram, Activity Diagram, Sequence Diagram và Entity Relationship Diagram (ERD)
* Thiết kế kiến trúc phần mềm và cơ sở dữ liệu
* Xây dựng REST API cho hệ thống
* Phát triển giao diện Web cho Photographer
* Phát triển giao diện Web cho Service Provider
* Phát triển giao diện Web cho Administrator
* Xây dựng chức năng xác thực và quản lý tài khoản
* Xây dựng chức năng tìm kiếm và xem Creative Space
* Xây dựng chức năng Booking và quản lý tài nguyên
* Xây dựng chức năng thanh toán và hóa đơn
* Xây dựng chức năng Workshop
* Xây dựng chức năng quản lý Creative Space, Equipment và Service Package
* Xây dựng chức năng quản lý người dùng và Service Provider
* Xây dựng chức năng phê duyệt Service Provider
* Kiểm thử chức năng và kiểm thử tích hợp
* Hoàn thiện tài liệu SRS và báo cáo Capstone

## V. Cấu trúc dự án

```text
CNPM/
├── Doc/
│   └── SRS/
│       ├── Chapter/
│       ├── images/
│       ├── diagram/
│       └── main.tex
│
├── Flask-cleanArchitecture/
│   ├── src/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   ├── scripts/
│   │   ├── services/
│   │   └── app.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── admin/
│   ├── components/
│   ├── photographer/
│   ├── provider/
│   ├── css/
│   ├── js/
│   └── *.html
│
└── README.md