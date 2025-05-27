# BNO08x Micropython I2C Test programm by Dobodu
# Modified for 100Hz position tracking

from machine import I2C, Pin, Timer
from utime import ticks_ms, sleep_ms, ticks_diff, sleep_us
import math
from bno08x import *

I2C1_SDA = Pin(5) #XIAO-ESP32C6:22, M5StickC:0 C3:6 S3:5   
I2C1_SCL = Pin(6) #XIAO-ESP32C6:23, M5StickC:26 C6:7 S3:6

i2c1 = I2C(0, scl=I2C1_SCL, sda=I2C1_SDA, freq=400000, timeout=200000)

bno = BNO08X(i2c1, debug=False)
print("BNO08x I2C connection : Done\n")

# より高い更新レートでセンサーを有効化
bno.enable_feature(BNO_REPORT_ACCELEROMETER, 10)  # 10ms = 100Hz
bno.enable_feature(BNO_REPORT_MAGNETOMETER, 20)
bno.enable_feature(BNO_REPORT_GYROSCOPE, 10)  # 10ms = 100Hz
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR, 10)
bno.enable_feature(BNO_REPORT_GRAVITY, 10)  # 10ms = 100Hz
bno.set_quaternion_euler_vector(BNO_REPORT_GAME_ROTATION_VECTOR)

class PositionTracker:
    def __init__(self):
        # 位置と速度の初期化
        self.pos_x, self.pos_y, self.pos_z = 0.0, 0.0, 0.0
        self.vel_x, self.vel_y, self.vel_z = 0.0, 0.0, 0.0
        self.last_time = None
        self.init_pos_x, self.init_pos_y, self.init_pos_z = 0.0, 0.0, 0.0
        
        # 二重積分誤差対策のパラメータ
        self.deadzone = 0.05        # デッドゾーン（m/s²）
        self.decay_factor = 0.99    # 速度減衰係数（ドリフト対策）
        
        # 計算パフォーマンス用変数
        self.update_count = 0
        self.last_print_time = 0
        self.min_dt = 1.0
        self.max_dt = 0.0
        self.avg_dt = 0.0
        self.total_dt = 0.0
        
    def reset(self):
        """位置と速度をリセットする"""
        self.init_pos_x, self.init_pos_y, self.init_pos_z = self.pos_x, self.pos_y, self.pos_z
        self.vel_x, self.vel_y, self.vel_z = 0.0, 0.0, 0.0
        self.last_time = ticks_ms()
        
        # 統計情報もリセット
        self.update_count = 0
        self.min_dt = 1.0
        self.max_dt = 0.0
        self.avg_dt = 0.0
        self.total_dt = 0.0
        self.last_print_time = ticks_ms()
        
    def update(self, accel_x, accel_y, accel_z):
        """加速度データから位置を更新する（100Hz呼び出し目標）"""
        current_time = ticks_ms()
        
        # 初回呼び出し時は時間だけ記録して終了
        if self.last_time is None:
            self.last_time = current_time
            return
        
        # 経過時間を計算（秒単位）
        dt = ticks_diff(current_time, self.last_time) / 1000.0
        self.last_time = current_time
        
        # 統計情報の更新
        self.update_count += 1
        self.total_dt += dt
        self.min_dt = min(self.min_dt, dt)
        self.max_dt = max(self.max_dt, dt)
        self.avg_dt = self.total_dt / self.update_count
        
        # デッドゾーン処理（小さな加速度は無視）
        if abs(accel_x) < self.deadzone: accel_x = 0
        if abs(accel_y) < self.deadzone: accel_y = 0
        if abs(accel_z) < self.deadzone: accel_z = 0
        
        # 速度を積分（台形則）
        self.vel_x += accel_x * dt
        self.vel_y += accel_y * dt
        self.vel_z += accel_z * dt
        
        # 速度の減衰（ドリフト対策）
        self.vel_x *= self.decay_factor
        self.vel_y *= self.decay_factor
        self.vel_z *= self.decay_factor
        
        # 位置を積分
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt
        self.pos_z += self.vel_z * dt
    
    def get_relative_position(self):
        """初期位置からの相対位置を返す"""
        rel_x = self.pos_x - self.init_pos_x
        rel_y = self.pos_y - self.init_pos_y
        rel_z = self.pos_z - self.init_pos_z
        return rel_x, rel_y, rel_z
        
    def print_position(self):
        """現在の相対位置と統計情報を出力する"""
        rel_x, rel_y, rel_z = self.get_relative_position()
        print("Position\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm".format(rel_x, rel_y, rel_z))
        print("Velocity\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm/s".format(self.vel_x, self.vel_y, self.vel_z))
        print("Update rate: {:.1f}Hz (dt min={:.1f}ms, max={:.1f}ms, avg={:.1f}ms)".format(
            self.update_count / (ticks_diff(ticks_ms(), self.last_print_time) / 1000), 
            self.min_dt * 1000, 
            self.max_dt * 1000, 
            self.avg_dt * 1000))


