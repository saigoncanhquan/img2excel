import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from core.activation.google_login import GoogleLoginManager
from ui.theme import Colors

class LoginFrame(ctk.CTkFrame):
    """Giao diện đăng nhập bắt buộc."""
    
    def __init__(self, master, on_login_success):
        super().__init__(master, fg_color=Colors.BG_MAIN)
        self.master = master
        self.on_login_success = on_login_success
        
        self.google_login = GoogleLoginManager()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # UI Elements
        self.title_label = ctk.CTkLabel(
            self, text="IMG2EXCEL", 
            font=("Segoe UI", 36, "bold"), text_color=Colors.ACCENT
        )
        self.title_label.grid(row=1, column=0, pady=(0, 10))
        
        self.desc_label = ctk.CTkLabel(
            self, text="Vui lòng đăng nhập để sử dụng phần mềm", 
            font=("Segoe UI", 16), text_color=Colors.TEXT_MUTED
        )
        self.desc_label.grid(row=2, column=0, pady=(0, 30))
        
        self.login_btn = ctk.CTkButton(
            self, text="Đăng nhập bằng Google",
            font=("Segoe UI", 16, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            height=45,
            width=250,
            command=self._handle_login
        )
        self.login_btn.grid(row=3, column=0, sticky="n")
        
        # Check auto login
        self.after(200, self._check_auto_login)

    def _check_auto_login(self):
        """Kiểm tra xem có token cũ hợp lệ không."""
        self.login_btn.configure(state="disabled", text="Đang kiểm tra...")
        
        if self.google_login.load_saved_token() and self.google_login.user_email:
            self._verify_access(self.google_login.user_email)
        else:
            self.login_btn.configure(state="normal", text="Đăng nhập bằng Google")

    def _handle_login(self):
        """Xử lý nút bấm đăng nhập."""
        self.login_btn.configure(state="disabled", text="Đang mở trình duyệt...")
        
        def _login_worker():
            success, info = self.google_login.login()
            self.after(0, lambda: self._process_login_result(success, info))
            
        import threading
        threading.Thread(target=_login_worker, daemon=True).start()

    def _process_login_result(self, success, info):
        if success:
            self._verify_access(info)
        else:
            messagebox.showerror("Lỗi đăng nhập", info)
            self.login_btn.configure(state="normal", text="Đăng nhập bằng Google")

    def _verify_access(self, email: str):
        """Kiểm soát quyền truy cập thông qua Strategy Pattern (Giai đoạn 1: Sheets Webhook)."""
        self.login_btn.configure(text="Đang xác thực quyền...")
        self.update()
        
        def _worker():
            from core.activation.licensing import OnlineSheetsLicenseProvider
            from utils.constants import REGISTRY_SUBMIT_URL
            
            # Giai đoạn 1: Online Sheets. Tương lai sẽ thay bằng BinaryFragmentLicenseProvider
            provider = OnlineSheetsLicenseProvider(webhook_url=REGISTRY_SUBMIT_URL)
            context = provider.verify_license(email)
            
            self.after(0, lambda: self._handle_verify_result(context))
            
        import threading
        threading.Thread(target=_worker, daemon=True).start()

    def _handle_verify_result(self, context):
        if not context.can_access_app():
            messagebox.showerror("Từ chối truy cập", context.message)
            self._reset_ui()
            return

        # Lưu context vào master để các module khác (như QuotaManager) sử dụng
        self.master.license_context = context
        
        # Cho phép truy cập
        self.on_login_success(context.email, context.machine_code)

    def _reset_ui(self):
        self.login_btn.configure(state="normal", text="Đăng nhập bằng Google")
        self.google_login.logout()
