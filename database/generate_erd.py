import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def build_erd_figure(theme='dark'):
    is_dark = (theme == 'dark')

    # Bảng màu theo theme
    if is_dark:
        bg_color = '#0F172A'       # Slate 900
        card_bg = '#1E293B'        # Slate 800
        card_border = '#334155'    # Slate 700
        text_title = '#F8FAFC'     # Slate 50
        text_sub = '#38BDF8'       # Sky 400
        text_muted = '#94A3B8'     # Slate 400
        text_col = '#F1F5F9'       # Slate 100
        text_type = '#94A3B8'      # Slate 400
        shadow_color = '#020617'   # Slate 950
        row_alt_bg = '#0F172A'
        legend_bg = '#1E293B'
        legend_border = '#475569'
    else:
        bg_color = '#F8FAFC'       # Slate 50
        card_bg = '#FFFFFF'        # White
        card_border = '#CBD5E1'    # Slate 300
        text_title = '#0F172A'     # Slate 900
        text_sub = '#0284C7'       # Sky 600
        text_muted = '#64748B'     # Slate 500
        text_col = '#1E293B'       # Slate 800
        text_type = '#64748B'      # Slate 500
        shadow_color = '#E2E8F0'   # Slate 200
        row_alt_bg = '#F1F5F9'
        legend_bg = '#FFFFFF'
        legend_border = '#CBD5E1'

    fig = plt.figure(figsize=(28, 16), dpi=300, facecolor=bg_color)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 16)
    ax.axis('off')

    font_main = 'Tahoma'

    # Tiêu đề biểu đồ
    ax.text(14, 15.35, "HE THONG DU BAO GIA NONG SAN & CANH BAO THI TRUONG (AGROFORECAST)",
            color=text_title, fontname=font_main, fontsize=20, weight='bold', ha='center', va='center')
    ax.text(14, 14.85, "SO DO THUC THE QUAN HE CO SO DU LIEU (DATABASE RELATIONAL ERD)",
            color=text_sub, fontname=font_main, fontsize=13, weight='semibold', ha='center', va='center')
    ax.text(14, 14.45, "He quan tri PostgreSQL 14+ | SQLAlchemy ORM | Khoa chinh (PK) & Khoa ngoai (FK) | Rang buoc ON DELETE CASCADE",
            color=text_muted, fontname=font_main, fontsize=10.5, ha='center', va='center')

    # Định nghĩa cấu trúc các bảng theo lưới 4 cột (Grid Layout)
    tables = {
        'system_settings': {
            'title': 'system_settings [Cau hinh he thong]',
            'color': '#7C3AED', # Tím
            'x': 1.0, 'y': 11.2, 'w': 4.8, 'h': 2.7,
            'cols': [
                ('key', 'VARCHAR(100)', 'PK', 'Khoa cau hinh'),
                ('value', 'TEXT', '', 'Gia tri thiet lap'),
                ('updated_at', 'TIMESTAMP', '', 'Thoi gian sua'),
            ]
        },
        'background_jobs': {
            'title': 'background_jobs [Tien trinh ngam]',
            'color': '#4F46E5', # Chàm
            'x': 1.0, 'y': 7.4, 'w': 4.8, 'h': 3.3,
            'cols': [
                ('id', 'INTEGER', 'PK', 'Khoa chinh tu tang'),
                ('kind', 'VARCHAR(30)', '', 'TRAIN_MODEL | SYNC_DATA'),
                ('status', 'VARCHAR(20)', '', 'RUNNING | DONE | FAILED'),
                ('records_processed', 'INTEGER', '', 'So ban ghi da xu ly'),
                ('progress', 'INTEGER', '', 'Tien do hoan thanh (%)'),
            ]
        },
        'price_history': {
            'title': 'price_history [Lich su gia thuc te]',
            'color': '#059669', # Xanh ngọc
            'x': 1.0, 'y': 0.8, 'w': 5.2, 'h': 6.1,
            'cols': [
                ('id', 'BIGSERIAL', 'PK', 'Khoa chinh 64-bit'),
                ('commodity_id', 'INTEGER', 'FK', 'Khoa ngoai -> commodities'),
                ('record_date', 'DATE', '', 'Ngay ghi nhan gia'),
                ('price', 'NUMERIC(14,2)', '', 'Gia binh quan ngay'),
                ('price_min', 'NUMERIC(14,2)', '', 'Gia thap nhat ngay'),
                ('price_max', 'NUMERIC(14,2)', '', 'Gia cao nhat ngay'),
                ('volume', 'NUMERIC(16,2)', '', 'Khoi luong giao dich'),
                ('source', 'VARCHAR(100)', '', 'Nguon cung cap gia'),
                ('created_at', 'TIMESTAMPTZ', '', 'Thoi diem ghi nhan'),
            ]
        },
        'commodities': {
            'title': 'commodities [Nong san - Bang Master Goc]',
            'color': '#0284C7', # Xanh dương
            'x': 7.6, 'y': 7.8, 'w': 5.4, 'h': 6.1,
            'cols': [
                ('id', 'SERIAL', 'PK', 'Khoa chinh tu tang'),
                ('code', 'VARCHAR(50)', 'UK', 'Ma nong san (Duy nhat)'),
                ('name', 'VARCHAR(150)', '', 'Ten hien thi nong san'),
                ('category', 'VARCHAR(50)', '', 'Nganh hang / Phan loai'),
                ('unit', 'VARCHAR(30)', '', 'Don vi tinh (VND/kg)'),
                ('region', 'VARCHAR(100)', '', 'Vung trong trong diem'),
                ('description', 'TEXT', '', 'Mo ta tieu chuan'),
                ('created_at', 'TIMESTAMPTZ', '', 'Ngay tao danh muc'),
                ('updated_at', 'TIMESTAMPTZ', '', 'Ngay cap nhat'),
            ]
        },
        'forecasts': {
            'title': 'forecasts [Ket qua du bao gia AI / ML]',
            'color': '#10B981', # Xanh lá
            'x': 7.6, 'y': 0.8, 'w': 5.4, 'h': 5.8,
            'cols': [
                ('id', 'BIGSERIAL', 'PK', 'Khoa chinh 64-bit'),
                ('commodity_id', 'INTEGER', 'FK', 'Khoa ngoai -> commodities'),
                ('model_name', 'VARCHAR(50)', '', 'LSTM, Prophet, ARIMA, XGB'),
                ('forecast_date', 'DATE', '', 'Ngay du bao tuong lai (T+30)'),
                ('predicted_price', 'NUMERIC(14,2)', '', 'Gia du bao diem'),
                ('lower_ci', 'NUMERIC(14,2)', '', 'Bien duoi khoang tin cay 95%'),
                ('upper_ci', 'NUMERIC(14,2)', '', 'Bien tren khoang tin cay 95%'),
                ('mae / rmse / mape', 'NUMERIC(10,4)', '', 'Chi so danh gia sai so'),
                ('training_date', 'DATE', '', 'Ngay train mo hinh'),
            ]
        },
        'users': {
            'title': 'users [Nguoi dung & Phan quyen RBAC]',
            'color': '#D97706', # Vàng cam
            'x': 14.6, 'y': 8.8, 'w': 5.2, 'h': 5.1,
            'cols': [
                ('id', 'SERIAL', 'PK', 'Khoa chinh'),
                ('email', 'VARCHAR(150)', 'UK', 'Email dang nhap (Duy nhat)'),
                ('password_hash', 'VARCHAR(255)', '', 'Mat khau bam Bcrypt'),
                ('full_name', 'VARCHAR(150)', '', 'Ho va ten nguoi dung'),
                ('role', 'VARCHAR(50)', '', 'admin | analyst | user'),
                ('is_active', 'BOOLEAN', '', 'Trang thai hoat dong'),
                ('created_at', 'TIMESTAMPTZ', '', 'Ngay dang ky'),
                ('updated_at', 'TIMESTAMPTZ', '', 'Ngay sua doi'),
            ]
        },
        'alert_rules': {
            'title': 'alert_rules [Quy tac canh bao gia]',
            'color': '#E11D48', # Đỏ hồng
            'x': 14.6, 'y': 1.6, 'w': 5.2, 'h': 6.2,
            'cols': [
                ('id', 'SERIAL', 'PK', 'Khoa chinh quy tac'),
                ('commodity_id', 'INTEGER', 'FK', 'Khoa ngoai -> commodities'),
                ('user_id', 'INTEGER', 'FK', 'Khoa ngoai -> users [NULL]'),
                ('rule_name', 'VARCHAR(150)', '', 'Ten quy tac thiet lap'),
                ('condition_type', 'VARCHAR(50)', '', 'PRICE_ABOVE, PRICE_BELOW..'),
                ('threshold_value', 'NUMERIC(14,2)', '', 'Nguong kich hoat canh bao'),
                ('email', 'VARCHAR(150)', '', 'Email nhan thong bao'),
                ('is_active', 'BOOLEAN', '', 'Trang thai bat/tat rule'),
                ('created_at', 'TIMESTAMPTZ', '', 'Ngay tao quy tac'),
            ]
        },
        'alert_logs': {
            'title': 'alert_logs [Nhat ky canh bao da gui]',
            'color': '#BE185D', # Hồng đậm
            'x': 21.6, 'y': 1.6, 'w': 5.2, 'h': 4.9,
            'cols': [
                ('id', 'BIGSERIAL', 'PK', 'Khoa chinh nhat ky'),
                ('rule_id', 'INTEGER', 'FK', 'Khoa ngoai -> alert_rules'),
                ('triggered_price', 'NUMERIC(14,2)', '', 'Gia tai thoi diem nhat ky'),
                ('message', 'TEXT', '', 'Noi dung canh bao da gui'),
                ('status', 'VARCHAR(30)', '', 'SENT | FAILED | PENDING'),
                ('triggered_at', 'TIMESTAMPTZ', '', 'Thoi diem kich hoat'),
            ]
        }
    }

    # Vẽ bảng
    for name, t in tables.items():
        x, y, w, h = t['x'], t['y'], t['w'], t['h']
        color = t['color']

        # Đổ bóng
        shadow = FancyBboxPatch((x + 0.08, y - 0.08), w, h,
                                boxstyle="round,pad=0.08,rounding_size=0.18",
                                facecolor=shadow_color, edgecolor='none', alpha=0.6 if is_dark else 0.4, zorder=2)
        ax.add_patch(shadow)

        # Thân bảng
        body = FancyBboxPatch((x, y), w, h,
                              boxstyle="round,pad=0.08,rounding_size=0.18",
                              facecolor=card_bg, edgecolor=card_border, linewidth=1.5, zorder=3)
        ax.add_patch(body)

        # Header
        header_h = 0.62
        header = FancyBboxPatch((x, y + h - header_h), w, header_h,
                                boxstyle="round,pad=0.08,rounding_size=0.18",
                                facecolor=color, edgecolor='none', zorder=4)
        ax.add_patch(header)

        rect_fix = patches.Rectangle((x - 0.08, y + h - header_h - 0.08), w + 0.16, 0.16,
                                     facecolor=color, edgecolor='none', zorder=4)
        ax.add_patch(rect_fix)

        ax.text(x + w / 2, y + h - header_h / 2, t['title'],
                color='#FFFFFF', fontname=font_main, fontsize=10, weight='bold',
                ha='center', va='center', zorder=5)

        # Dòng dữ liệu
        row_h = (h - header_h - 0.2) / max(len(t['cols']), 1)
        cur_y = y + h - header_h - 0.15

        for idx, (col, ctype, key_badge, desc) in enumerate(t['cols']):
            if idx % 2 == 1:
                row_bg = patches.Rectangle((x - 0.05, cur_y - row_h + 0.04), w + 0.1, row_h,
                                           facecolor=row_alt_bg, alpha=0.45 if is_dark else 0.6, edgecolor='none', zorder=4)
                ax.add_patch(row_bg)

            # Badge
            if key_badge == 'PK':
                badge = FancyBboxPatch((x + 0.18, cur_y - row_h * 0.72), 0.50, row_h * 0.66,
                                       boxstyle="round,pad=0.02,rounding_size=0.06",
                                       facecolor='#F59E0B', edgecolor='none', zorder=5)
                ax.add_patch(badge)
                ax.text(x + 0.43, cur_y - row_h * 0.39, 'PK',
                        color='#000000', fontname=font_main, fontsize=7.5, weight='bold',
                        ha='center', va='center', zorder=6)
            elif key_badge == 'FK':
                badge = FancyBboxPatch((x + 0.18, cur_y - row_h * 0.72), 0.50, row_h * 0.66,
                                       boxstyle="round,pad=0.02,rounding_size=0.06",
                                       facecolor='#3B82F6', edgecolor='none', zorder=5)
                ax.add_patch(badge)
                ax.text(x + 0.43, cur_y - row_h * 0.39, 'FK',
                        color='#FFFFFF', fontname=font_main, fontsize=7.5, weight='bold',
                        ha='center', va='center', zorder=6)
            elif key_badge == 'UK':
                badge = FancyBboxPatch((x + 0.18, cur_y - row_h * 0.72), 0.50, row_h * 0.66,
                                       boxstyle="round,pad=0.02,rounding_size=0.06",
                                       facecolor='#8B5CF6', edgecolor='none', zorder=5)
                ax.add_patch(badge)
                ax.text(x + 0.43, cur_y - row_h * 0.39, 'UK',
                        color='#FFFFFF', fontname=font_main, fontsize=7.5, weight='bold',
                        ha='center', va='center', zorder=6)
            else:
                ax.plot(x + 0.43, cur_y - row_h * 0.39, marker='o', markersize=3, color='#94A3B8', zorder=5)

            col_weight = 'bold' if key_badge in ['PK', 'FK', 'UK'] else 'normal'
            ax.text(x + 0.80, cur_y - row_h * 0.39, col,
                    color=text_col, fontname=font_main, fontsize=8.5, weight=col_weight,
                    ha='left', va='center', zorder=6)

            ax.text(x + w - 0.22, cur_y - row_h * 0.39, ctype,
                    color=text_type, fontname='Consolas', fontsize=8,
                    ha='right', va='center', zorder=6)

            cur_y -= row_h

    # Hàm vẽ đường nối
    def draw_connection(x1, y1, x2, y2, rad, label, color='#38BDF8', src_card='1', dst_card='N'):
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                connectionstyle=f"arc3,rad={rad}",
                                arrowstyle='-|>', mutation_scale=16,
                                color=color, linewidth=2.2, linestyle='-', zorder=7)
        ax.add_patch(arrow)

        badge_bg = '#0F172A' if is_dark else '#FFFFFF'

        ax.text(x1 + (0.16 if x2 >= x1 else -0.16), y1 + 0.15, src_card,
                color='#F59E0B', fontname=font_main, fontsize=9, weight='bold',
                ha='center', va='center', zorder=8,
                bbox=dict(boxstyle='round,pad=0.18', facecolor=badge_bg, edgecolor='#F59E0B', linewidth=1.2))

        ax.text(x2 + (0.16 if x2 < x1 else -0.16), y2 + 0.15, dst_card,
                color='#38BDF8', fontname=font_main, fontsize=9, weight='bold',
                ha='center', va='center', zorder=8,
                bbox=dict(boxstyle='round,pad=0.18', facecolor=badge_bg, edgecolor='#38BDF8', linewidth=1.2))

        mx = (x1 + x2) / 2 + rad * (y2 - y1) * 0.35
        my = (y1 + y2) / 2 - rad * (x2 - x1) * 0.35

        lbl_box = '#1E293B' if is_dark else '#FFFFFF'
        lbl_txt = '#FFFFFF' if is_dark else '#0F172A'

        ax.text(mx, my, label,
                color=lbl_txt, fontname=font_main, fontsize=7.5, weight='bold',
                ha='center', va='center', zorder=9,
                bbox=dict(boxstyle='round,pad=0.28', facecolor=lbl_box, edgecolor=color, linewidth=1.3))

    # ==========================================
    # CÁC MỐI NỐI QUAN HỆ KHÓA NGOẠI
    # ==========================================

    # 1. commodities (id) -> price_history (commodity_id)
    draw_connection(7.6, 10.5, 6.2, 5.8, rad=-0.22,
                    label="FK: commodity_id -> id\n(1 : N, ON DELETE CASCADE)",
                    color='#0284C7', src_card='1', dst_card='N')

    # 2. commodities (id) -> forecasts (commodity_id)
    draw_connection(10.3, 7.8, 10.3, 6.6, rad=0.0,
                    label="FK: commodity_id -> id\n(1 : N, ON DELETE CASCADE)",
                    color='#10B981', src_card='1', dst_card='N')

    # 3. commodities (id) -> alert_rules (commodity_id)
    draw_connection(13.0, 10.0, 14.6, 6.5, rad=0.18,
                    label="FK: commodity_id -> id\n(1 : N, ON DELETE CASCADE)",
                    color='#E11D48', src_card='1', dst_card='N')

    # 4. users (id) -> alert_rules (user_id)
    draw_connection(17.2, 8.8, 17.2, 7.8, rad=0.0,
                    label="FK: user_id -> id\n(0..1 : N, ON DELETE CASCADE)",
                    color='#D97706', src_card='0..1', dst_card='N')

    # 5. alert_rules (id) -> alert_logs (rule_id)
    draw_connection(19.8, 4.5, 21.6, 4.5, rad=0.0,
                    label="FK: rule_id -> id\n(1 : N, ON DELETE CASCADE)",
                    color='#BE185D', src_card='1', dst_card='N')

    # ==========================================
    # KHUNG CHÚ GIẢI (LEGEND & METADATA)
    # ==========================================
    legend_box = FancyBboxPatch((21.6, 7.8), 5.2, 6.1,
                                boxstyle="round,pad=0.08,rounding_size=0.18",
                                facecolor=legend_bg, edgecolor=legend_border, linewidth=1.4, zorder=3)
    ax.add_patch(legend_box)

    ax.text(24.2, 13.4, "[ CHU GIAI & QUY UOC CSDL ]",
            color=text_title, fontname=font_main, fontsize=10.5, weight='bold', ha='center', va='center', zorder=5)

    # Khóa chính
    p1 = FancyBboxPatch((22.0, 12.65), 0.52, 0.36, boxstyle="round,pad=0.02,rounding_size=0.06", facecolor='#F59E0B')
    ax.add_patch(p1)
    ax.text(22.26, 12.83, "PK", color='#000000', fontname=font_main, fontsize=8, weight='bold', ha='center', va='center', zorder=6)
    ax.text(22.8, 12.83, "Khoa chinh (Primary Key)", color=text_col, fontname=font_main, fontsize=8.5, weight='bold', ha='left', va='center', zorder=6)

    # Khóa ngoại
    p2 = FancyBboxPatch((22.0, 12.10), 0.52, 0.36, boxstyle="round,pad=0.02,rounding_size=0.06", facecolor='#3B82F6')
    ax.add_patch(p2)
    ax.text(22.26, 12.28, "FK", color='#FFFFFF', fontname=font_main, fontsize=8, weight='bold', ha='center', va='center', zorder=6)
    ax.text(22.8, 12.28, "Khoa ngoai (Foreign Key)", color=text_col, fontname=font_main, fontsize=8.5, weight='bold', ha='left', va='center', zorder=6)

    # Khóa duy nhất
    p3 = FancyBboxPatch((22.0, 11.55), 0.52, 0.36, boxstyle="round,pad=0.02,rounding_size=0.06", facecolor='#8B5CF6')
    ax.add_patch(p3)
    ax.text(22.26, 11.73, "UK", color='#FFFFFF', fontname=font_main, fontsize=8, weight='bold', ha='center', va='center', zorder=6)
    ax.text(22.8, 11.73, "Khoa duy nhat (Unique Key)", color=text_col, fontname=font_main, fontsize=8.5, weight='bold', ha='left', va='center', zorder=6)

    # Đường nối
    ax.plot([22.0, 22.5], [11.05, 11.05], color='#0284C7', linewidth=2.2)
    ax.plot(22.5, 11.05, marker='>', color='#0284C7', markersize=6)
    ax.text(22.8, 11.05, "Quan he lien ket 1 : N", color=text_col, fontname=font_main, fontsize=8.5, weight='bold', ha='left', va='center', zorder=6)

    # Toàn vẹn tham chiếu
    ax.text(22.0, 10.45, "TOAN VEN THAM CHIEU (INTEGRITY):", color=text_sub, fontname=font_main, fontsize=8.5, weight='bold', ha='left', va='center', zorder=6)
    ax.text(22.0, 9.45, "- RTM: ON DELETE CASCADE tren moi FK\n- Xoa nong san -> tu dong don dep sach:\n  lich su gia, du bao va rule lien quan\n- Composite Index: (commodity_id, date)\n- Dam bao chuan hoa 3NF & hieu nang",
            color=text_muted, fontname=font_main, fontsize=8, ha='left', va='center', zorder=6)

    return fig