# 位置追跡オブジェクトの作成
position_tracker = PositionTracker()

print("BNO08x sensors enabling : Done\n")
print("Position tracking initialized. Starting in 3 seconds...")
sleep_ms(3000)  # センサー初期化と安定化の時間
position_tracker.reset()  # 位置追跡をリセット

# メインループのタイミング制御用変数
cpt = 0
timer_origin = ticks_ms()
last_update_time = ticks_ms()
last_display_time = ticks_ms()

# キャリブレーション（起動時に行う）
bno.calibration()
print("Initial sensor calibration complete")
sleep_ms(1000)
bno.tare()  # 姿勢の零点調整
print("Tare operation complete - current orientation set as reference")
sleep_ms(1000)

while True:
    current_time = ticks_ms()
    
    # 100Hz (10ms) での更新を目指す
    if ticks_diff(current_time, last_update_time) >= 10:  # 10ms = 100Hz
        # センサーデータ取得
        accel_x, accel_y, accel_z = bno.acc
        grav_x, grav_y, grav_z = bno.gravity
        
        # 線形加速度（重力補正した加速度）を計算
        linear_x = accel_x - grav_x
        linear_y = accel_y - grav_y
        linear_z = accel_z - grav_z
        
        # 位置を更新
        position_tracker.update(linear_x, linear_y, linear_z)
        
        last_update_time = current_time
        cpt += 1
    
    # 画面表示は5回/秒に制限（200ms）
    if ticks_diff(current_time, last_display_time) >= 200:
        print("\n===== Position Update (count: {}) =====".format(cpt))
        
        # センサー値表示
        accel_x, accel_y, accel_z = bno.acc
        grav_x, grav_y, grav_z = bno.gravity
        linear_x = accel_x - grav_x
        linear_y = accel_y - grav_y
        linear_z = accel_z - grav_z
        
        print("Acceleration\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm/s²".format(accel_x, accel_y, accel_z))
        print("Gravity\t\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm/s²".format(grav_x, grav_y, grav_z))
        print("Linear Accel\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\tm/s²".format(linear_x, linear_y, linear_z))
        
        gyro_x, gyro_y, gyro_z = bno.gyro
        print("Gyroscope\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}\trads/s".format(gyro_x, gyro_y, gyro_z))
        
        R, T, P = bno.euler
        print("Euler Angle\tX: {:+.3f}\tY: {:+.3f}\tZ: {:+.3f}".format(R, T, P))
        
        # 位置情報の出力
        position_tracker.print_position()
        
        last_display_time = current_time
    
    # 1秒ごとに位置追跡をリセットする（長時間ドリフト対策）
    if cpt % 100 == 0 and cpt > 0:
        position_tracker.reset()
        print("Position tracking reset to prevent drift")
    
    # ループ内でのスリープ（CPU負荷軽減）
    sleep_us(100)  # 0.1msの短いスリープ




