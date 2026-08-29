-- ==============================================================================
-- HỆ THỐNG DỰ BÁO GIÁ NÔNG SẢN & CẢNH BÁO THỊ TRƯỜNG (AgroForecast)
-- Database Initialization Script (PostgreSQL 14+) - RBAC & Auth Version
-- File: database/init.sql
-- ==============================================================================

-- Drop tables if exists (theo thứ tự khóa ngoại)
DROP TABLE IF EXISTS alert_logs CASCADE;
DROP TABLE IF EXISTS alert_rules CASCADE;
DROP TABLE IF EXISTS forecasts CASCADE;
DROP TABLE IF EXISTS price_history CASCADE;
DROP TABLE IF EXISTS commodities CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ------------------------------------------------------------------------------
-- 1. BẢNG NGƯỜI DÙNG & PHÂN QUYỀN (users)
-- ------------------------------------------------------------------------------
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'analyst', -- 'analyst' hoặc 'admin'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);

-- ------------------------------------------------------------------------------
-- 2. BẢNG NÔNG SẢN (commodities)
-- ------------------------------------------------------------------------------
CREATE TABLE commodities (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,            -- Mã định danh (vd: RICE_IR504, COFFEE_ROBUSTA, PEPPER_BLACK, SUGARCANE)
    name VARCHAR(150) NOT NULL,                  -- Tên nông sản tiếng Việt (vd: Lúa gạo IR50404, Cà phê Robusta...)
    category VARCHAR(50) NOT NULL,               -- Phân loại (Lương thực, Nông sản xuất khẩu, Cây công nghiệp)
    unit VARCHAR(30) NOT NULL,                   -- Đơn vị tính (VNĐ/kg, VNĐ/tấn...)
    region VARCHAR(100) NOT NULL,                -- Vùng trọng điểm (Đồng bằng Sông Cửu Long, Tây Nguyên...)
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------------------------
-- 3. BẢNG LỊCH SỬ GIÁ THỰC TẾ (price_history)
-- ------------------------------------------------------------------------------
CREATE TABLE price_history (
    id BIGSERIAL PRIMARY KEY,
    commodity_id INT NOT NULL REFERENCES commodities(id) ON DELETE CASCADE,
    record_date DATE NOT NULL,                   -- Ngày ghi nhận giá
    price NUMERIC(14, 2) NOT NULL,               -- Mức giá bình quân trong ngày
    price_min NUMERIC(14, 2),                    -- Mức giá thấp nhất
    price_max NUMERIC(14, 2),                    -- Mức giá cao nhất
    volume NUMERIC(16, 2) DEFAULT 0,             -- Khối lượng giao dịch ước tính (tấn)
    source VARCHAR(100) DEFAULT 'Sở NN&PTNT / Hiệp hội Nông sản',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_commodity_date UNIQUE (commodity_id, record_date)
);

CREATE INDEX idx_price_history_commodity_date ON price_history(commodity_id, record_date DESC);
CREATE INDEX idx_price_history_date ON price_history(record_date);

-- ------------------------------------------------------------------------------
-- 4. BẢNG DỰ BÁO GIÁ (forecasts)
-- ------------------------------------------------------------------------------
CREATE TABLE forecasts (
    id BIGSERIAL PRIMARY KEY,
    commodity_id INT NOT NULL REFERENCES commodities(id) ON DELETE CASCADE,
    model_name VARCHAR(50) NOT NULL,             -- LSTM, Prophet, ARIMA
    forecast_date DATE NOT NULL,                 -- Ngày trong tương lai được dự báo (T+1 -> T+30)
    predicted_price NUMERIC(14, 2) NOT NULL,     -- Giá dự báo điểm (Point estimate)
    lower_ci NUMERIC(14, 2) NOT NULL,            -- Biên dưới khoảng tin cậy 95%
    upper_ci NUMERIC(14, 2) NOT NULL,            -- Biên trên khoảng tin cậy 95%
    mae NUMERIC(10, 4),                          -- Mean Absolute Error trên tập Test
    rmse NUMERIC(10, 4),                         -- Root Mean Squared Error
    mape NUMERIC(10, 4),                         -- Mean Absolute Percentage Error (%)
    r2 NUMERIC(10, 4),                           -- R-squared score
    training_date DATE DEFAULT CURRENT_DATE,     -- Ngày huấn luyện/chạy mô hình
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_forecast_commodity_model_date UNIQUE (commodity_id, model_name, forecast_date, training_date)
);

CREATE INDEX idx_forecasts_lookup ON forecasts(commodity_id, model_name, forecast_date);

-- ------------------------------------------------------------------------------
-- 5. BẢNG QUY TẮC CẢNH BÁO BIẾN ĐỘNG GIÁ (alert_rules)
-- ------------------------------------------------------------------------------
CREATE TABLE alert_rules (
    id SERIAL PRIMARY KEY,
    commodity_id INT NOT NULL REFERENCES commodities(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE CASCADE, -- Người tạo rule
    rule_name VARCHAR(150) NOT NULL,
    condition_type VARCHAR(50) NOT NULL,         -- PRICE_ABOVE, PRICE_BELOW, PCT_INC_7D, PCT_DEC_7D
    threshold_value NUMERIC(14, 2) NOT NULL,     -- Giá trị ngưỡng (VD: 120000 VNĐ hoặc 5.0%)
    email VARCHAR(150) NOT NULL,                 -- Email nhận thông báo
    is_active BOOLEAN DEFAULT TRUE,              -- Trạng thái bật/tắt rule
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alert_rules_commodity ON alert_rules(commodity_id, is_active);
CREATE INDEX idx_alert_rules_user ON alert_rules(user_id);

-- ------------------------------------------------------------------------------
-- 6. BẢNG NHẬT KÝ CẢNH BÁO ĐÃ KÍCH HOẠT (alert_logs)
-- ------------------------------------------------------------------------------
CREATE TABLE alert_logs (
    id BIGSERIAL PRIMARY KEY,
    rule_id INT NOT NULL REFERENCES alert_rules(id) ON DELETE CASCADE,
    triggered_price NUMERIC(14, 2) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'SENT',           -- SENT, FAILED, PENDING
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alert_logs_rule ON alert_logs(rule_id, triggered_at DESC);

-- ==============================================================================
-- SEED DATA: DỮ LIỆU MẪU BAN ĐẦU
-- ==============================================================================

-- 1. Thêm 2 tài khoản mẫu (Analyst và Admin)
-- Mật khẩu 123456: $2b$12$BD1uwhMedtGp8oqF.QorBur9P4tIGxLC.vNETDzc/4dJUE2Je5dbu
-- Mật khẩu admin123: $2b$12$ij.Fr/HiOE0MzRV7a8Gz/eWJAzF5NlFpkbkCOzBUugKXob4yMC3HC
INSERT INTO users (id, email, password_hash, full_name, role) VALUES
(1, 'anhnguyen@agroforecast.vn', '$2b$12$BD1uwhMedtGp8oqF.QorBur9P4tIGxLC.vNETDzc/4dJUE2Je5dbu', 'Anh Nguyễn', 'analyst'),
(2, 'admin@agroforecast.vn', '$2b$12$ij.Fr/HiOE0MzRV7a8Gz/eWJAzF5NlFpkbkCOzBUugKXob4yMC3HC', 'Quản trị viên Hệ thống', 'admin');

ALTER SEQUENCE users_id_seq RESTART WITH 3;

-- 2. Thêm 4 loại nông sản chủ lực
INSERT INTO commodities (id, code, name, category, unit, region, description) VALUES
(1, 'RICE_IR504', 'Lúa gạo IR50404', 'Lương thực', 'VNĐ/kg', 'Đồng bằng Sông Cửu Long', 'Lúa tươi chất lượng thương phẩm cao tại ruộng An Giang, Tiền Giang, Đồng Tháp'),
(2, 'COFFEE_ROBUSTA', 'Cà phê Robusta', 'Nông sản xuất khẩu', 'VNĐ/kg', 'Tây Nguyên (Đắk Lắk, Lâm Đồng)', 'Cà phê nhân xô Robusta loại 1 Đắk Lắk, Gia Lai'),
(3, 'PEPPER_BLACK', 'Hồ tiêu đen', 'Gia vị & Nông sản', 'VNĐ/kg', 'Tây Nguyên & Đông Nam Bộ', 'Tiêu đen xô khô độ ẩm tiêu chuẩn 13% tại Chư Sê, Đắk Lắk'),
(4, 'SUGARCANE', 'Mía đường', 'Cây công nghiệp', 'VNĐ/tấn', 'Miền Trung & Tây Nam Bộ', 'Mía nguyên liệu đạt 10 CCS tại nhà máy đường');

ALTER SEQUENCE commodities_id_seq RESTART WITH 5;

-- 3. Thêm chuỗi dữ liệu lịch sử giá 60 ngày gần nhất
DO $$
DECLARE
    curr_date DATE := CURRENT_DATE - INTERVAL '60 days';
    i INT;
    p_rice NUMERIC;
    p_coffee NUMERIC;
    p_pepper NUMERIC;
    p_sugar NUMERIC;
BEGIN
    p_rice := 7800.00;
    p_coffee := 112000.00;
    p_pepper := 138000.00;
    p_sugar := 1150000.00;

    FOR i IN 1..60 LOOP
        p_rice := ROUND((p_rice + (sin(i::float/5.0) * 80 + (random() * 60 - 25)))::numeric, 2);
        p_coffee := ROUND((p_coffee + (cos(i::float/4.0) * 1200 + (random() * 1500 - 600)))::numeric, 2);
        p_pepper := ROUND((p_pepper + (sin(i::float/6.0) * 900 + (random() * 1100 - 450)))::numeric, 2);
        p_sugar := ROUND((p_sugar + (sin(i::float/7.0) * 5000 + (random() * 8000 - 3500)))::numeric, 2);

        -- Insert Lúa Gạo
        INSERT INTO price_history (commodity_id, record_date, price, price_min, price_max, volume, source)
        VALUES (1, curr_date, p_rice, p_rice - 150, p_rice + 200, ROUND((1200 + random()*400)::numeric, 1), 'Sở NN&PTNT An Giang');

        -- Insert Cà phê
        INSERT INTO price_history (commodity_id, record_date, price, price_min, price_max, volume, source)
        VALUES (2, curr_date, p_coffee, p_coffee - 800, p_coffee + 1000, ROUND((450 + random()*200)::numeric, 1), 'Hiệp hội Cà phê Ca cao VN (VICOFA)');

        -- Insert Hồ tiêu
        INSERT INTO price_history (commodity_id, record_date, price, price_min, price_max, volume, source)
        VALUES (3, curr_date, p_pepper, p_pepper - 1200, p_pepper + 1500, ROUND((310 + random()*120)::numeric, 1), 'Hiệp hội Hồ tiêu Chư Sê');

        -- Insert Mía đường
        INSERT INTO price_history (commodity_id, record_date, price, price_min, price_max, volume, source)
        VALUES (4, curr_date, p_sugar, p_sugar - 15000, p_sugar + 20000, ROUND((2500 + random()*800)::numeric, 1), 'Hiệp hội Mía đường Việt Nam (VSSA)');

        curr_date := curr_date + INTERVAL '1 day';
    END LOOP;
END $$;

-- 4. Thêm dữ liệu dự báo mẫu 30 ngày tới
DO $$
DECLARE
    base_coffee NUMERIC := 121500.00;
    base_rice NUMERIC := 8450.00;
    base_pepper NUMERIC := 142000.00;
    base_sugar NUMERIC := 1180000.00;
    f_date DATE;
    j INT;
    ci_spread NUMERIC;
BEGIN
    FOR j IN 1..30 LOOP
        f_date := CURRENT_DATE + (j || ' days')::interval;
        ci_spread := j * 0.005;

        -- CÀ PHÊ ROBUSTA - Model LSTM
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            2, 'LSTM', f_date,
            ROUND((base_coffee * (1 + 0.004 * j + sin(j::float)*0.002))::numeric, 2),
            ROUND((base_coffee * (1 + 0.004 * j) * (1 - ci_spread))::numeric, 2),
            ROUND((base_coffee * (1 + 0.004 * j) * (1 + ci_spread))::numeric, 2),
            850.2500, 1120.4000, 0.7250, 0.9620
        );

        -- CÀ PHÊ ROBUSTA - Model Prophet
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            2, 'Prophet', f_date,
            ROUND((base_coffee * (1 + 0.0035 * j))::numeric, 2),
            ROUND((base_coffee * (1 + 0.0035 * j) * (1 - ci_spread * 1.15))::numeric, 2),
            ROUND((base_coffee * (1 + 0.0035 * j) * (1 + ci_spread * 1.15))::numeric, 2),
            1050.8000, 1380.1500, 0.8920, 0.9410
        );

        -- CÀ PHÊ ROBUSTA - Model ARIMA
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            2, 'ARIMA', f_date,
            ROUND((base_coffee * (1 + 0.003 * j))::numeric, 2),
            ROUND((base_coffee * (1 + 0.003 * j) * (1 - ci_spread * 1.3))::numeric, 2),
            ROUND((base_coffee * (1 + 0.003 * j) * (1 + ci_spread * 1.3))::numeric, 2),
            1320.4000, 1650.7500, 1.1200, 0.9130
        );

        -- LÚA GẠO IR504 - Model LSTM
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            1, 'LSTM', f_date,
            ROUND((base_rice * (1 + 0.002 * j + cos(j::float)*0.001))::numeric, 2),
            ROUND((base_rice * (1 + 0.002 * j) * (1 - ci_spread))::numeric, 2),
            ROUND((base_rice * (1 + 0.002 * j) * (1 + ci_spread))::numeric, 2),
            65.5000, 88.3000, 0.7800, 0.9540
        );

        -- LÚA GẠO IR504 - Model Prophet
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            1, 'Prophet', f_date,
            ROUND((base_rice * (1 + 0.0015 * j))::numeric, 2),
            ROUND((base_rice * (1 + 0.0015 * j) * (1 - ci_spread * 1.15))::numeric, 2),
            ROUND((base_rice * (1 + 0.0015 * j) * (1 + ci_spread * 1.15))::numeric, 2),
            75.5000, 95.3000, 0.8500, 0.9320
        );

        -- LÚA GẠO IR504 - Model ARIMA
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            1, 'ARIMA', f_date,
            ROUND((base_rice * (1 + 0.001 * j))::numeric, 2),
            ROUND((base_rice * (1 + 0.001 * j) * (1 - ci_spread * 1.3))::numeric, 2),
            ROUND((base_rice * (1 + 0.001 * j) * (1 + ci_spread * 1.3))::numeric, 2),
            80.5000, 105.3000, 0.9500, 0.9120
        );

        -- HỒ TIÊU ĐEN - Model LSTM
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            3, 'LSTM', f_date,
            ROUND((base_pepper * (1 + 0.003 * j))::numeric, 2),
            ROUND((base_pepper * (1 + 0.003 * j) * (1 - ci_spread))::numeric, 2),
            ROUND((base_pepper * (1 + 0.003 * j) * (1 + ci_spread))::numeric, 2),
            1150.0000, 1490.0000, 0.8100, 0.9480
        );

        -- HỒ TIÊU ĐEN - Model Prophet
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            3, 'Prophet', f_date,
            ROUND((base_pepper * (1 + 0.0025 * j))::numeric, 2),
            ROUND((base_pepper * (1 + 0.0025 * j) * (1 - ci_spread * 1.15))::numeric, 2),
            ROUND((base_pepper * (1 + 0.0025 * j) * (1 + ci_spread * 1.15))::numeric, 2),
            1250.0000, 1590.0000, 0.8800, 0.9280
        );

        -- HỒ TIÊU ĐEN - Model ARIMA
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            3, 'ARIMA', f_date,
            ROUND((base_pepper * (1 + 0.002 * j))::numeric, 2),
            ROUND((base_pepper * (1 + 0.002 * j) * (1 - ci_spread * 1.3))::numeric, 2),
            ROUND((base_pepper * (1 + 0.002 * j) * (1 + ci_spread * 1.3))::numeric, 2),
            1350.0000, 1690.0000, 0.9800, 0.9080
        );

        -- MÍA ĐƯỜNG - Model LSTM
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            4, 'LSTM', f_date,
            ROUND((base_sugar * (1 + 0.0015 * j))::numeric, 2),
            ROUND((base_sugar * (1 + 0.0015 * j) * (1 - ci_spread))::numeric, 2),
            ROUND((base_sugar * (1 + 0.0015 * j) * (1 + ci_spread))::numeric, 2),
            8200.0000, 10500.0000, 0.7100, 0.9610
        );
        
        -- MÍA ĐƯỜNG - Model Prophet
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            4, 'Prophet', f_date,
            ROUND((base_sugar * (1 + 0.0012 * j))::numeric, 2),
            ROUND((base_sugar * (1 + 0.0012 * j) * (1 - ci_spread * 1.15))::numeric, 2),
            ROUND((base_sugar * (1 + 0.0012 * j) * (1 + ci_spread * 1.15))::numeric, 2),
            9200.0000, 11500.0000, 0.7800, 0.9410
        );

        -- MÍA ĐƯỜNG - Model ARIMA
        INSERT INTO forecasts (commodity_id, model_name, forecast_date, predicted_price, lower_ci, upper_ci, mae, rmse, mape, r2)
        VALUES (
            4, 'ARIMA', f_date,
            ROUND((base_sugar * (1 + 0.001 * j))::numeric, 2),
            ROUND((base_sugar * (1 + 0.001 * j) * (1 - ci_spread * 1.3))::numeric, 2),
            ROUND((base_sugar * (1 + 0.001 * j) * (1 + ci_spread * 1.3))::numeric, 2),
            10200.0000, 12500.0000, 0.8800, 0.9210
        );
    END LOOP;
