# HƯỚNG DẪN SỬ DỤNG PHẦN MỀM IMG2EXCEL
> **Phần mềm chuyển đổi ảnh chụp, hóa đơn & Căn cước công dân (CCCD) sang Excel bằng Trí tuệ Nhân tạo (AI)**

---

## 📖 MỤC LỤC
1. [Giới thiệu về img2excel](#1-giới-thiệu-về-img2excel)
2. [Cài đặt & Đăng nhập lần đầu](#2-cài-đặt--đăng-nhập-lần-đầu)
3. [Hướng dẫn lấy và cài đặt Google API Key (Miễn phí 100%)](#3-hướng-dẫn-lấy-và-cài-đặt-google-api-key-miễn-phí-100)
4. [Hướng dẫn sử dụng chi tiết](#4-hướng-dẫn-sử-dụng-chi-tiết)
   - [Chế độ 1: Trích xuất danh sách Căn cước công dân (CCCD)](#chế-độ-1-trích-xuất-danh-sách-căn-cước-công-dân-cccd)
   - [Chế độ 2: Trích xuất Bảng biểu / Hóa đơn / Tài liệu tổng quát](#chế-độ-2-trích-xuất-bảng-biểu--hóa-đơn--tài-liệu-tổng-quát)
5. [Xem trước kết quả & Mở file Excel](#5-xem-trước-kết-quả--mở-file-excel)
6. [Hạn mức & Hướng dẫn nâng cấp bản Pro tự động](#6-hạn-mức--hướng-dẫn-nâng-cấp-bản-pro-tự-động)
7. [Mẹo chụp ảnh / Scan để đạt độ chính xác 100%](#7-mẹo-chụp-ảnh--scan-để-đạt-độ-chính-xác-100)
8. [Các câu hỏi thường gặp (FAQ) & Xử lý lỗi](#8-các-câu-hỏi-thường-gặp-faq--xử-lý-lỗi)

---

## 1. Giới thiệu về img2excel

**img2excel** là công cụ thông minh giúp bạn tiết kiệm hàng giờ gõ tay văn bản. Bạn chỉ cần đưa ảnh chụp hoặc tệp PDF vào, ứng dụng sẽ tự động đọc dữ liệu và điền vào bảng tính Excel một cách hoàn hảo:

- 🪪 **Chuyên biệt cho Căn cước công dân (CCCD):** Đọc chính xác cả CCCD gắn chip, mã vạch, CMND cũ và Thẻ Căn cước mẫu mới 2024. Đọc nhiều ảnh/PDF cùng lúc và **gộp chung vào 1 file Excel duy nhất**.
- 📊 **Trích xuất Bảng biểu & Hóa đơn:** Đọc hóa đơn mua bán, bảng chấm công, bảng kê, bảng báo giá... giữ nguyên cấu trúc hàng và cột.
- 🎯 **Không bao giờ mất số `0` ở đầu:** Tự động giữ chuẩn định dạng văn bản cho số CCCD (ví dụ: `00120...`), số điện thoại, ngày tháng năm sinh.
- ⚡ **Giao diện hiện đại, dễ dùng:** Kéo thả chuột tiện lợi, nút bấm to rõ ràng, hỗ trợ tiếng Việt có dấu 100%.

---

## 2. Cài đặt & Đăng nhập lần đầu

### 2.1 Mở ứng dụng
1. Tải về bộ cài đặt hoặc tệp chạy `img2excel.exe`.
2. Nhấp đúp chuột vào biểu tượng **img2excel** để mở ứng dụng.

### 2.2 Đăng nhập bằng Google
Khi mở lần đầu, bạn sẽ thấy màn hình đăng nhập:
1. Bấm nút màu xanh **"Đăng nhập bằng Google"**.
2. Trình duyệt web mặc định của bạn sẽ tự động mở trang xác thực tài khoản Google.
3. Chọn tài khoản Gmail của bạn và bấm **Cho phép** (hoặc Đăng nhập).
4. Sau khi đăng nhập thành công, trình duyệt sẽ báo hoàn tất và phần mềm **img2excel** sẽ tự động mở ra màn hình làm việc chính.

> 💡 **Lưu ý:** Phần mềm sẽ tự động ghi nhớ phiên đăng nhập. Ở những lần mở sau, bạn sẽ vào thẳng phần mềm mà không cần đăng nhập lại.

---

## 3. Hướng dẫn lấy và cài đặt Google API Key (Miễn phí 100%)

Để phần mềm có thể sử dụng Trí tuệ Nhân tạo Google AI đọc được chữ trong ảnh, bạn cần trang bị một "Mã chìa khóa" (API Key) của Google. Mã này được Google **cung cấp miễn phí 100%** cho mỗi tài khoản Gmail cá nhân.

Bạn chỉ cần thực hiện bước này **DUY NHẤT 1 LẦN**:

### Các bước lấy API Key (chưa đầy 1 phút):
1. Trên giao diện bên trái của img2excel, tìm mục **"Google Gemini API Key"** và bấm nút **"Lấy Key Web"** *(hoặc truy cập trực tiếp trang web [aistudio.google.com](https://aistudio.google.com/app/apikey))*.
2. Đăng nhập bằng tài khoản Gmail của bạn nếu web yêu cầu.
3. Nhấp vào nút màu xanh **"Create API key"** (Tạo API Key).
4. Chọn **"Create API key in new project"** (Tạo trong dự án mới).
5. Trang web sẽ hiện ra một dãy ký tự dài bắt đầu bằng `AIzaSy...`. Hãy bấm nút **Copy** (Sao chép).

### Cài đặt vào ứng dụng:
1. Quay lại cửa sổ phần mềm **img2excel**.
2. Bấm nút **"Dán"** (hoặc dán vào ô nhập liệu rồi bấm **"Lưu"**).
3. Màn hình sẽ hiện thông báo xanh: **"Đã kết nối API thành công!"**. Từ lúc này, bạn đã sẵn sàng sử dụng!

---

## 4. Hướng dẫn sử dụng chi tiết

---

### Chế độ 1: Trích xuất danh sách Căn cước công dân (CCCD)
*(Dành cho phòng nhân sự, kế toán, văn phòng công chứng, bảo hiểm, ngân hàng, trường học...)*

Chế độ này cho phép bạn đưa vào hàng chục hoặc hàng trăm ảnh chụp CCCD (mặt trước/mặt sau) hoặc file scan PDF nhiều trang. Phần mềm sẽ nhận diện từng người và xuất tất cả ra **1 tệp Excel tổng hợp**.

#### Các bước thực hiện:
1. Ở góc trên bên phải màn hình, chọn thẻ: **"Danh sách CCCD"**.
2. **Thêm tài liệu:**
   - Cách 1: Bấm nút **"Chọn tệp"** để chọn các ảnh (`.jpg`, `.jpeg`, `.png`, `.webp`) hoặc file `.pdf` từ máy tính.
   - Cách 2: **Kéo và thả** trực tiếp các tệp từ thư mục Windows vào vùng khung xám giữa màn hình.
3. Kiểm tra danh sách tệp hiển thị. Nếu muốn bỏ tệp nào, bạn có thể xóa tệp đó khỏi danh sách.
4. Bấm nút lớn màu xanh: **"Bắt đầu trích xuất sang Excel"**.
5. Phần mềm sẽ lần lượt xử lý từng trang, thanh tiến trình màu xanh sẽ báo % hoàn thành.
6. Khi hoàn tất, file Excel có tên `Danh_sach_CCCD.xlsx` sẽ tự động được lưu cùng thư mục với các tệp ảnh/PDF của bạn.

#### Dữ liệu tự động bóc tách vào Excel bao gồm:
| Cột trong Excel | Mô tả chi tiết |
| :--- | :--- |
| **Loại thẻ** | Nhận diện rõ: CCCD gắn chip, Căn cước 2024, CMND 9 số / 12 số |
| **Số CMND/CCCD** | Chuẩn 12 chữ số, **giữ nguyên số 0 ở đầu** (dạng văn bản chuẩn) |
| **Họ và tên** | Tên đầy đủ có dấu viết hoa chuẩn Tiếng Việt |
| **Ngày sinh** | Định dạng ngày/tháng/năm |
| **Giới tính** | Nam / Nữ |
| **Quốc tịch** | Việt Nam |
| **Quê quán** | Xã/Phường, Quận/Huyện, Tỉnh/Thành phố |
| **Nơi thường trú** | Địa chỉ ghi trên mặt sau hoặc mặt trước thẻ |
| **Ngày cấp** | Ngày cấp căn cước |
| **Ngày hết hạn** | Thời hạn sử dụng thẻ |
| **Nơi cấp** | Cục Cảnh sát ĐKQL cư trú hoặc Bộ Công an |

---

### Chế độ 2: Trích xuất Bảng biểu / Hóa đơn / Tài liệu tổng quát
*(Dành cho người cần số hóa hóa đơn giấy, bảng kê chứng từ, bảng chấm công, hợp đồng dạng bảng...)*

Chế độ này quét tài liệu và phát hiện mọi bảng biểu có trong tài liệu, sau đó tái tạo chính xác thành các ô dòng/cột trong Excel.

#### Các bước thực hiện:
1. Ở góc trên bên phải, bấm chọn thẻ: **"Tài liệu / Hóa đơn"**.
2. Kéo thả hoặc bấm **"Chọn tệp"** để tải lên hóa đơn, chứng từ (ảnh chụp hoặc PDF).
3. Bấm **"Bắt đầu trích xuất sang Excel"**.
4. Ứng dụng sẽ tự động phân tích hàng và cột, sau đó xuất ra file Excel tương ứng với từng tài liệu.

---

### Các nút điều khiển trong khi trích xuất
Trong quá trình phần mềm đang xử lý, nếu cần điều chỉnh bạn có thể dùng các nút:
- **Tạm dừng / Tiếp tục:** Tạm dừng tiến trình nếu bạn muốn tạm hoãn để làm việc khác, sau đó bấm tiếp tục để chạy tiếp.
- **Dừng:** Hủy tiến trình hiện tại.
- **Xuất kết quả hiện có:** Nếu bạn đưa vào 100 trang nhưng đang xử lý đến trang 30 mà cần dùng gấp, bấm nút này để xuất ngay 30 trang đầu vào Excel.

---

## 5. Xem trước kết quả & Mở file Excel

Ngay sau khi quá trình trích xuất hoàn tất, giao diện sẽ chuyển sang màn hình **Xem trước dữ liệu**:

1. **Bảng xem trước:** Hiển thị 5-6 dòng kết quả đầu tiên để bạn kiểm tra nhanh độ chính xác của thông tin mà không cần mở Excel.
2. **Nút "Mở file Excel":** Bấm nút màu xanh để mở ngay tệp Excel vừa tạo bằng ứng dụng Microsoft Excel hoặc WPS Office trên máy bạn.
3. **Nút "Mở thư mục chứa":** Mở thư mục trên máy tính nơi file Excel được lưu trữ để bạn dễ dàng gửi qua Zalo, Email hoặc đưa lên Google Drive.
4. **Tùy chọn "Tự động mở file khi hoàn tất":** Nếu tích chọn ô này, file Excel sẽ tự động bật lên ngay khi vừa xuất xong.

---

## 6. Hạn mức & Hướng dẫn nâng cấp bản Pro tự động

### 6.1 Gói Miễn phí (Free)
- Khi bắt đầu sử dụng, bạn có hạn mức miễn phí: **20 trang/lần xử lý** và **500 trang/ngày**.
- Quota còn lại luôn được hiển thị ở góc trên bên trái màn hình (`Quota: ... trang`).

### 6.2 Nâng cấp lên Gói Pro (Kích hoạt tức thì bằng VietQR)
Khi có nhu cầu xử lý khối lượng lớn tài liệu không giới hạn, bạn có thể nâng cấp lên Gói Pro với quy trình thanh toán hoàn toàn tự động 24/7:

1. Bấm vào nút **"Nâng cấp Pro"** ở thanh menu bên trái.
2. **Chọn gói thời hạn phù hợp:**
   - 🌟 Gói 1 Tháng
   - 🌟 Gói 6 Tháng
   - 🌟 Gói 1 Năm
3. Bấm nút **"Tiếp tục thanh toán"**.
4. Màn hình sẽ hiện ra **Mã QR chuyển khoản ngân hàng (Napas 247)** kèm đầy đủ:
   - Số tiền chính xác.
   - Nội dung chuyển khoản định danh riêng cho máy của bạn (Ví dụ: `IMGX...`).
5. **Thanh toán:**
   - Mở ứng dụng ngân hàng bất kỳ trên điện thoại (Vietcombank, MB, Techcombank, Sacombank, VPBank, MoMo...).
   - Chọn chức năng **Quét mã QR** và quét mã hiển thị trên màn hình máy tính.
   - Xác nhận chuyển tiền (Nội dung và số tiền đã được điền tự động chính xác 100%).
6. **Kích hoạt tức thì:**
   - Trong vòng 5-10 giây sau khi chuyển tiền thành công, phần mềm sẽ tự động nhận diện và hiện thông báo **"Kích hoạt thành công!"**.
   - Hạn mức sẽ được mở khóa ngay lập tức mà bạn không cần phải chụp biên lai hay chờ đợi hỗ trợ viên duyệt thủ công.

---

## 7. Mẹo chụp ảnh / Scan để đạt độ chính xác 100%

Mặc dù Trí tuệ Nhân tạo của img2excel rất mạnh mẽ, việc cung cấp ảnh đầu vào rõ nét sẽ giúp độ chính xác đạt mức tuyệt đối:

- 📸 **Tránh lóa sáng bóng đèn:** Khi chụp CCCD có lớp ép nhựa bóng, hãy nghiêng góc chụp một chút hoặc tắt bớt đèn rọi trực diện để không bị vệt sáng trắng che mất chữ số.
- 📐 **Chụp phẳng và đủ 4 góc:** Đặt thẻ hoặc hóa đơn trên mặt phẳng có màu tương phản (ví dụ: mặt bàn gỗ tối màu). Chụp thẳng từ trên xuống, không bị nghiêng chéo quá mức.
- 🔍 **Độ nét rõ ràng:** Đảm bảo camera lấy nét vào các dòng chữ nhỏ như "Nơi thường trú", "Quê quán". Tránh chụp khi tay đang rung lắc.
- 📑 **Đối với tệp PDF scan:** Hãy đặt máy scan ở độ phân giải khuyến nghị từ **200 DPI đến 300 DPI**.

---

## 8. Các câu hỏi thường gặp (FAQ) & Xử lý lỗi

### ❓ Câu 1: Tại sao khi mở file Excel, số CCCD vẫn giữ nguyên số 0 ở đầu?
**Trả lời:** img2excel được lập trình đặc biệt để tự động áp dụng định dạng văn bản (`Text`) cho cột số định danh và số điện thoại. Do đó, các số có chữ số 0 đầu như `00120...` hay `0912...` sẽ không bao giờ bị Excel tự động xóa mất số 0 như khi bạn copy-paste thông thường.

### ❓ Câu 2: Thông báo lỗi: "Hết hạn mức API Google (429)" hoặc "Hệ thống AI đang quá tải (503)" là gì?
**Trả lời:** 
- Lỗi **429**: Bạn đã gửi yêu cầu quá nhanh trong 1 phút so với gói miễn phí của Google. Bạn chỉ cần chờ khoảng **1-2 phút** rồi bấm chạy lại.
- Lỗi **503**: Máy chủ Google tạm thời bận. Phần mềm có cơ chế tự động chờ và thử lại, bạn hãy thử lại sau vài giây.

### ❓ Câu 3: Dữ liệu hình ảnh và thông tin của tôi có bị lộ ra ngoài không?
**Trả lời:** Hoàn toàn an toàn và bảo mật. Toàn bộ hình ảnh được xử lý trực tiếp từ máy tính của bạn gửi qua đường truyền mã hóa SSL/HTTPS tới máy chủ trí tuệ nhân tạo chính thức của Google để phân tích và trả dữ liệu về máy bạn. Phần mềm không lưu trữ ảnh hay hồ sơ của bạn lên bất kỳ máy chủ bên thứ ba nào.

### ❓ Câu 4: Tôi cài lại Windows hoặc đổi máy tính thì gói Pro có dùng tiếp được không?
**Trả lời:** Có. Bạn chỉ cần liên hệ với bộ phận hỗ trợ khách hàng và cung cấp lại mã đơn hàng chuyển khoản trước đó để được cấp mã chuyển quyền sang máy tính mới.

---

> 📞 **Hỗ trợ & Đóng góp ý kiến:**  
> Nếu bạn gặp khó khăn trong quá trình sử dụng hoặc cần hỗ trợ thêm tính năng, vui lòng liên hệ qua kênh hỗ trợ đính kèm trong phần mềm hoặc truy cập [excelcappy.blogspot.com](https://excelcappy.blogspot.com/).
