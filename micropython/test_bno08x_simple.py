# BNO08x Micropython I2C Test program - Simplified version
# Basic sensor data display only

from machine import I2C, Pin
from utime import sleep_ms
from bno08x import *

# I2Cピン設定（ESP32モデル別）
I2C1_SDA = Pin(5)  # XIAO-ESP32 S3:5, C6:22, C3:6
I2C1_SCL = Pin(6)  # XIAO-ESP32 S3:6, C6:23, C3:7

# I2C初期化
i2c1 = I2C(0, scl=I2C1_SCL, sda=I2C1_SDA, freq=400000, timeout=200000)

# BNO085センサー初期化
bno = BNO08X(i2c1, debug=False)
print("BNO08x I2C connection : Done\n")

# センサー機能を有効化
bno.enable_feature(BNO_REPORT_ACCELEROMETER, 50)        # 加速度センサー 50ms間隔
bno.enable_feature(BNO_REPORT_GYROSCOPE, 50)            # ジャイロスコープ 50ms間隔
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR, 50) # ゲーム回転ベクトル 50ms間隔
bno.enable_feature(BNO_REPORT_GRAVITY, 50)              # 重力ベクトル 50ms間隔

# オイラー角とクォータニオンの設定
bno.set_quaternion_euler_vector(BNO_REPORT_GAME_ROTATION_VECTOR)

print("BNO08x sensors enabling : Done\n")
print("Starting sensor data display in 3 seconds...")
sleep_ms(3000)

# 初期キャリブレーション
bno.calibration()
print("Initial sensor calibration complete")
sleep_ms(1000)

# 姿勢の零点調整
bno.tare()
print("Tare operation complete - current orientation set as reference")
sleep_ms(1000)

print("\n===== Starting sensor data display =====\n")

# メインループ
count = 0
while True:
    count += 1
    
    print(f"===== Sensor Data Update #{count} =====")
    
    # 加速度データ（重力込み）
    accel_x, accel_y, accel_z = bno.acc
    print(f"Acceleration\tX: {accel_x:+.3f}\tY: {accel_y:+.3f}\tZ: {accel_z:+.3f}\tm/s²")
    
    # 重力ベクトル
    grav_x, grav_y, grav_z = bno.gravity
    print(f"Gravity\t\tX: {grav_x:+.3f}\tY: {grav_y:+.3f}\tZ: {grav_z:+.3f}\tm/s²")
    
    # 線形加速度（重力補正済み）
    linear_x = accel_x - grav_x
    linear_y = accel_y - grav_y
    linear_z = accel_z - grav_z
    print(f"Linear Accel\tX: {linear_x:+.3f}\tY: {linear_y:+.3f}\tZ: {linear_z:+.3f}\tm/s²")
    
    # ジャイロスコープ（角速度）
    gyro_x, gyro_y, gyro_z = bno.gyro
    print(f"Gyroscope\tX: {gyro_x:+.3f}\tY: {gyro_y:+.3f}\tZ: {gyro_z:+.3f}\trad/s")
    
    # オイラー角（Roll, Pitch, Yaw）
    roll, pitch, yaw = bno.euler
    print(f"Euler Angle\tRoll: {roll:+.3f}\tPitch: {pitch:+.3f}\tYaw: {yaw:+.3f}\trad")
    
    # クォータニオン
    quat_w, quat_x, quat_y, quat_z = bno.quaternion
    print(f"Quaternion\tW: {quat_w:+.3f}\tX: {quat_x:+.3f}\tY: {quat_y:+.3f}\tZ: {quat_z:+.3f}")
    
    print()  # 空行
    
    # 1秒間隔で表示
    sleep_ms(1000) 



'''    
===== Sensor Data Update #42 =====
Acceleration	X: -3.016	Y: -8.043	Z: -4.281	m/s²
Gravity		X: -3.023	Y: -8.047	Z: -4.281	m/s²
Linear Accel	X: +0.008	Y: +0.004	Z: +0.000	m/s²
Gyroscope	X: +0.008	Y: -0.008	Z: +0.008	rad/s
Euler Angle	Roll: -118.298	Pitch: +18.422	Yaw: -33.818	rad
Quaternion	W: -0.787	X: +0.325	Y: -0.016	Z: +0.524

'''