END $$;

-- 5. Thêm các quy tắc cảnh báo mẫu (liên kết với user_id)
INSERT INTO alert_rules (commodity_id, user_id, rule_name, condition_type, threshold_value, email, is_active) VALUES
(2, 1, 'Cảnh báo Cà phê Robusta vượt 125,000 VNĐ/kg', 'PRICE_ABOVE', 125000.00, 'nongsanviet.alert@gmail.com', TRUE),
(2, 1, 'Cảnh báo Cà phê Robusta giảm dưới 110,000 VNĐ/kg', 'PRICE_BELOW', 110000.00, 'nongsanviet.alert@gmail.com', TRUE),
(1, 1, 'Cảnh báo Lúa gạo IR504 vượt đỉnh 9,000 VNĐ/kg', 'PRICE_ABOVE', 9000.00, 'gaomientay.market@gmail.com', TRUE),
(3, 2, 'Cảnh báo Hồ tiêu biến động tăng mạnh trên 145,000 VNĐ/kg', 'PRICE_ABOVE', 145000.00, 'chuse.pepper@gmail.com', FALSE);

-- 6. Thêm lịch sử cảnh báo đã kích hoạt (Alert Logs)
INSERT INTO alert_logs (rule_id, triggered_price, message, status) VALUES
(1, 125200.00, 'Giá Cà phê Robusta tại Đắk Lắk đã chạm mốc 125,200 VNĐ/kg, vượt ngưỡng thiết lập 125,000 VNĐ/kg.', 'SENT'),
(3, 9050.00, 'Giá Lúa gạo IR50404 tại Tiền Giang chạm mốc 9,050 VNĐ/kg, vượt ngưỡng thiết lập 9,000 VNĐ/kg.', 'SENT');
