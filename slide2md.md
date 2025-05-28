ご提示いただいたソースに基づき、Markdown形式で内容をまとめます。画像のダウンロードについては、システム上の制約により直接提供することができません。元のソースのスライドをご参照いただく形となりますことをご了承ください。

---

# XIAO-Coin 半田付け手順


ウェブサイトリンク: [https://www.switch-science.com/products/10032](https://www.switch-science.com/products/10032)

## 注意点


- CR2032電池は使えません。 (画像にはCR2032電池がバツ印と共に示されています)
- リチウム電池は使えません。
- **リチウムイオンコイン電池であるLIR2032/2450専用です**。
- **半田付けに慣れていないと難しいです**。

## 更新履歴


2025/5/23
1. XIAOと基板の充電端子を半田付けし易くするため中央部分をカットし、Castellated Holeとしました。
2. Grove端子の電源のデフォルトは3.3Vですが、Solder Jumperにより5Vを選択できるようにしました。
   またGrove端子を追加で表にもう一つ付けられるようにしました。
   (画像には基板の表と裏が示されており、変更点と思われる箇所がオレンジ色で囲まれています)

![xiao-coin_v0.4_difference.png](img/xiao-coin_v0.4_difference.png)


## 製品紹介

 (画像は「製品紹介」のタイトルのみ)



## 用途例


## 特徴


- XIAOの小ささとLipo充電端子を生かしたコインホルダー一体型無線マイコン。
- Grove端子でその他I2Cセンサ接続可。
- 電池容量の例は45mAh ～ 120mAh (2032 ～ 2450サイズ対応)。 (ソースはこれらの容量の電池販売ページを示唆しています)
- 各種XIAOシリーズに対応 (C3, S3, C6...)。
- 別途、IMUセンサが付けられる基板販売予定。
- また、表面実装ICのカスタムセンサ基板制作のご依頼受け付けます。


## LIR2032コイン電池 70mAh

EEMB LIR2032H 充電式バッテリー 3.7V リチウムイオン コインボタン電池 70mAh
価格: ¥1,309

![LIR2032Hコイン電池70mAh.png](img/LIR2032Hコイン電池70mAh.png)

## 詳細


BOM,
[https://docs.google.com/spreadsheets/d/1hsU4CdXzT7cGG6bdwNirwb3Pn3HpmJ6PeojrWailB_KM/edit?usp=sharing](https://docs.google.com/spreadsheets/d/1hsU4CdXzT7cGG6bdwNirwb3Pn3HpmJ6PeojrWailB_KM/edit?usp=sharing)
Github (PCB) 準備中

## Schematics

![XIAO_接続図.png](img/XIAO_接続図.png)

## PCB

![XIAO_PCB.png](img/XIAO_PCB.png)


## BOM

| 名称 | 価格 | 販売先 | 備考 | URL |
|------|------|--------|------|-----|
| XIAO ESP32 C3/C6/S3 | 630円 | Seeed | C6 4.9$<br>C3 4.2$<br>150円/$ | - |
| ボタン電池基板取付用ホルダー CH29-2032LF | 50円 | 秋月電子 | - | https://akizukidenshi.com/catalog/g/g108965/ |
| スライドスイッチ MK-12D13G4-B | 40$/500個 | - | - | https://www.lcsc.com/product-detail/Slide-Switches_HOOYA-MK-12D13G4-B_C20611678.html |
| Groveコネクター L型 スルーホール | 15円 | 秋月電子 | 1個 | https://akizukidenshi.com/catalog/g/g112634/ |



### コスト
#### XIAO各種モデルの単価（Seeed社から10個購入時）

XIAOの単価はC3が最も安くC3だと630円/個で試作できるため、各種センサの動作評価に向いています。私は毎回ソフトやセンサを付け替えて後で動作させるのに時間がかからないように、動作したセンサとセットで組み合わせて保管するようにしています。


| モデル | 単価（USD） | 単価（円）* |
|--------|-------------|-------------|
| XIAO ESP32 C3 | $4.20 | 630円 |
| XIAO ESP32 C6 | $4.90 | 735円 |
| XIAO ESP32 S3 | $5.40 | 810円 |

*為替レート: 1USD = 150円で計算

Groveコネクタが必要だったり、充電池と電源スイッチが必要な場合、このXIAOコイン基板は向いています。





## 連絡先

やわらかじお
[yawaraka.radio@gmail.com](mailto:yawaraka.radio@gmail.com)

---
画像のダウンロードについては、前述の通り直接提供することができません。内容は上記のMarkdown形式でまとめましたので、ご活用ください。