def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    docs_dir = os.path.join(os.path.dirname(out_dir), "docs")
    root_dir = os.path.dirname(out_dir)
    print("[*] Dang ket xuat cac ban ve ERD...")

    # 1. Bản vẽ Dark Mode (Sleek High-Tech)
    fig_dark = build_erd_figure(theme='dark')
    fig_dark.savefig(os.path.join(docs_dir, "erd_diagram.png"), dpi=300, facecolor='#0F172A', bbox_inches='tight')
    fig_dark.savefig(os.path.join(docs_dir, "erd_diagram.svg"), facecolor='#0F172A', bbox_inches='tight')
    fig_dark.savefig(os.path.join(root_dir, "erd_diagram.png"), dpi=300, facecolor='#0F172A', bbox_inches='tight')
    fig_dark.savefig(os.path.join(root_dir, "erd_diagram.svg"), facecolor='#0F172A', bbox_inches='tight')
    plt.close(fig_dark)
    print("  [+] Da xuat ban ve Dark Mode (erd_diagram.png & svg)")

    # 2. Bản vẽ Light Mode (Phuc vu in an bao cao DATN / Word / PDF / Slide nen sang)
    fig_light = build_erd_figure(theme='light')
    fig_light.savefig(os.path.join(docs_dir, "erd_diagram_light.png"), dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    fig_light.savefig(os.path.join(docs_dir, "erd_diagram_light.svg"), facecolor='#F8FAFC', bbox_inches='tight')
    fig_light.savefig(os.path.join(root_dir, "erd_diagram_light.png"), dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    fig_light.savefig(os.path.join(root_dir, "erd_diagram_light.svg"), facecolor='#F8FAFC', bbox_inches='tight')
    plt.close(fig_light)
    print("  [+] Da xuat ban ve Light Mode (erd_diagram_light.png & svg)")

    print("[✓] Hoan thanh 100% cac ban ve hinh anh ERD!")

if __name__ == "__main__":
    main()
