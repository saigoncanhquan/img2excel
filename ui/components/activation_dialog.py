"""Dialog kích hoạt Pro Mode — nhập gmail, hiển thị mã máy, chọn file key.

Workflow:
1. Nhập gmail → hiện mã máy (gửi cho admin)
2. Nhận file key → Browse chọn file .bin
3. Xác thực → kích hoạt pro
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable

import customtkinter as ctk
from ui.theme import Colors, Fonts


class ActivationDialog(ctk.CTkToplevel):
    """Cửa sổ kích hoạt Pro Mode."""

    def __init__(
        self,
        master,
        on_activated: Callable[[], None] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, **kwargs)

        self.on_activated = on_activated
        self._machine_code: str = ""

        # Window setup
        self.title("Kích hoạt Pro")
        self.geometry("480x420")
        self.resizable(False, False)
        self.configure(fg_color=Colors.BG_MAIN)
        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self) -> None:
        """Xây dựng giao diện dialog."""
        pad = {"padx": 24, "pady": (0, 10)}

        # Title (Xanh thương hiệu ChatTingTing)
        title = ctk.CTkLabel(
            self, text="Kích hoạt bản Pro", font=Fonts.H2,
            text_color=Colors.ACCENT,
        )
        title.pack(pady=(24, 16))

        # Step 1: Nhập Gmail
        lbl_gmail = ctk.CTkLabel(
            self, text="1. Nhập email Google đăng ký:", font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED, anchor="w",
        )
        lbl_gmail.pack(fill="x", **pad)

        self.gmail_entry = ctk.CTkEntry(
            self, placeholder_text="example@gmail.com", font=Fonts.DEFAULT,
            fg_color=Colors.BG_INPUT, text_color=Colors.TEXT_MAIN,
            placeholder_text_color=Colors.TEXT_MUTED, border_color=Colors.BORDER,
        )
        self.gmail_entry.pack(fill="x", **pad)

        btn_gen = ctk.CTkButton(
            self, text="Tạo mã máy", font=Fonts.DEFAULT,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER,
            command=self._generate_machine_code,
        )
        btn_gen.pack(fill="x", **pad)

        # Machine code display
        self.mc_frame = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, corner_radius=8)
        self.mc_frame.pack(fill="x", padx=24, pady=(0, 10))

        lbl_mc = ctk.CTkLabel(
            self.mc_frame, text="Mã máy (gửi cho admin):", font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED, anchor="w",
        )
        lbl_mc.pack(fill="x", padx=12, pady=(8, 0))

        self.mc_display = ctk.CTkLabel(
            self.mc_frame, text="—", font=("Consolas", 13),
            text_color=Colors.ACCENT, anchor="w",
        )
        self.mc_display.pack(fill="x", padx=12, pady=(0, 8))

        btn_copy = ctk.CTkButton(
            self.mc_frame, text="Sao chép", font=Fonts.SMALL, width=80,
            fg_color=Colors.ACCENT, hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            command=self._copy_machine_code,
        )
        btn_copy.pack(padx=12, pady=(0, 8), anchor="e")

        # Step 2: Chọn file key
        lbl_key = ctk.CTkLabel(
            self, text="2. Chọn file key đã nhận:", font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED, anchor="w",
        )
        lbl_key.pack(fill="x", **pad)

        key_row = ctk.CTkFrame(self, fg_color="transparent")
        key_row.pack(fill="x", padx=24, pady=(0, 10))

        self.key_path_lbl = ctk.CTkLabel(
            key_row, text="Chưa chọn file", font=Fonts.SMALL,
            text_color=Colors.TEXT_MAIN, anchor="w",
        )
        self.key_path_lbl.pack(side="left", fill="x", expand=True)

        btn_browse = ctk.CTkButton(
            key_row, text="Browse...", font=Fonts.SMALL, width=80,
            fg_color=Colors.BG_CARD, hover_color=Colors.BG_HOVER,
            text_color=Colors.TEXT_MAIN, border_width=1, border_color=Colors.BORDER,
            command=self._browse_key,
        )
        btn_browse.pack(side="right")

        # Activate button
        self.btn_activate = ctk.CTkButton(
            self, text="Kích hoạt Pro", font=("Segoe UI", 14, "bold"),
            fg_color=Colors.ACCENT, hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            height=42, command=self._activate,
        )
        self.btn_activate.pack(fill="x", padx=24, pady=(10, 24))

        # Toast
        self.toast_lbl = ctk.CTkLabel(
            self, text="", font=Fonts.DEFAULT, corner_radius=8, height=32,
        )

    # ── Handlers ────────────────────────────────────────

    def _generate_machine_code(self) -> None:
        gmail = self.gmail_entry.get().strip()
        if not gmail or "@" not in gmail:
            self._show_toast("Vui lòng nhập email hợp lệ!", Colors.DANGER)
            return

        try:
            from core.activation.machine_id import get_machine_code
            self._machine_code = get_machine_code(gmail)
            display = self._machine_code[:16].upper()
            self.mc_display.configure(text=self._machine_code)
            self._show_toast("Đã tạo mã máy!", Colors.SUCCESS)
        except Exception as e:
            self._show_toast(f"Lỗi: {e}", Colors.DANGER)

    def _copy_machine_code(self) -> None:
        if self._machine_code:
            self.clipboard_clear()
            self.clipboard_append(self._machine_code)
            self._show_toast("Đã sao chép mã máy!", Colors.SUCCESS)

    def _browse_key(self) -> None:
        from customtkinter import filedialog
        path = filedialog.askopenfilename(
            title="Chọn file key",
            filetypes=[("Key files", "*.bin"), ("All files", "*.*")],
        )
        if path:
            self._key_path = Path(path)
            self.key_path_lbl.configure(text=self._key_path.name)

    def _activate(self) -> None:
        gmail = self.gmail_entry.get().strip()
        if not gmail or not self._machine_code:
            self._show_toast("Cần tạo mã máy trước!", Colors.DANGER)
            return

        if not hasattr(self, "_key_path") or not self._key_path.exists():
            self._show_toast("Cần chọn file key!", Colors.DANGER)
            return

        try:
            from core.activation.machine_id import get_main_board_id
            from core.activation.key_reader import read_key_file

            main = get_main_board_id()
            result = read_key_file(self._key_path, main, gmail)

            # Lưu thông tin activation vào config
            import json
            from utils.constants import CONFIG_PATH

            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            data = {}
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)

            data["pro_status"] = "active"
            data["gmail"] = gmail
            data["activation_date"] = result.activation.activation_date
            data["expiry_date"] = result.activation.expiry_date
            data["fail_counter"] = 0

            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self._show_toast("Kích hoạt thành công!", Colors.SUCCESS)

            if self.on_activated:
                self.on_activated()

            self.after(1500, self.destroy)

        except ValueError as e:
            self._show_toast(str(e), Colors.DANGER)
        except Exception as e:
            self._show_toast(f"Lỗi: {e}", Colors.DANGER)

    def _show_toast(self, msg: str, color: str) -> None:
        self.toast_lbl.configure(text=f"  {msg}  ", fg_color=color, text_color=Colors.TEXT_ON_ACCENT)
        self.toast_lbl.place(relx=0.5, rely=0.05, anchor="center")
        self.after(3000, self.toast_lbl.place_forget)
