# Fusion360 JSONParam2STL

Fusion360で、複数のパラメータをパラメータセットとして変更しながらのボディの連続STL出力が可能です。

## 概要

Fusion360の複数のパラメータを、パラメータセットとしてJSONファイルで定義し、変更しながらの連続STL出力が可能です。
押し出し高さや面のオフセット等のフィーチャーの値を外部ファイルで定義し、一括でSTL出力できるので、高さ違いを複数造りたい時や、3Dプリンターの精度が良くない時の嵌め合いパラメーター調整等の手間が省けます。
例えば、高さ1mm違いのモデル20個のSTLを10秒で一括出力できます。

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

以下の手順でプロジェクトをFusion360のマイスクリプト（メインメニューの「ユーティリティ」→「アドイン」→「スクリプトとアドイン」）としてインストールしてください。
マイスクリプトのディレクトリは、ダミーでマイスクリプトをつくって右クリック→「ファイルの場所を開く」で見つかります。

```Console
Fusion360のマイスクリプトのディレクトリにリポジトリをクローン
git clone https://github.com/mizunon/JSONParam2STL.git
```

## 使い方

- メインメニュー「ソリッド」→「修正」→「パラメータの変更」を選択。
- 「パラメータ」ウィンドウで設定したい個所のパラメータの「名前」を分かり安く変更します。この名前がJSONファイルのパラメータ名になります。変更できない「パラメータ」列の名称ではないので注意して下さい。
- Sample.jsonを参考にJSONファイルを作ります。１つのセットでパラメータはいくつでも設定できます。
- パラメータセットのname要素が、ファイル名の末尾に付与されます。

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
- 使用したFusion360のバージョン：2.0.20981 x86_64 / Windows 11 Pro 23H2


## 作成者
Takuhiro Mizuno
[@mizunon](https://twitter.com/mizunon)


## ライセンス

このプロジェクトはMITライセンスのもとで公開されています。
"Fusion360 JSONParam2STL" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).
