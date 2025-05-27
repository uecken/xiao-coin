# MicroPython ESP32 開発ガイド

## 目次
1. [開発環境の準備](#開発環境の準備)
2. [Thonnyの設定](#thonnyの設定)
3. [BNO085センサーの使用方法](#bno085センサーの使用方法)
4. [実践的なプロジェクト例](#実践的なプロジェクト例)

## 開発環境の準備

### 必要なもの
- ESP32開発ボード
- BNO085センサーモジュール
- ジャンパーワイヤー
- USB-Cケーブル（ESP32による）
- PC（Windows/Mac/Linux）

### Thonnyのインストール

1. [Thonny公式サイト](https://thonny.org/)からダウンロード
2. インストーラーを実行してセットアップ

![Thonnyダウンロードページ](images/thonny_download.png)

## Thonnyの設定



### MicroPythonファームウェアの書き込み

1. Thonnyメニューから「Tools」→「Options」
2. 上部オレンジ枠にて、MicroPython(ESP32)を選択
3. 右下オレンジ枠の「Install or update MicroPython(esptool)」を選択

![Thonny_Options](img_micropython/Thonny_Options.png)

3. XIAO EPS32のBootボタンを押しながらUSBケーブルを接続する。<br>
オレンジ枠にて、USB JTAG...と表示されているCOMポートを選択する。

4. ESP32用ファームウェアを選択し、Installボタンを押す。<br>
今回はXIAO ESP32S3を利用している。ESP32系に応じて選択する事。

![ファームウェア書き込み](img_micropython/Thonny_Install_micropython.png)



### ESP32への接続

1. XIAO EPS32のリセットボタンを押すか、USBケーブルを差し直す。
2. Thonnyで右下の"Local Python3"と表示されている個所をクリックし、適切なCOMポートを選択<br>
![Thonny_Select_COMPort](img_micropython/Thonny_Select_COMPort.png)


3. 接続確認 と ファイルアップロード
MicroPython(ESP32)と表示されていれば接続出来ている。

ファイルツリーが表示されていない場合、 View > File にて、ファイルツリーを表示する。
![Thonny_View_Files](img_micropython/Thonny_View_Files.png)


Githubのリポジトリからmicropythonフォルダをダウンロードし、Cドライブ直下に格納する。
https://github.com/uecken/xiao-coin

micropythonフォルダ内のファイルを選択し、アップロードする。
![Thonny_File_Upload](img_micropython/Thonny_File_Upload.png)


3. hellp.pyの動作確認
　hello.pyをダブルクリックし、再生ボタンを押す。
  コンソールに "hello" と表示されれば正常動作している。
![Thonny_hello.png](img_micropython/Thonny_hello.png)




## IMUセンサBNO085

1. 調達

* BNO085は AliExpressから購入すると安いです。
* 但しGroveコネクタを使う場合、3.3V⇔GND、SDA⇔SDLピンをそれぞれ入れ替える必要があるので注意してください。
https://ja.aliexpress.com/item/1005005902501032.html?spm=a2g0o.productlist.main.1.76313ee0UqewA3&algo_pvid=e84a5c67-44ba-44e8-b657-10176409957d&algo_exp_id=e84a5c67-44ba-44e8-b657-10176409957d-0&pdp_ext_f=%7B%22order%22%3A%22173%22%2C%22eval%22%3A%221%22%7D&pdp_npi=4%40dis%21JPY%212087%212087%21%21%21102.65%21102.65%21%402140ed7717480680463497576e6c43%2112000039594194852%21sea%21JP%211851543254%21X&curPageLogUid=CzGiY2nmisD4&utparam-url=scene%3Asearch%7Cquery_from%3A

![BNO085.png](img_micropython/BNO085.png)

2. 配線

- Groveコネクタを図のように配置し、3.3V⇔GND、SDA⇔SDLピンをそれぞれ入れ替えていることに注意してください。
- 一般的にI2CはSDAとSCLにプルアップ抵抗が必要です。通信が安定しない場合、3.3VとSDA、3.3VとSCLを繋ぐように4.7kΩの抵抗を接続して下さい。
![XIAO-BNO085_配線.png](img_micropython/XIAO-BNO085_配線.png)



 - 参考までに、Aliexpressのモジュールのピン配置、正規のGroveコネクタのピン配置を参考として示します。正規のGroveコネクタのピン配置に合わせるために、3.3V⇔GND、SDA⇔SDLピンをそれぞれ入れ替える必要があります。
![Groveピン配_Aliexモジュールピン配.png](img_micropython/Groveピン配_Aliexモジュールピン配.png)





3. I2CのSDAとSDLピン合わせ

I2Cのピン配置は利用するESP32のピン配置によって異なります。
```
I2C1_SDA = Pin(5) #XIAO-ESP32C6:22,  C3:6, S3:5, M5StickC:0
I2C1_SCL = Pin(6) #XIAO-ESP32C6:23,  C6:7, S3:6, M5StickC:26
```

test_bno08x.pyを選択し、実行する。
![Thonny_プログラム実行](img_micropython/Thonny_BNO085_プログラム実行.png)

参考までに、Ceva BNO085は高精度IMUであり多くのロボットやゲーム器に採用されている。
Euler AngleのX,Yは水平角度のずれを示すので、水平器等に応用ができる。
