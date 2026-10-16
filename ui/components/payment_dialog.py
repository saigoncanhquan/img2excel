# -*- coding: utf-8 -*-
"""
Payment & Licensing Dialogs for img2excel (CustomTkinter + VietQR).
Tuân thủ chuẩn thẩm mỹ ChatTingTing: Silver Gray (#B2B2B2), Card (#DFDFDF), Accent Green (#107C41).
"""
from __future__ import annotations

import io
import os
import threading
import time
from typing import Callable, Optional, Dict, Any, List

import customtkinter as ctk
from PIL import Image

from client.config import ClientConfig
from client.licensing_core import LicensingClient
from client.qr_generator import QRGenerator
from ui.theme import Colors, Fonts


class PlanSelectionDialog(ctk.CTkToplevel):
    """Hộp thoại chọn gói cước bản quyền (Lấy động từ Google Sheet PriceList)."""

    def __init__(
        self,
        master,
        lc: LicensingClient,
        on_plan_selected: Callable[[Dict[str, Any]], None],
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.lc = lc
        self.on_plan_selected = on_plan_selected
        self.selected_plan: Optional[Dict[str, Any]] = None

        self.title("Chọn gói bản quyền - img2excel")
        self.geometry("540x500")
        self.minsize(480, 420)
        self.configure(fg_color=Colors.BG_MAIN)
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self._load_plans_async()

    def _build_ui(self):
        # 1. Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=24, pady=(20, 10))

        title = ctk.CTkLabel(
            header_frame,
            text="Nâng cấp Bản quyền img2excel",
            font=Fonts.H2,
            text_color=Colors.ACCENT
        )
        title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Chọn gói phù hợp để mở khóa toàn bộ giới hạn trích xuất CCCD và tài liệu.",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        # 2. Status Label (khi đang tải)
        self.status_lbl = ctk.CTkLabel(
            self,
            text="⏳ Đang tải bảng giá từ máy chủ...",
            font=Fonts.DEFAULT,
            text_color=Colors.TEXT_MAIN
        )
        self.status_lbl.pack(pady=10)

        # 3. Danh sách gói (Scrollable)
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=Colors.BG_CARD,
            corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=24, pady=10)

        # 4. Nút Đóng
        btn_close = ctk.CTkButton(
            self,
            text="Đóng",
            font=Fonts.DEFAULT,
            fg_color=Colors.BG_CARD,
            hover_color=Colors.BG_HOVER,
            border_width=1,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_MAIN,
            height=36,
            command=self.destroy
        )
        btn_close.pack(fill="x", padx=24, pady=(0, 20))

    def _load_plans_async(self):
        def _worker():
            try:
                plans = self.lc.get_prices()
            except Exception as e:
                plans = []
            self.after(0, lambda: self._render_plans(plans))

        threading.Thread(target=_worker, daemon=True).start()

    def _render_plans(self, plans: List[Dict[str, Any]]):
        self.status_lbl.pack_forget()

        if not plans:
            lbl_err = ctk.CTkLabel(
                self.scroll_frame,
                text="Không thể tải bảng giá từ máy chủ.\nVui lòng kiểm tra kết nối mạng và thử lại.",
                font=Fonts.DEFAULT,
                text_color=Colors.DANGER
            )
            lbl_err.pack(pady=30)
            return

        for plan in plans:
            plan_name = plan.get("name") or plan.get("plan_name", "Gói Pro")
            price = int(plan.get("price") or plan.get("amount", 0))
            days = int(plan.get("days") or plan.get("duration_days", 30))
            features = plan.get("description") or plan.get("features", "Xử lý CCCD & Tài liệu")

            card = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=Colors.BG_MAIN,
                border_width=1,
                border_color=Colors.BORDER,
                corner_radius=6
            )
            card.pack(fill="x", pady=6, padx=6)

            card.grid_columnconfigure(0, weight=1)

            # Tên gói & tính năng
            left_frame = ctk.CTkFrame(card, fg_color="transparent")
            left_frame.grid(row=0, column=0, sticky="w", padx=12, pady=10)

            title_row = ctk.CTkLabel(
                left_frame,
                text=f"{plan_name} ({days} ngày)",
                font=("Segoe UI", 14, "bold"),
                text_color=Colors.TEXT_MAIN
            )
            title_row.pack(anchor="w")

            desc_row = ctk.CTkLabel(
                left_frame,
                text=f"Mở khóa: {features}",
                font=Fonts.SMALL,
                text_color=Colors.TEXT_MUTED
            )
            desc_row.pack(anchor="w")

            # Giá & Nút chọn
            right_frame = ctk.CTkFrame(card, fg_color="transparent")
            right_frame.grid(row=0, column=1, sticky="e", padx=12, pady=10)

            price_lbl = ctk.CTkLabel(
                right_frame,
                text=f"{price:,} VNĐ",
                font=("Segoe UI", 14, "bold"),
                text_color=Colors.ACCENT
            )
            price_lbl.pack(side="left", padx=(0, 12))

            btn_select = ctk.CTkButton(
                right_frame,
                text="Chọn gói",
                font=("Segoe UI", 12, "bold"),
                fg_color=Colors.ACCENT,
                hover_color=Colors.ACCENT_HOVER,
                text_color=Colors.TEXT_ON_ACCENT,
                width=90,
                height=32,
                command=lambda p=plan: self._choose_plan(p)
            )
            btn_select.pack(side="left")

    def _choose_plan(self, plan: Dict[str, Any]):
        self.selected_plan = plan
        self.destroy()
        if self.on_plan_selected:
            self.on_plan_selected(plan)


