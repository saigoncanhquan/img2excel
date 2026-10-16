import os
from pathlib import Path
from typing import Callable, List, Tuple

import customtkinter as ctk
from customtkinter import filedialog
from tkinterdnd2 import DND_FILES


from ui.theme import Colors, Fonts

class FilePicker(ctk.CTkFrame):
    """Component chọn file và quản lý danh sách file đầu vào."""

    def __init__(self, master, on_pages_changed: Callable[[int], None] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.on_pages_changed = on_pages_changed
        self.selected_files: List[Tuple[Path, int]] = []  # List of (filepath, num_pages)
        self.total_pages = 0
        
        # 1. Header controls (Button)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        self.btn_add = ctk.CTkButton(
            self.header_frame, 
            text="+ Chọn tệp (PDF, JPG, PNG)", 
            font=Fonts.DEFAULT,
            fg_color=Colors.BG_CARD,
            hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN,
            border_width=1,
            border_color=Colors.BORDER,
            command=self._browse_files
        )
        self.btn_add.pack(side="left")
        
        self.lbl_info = ctk.CTkLabel(self.header_frame, text="0 tệp - 0 trang", font=Fonts.SMALL, text_color=Colors.TEXT_MUTED)
        self.lbl_info.pack(side="right", padx=10)
        
        # 2. Scrollable list
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color=Colors.BG_CARD, corner_radius=8)
        self.list_frame.pack(fill="both", expand=True)
        
        # 3. Kích hoạt Drag & Drop
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self._on_drop)
        except Exception:
            pass

    def _on_drop(self, event):
        try:
            filepaths = self.winfo_toplevel().tk.splitlist(event.data)
            self._add_files(filepaths)
        except Exception:
            pass

    def _browse_files(self):
        filetypes = [("Supported Files", "*.pdf;*.jpg;*.jpeg;*.png;*.webp")]
        filepaths = filedialog.askopenfilenames(title="Chọn tài liệu", filetypes=filetypes)
        if filepaths:
            self._add_files(filepaths)

    def _add_files(self, filepaths):
        for path_str in filepaths:
            path = Path(path_str)
            if any(p[0] == path for p in self.selected_files):
                continue  # Bỏ qua file trùng
                
            pages = self._count_pages(path)
            
            # Lấy limit hiện tại
            batch_limit = 20
            if hasattr(self.winfo_toplevel(), "main_window"):
                batch_limit = self.winfo_toplevel().main_window.quota_manager.batch_limit
                
            # Kiểm tra ngay nếu vượt quota trang mỗi lần (batch limit)
            if self.total_pages + pages > batch_limit:
                if hasattr(self.winfo_toplevel(), "main_window"):
                    self.winfo_toplevel().main_window.show_toast(f"Vượt quá {batch_limit} trang/lần!", Colors.DANGER)
                break
                
            self.selected_files.append((path, pages))
            self.total_pages += pages
            
        self._refresh_list()

    def _count_pages(self, path: Path) -> int:
        if path.suffix.lower() == ".pdf":
            try:
                import pypdfium2 as pdfium
                pdf = pdfium.PdfDocument(str(path))
                return len(pdf)
            except Exception:
                return 1
        return 1  # Ảnh tính là 1 trang

    def _remove_file(self, index: int):
        removed_path, pages = self.selected_files.pop(index)
        self.total_pages -= pages
        self._refresh_list()

    def _refresh_list(self):
        # Clear UI
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        # Re-render
        for i, (path, pages) in enumerate(self.selected_files):
            item = ctk.CTkFrame(self.list_frame, fg_color="transparent")
            item.pack(fill="x", pady=2)
            
            size_kb = path.stat().st_size / 1024
            info = f"{path.name} ({size_kb:.0f} KB, {pages} trang)"
            
            lbl = ctk.CTkLabel(item, text=info, font=Fonts.SMALL, anchor="w", text_color=Colors.TEXT_MAIN)
            lbl.pack(side="left", fill="x", expand=True, padx=5)
            
            btn_del = ctk.CTkButton(
                item, 
                text="X", 
                width=30, 
                fg_color=Colors.DANGER, 
                hover_color=Colors.DANGER_HOVER,
                text_color=Colors.TEXT_ON_ACCENT,
                command=lambda idx=i: self._remove_file(idx)
            )
            btn_del.pack(side="right", padx=5)
            
        self.lbl_info.configure(text=f"{len(self.selected_files)} tệp - {self.total_pages} trang")
        
        if self.on_pages_changed:
            self.on_pages_changed(self.total_pages)

    def get_files(self) -> List[Path]:
        return [p[0] for p in self.selected_files]
    
    def clear(self):
        self.selected_files.clear()
        self.total_pages = 0
        self._refresh_list()
