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


![Thonny_File_Upload](img_micropython/Thonny_File_Upload.png)



## BNO085センサーの使用方法

### 配線図

BNO085とESP32の接続：