class PaymentDialog(ctk.CTkToplevel):
    """Hộp thoại thanh toán qua VietQR Napas 247 và kiểm tra tự động kích hoạt."""

    def __init__(
        self,
        master,
        lc: LicensingClient,
        plan: Dict[str, Any],
        on_success: Optional[Callable[[Dict[str, Any]], None]] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.lc = lc
        self.plan = plan
        self.on_success = on_success
        self.is_running = True

        self.title("Thanh toán - Kích hoạt tự động VietQR")
        self.geometry("520x680")
        self.minsize(480, 600)
        self.configure(fg_color=Colors.BG_MAIN)
        self.transient(master)
        self.grab_set()

        # Dữ liệu thanh toán
        self.plan_name = plan.get("name") or plan.get("plan_name", "Gói Pro")
        self.plan_id = plan.get("plan_id") or plan.get("tier", "PRO")
        self.amount = int(plan.get("price") or plan.get("amount", 2000))

        prefix = getattr(ClientConfig, "TX_PREFIX", "IMGX") or "IMGX"
        self.order_code = QRGenerator.generate_order_code(prefix)
        self.user_id = getattr(self.lc, "_user_id", None) or f"IMGX{self.lc.get_device_id()[:12].upper()}"

        self.bank_name = "Sacombank"
        self.bank_account = getattr(ClientConfig, "BANK_ACCOUNT", "123456789")
        self.bank_account_name = getattr(ClientConfig, "BANK_ACCOUNT_NAME", "NGUYEN VAN A")

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._build_ui()
        self._start_order_and_qr()
        self._start_polling_thread()

    def _build_ui(self):
        # 1. Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(16, 8))

        title = ctk.CTkLabel(
            header,
            text="Thanh toán VietQR Napas 247",
            font=Fonts.H2,
            text_color=Colors.ACCENT
        )
        title.pack(anchor="w")

        sub = ctk.CTkLabel(
            header,
            text="Quét mã QR bằng App ngân hàng bất kỳ để hệ thống tự động kích hoạt sau 1-3 giây.",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        )
        sub.pack(anchor="w")

        # 2. Info Card
        info_card = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, border_width=1, border_color=Colors.BORDER, corner_radius=6)
        info_card.pack(fill="x", padx=24, pady=4)
        info_card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(info_card, text="Gói đăng ký:", font=Fonts.DEFAULT, text_color=Colors.TEXT_MUTED).grid(row=0, column=0, padx=12, pady=4, sticky="w")
        ctk.CTkLabel(info_card, text=f"{self.plan_name}", font=("Segoe UI", 13, "bold"), text_color=Colors.TEXT_MAIN).grid(row=0, column=1, padx=12, pady=4, sticky="w")

        ctk.CTkLabel(info_card, text="Số tiền:", font=Fonts.DEFAULT, text_color=Colors.TEXT_MUTED).grid(row=1, column=0, padx=12, pady=4, sticky="w")
        ctk.CTkLabel(info_card, text=f"{self.amount:,} VNĐ", font=("Segoe UI", 14, "bold"), text_color=Colors.ACCENT).grid(row=1, column=1, padx=12, pady=4, sticky="w")

        ctk.CTkLabel(info_card, text="Mã đơn hàng:", font=Fonts.DEFAULT, text_color=Colors.TEXT_MUTED).grid(row=2, column=0, padx=12, pady=4, sticky="w")
        code_frame = ctk.CTkFrame(info_card, fg_color="transparent")
        code_frame.grid(row=2, column=1, padx=12, pady=4, sticky="w")
        ctk.CTkLabel(code_frame, text=self.order_code, font=("Segoe UI", 14, "bold"), text_color=Colors.ACCENT).pack(side="left")
        btn_copy_code = ctk.CTkButton(code_frame, text="Copy", font=Fonts.SMALL, width=45, height=22, fg_color=Colors.BG_MAIN, hover_color=Colors.BG_HOVER, text_color=Colors.TEXT_MAIN, command=lambda: self._copy_text(self.order_code, btn_copy_code))
        btn_copy_code.pack(side="left", padx=(8, 0))

        # 3. QR Code View Frame
        self.qr_frame = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, corner_radius=8, width=220, height=220)
        self.qr_frame.pack(padx=24, pady=8)
        self.qr_frame.pack_propagate(False)

        self.qr_label = ctk.CTkLabel(
            self.qr_frame,
            text="⏳ Đang tải mã VietQR...",
            font=Fonts.DEFAULT,
            text_color=Colors.TEXT_MUTED
        )
        self.qr_label.place(relx=0.5, rely=0.5, anchor="center")

        # 4. Manual Transfer Details (Dành cho người không tiện quét QR)
        manual_frame = ctk.CTkFrame(self, fg_color=Colors.BG_CARD, border_width=1, border_color=Colors.BORDER, corner_radius=6)
        manual_frame.pack(fill="x", padx=24, pady=4)
        manual_frame.grid_columnconfigure(1, weight=1)

        def add_row(r_idx, label, val):
            ctk.CTkLabel(manual_frame, text=label, font=Fonts.SMALL, text_color=Colors.TEXT_MUTED).grid(row=r_idx, column=0, padx=10, pady=2, sticky="w")
            ctk.CTkLabel(manual_frame, text=val, font=("Segoe UI", 11, "bold"), text_color=Colors.TEXT_MAIN).grid(row=r_idx, column=1, padx=6, pady=2, sticky="w")
            b = ctk.CTkButton(manual_frame, text="Copy", font=("Segoe UI", 10), width=45, height=20, fg_color=Colors.BG_MAIN, hover_color=Colors.BG_HOVER, text_color=Colors.TEXT_MAIN)
            b.configure(command=lambda t=val, btn=b: self._copy_text(t, btn))
            b.grid(row=r_idx, column=2, padx=10, pady=2, sticky="e")

        add_row(0, "Ngân hàng:", self.bank_name)
        add_row(1, "Số tài khoản:", self.bank_account)
        add_row(2, "Chủ tài khoản:", self.bank_account_name)
        add_row(3, "Nội dung CK:", self.order_code)

        # 5. Status Label
        self.status_lbl = ctk.CTkLabel(
            self,
            text="⏳ Đang chờ thanh toán (Hệ thống tự động kiểm tra liên tục)...",
            font=("Segoe UI", 12, "bold"),
            text_color=Colors.WARNING
        )
        self.status_lbl.pack(pady=(6, 4))

        # 6. Action Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=24, pady=(4, 16))
        btn_frame.grid_columnconfigure(0, weight=2)
        btn_frame.grid_columnconfigure(1, weight=1)

        self.btn_check_now = ctk.CTkButton(
            btn_frame,
            text="Tôi đã chuyển khoản (Kiểm tra ngay)",
            font=("Segoe UI", 13, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            text_color=Colors.TEXT_ON_ACCENT,
            height=38,
            command=self._manual_check
        )
        self.btn_check_now.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="Hủy / Đóng",
            font=Fonts.DEFAULT,
            fg_color=Colors.BG_CARD,
            hover_color=Colors.BG_HOVER,
            border_width=1,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_MAIN,
            height=38,
            command=self._on_close
        )
        btn_cancel.grid(row=0, column=1, padx=(6, 0), sticky="ew")

    def _copy_text(self, text: str, btn: Optional[ctk.CTkButton] = None):
        self.clipboard_clear()
        self.clipboard_append(text)
        if btn:
            btn.configure(text="Đã copy")
            self.after(2000, lambda: btn.configure(text="Copy"))

    def _start_order_and_qr(self):
        def _worker():
            # 1. Đăng ký đơn hàng PENDING lên máy chủ
            try:
                self.lc.create_order(
                    plan_id=self.plan_id,
                    amount=self.amount,
                    order_code=self.order_code
                )
            except Exception:
                pass

            # 2. Sinh URL VietQR Napas 247 chuẩn hóa
            qr_gen = QRGenerator(
                bank_id="SACOMBANK",
                bank_account=self.bank_account,
                account_name=self.bank_account_name
            )
            vietqr_url = qr_gen.get_vietqr_url(amount=self.amount, message=self.order_code)

            # 3. Tải ảnh VietQR hoặc fallback tạo ảnh QR cục bộ
            pil_img = None
            try:
                import requests
                resp = requests.get(vietqr_url, timeout=10)
                if resp.status_code == 200:
                    pil_img = Image.open(io.BytesIO(resp.content))
            except Exception:
                pass

            if pil_img is None:
                try:
                    import qrcode
                    qr = qrcode.QRCode(box_size=8, border=2)
                    qr.add_data(vietqr_url)
                    qr.make(fit=True)
                    pil_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
                except Exception:
                    pass

            self.after(0, lambda: self._show_qr_image(pil_img))

        threading.Thread(target=_worker, daemon=True).start()

    def _show_qr_image(self, pil_img: Optional[Image.Image]):
        if pil_img:
            ctk_img = ctk.CTkImage(light_image=pil_img, size=(210, 210))
            self.qr_label.configure(image=ctk_img, text="")
        else:
            self.qr_label.configure(text="Không thể tải mã QR.\nVui lòng chuyển khoản theo thông tin bên dưới.")

    def _start_polling_thread(self):
        def _poll():
            time.sleep(2)  # Đợi 2 giây ban đầu
            while self.is_running:
                try:
                    status = self.lc.check_payment(order_code=self.order_code, user_id=self.user_id)
                    if status and status.get("status") in ("ACTIVATED", "PAID"):
                        # Bản quyền đã kích hoạt thành công trên máy chủ
                        self.after(0, lambda: self._on_activated_success(status))
                        break
                    elif status and status.get("status") == "MATCHED":
                        # Đã khớp tiền nhưng chưa kích hoạt
                        self.lc.activate(self.plan_id, user_id=self.user_id)
                        self.after(0, lambda: self._on_activated_success(status))
                        break
                except Exception:
                    pass

                for _ in range(12):  # Polling cách nhau 2.4 giây
                    if not self.is_running:
                        break
                    time.sleep(0.2)

        threading.Thread(target=_poll, daemon=True).start()

    def _manual_check(self):
        self.btn_check_now.configure(state="disabled", text="Đang kiểm tra...")
        self.status_lbl.configure(text="🔍 Đang tra cứu biến động số dư ngân hàng...", text_color=Colors.INFO)

        def _worker():
            status = None
            try:
                status = self.lc.check_payment(order_code=self.order_code, user_id=self.user_id)
            except Exception:
                pass

            def _handle():
                self.btn_check_now.configure(state="normal", text="Tôi đã chuyển khoản (Kiểm tra ngay)")
                if status and status.get("status") in ("ACTIVATED", "PAID", "MATCHED"):
                    self._on_activated_success(status)
                else:
                    self.status_lbl.configure(
                        text="Chưa nhận được giao dịch. Ngân hàng có thể mất 15-30 giây để xử lý.",
                        text_color=Colors.WARNING
                    )

            self.after(0, _handle)

        threading.Thread(target=_worker, daemon=True).start()

    def _on_activated_success(self, status_res: Dict[str, Any]):
        self.is_running = False
        # Xác thực và lưu cache bản quyền mới ngay lập tức
        try:
            self.lc.verify_license(user_id=self.user_id, force_online=True)
        except Exception:
            pass

        self.status_lbl.configure(
            text="🎉 THANH TOÁN THÀNH CÔNG! Bản quyền đã được kích hoạt.",
            text_color=Colors.SUCCESS
        )
        self.btn_check_now.configure(state="disabled", text="Đã kích hoạt thành công")

        if self.on_success:
            self.on_success(status_res)

        # Tự động đóng cửa sổ sau 1.8 giây
        self.after(1800, self.destroy)

    def _on_close(self):
        self.is_running = False
        self.destroy()
