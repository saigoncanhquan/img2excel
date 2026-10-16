import threading
import customtkinter as ctk
from customtkinter import filedialog
from pathlib import Path

from core.quota.manager import QuotaManager, QuotaExceededError
from core.ocr.preprocessor import Preprocessor
from core.gemini.extractor import GeminiExtractor
from ui.theme import Colors, Fonts
from ui.components.file_picker import FilePicker
from ui.components.result_preview import ResultPreview
from ui.components.payment_dialog import PlanSelectionDialog, PaymentDialog
from client.config import ClientConfig
from client.licensing_core import LicensingClient
from utils.logger import log_error

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Khởi tạo dữ liệu Quota & Licensing Client
        self.quota_manager = QuotaManager()
        self.licensing_client = LicensingClient()
        self._sync_license_status()
        
        # Chia layout 2 cột
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0, minsize=260)  # Sidebar cố định
        self.grid_columnconfigure(1, weight=1)               # Workspace linh hoạt
        
        self._build_sidebar()
        self._build_workspace()
        
    def _build_sidebar(self):
        """Khung Sidebar bên trái (Quản lý kết nối, Cài đặt, Thông tin Quota)."""
        self.sidebar = ctk.CTkFrame(self, fg_color=Colors.BG_SIDEBAR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Đẩy nút Cài đặt và Đăng xuất xuống đáy
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # 1. Tiêu đề Logo (Màu xanh thương hiệu ChatTingTing)
        title = ctk.CTkLabel(self.sidebar, text="img2excel", font=Fonts.H1, text_color=Colors.ACCENT)
        title.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")
        
        # 2. Quota Badge & License Status
        # Đọc thông tin từ LicenseContext
        context = getattr(self.master, 'license_context', None)
        status_text = f"[{context.status}] " if context else "[FREE] "
        
        # Override quota manager limit theo chính sách từ server TRƯỚC KHI TÍNH REMAINING
        if context:
            self.quota_manager.batch_limit = context.max_batch_size
            self.quota_manager.daily_limit = context.daily_quota
            self.quota_manager.hourly_limit = getattr(context, 'hourly_quota', 0)
        
        try:
            quota_remaining = self.quota_manager.get_remaining_quota()
        except Exception:
            quota_remaining = 0
            
        self.quota_badge = ctk.CTkLabel(
            self.sidebar, 
            text=f"{status_text}Quota: {quota_remaining} trang", 
            font=Fonts.SMALL,
            fg_color=Colors.SUCCESS if context and context.status in ("PRO", "LIFETIME") else Colors.BORDER,
            text_color=Colors.TEXT_ON_ACCENT if context and context.status in ("PRO", "LIFETIME") else Colors.TEXT_MAIN,
            corner_radius=12,
            height=28
        )
        self.quota_badge.grid(row=1, column=0, padx=20, pady=(0, 8), sticky="w")
        
        # 2.1 Nút Mua bản quyền / Nâng cấp Pro
        self.btn_upgrade = ctk.CTkButton(
            self.sidebar,
            text="⭐ Nâng cấp Pro ⭐",
            font=("Segoe UI", 12, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            height=32,
            command=self._open_plan_selection
        )
        self.btn_upgrade.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        if context:
            if context.status in ("PRO", "LIFETIME"):
                exp = getattr(context, 'expiry_date', '')
                if context.status == "LIFETIME":
                    formatted_exp = "31/12/9999"
                else:
                    try:
                        parts = exp.split("T")[0].split("-")
                        if len(parts) == 3:
                            formatted_exp = f"{parts[2]}/{parts[1]}/{parts[0]}"
                        else:
                            formatted_exp = exp
                    except Exception:
                        formatted_exp = exp
                        
                if formatted_exp:
                    status_text = f"[{context.status} đến {formatted_exp}] "
                    self.quota_badge.configure(text=f"{status_text}Quota: {quota_remaining} trang")
        
        # 3. Nút Lấy API Key và Ô nhập
        api_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        api_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        lbl_api = ctk.CTkLabel(api_frame, text="Google Gemini API Key:", font=Fonts.SMALL, text_color=Colors.TEXT_MUTED)
        lbl_api.pack(anchor="w", pady=(0, 5))
        
        self.api_entry = ctk.CTkEntry(
            api_frame, placeholder_text="Nhập hoặc dán key", show="*",
            font=Fonts.DEFAULT, fg_color=Colors.BG_INPUT,
            text_color=Colors.TEXT_MAIN, placeholder_text_color=Colors.TEXT_MUTED,
            border_color=Colors.BORDER
        )
        self.api_entry.pack(fill="x", pady=(0, 5))
        
        # Load API key nếu đã có
        saved_key = self.master.auth_manager.get_api_key()
        if saved_key:
            self.api_entry.insert(0, saved_key)
            
        btn_row = ctk.CTkFrame(api_frame, fg_color="transparent")
        btn_row.pack(fill="x")
        
        btn_paste = ctk.CTkButton(
            btn_row, text="Dán", font=Fonts.SMALL, width=40,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER,
            command=self._paste_and_save_api
        )
        btn_paste.pack(side="left", padx=(0, 5))
        
        btn_save = ctk.CTkButton(
            btn_row, text="Lưu", font=Fonts.SMALL, width=40,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER,
            command=self._save_manual_api
        )
        btn_save.pack(side="left", padx=(0, 5))
        
        btn_link = ctk.CTkButton(
            btn_row, text="Lấy Key Web", font=Fonts.SMALL, 
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            border_width=1, border_color=Colors.BORDER,
            text_color=Colors.TEXT_MAIN,
            command=self.master.auth_manager.open_api_key_page
        )
        btn_link.pack(side="right", fill="x", expand=True)
        
        self.btn_settings = ctk.CTkButton(
            self.sidebar,
            text="hlvd 2026",
            font=Fonts.DEFAULT,
            fg_color="transparent",
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MUTED,
            command=self._open_blog_link
        )
        self.btn_settings.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="ew")

        # 5. Nút Đăng xuất
        self.btn_logout = ctk.CTkButton(
            self.sidebar,
            text="Đăng xuất",
            font=Fonts.DEFAULT,
            fg_color=Colors.DANGER,
            hover_color=Colors.DANGER_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            command=self.master.logout
        )
        self.btn_logout.grid(row=6, column=0, padx=20, pady=(5, 20), sticky="ew")

    def _open_blog_link(self):
        import webbrowser
        webbrowser.open("https://example.com")

    def _paste_and_save_api(self):
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text:
                if self.master.auth_manager.detect_and_save_from_clipboard(clipboard_text):
                    self.api_entry.delete(0, "end")
                    self.api_entry.insert(0, clipboard_text.strip())
                    self.show_toast("Đã kết nối API thành công!", Colors.SUCCESS)
                    self.clipboard_clear()
                else:
                    self.show_toast("Mã API không hợp lệ hoặc lỗi mạng!", Colors.DANGER)
        except Exception:
            pass

    def _save_manual_api(self):
        key = self.api_entry.get()
        if key:
            if self.master.auth_manager.detect_and_save_from_clipboard(key):
                self.show_toast("Đã kết nối API thành công!", Colors.SUCCESS)
            else:
                self.show_toast("Mã API không hợp lệ hoặc lỗi mạng!", Colors.DANGER)
        else:
            self.show_toast("Vui lòng nhập API Key!", Colors.DANGER)
            
    def _build_workspace(self):
        """Khung Workspace bên phải (Chọn file, Xử lý dữ liệu)."""
        self.workspace = ctk.CTkFrame(self, fg_color=Colors.BG_MAIN, corner_radius=0)
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_rowconfigure(1, weight=1)  # Vùng List file
        
        # 1. Header
        header_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        header = ctk.CTkLabel(header_frame, text="Trích xuất Dữ liệu", font=Fonts.H2, text_color=Colors.TEXT_MAIN)
        header.pack(side="left")
        
        self.extract_mode_var = ctk.StringVar(value="id_card")
        
        # Cờ trạng thái điều khiển
        self.is_running = False
        self.is_paused = False
        self.collected_data = []
        self.current_out_path = None
        
        def _get_mode(): return self.extract_mode_var.get()
        
        self.mode_selector = ctk.CTkSegmentedButton(
            header_frame, 
            values=["Tài liệu / Hóa đơn", "Danh sách CCCD"],
            command=lambda v: self.extract_mode_var.set("document" if "Tài liệu" in v else "id_card"),
            font=Fonts.SMALL,
            selected_color=Colors.ACCENT,
            selected_hover_color=Colors.ACCENT_HOVER,
            unselected_color=Colors.BG_CARD,
            unselected_hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN
        )
        self.mode_selector.set("Danh sách CCCD")
        self.mode_selector.pack(side="right")
        
        # 2. File Picker Component
        self.file_picker = FilePicker(self.workspace)
        self.file_picker.grid(row=1, column=0, sticky="nsew")
        
        # 2.1 Result Preview (Ẩn mặc định)
        self.result_preview = ResultPreview(self.workspace)
        self.result_preview.grid(row=1, column=0, sticky="nsew")
        self.result_preview.grid_remove()
        
        # 3. Thanh tiến trình & Trạng thái
        self.progress_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=(20, 10))
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.lbl_status = ctk.CTkLabel(self.progress_frame, text="", font=Fonts.SMALL, text_color=Colors.TEXT_MUTED)
        self.lbl_status.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, progress_color=Colors.ACCENT, fg_color=Colors.BG_CARD)
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        self.progress_bar.set(0)
        self.progress_frame.grid_remove() # Ẩn đi khi chưa chạy
        
        # 4. Nút Start
        self.btn_start = ctk.CTkButton(
            self.workspace,
            text="Bắt đầu trích xuất sang Excel",
            font=("Segoe UI", 14, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            height=45,
            command=self._start_extraction
        )
        self.btn_start.grid(row=3, column=0, sticky="ew")
        
        self.controls_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.controls_frame.grid_columnconfigure((0,1,2), weight=1)
        
        self.btn_pause = ctk.CTkButton(
            self.controls_frame, text="Tạm dừng", command=self._toggle_pause,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER
        )
        self.btn_pause.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.btn_stop = ctk.CTkButton(
            self.controls_frame, text="Dừng", command=self._stop_extraction,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER
        )
        self.btn_stop.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.btn_export = ctk.CTkButton(
            self.controls_frame, text="Xuất kết quả hiện có", command=self._export_partial,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER
        )
        self.btn_export.grid(row=0, column=2, padx=5, sticky="ew")
        
        self.controls_frame.grid_remove()
        
        # 5. Toast Widget
        self.toast_lbl = ctk.CTkLabel(self.workspace, text="", font=Fonts.DEFAULT, corner_radius=8, height=36)
        
    def show_toast(self, message: str, color: str):
        """Hiển thị thông báo tạm thời ở giữa màn hình workspace."""
        self.toast_lbl.configure(text=f"  {message}  ", fg_color=color, text_color=Colors.TEXT_ON_ACCENT)
        self.toast_lbl.place(relx=0.5, rely=0.1, anchor="center")
        self.after(3000, self.toast_lbl.place_forget)
        
    def _update_ui(self, status: str = None, progress: float = None, enable_btn: bool = None, toast: tuple = None):
        """Hàm helper để update UI từ worker thread an toàn."""
        if status is not None:
            self.lbl_status.configure(text=status)
        if progress is not None:
            self.progress_bar.set(progress)
        if enable_btn is not None:
            if enable_btn:
                self.btn_start.grid()
                self.controls_frame.grid_remove()
            else:
                self.btn_start.grid_remove()
                self.controls_frame.grid(row=3, column=0, sticky="ew")
        if toast is not None:
            self.show_toast(toast[0], toast[1])

    def _toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.btn_pause.configure(text="Tạm dừng", fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER)
            self._update_ui(status="Đã tiếp tục tiến trình...")
        else:
            self.is_paused = True
            self.btn_pause.configure(text="Tiếp tục", fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER)
            self._update_ui(status="Đã tạm dừng. Bấm 'Tiếp tục' để chạy tiếp.")

    def _stop_extraction(self):
        self.is_running = False
        self.is_paused = False
        self._update_ui(status="Đang dừng tiến trình...", enable_btn=True)
        
    def _export_partial(self):
        if not self.collected_data:
            self.show_toast("Chưa có dữ liệu nào được trích xuất!", Colors.DANGER)
            return
            
        import time
        mode = self.extract_mode_var.get()
        from core.gemini.extractor import GeminiExtractor
        extractor = GeminiExtractor(api_key="mock")
        out_path = self.current_out_path or (self.file_picker.get_files()[0].parent / f"Partial_Export_{int(time.time())}.xlsx")
        
        extractor.to_excel(self.collected_data, out_path, mode=mode)
        self.show_toast(f"Đã xuất dữ liệu hiện có ra file Excel!", Colors.SUCCESS)

    def _countdown_delay(self, seconds: int, reason: str):
        import time
        for i in range(seconds, 0, -1):
            if not self.is_running:
                break
            self.after(0, lambda sec=i: self._update_ui(status=f"⏳ {reason}: Còn {sec}s..."))
            time.sleep(1)

    def _start_extraction(self):
        """Bắt đầu tiến trình (Đẩy qua Thread mới)."""
        files = self.file_picker.get_files()
        if not files:
            self.show_toast("Vui lòng chọn ít nhất 1 file!", Colors.DANGER)
            return
            
        api_key = self.master.auth_manager.get_api_key()
        if not api_key:
            self.show_toast("Chưa cấu hình API Key. Vui lòng kết nối API trước!", Colors.DANGER)
            return

        # Disable UI
        self._update_ui(enable_btn=False)
        self.progress_frame.grid()
        self.is_running = True
        self.is_paused = False
        self.collected_data = []
        self.lbl_status.configure(text="Khởi động tiến trình...")
        self.progress_bar.set(0)
        
        # Chạy Thread ngầm
        mode = self.extract_mode_var.get()
        threading.Thread(target=self._process_task, args=(files, api_key, mode), daemon=True).start()

    def _get_safe_path(self, base_path: Path) -> Path:
        """Tạo đường dẫn không bị trùng lặp."""
        out_path = base_path
        counter = 1
        while out_path.exists():
            out_path = base_path.with_name(f"{base_path.stem}_{counter}{base_path.suffix}")
            counter += 1
        return out_path

    def _process_task(self, files: list[Path], api_key: str, extract_mode: str):
        """Worker thread xử lý toàn bộ pipeline."""
        try:
            import time
            total_pages = self.file_picker.total_pages
            # 1. Kiểm tra tính hợp lệ của Quota trước (chưa trừ)
            self.quota_manager.check_quota(total_pages)

            # 2. Xử lý ảnh & Gọi Gemini
            preprocessor = Preprocessor()
            extractor = GeminiExtractor(api_key=api_key)
            all_tables_preview = []
            last_out_path = None
            processed_count = 0
            BATCH_SIZE = 2
            
            def _ext_callback(msg, sec=0):
                if sec > 0:
                    self._countdown_delay(sec, msg)
                else:
                    self.after(0, lambda m=msg: self._update_ui(status=m))
            
            if extract_mode == "id_card":
                # CHẾ ĐỘ CCCD: GOM CHUNG 1 FILE
                all_id_cards = []
                for fpath in files:
                    self.after(0, lambda name=fpath.name: self._update_ui(status=f"Đang xử lý CCCD: {name}..."))
                    image_bytes_list = preprocessor.process_file(fpath)
                    
                    for j in range(0, len(image_bytes_list), BATCH_SIZE):
                        while self.is_paused and self.is_running:
                            time.sleep(1)
                        if not self.is_running:
                            raise InterruptedError("Tiến trình bị dừng bởi người dùng.")
                            
                        batch = image_bytes_list[j:j+BATCH_SIZE]
                        end_idx = min(j+BATCH_SIZE, len(image_bytes_list))
                        self.after(0, lambda p=j+1, end=end_idx, tot=len(image_bytes_list), name=fpath.name: self._update_ui(status=f"Đang trích xuất dữ liệu CCCD {p}-{end}/{tot} ({name})..."))
                        
                        id_data = extractor.extract_data(
                            batch, 
                            mode="id_card",
                            status_callback=_ext_callback
                        )
                        cards = id_data.get("cards", []) if isinstance(id_data, dict) else []
                        all_id_cards.extend(cards)
                        self.collected_data.extend(cards)
                        
                        processed_count += len(batch)
                        self.after(0, lambda p=processed_count/total_pages: self._update_ui(progress=p))
                        
                        if processed_count < total_pages:
                            self._countdown_delay(5, "Nghỉ chủ động (Batching)")
                        
                # Xuất file gộp chung
                out_dir = files[0].parent
                base_out_path = out_dir / "Danh_sach_CCCD.xlsx"
                last_out_path = self._get_safe_path(base_out_path)
                self.current_out_path = last_out_path
                
                self.after(0, lambda: self._update_ui(status="Đang ghi file Excel (Danh sách CCCD)..."))
                extractor.to_excel(all_id_cards, last_out_path, mode="id_card")
                
                # Mock TableData để ResultPreview có thể render (do ResultPreview mong TableData)
                # Tạm thời gán rỗng vì ResultPreview hiện chỉ xem được dạng Document
                dummy_row = {"cells": [f"Đã xuất {len(all_id_cards)} CCCD ra file Excel"]}
                all_tables_preview.append({"rows": [dummy_row]})
                
            else:
                # CHẾ ĐỘ TÀI LIỆU: MỖI FILE 1 EXCEL
                for i, fpath in enumerate(files):
                    self.after(0, lambda name=fpath.name: self._update_ui(status=f"Đang tách và nén ảnh tệp: {name}..."))
                    image_bytes_list = preprocessor.process_file(fpath)
                    
                    if fpath.suffix.lower() == ".pdf":
                        out_dir = fpath.parent / fpath.stem
                        out_dir.mkdir(exist_ok=True)
                        base_out_path = out_dir / f"{fpath.stem}.xlsx"
                    else:
                        base_out_path = fpath.with_suffix(".xlsx")
                        
                    out_path = self._get_safe_path(base_out_path)
                    last_out_path = out_path
                    self.current_out_path = out_path
                    
                    file_tables = []
                    for j in range(0, len(image_bytes_list), BATCH_SIZE):
                        while self.is_paused and self.is_running:
                            time.sleep(1)
                        if not self.is_running:
                            raise InterruptedError("Tiến trình bị dừng bởi người dùng.")
                            
                        batch = image_bytes_list[j:j+BATCH_SIZE]
                        end_idx = min(j+BATCH_SIZE, len(image_bytes_list))
                        self.after(0, lambda p=j+1, end=end_idx, tot=len(image_bytes_list), name=fpath.name: self._update_ui(status=f"Đang trích xuất dữ liệu trang {p}-{end}/{tot} ({name})..."))
                        
                        table_data_list = extractor.extract_data(
                            batch, 
                            mode="document",
                            status_callback=_ext_callback
                        )
                        documents = table_data_list.get("documents", []) if isinstance(table_data_list, dict) else []
                        file_tables.extend(documents)
                        self.collected_data.extend(documents)
                        
                        processed_count += len(batch)
                        self.after(0, lambda p=processed_count/total_pages: self._update_ui(progress=p))
                        
                        if processed_count < total_pages:
                            self._countdown_delay(5, "Nghỉ chủ động (Batching)")

                    self.after(0, lambda name=fpath.name: self._update_ui(status=f"Đang ghi file Excel cho {name}..."))
                    extractor.to_excel(file_tables, out_path, mode="document")
                    all_tables_preview.extend(file_tables)
            
            # 4. Thành công: Trừ quota và cập nhật UI
            self.quota_manager.consume(processed_count)
            self.after(0, lambda: self.quota_badge.configure(text=f"Quota: {self.quota_manager.get_remaining_quota()} trang"))
            
            self.after(0, lambda: self._update_ui(enable_btn=True, toast=("Xuất file Excel thành công!", Colors.SUCCESS)))
            
            # Hiển thị Preview thay cho File Picker
            def show_preview(last_path, tables):
                self.file_picker.grid_remove()
                self.result_preview.grid()
                self.result_preview.load_data(last_path, tables)
            self.after(0, lambda p=last_out_path, t=all_tables_preview: show_preview(p, t))
            
        except QuotaExceededError as e:
            self.after(0, lambda err=str(e): self._update_ui(enable_btn=True, toast=(err, Colors.DANGER)))
            self.after(1500, self._open_plan_selection)
        except InterruptedError as e:
            self.after(0, lambda err=str(e): self._update_ui(enable_btn=True, toast=(err, Colors.WARNING)))
        except Exception as e:
            from utils.logger import log_error
            log_path = log_error(e, context="Trong lúc chạy tiến trình xuất")
            
            error_toast = "Đã xảy ra lỗi hệ thống!"
            error_msg = str(e)
            
            # Xử lý lỗi API Google thân thiện hơn
            try:
                import httpx
                if isinstance(e, httpx.HTTPStatusError):
                    code = e.response.status_code
                    if code == 503:
                        error_toast = "Hệ thống AI đang quá tải. Thử lại sau."
                    elif code == 429:
                        error_toast = "Hết hạn mức API Google. Thử lại sau."
                    else:
                        error_toast = f"Lỗi API Google ({code})!"
            except ImportError:
                pass
                
            msg = f"Chi tiết lỗi đã được lưu vào {log_path}"
            def _handle_error_ui(m, t):
                self._update_ui(status=m, enable_btn=True, toast=(t, Colors.DANGER))
                self.progress_bar.grid_remove() # Ẩn thanh progress bar để tránh gây hiểu lầm app bị treo
                
            self.after(0, lambda m=msg, t=error_toast: _handle_error_ui(m, t))

    def _sync_license_status(self):
        """Kiểm tra bản quyền từ cache/server khi khởi động MainWindow."""
        try:
            is_valid = self.licensing_client.verify_license()
            if is_valid:
                self.quota_manager.batch_limit = 500
                self.quota_manager.daily_limit = 9999
                context = getattr(self.master, 'license_context', None)
                if context:
                    context.status = "PRO"
                    context.max_batch_size = 500
                    context.daily_quota = 9999
        except Exception:
            pass

    def _open_plan_selection(self):
        """Mở hộp thoại chọn gói cước và chuyển tiếp sang thanh toán VietQR."""
        def _on_plan_chosen(plan):
            self._open_payment_dialog(plan)

        PlanSelectionDialog(
            master=self.winfo_toplevel(),
            lc=self.licensing_client,
            on_plan_selected=_on_plan_chosen
        )

    def _open_payment_dialog(self, plan: dict):
        """Mở hộp thoại thanh toán VietQR và tự động kích hoạt."""
        def _on_success(status_res):
            self._handle_license_upgrade_success(status_res)

        PaymentDialog(
            master=self.winfo_toplevel(),
            lc=self.licensing_client,
            plan=plan,
            on_success=_on_success
        )

    def _handle_license_upgrade_success(self, status_res: dict):
        """Cập nhật giao diện và chính sách Quota sau khi thanh toán thành công."""
        self.quota_manager.batch_limit = 500
        self.quota_manager.daily_limit = 9999
        self.quota_manager.hourly_limit = 0

        context = getattr(self.master, 'license_context', None)
        if context:
            context.status = "PRO"
            context.max_batch_size = 500
            context.daily_quota = 9999

        try:
            remaining = self.quota_manager.get_remaining_quota()
        except Exception:
            remaining = 9999

        self.quota_badge.configure(
            text=f"[PRO] Quota: {remaining} trang",
            fg_color=Colors.SUCCESS,
            text_color=Colors.TEXT_ON_ACCENT
        )
        self.show_toast("🎉 Kích hoạt bản quyền PRO thành công!", Colors.SUCCESS)
