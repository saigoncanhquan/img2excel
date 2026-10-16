import os
import subprocess
from pathlib import Path
from typing import List, Any
import customtkinter as ctk
from ui.theme import Colors, Fonts

class ResultPreview(ctk.CTkFrame):
    """Component hiển thị kết quả trích xuất và các nút hành động (Mở file, Mở thư mục)."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Colors.BG_CARD, corner_radius=8, **kwargs)
        
        self.out_path: Path = None
        self.tables: List[Any] = []
        
        # Grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # 1. Header & Checkbox
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        lbl_title = ctk.CTkLabel(self.header_frame, text="Xem trước dữ liệu", font=Fonts.H2, text_color=Colors.TEXT_MAIN)
        lbl_title.pack(side="left")
        
        self.auto_open_var = ctk.BooleanVar(value=True)
        self.chk_auto_open = ctk.CTkCheckBox(
            self.header_frame, 
            text="Tự động mở file khi hoàn tất", 
            variable=self.auto_open_var,
            font=Fonts.SMALL,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_MAIN
        )
        self.chk_auto_open.pack(side="right")
        
        # 2. Preview Grid (Scrollable)
        self.preview_frame = ctk.CTkScrollableFrame(self, fg_color=Colors.BG_MAIN, corner_radius=0)
        self.preview_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # 3. Nút hành động
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        self.btn_open_file = ctk.CTkButton(
            self.action_frame,
            text="Mở file Excel",
            font=Fonts.DEFAULT,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            command=self._open_file
        )
        self.btn_open_file.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_open_dir = ctk.CTkButton(
            self.action_frame,
            text="Mở thư mục chứa",
            font=Fonts.DEFAULT,
            fg_color=Colors.BG_CARD,
            border_width=1,
            border_color=Colors.BORDER,
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN,
            command=self._open_directory
        )
        self.btn_open_dir.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def load_data(self, out_path: Path, tables: List[Any]):
        """Cập nhật giao diện với dữ liệu mới."""
        self.out_path = out_path
        self.tables = tables
        
        # Xóa dữ liệu cũ
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
            
        if not tables:
            lbl_empty = ctk.CTkLabel(self.preview_frame, text="Không có dữ liệu.", text_color=Colors.TEXT_MUTED)
            lbl_empty.pack(pady=20)
            self._handle_auto_open()
            return
            
        # Trích xuất dữ liệu mảng thô (tối đa 5-6 dòng)
        max_rows = 6
        rows_to_render = []
        for item in tables:
            if isinstance(item, dict) and "rows" in item:
                # Chế độ Tài liệu
                for row in item.get("rows", []):
                    rows_to_render.append(row.get("cells", []))
            elif isinstance(item, dict) and "so_cccd" in item:
                # Chế độ CCCD
                keys = ["loai_giay_to", "so_cccd", "ho_ten", "ngay_sinh", "gioi_tinh", "quoc_tich", "que_quan", "noi_thuong_tru", "ngay_cap", "ngay_het_han", "noi_cap"]
                if not rows_to_render:
                    rows_to_render.append(["Loại thẻ", "Số CMND/CCCD", "Họ tên", "Ngày sinh", "Giới tính", "Quốc tịch", "Quê quán", "Nơi thường trú", "Ngày cấp", "Ngày hết hạn", "Nơi cấp"])
                rows_to_render.append([str(item.get(k, "")) for k in keys])
                
            if len(rows_to_render) >= max_rows:
                break
        
        rows_to_render = rows_to_render[:max_rows]
        
        # Tính số cột lớn nhất
        max_cols = max(len(row) for row in rows_to_render)
        for i in range(max_cols):
            self.preview_frame.grid_columnconfigure(i, weight=1, minsize=100)
            
        # Render grid
        for r_idx, row_data in enumerate(rows_to_render):
            for c_idx, cell_text in enumerate(row_data):
                # Header row (r_idx == 0) highlight
                fg = Colors.BORDER if r_idx == 0 else "transparent"
                txt_col = Colors.TEXT_ON_ACCENT if r_idx == 0 else Colors.TEXT_MAIN
                lbl = ctk.CTkLabel(
                    self.preview_frame, 
                    text=str(cell_text),
                    fg_color=fg,
                    text_color=txt_col,
                    padx=10, 
                    pady=5,
                    corner_radius=4
                )
                lbl.grid(row=r_idx, column=c_idx, sticky="nsew", padx=1, pady=1)
                
        self._handle_auto_open()

    def _handle_auto_open(self):
        if self.auto_open_var.get() and self.out_path and self.out_path.exists():
            self._open_file()

    def _open_file(self):
        if self.out_path and self.out_path.exists():
            try:
                os.startfile(self.out_path)
            except Exception as e:
                if hasattr(self.winfo_toplevel(), "main_window"):
                    self.winfo_toplevel().main_window.show_toast(f"Lỗi mở file: {e}", Colors.DANGER)

    def _open_directory(self):
        if self.out_path and self.out_path.exists():
            try:
                subprocess.Popen(f'explorer /select,"{self.out_path}"')
            except Exception:
                pass
