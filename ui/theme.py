class Colors:
    """Bảng màu chủ đạo theo phong cách ChatTingTing (Silver Gray & Accent Green)."""
    # ── Nền tổng thể & Phân cấp khối ──────────────────────────
    BG_MAIN = "#B2B2B2"          # Nền chính xám bạc đặc trưng của ChatTingTing
    BG_SIDEBAR = "#C8C8C8"       # Nền sidebar phân tách nhẹ nhàng với main
    BG_CARD = "#DFDFDF"          # Nền thẻ / card / danh sách / panel
    BG_HOVER = "#D0D0D0"         # Hover cho các nút trung tính
    BG_INPUT = "#DFDFDF"         # Nền ô nhập liệu
    BORDER = "#8A8A8A"           # Viền sắc nét chuẩn ChatTingTing
    BORDER_LIGHT = "#9A9A9A"     # Viền nhẹ

    # ── Màu nhấn chủ đạo (Office / Excel / ChatTingTing Green) ──
    ACCENT = "#107C41"           # Xanh lá Office / ChatTingTing
    ACCENT_HOVER = "#128E4A"     # Hover xanh lá sáng hơn
    ACCENT_ACTIVE = "#0C6132"    # Trạng thái nhấn

    # ── Màu chữ (High contrast trên nền xám bạc) ───────────────
    TEXT_MAIN = "#262626"        # Chữ đen xám đậm dễ đọc
    TEXT_MUTED = "#595959"       # Chữ phụ / chú thích / placeholder
    TEXT_ON_ACCENT = "#FFFFFF"   # Chữ trắng tương phản tuyệt đối trên nút ACCENT
    TEXT_WHITE = "#FFFFFF"       # Chữ trắng dùng cho badge / toast

    # ── Trạng thái thông báo ───────────────────────────────────
    SUCCESS = "#107C41"          # Thành công (trùng màu thương hiệu)
    SUCCESS_HOVER = "#0E6B38"
    DANGER = "#D13438"           # Đỏ cảnh báo / lỗi
    DANGER_HOVER = "#B32C30"
    WARNING = "#D89C00"          # Vàng cảnh báo
    WARNING_HOVER = "#B28000"
    INFO = "#0078D4"             # Xanh dương thông tin


class Fonts:
    """Định nghĩa Font chữ chung toàn ứng dụng (Segoe UI)."""
    DEFAULT = ("Segoe UI", 13)
    H1 = ("Segoe UI", 24, "bold")
    H2 = ("Segoe UI", 18, "bold")
    SMALL = ("Segoe UI", 11)
