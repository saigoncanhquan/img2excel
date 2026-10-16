import customtkinter as ctk
import tkinter as tk
from tkinterdnd2 import TkinterDnD

from core.activation.auth_manager import AuthManager
from ui.theme import Colors
from ui.main_window import MainWindow
from ui.components.login_frame import LoginFrame

class CTkDnD(ctk.CTk, TkinterDnD.DnDWrapper):
    """Lớp đệm để CustomTkinter tương thích với thư viện TkinterDnD2."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

class Img2ExcelApp(CTkDnD):
    """Cửa sổ root của ứng dụng (Khởi tạo Theme và sự kiện Global)."""
    
    def __init__(self):
        super().__init__()
        
        # 1. Setup Window cơ bản
        self.title("img2excel - Data Extractor")
        self.geometry("1000x650")
        self.minsize(800, 500)
        
        # 2. Áp dụng Theme (Phong cách ChatTingTing Silver Gray & Office Green)
        ctk.set_appearance_mode("light")
        self.configure(fg_color=Colors.BG_MAIN)
        
        # 3. Khởi tạo Logic Managers
        self.auth_manager = AuthManager()
        self.user_email = None
        self.machine_code = None
        
        # 4. Gắn Layout chính
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 5. Hiển thị Màn hình Đăng nhập trước
        self.login_frame = LoginFrame(self, on_login_success=self._on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
        # 6. Lắng nghe sự kiện Global
        self.bind("<FocusIn>", self._check_clipboard)
        self.bind("<Button-1>", self._check_clipboard)
        
    def _on_login_success(self, email: str, machine_code: str):
        """Được gọi khi đăng nhập và xác thực quyền thành công."""
        self.user_email = email
        self.machine_code = machine_code
        
        # Hủy frame đăng nhập
        self.login_frame.destroy()
        
        # Hiển thị màn hình chính
        self.main_window = MainWindow(self)
        self.main_window.grid(row=0, column=0, sticky="nsew")
        
        # Có thể truyền email xuống main_window nếu cần hiển thị
        if hasattr(self.main_window, "show_toast"):
            self.main_window.show_toast(f"Đăng nhập thành công: {email}", Colors.SUCCESS)

    def logout(self):
        """Xử lý đăng xuất: xóa credentials và quay về màn hình đăng nhập."""
        self.user_email = None
        self.machine_code = None
        
        # Xóa session từ GoogleLoginManager
        if hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
            self.login_frame.google_login.logout()
        else:
            from core.activation.google_login import GoogleLoginManager
            GoogleLoginManager().logout()
        
        # Hủy main_window
        if hasattr(self, 'main_window') and self.main_window.winfo_exists():
            self.main_window.destroy()
            
        # Bật lại màn hình Login
        from ui.components.login_frame import LoginFrame
        self.login_frame = LoginFrame(self, on_login_success=self._on_login_success)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        
    def _check_clipboard(self, event=None):
        """Kích hoạt khi cửa sổ nhận lại Focus hoặc click chuột.
        Bắt Clipboard, kiểm tra API Key tự động.
        """
        # Tránh trigger liên tục từ các widget con (chỉ tính khi app nhận focus)
        if event and getattr(event, "widget", None) != self:
            return
            
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text:
                is_valid_and_saved = self.auth_manager.detect_and_save_from_clipboard(clipboard_text)
                
                if is_valid_and_saved:
                    # Báo thành công và xoá clipboard để không lặp lại
                    self.main_window.show_toast("Đã kết nối API thành công!", Colors.SUCCESS)
                    if hasattr(self.main_window, "api_entry"):
                        self.main_window.api_entry.delete(0, "end")
                        self.main_window.api_entry.insert(0, clipboard_text.strip())
                    self.clipboard_clear()
        except (tk.TclError, Exception):
            # Bỏ qua nếu clipboard rỗng hoặc chứa dữ liệu phi văn bản
            pass
