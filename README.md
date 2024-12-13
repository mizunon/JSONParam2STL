# JSONParam2STL for AutoDesk Fusion (Fusion360)

AutoDesk Fusion (Fusion360)で、複数のパラメータをパラメータセットとして変更しながらのボディの連続STL出力が可能です。

## 概要

- Fusionの複数のパラメータを、パラメータセットとしてJSONファイルで定義し、変更しながらの連続STL出力が可能です。
- 押し出し高さや面のオフセット等のフィーチャーの値を外部ファイルで定義し、一括でSTL出力できるので、高さ違いを複数造りたい時や、3Dプリンターの精度が良くない時の嵌め合いパラメーター調整等の手間が省けます。
- 例えば、高さ1mm違いのモデル20個のSTLを10秒で一括出力できます。

### 良い所
- 可視になっているボディ全てがSTL出力されます。不可視のボディは出力されません。
- 設定内容となるパラメータセットはJSONファイルで定義可能。
- STLの単位等の出力パラメータも変更可能。
- STLはパラメータセットごとにファイル出力され、ファイル名にはセット名が付与されます。
- STL出力後には、パラメータは出力前に戻ります。

### 悪い所
- Undoバッファに変更履歴が沢山記録されます。

### 良いのか悪いのか分からない所
- 2つ目以降のパラメータセットで変更すべき変数名を忘れると、前のセットの値が引き継がれてしまう。


## インストール方法

-以下の手順でプロジェクトをFusionのマイスクリプト（メインメニューの「ユーティリティ」→「アドイン」→「スクリプトとアドイン」）としてインストールしてください。
-マイスクリプトのディレクトリは、ダミーでマイスクリプトをつくって右クリック→「ファイルの場所を開く」で見つかります。

```Console
Fusion360のマイスクリプトのディレクトリにリポジトリをクローン
git clone https://github.com/mizunon/JSONParam2STL.git
```

## 使い方

- メインメニュー「ソリッド」→「修正」→「パラメータの変更」を選択。
- 「パラメータ」ウィンドウで設定したい個所のパラメータの「名前」を分かりやすく変更します。この名前がJSONファイルのパラメータ名になります。
  - 「名前」は下記の画像での「case_lower_h」や「sukima」です。変更できない「パラメータ」列の名称（「AlongDistance」や「distance」）ではないので注意して下さい。
  - ![2024y12m14d_015418447](https://github.com/user-attachments/assets/c03bbf43-d00e-43d2-b126-1b8764de4520)
- Sample.jsonを参考にJSONファイルを作ります。１つのセットでパラメータはいくつでも設定できます。
- パラメータセットのname要素が、ファイル名の末尾に付与されます。
- メインメニューの「ユーティリティ」→「アドイン」→「スクリプトとアドイン」から「JSONParam2STL」をダブルクリックか右下の「実行」を選択してスクリプトを実行します。
  - ![2024y12m14d_015620995](https://github.com/user-attachments/assets/a8ae2107-a57e-4d32-a93b-57d4f3c20ea4)
- JSONファイルの選択ダイアログが開きます。作成したJSONファイルを選択してください。
- JSONのoutput_folder要素が設定されていればそのディレクトリに、設定されていなければ、ディレクトリの指定ダイアログでSTLの保存場所を指定できます。
- 指定されたディレクトリにSTLファイルが連続出力されます。
  - ![2024y12m14d_023516203](https://github.com/user-attachments/assets/9d0bde5b-9ccf-449c-8ed6-1f85e3a49b34)

- JSONファイルのサンプル（上記の出力例）
```Sample.json
{
  "stl_settings": {
    "refinement": "medium",
    "unit_type": "mm",
    "output_folder": "",
    
    "surface_deviation": 0,
    "normal_deviation": 0,
    "max_edge_length": 0,
    "aspect_ratio": 0
  },
  "parameter_sets": [
	  {
	    "name": "p005mm",
	    "parameters": {
	      "sukima": "0.05 mm",
	      "case_lower_h": "2.5 mm"
	    }
	  },
	  {
	    "name": "p010mm",
	    "parameters": {
	      "sukima": "0.1 mm",
	      "case_lower_h": "5 mm"
	    }
	  },
	  {
	    "name": "n001mm",
	    "parameters": {
	      "sukima": "-0.1 mm",
	      "case_lower_h": "10 mm"
	    }
	  }
  ]
}
```

## 作成完了
- 使用したFusionのバージョン：2.0.20981 x86_64 / Windows 11 Pro 23H2


## 作成者
Takuhiro Mizuno / 水野 拓宏 / [@mizunon](https://twitter.com/mizunon)


## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。
"Fusion360 JSONParam2STL" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
