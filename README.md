# IMG2EXCEL USER GUIDE
> **AI-Powered Image, Invoice & ID Card to Excel Conversion Tool**

---

## 📖 TABLE OF CONTENTS
1. [Introduction to img2excel](#1-introduction-to-img2excel)
2. [Installation & First-Time Sign In](#2-installation--first-time-sign-in)
3. [How to Get and Set Up Your Free Google API Key (100% Free)](#3-how-to-get-and-set-up-your-free-google-api-key-100-free)
4. [Step-by-Step Usage Guide](#4-step-by-step-usage-guide)
   - [Mode 1: Batch Citizen ID Card (CCCD) Extraction](#mode-1-batch-citizen-id-card-cccd-extraction)
   - [Mode 2: Tables / Invoices / General Documents](#mode-2-tables--invoices--general-documents)
5. [Previewing Results & Opening Excel Files](#5-previewing-results--opening-excel-files)
6. [Quotas & Instant Pro Upgrade via QR Payment](#6-quotas--instant-pro-upgrade-via-qr-payment)
7. [Photography & Scanning Tips for 100% Accuracy](#7-photography--scanning-tips-for-100-accuracy)
8. [Frequently Asked Questions (FAQ) & Troubleshooting](#8-frequently-asked-questions-faq--troubleshooting)

---

## 1. Introduction to img2excel

**img2excel** is an intelligent desktop application designed to save you hours of manual data entry. Simply feed in photographed documents or scanned PDF files, and the app will automatically recognize the data and export it into clean, perfectly formatted Excel spreadsheets:

- 🪪 **Specialized in Citizen ID Cards (CCCD):** Flawlessly extracts data from chip-based ID cards, barcode cards, older 9/12-digit identity cards, and newly issued 2024 National Identity Cards. Process dozens or hundreds of images/PDFs at once and **automatically merge them into a single consolidated Excel file**.
- 📊 **Table & Invoice Recognition:** Scans receipts, invoices, timesheets, payrolls, contracts, and quotes while accurately preserving row and column structures.
- 🎯 **Never Loses Leading Zeros:** Automatically applies standard Text formatting (`@`) to ID numbers (e.g., `00120...`), phone numbers, and dates so Excel won't drop the leading zero `0`.
- ⚡ **Modern & Intuitive Interface:** Drag-and-drop file upload, clear controls, and responsive feedback.

---

## 2. Installation & First-Time Sign In

### 2.1 Launching the App
1. Download the installer or executable file `img2excel.exe`.
2. Double-click the **img2excel** icon to launch the software.

### 2.2 Sign in with Google
On the initial launch, you will see a sign-in screen:
1. Click the green button: **"Đăng nhập bằng Google"** (Sign in with Google).
2. Your default web browser will automatically open Google's authentication page.
3. Choose your Google/Gmail account and click **Allow** (or Sign in).
4. Once verified, return to **img2excel**; the main workspace will load immediately.

> 💡 **Tip:** The software remembers your session. On future launches, you will jump straight into the application without having to sign in again.

---

## 3. How to Get and Set Up Your Free Google API Key (100% Free)

To allow the app's AI engine to recognize and extract text from images, you need a Google Gemini API Key. Google provides this key **completely free of charge** for every personal Gmail account.

You only need to complete this setup **ONCE**:

### Steps to get your API Key (takes under 1 minute):
1. In the left sidebar of img2excel, locate **"Google Gemini API Key"** and click **"Lấy Key Web"** (Get Web Key) *(or navigate directly to [aistudio.google.com](https://aistudio.google.com/app/apikey))*.
2. Sign in with your personal Google account if prompted.
3. Click the blue button: **"Create API key"**.
4. Select **"Create API key in new project"**.
5. A long string starting with `AIzaSy...` will be displayed. Click the **Copy** button.

### Adding it to the application:
1. Return to the **img2excel** window.
2. Click **"Dán"** (Paste) or paste the key into the text box, then click **"Lưu"** (Save).
3. A green notification will confirm: **"Đã kết nối API thành công!"** (API connected successfully!). You are now ready to extract data!

---

## 4. Step-by-Step Usage Guide

---

### Mode 1: Batch Citizen ID Card (CCCD) Extraction
*(Ideal for HR, Accounting, Notary offices, Insurance, Banking, Schools, and Legal teams)*

This mode lets you import multiple ID card photos (front/back) or multi-page scanned PDFs. The software processes each record and compiles everything into **one unified Excel workbook**.

#### How to use:
1. In the top-right corner of the workspace, select the tab: **"Danh sách CCCD"** (Citizen ID List).
2. **Add files:**
   - Option A: Click **"Chọn tệp"** (Select Files) to browse image files (`.jpg`, `.jpeg`, `.png`, `.webp`) or `.pdf` documents from your PC.
   - Option B: **Drag and drop** files directly from Windows File Explorer into the central drop zone.
3. Review your imported file list. You can remove individual files if needed.
4. Click the large green button: **"Bắt đầu trích xuất sang Excel"** (Start Extraction to Excel).
5. The software will process page by page; the progress bar will indicate the current status.
6. Upon completion, a clean Excel file named `Danh_sach_CCCD.xlsx` is saved directly into the folder where your input files reside.

#### Extracted Data Fields in Excel:
| Excel Column Header | Description |
| :--- | :--- |
| **Loại thẻ** (Card Type) | Chip-based CCCD, 2024 Identity Card, or 9/12-digit CMND |
| **Số CMND/CCCD** (ID Number) | Full 12-digit number, **with leading zeros preserved** |
| **Họ tên** (Full Name) | Capitalized full legal name with Vietnamese accent marks |
| **Ngày sinh** (Date of Birth) | Standardized `dd/mm/yyyy` format |
| **Giới tính** (Gender) | Male / Female |
| **Quốc tịch** (Nationality) | Vietnam |
| **Quê quán** (Place of Origin) | Ward/Commune, District, Province/City |
| **Nơi thường trú** (Permanent Address) | Full permanent residence address |
| **Ngày cấp** (Issue Date) | Date the ID card was issued |
| **Ngày hết hạn** (Expiry Date) | Expiration date of the card |
| **Nơi cấp** (Issuing Authority) | Police Department of Administrative Management / Ministry of Public Security |

---

### Mode 2: Tables / Invoices / General Documents
*(Ideal for digitizing paper invoices, receipts, timesheets, accounting vouchers, and contracts)*

This mode scans documents, automatically detects tabular areas, and reconstructs identical rows and columns inside Excel.

#### How to use:
1. In the top-right corner, select the tab: **"Tài liệu / Hóa đơn"** (Documents / Invoices).
2. Drag and drop or browse to select your scanned invoices or PDF reports.
3. Click **"Bắt đầu trích xuất sang Excel"**.
4. The application analyzes each document and generates a corresponding `.xlsx` spreadsheet for each file.

---

### Controls During Extraction
While the extraction is underway, you can control the execution using the control panel:
- **Tạm dừng / Tiếp tục** (Pause / Resume): Temporarily pause execution, then resume at your convenience.
- **Dừng** (Stop): Cancel the remaining tasks in the current batch.
- **Xuất kết quả hiện có** (Export Current Progress): If you queued 100 pages and only 30 have finished when you need the data urgently, click this button to immediately export the completed 30 pages to Excel.

---

## 5. Previewing Results & Opening Excel Files

Immediately after processing finishes, the workspace switches to the **Data Preview** screen:

1. **Preview Table:** Displays the first 5–6 rows of extracted data so you can quickly inspect accuracy without launching Excel.
2. **"Mở file Excel" (Open Excel File) Button:** Instantly opens the generated spreadsheet in Microsoft Excel, WPS Office, or your default spreadsheet editor.
3. **"Mở thư mục chứa" (Open Containing Folder) Button:** Opens Windows File Explorer pointing directly to where the `.xlsx` file is saved, making it easy to attach to emails or share via Zalo / Google Drive.
4. **"Tự động mở file khi hoàn tất" (Auto-open when finished) Checkbox:** When checked, the spreadsheet will launch automatically upon completion.

---

## 6. Quotas & Instant Pro Upgrade via QR Payment

### 6.1 Free Plan
- New users receive a generous free quota: **20 pages per batch** and **500 pages per day**.
- Your remaining quota is always visible in the upper-left corner of the sidebar (`Quota: ... trang`).

### 6.2 Upgrading to Pro (Instant Activation via VietQR Napas 247)
When you need to process large document volumes without restrictions, you can upgrade to Pro through an automated 24/7 payment flow:

1. Click **"Nâng cấp Pro"** (Upgrade Pro) in the left sidebar.
2. **Select your preferred subscription period:**
   - 🌟 1 Month Plan
   - 🌟 6 Months Plan
   - 🌟 1 Year Plan
3. Click **"Tiếp tục thanh toán"** (Proceed to Payment).
4. A **VietQR (Napas 247)** payment dialog will appear displaying:
   - The exact payment amount.
   - An order reference code unique to your computer hardware (e.g., `IMGX...`).
5. **Making Payment:**
   - Open any mobile banking application on your phone (Vietcombank, MB Bank, Techcombank, Sacombank, VPBank, MoMo, etc.).
   - Select **Scan QR** and scan the QR code displayed on your computer screen.
   - Confirm the transaction (the amount and transaction description are filled automatically).
6. **Instant Activation:**
   - Within 5–10 seconds after payment completion, img2excel detects the transaction and shows **"Kích hoạt thành công!"** (Activated Successfully!).
   - Your quota limits are elevated immediately without having to send payment receipts or wait for manual admin approval.

---

## 7. Photography & Scanning Tips for 100% Accuracy

While the underlying AI is capable of handling complex document layouts, following these simple photography guidelines ensures maximum accuracy:

- 📸 **Avoid Flash & Lamp Reflections:** Plastic-laminated ID cards reflect direct lighting. Tilt the card slightly or reposition direct desk lamps to avoid bright white glare over numbers.
- 📐 **Flat and Square Alignment:** Lay the document flat on a contrasting background (e.g., a dark wooden table). Shoot straight from above rather than at a steep angle.
- 🔍 **Sharp Focus:** Ensure your phone camera focuses sharply on small printed text such as "Permanent Address" or "Place of Origin" before capturing.
- 📑 **For Scanned PDFs:** Configure your scanner with a recommended resolution between **200 DPI and 300 DPI**.

---

## 8. Frequently Asked Questions (FAQ) & Troubleshooting

### ❓ Q1: Why do ID numbers keep their leading zeros in Excel?
**Answer:** img2excel explicitly formats numeric identity fields as text (`@`). Unlike manual copy-pasting where Excel strips leading zeros (turning `001200000001` into `1200000001`), our generated Excel files preserve every digit intact.

### ❓ Q2: What should I do if I see "Rate Limit Exceeded (429)" or "AI Overloaded (503)"?
**Answer:**
- **Error 429:** You have sent requests faster than Google's free-tier per-minute rate limit. Wait **1 to 2 minutes**, then click resume/start again.
- **Error 503:** Google's AI servers are temporarily busy. The app includes automatic backoff retry logic, so waiting a few moments will resolve it.

### ❓ Q3: Is my document data and personal information secure?
**Answer:** Completely secure. Document images are transmitted directly from your local machine to Google's official AI endpoints over encrypted SSL/HTTPS connections. No customer images or personal records are stored on third-party intermediary servers.

### ❓ Q4: If I reinstall Windows or change computers, can I transfer my Pro license?
**Answer:** Yes. Simply reach out to customer support with your original order reference code to have your license migrated to your new machine.

---

> 📞 **Support & Feedback:**  
> If you have questions or need assistance, feel free to visit [excelcappy.blogspot.com](https://excelcappy.blogspot.com/) or contact support via the in-app links.
