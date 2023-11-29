# 対話システムライブコンペティションセットアップ

## 推奨環境環境

### 一般開発者

- Windows 11
- CUDA 12.1

### SUNABA開発者

- Windows 11


## ディレクトリ構成の要件

ダウンロードするソフトウェアは以下のような構成になるようにしてください。
`start.bat`は以下の構成でなければ正しく動作しません。

```
-- AmazonPollyServer/
|   |- config/
|   |- docs/
|   |- 00-launch-AmazonPollyServer.bat
|   |- ...
|- CGEricaSet/
|   |- 01-OculusLipSync/
|   |- 02-CGErica/
|   |- 03-MiracleErica/
|   |- 04-JointMapper/
|- dslc6/
|   |- dslclib/
|   |   |- ...
|   |- dockerfile
|   |- sample.py
|- FaceRecognitionServer/
|   |- face_recognition_server.pyz
|   |- ...
|- WebSocketBridge2/
|   |- Launcher2-TCPClient.bat
|   |- ...
|- installer.bat
|- README.md
|- start.bat
```


## セットアップ手順

### WSL2を有効化する (**必須ではありません**)

少なからずUNIX系での開発が好まれる方もいると思います。

その場合はWSL2を有効化し、`wsl -d Ubuntu`のようにして、Ubuntu環境で開発することができます。

また、こちらで検証はできていませんが、WSL経由のほうがWin上よりもGPUの動作が高速であるような記事も目にしていますので、
モデルの学習を行いたい方は配布するdockerコンテナをWSL上に建てるなどして使うと良いかもしれません。

[参考記事](https://www.kagoya.jp/howto/cloud/container/wsl2_docker/)

[はまりどころ](https://zenn.dev/ohno/articles/1cb49d190af1f4)

**必ずWindows Powershellの管理者権限で行うこと！！**

```bash
$ wsl --set-default-version 2
$ wsl --install
```

Ubuntuのディストリビューションを使う場合は次のようにして起動できます。

```bash
$ wsl -d Ubuntu
```

### インストール

今回セットアップ簡易化のため、`installer.bat`のバッチファイルを作成しています。

`installer.bat`を使用する場合は、**コマンドプロンプト**で以下のようにコマンドを打ってください。（`$`は入力しないでください。）

```
$ intaller.bat
```

以下のセットアップを順番に行います。手動での作業を促すため、完全に自動化されたものではないことに注意してください。
また、もともと開発者がインストールしているものとは競合を起こす可能性がありますので、以下インストールを促されるソフトウェアを見て、注意して扱ってください。

※`installer.bat`では、インストール前に対象ソフトウェアがインストール済みであるかチェックをかけます。その際に見つかった場合はインストールの手続きは行われません。

インストールをするもの
1. Java
2. Voicemeeter Banana
3. Python3.10.11
4. Docker for Windows

`installer.bat`を用いない場合、対話システムライブコンペティション5にて記載された手順を参考にセットアップを進めてください。

## 起動方法 (サンプルコードを動かす方法)

`start.bat`をたたくと、必要なアプリがすべて順番に起動します。

`start.bat`のバッチファイルの実行がすべて終わったのちに、dockerを立ち上げて、オウム返し対話システムを起動してください。

サンプルプログラムの一連の流れが以下になります。

### コマンドプロンプト1

```
$ start.bat

AmazonPollyServerを起動します。
AmazonPollyServerが起動しました。
続行するには何かキーを押してください . . .
CGEricaを起動します。
    OculusLipSyncを起動します。
続行するには何かキーを押してください . . .
    CGEricaを起動します。
続行するには何かキーを押してください . . .
    MiracleEricaを起動します。
続行するには何かキーを押してください . . .
    JointMapperを起動します。
CGEricaが起動しました。
続行するには何かキーを押してください . . .
FaceRecognitionServerを起動します。
FaceRecognitionServerが起動しました。
続行するには何かキーを押してください . . .
TCPSocketBridge2を起動します。
TCPSocketBridge2が起動しました。
Google Speech APIを起動します。connectを押してソケット通信を開始してください。
続行するには何かキーを押してください . . .

$
```
表示に従って順番に起動します。**順番に起動することが重要**です。（特にCGErica）

一つ一つアプリが起動するため、起動を確認してからキーを押し、次のアプリの立ち上げを行ってください。

**これは一度だけ起動してください。**

### コマンドプロンプト2

```
$ docker build dslc6 -t dslc6
```

まずは、docker imageをビルドします。
`-t dslc6`と指定することで、作成されたイメージに`dslc6`の名前を与えます。
これにより起動したいイメージを探す必要がなくなります。

```
$ docker run --add-host="host.docker.internal:host-gateway" --rm -it dslc6
```

`docker run dslc6`によって、dslc6として作成したイメージを使用し、dockerコンテナを開始します。

`--rm`は、dockerコンテナを抜けたときに自動で削除するオプションです。これをつけないと、実行のたびにいらないコンテナがたまっていくので、つけることをお勧めします。

`-it`はコンテナの中に入るかどうかです。サンプルプログラムはコンテナの立ち上げと同時にpythonプログラムが起動する設定にしています。
`-it`なしでもプログラムは起動しますが、標準出力などをしているため、コンテナ内に入ったほうがどのようにプログラムがうごいているのかがわかると思います。

`--add-host="host.docker.internal:host-gateway"`は**必ず**つけるようにしてください。これはdockerコンテナ内から、ホストのポートとソケット通信を行うためです。
この手の処理は非常に面倒だと思われるため、対話コンペ用のPythonライブラリ`dslclib`を作成しました。この中で、自動でdockerコンテナ内かホストOSかを認識してipアドレスを自動設定します。

そのため、`--add-host="host.docker.internal:host-gateway"`は**必ず**つけるようにしてください。

## 起動方法 (開発時のすすめ)

先のサンプルコード用の起動とほとんど変わりませんが、開発時にはインタラクティブにコードを書き換えたいです。
そのため、すこし修正し、開発がインタラクティブにできるような方法を示します。

`start.bat`をたたくと、必要なアプリがすべて順番に起動します。

`start.bat`のバッチファイルの実行がすべて終わったのちに、dockerを立ち上げて、オウム返し対話システムを起動してください。

この流れ自体は変わりません。dockerの起動部分に少し工夫を加えます。

サンプルプログラムの一連の流れが以下になります。

### コマンドプロンプト1

```
$ start.bat

AmazonPollyServerを起動します。
AmazonPollyServerが起動しました。
続行するには何かキーを押してください . . .
CGEricaを起動します。
    OculusLipSyncを起動します。
続行するには何かキーを押してください . . .
    CGEricaを起動します。
続行するには何かキーを押してください . . .
    MiracleEricaを起動します。
続行するには何かキーを押してください . . .
    JointMapperを起動します。
CGEricaが起動しました。
続行するには何かキーを押してください . . .
FaceRecognitionServerを起動します。
FaceRecognitionServerが起動しました。
続行するには何かキーを押してください . . .
TCPSocketBridge2を起動します。
TCPSocketBridge2が起動しました。
Google Speech APIを起動します。connectを押してソケット通信を開始してください。
続行するには何かキーを押してください . . .

$
```
表示に従って順番に起動します。**順番に起動することが重要**です。（特にCGErica）

一つ一つアプリが起動するため、起動を確認してからキーを押し、次のアプリの立ち上げを行ってください。

**これは一度だけ起動してください。**


### コマンドプロンプト2

```
$ docker build dslc6 -t dslc6
```

まずは、docker imageをビルドします。
`-t dslc6`と指定することで、作成されたイメージに`dslc6`の名前を与えます。
これにより起動したいイメージを探す必要がなくなります。

```
$ docker run --add-host="host.docker.internal:host-gateway" -v <開発用のディレクトリの絶対パス>:/home/ubuntu/<任意のディレクトリ名> --rm -it dslc6 /bin/bash
```

`docker run dslc6`によって、dslc6として作成したイメージを使用し、dockerコンテナを開始します。

`--rm`は、dockerコンテナを抜けたときに自動で削除するオプションです。これをつけないと、実行のたびにいらないコンテナがたまっていくので、つけることをお勧めします。

`-it`はコンテナの中に入るかどうかです。サンプルプログラムはコンテナの立ち上げと同時にpythonプログラムが起動する設定にしています。
`-it`なしでもプログラムは起動しますが、標準出力などをしているため、コンテナ内に入ったほうがどのようにプログラムがうごいているのかがわかると思います。

`--add-host="host.docker.internal:host-gateway"`は**必ず**つけるようにしてください。これはdockerコンテナ内から、ホストのポートとソケット通信を行うためです。
この手の処理は非常に面倒だと思われるため、対話コンペ用のPythonライブラリ`dslclib`を作成しました。この中で、自動でdockerコンテナ内かホストOSかを認識してipアドレスを自動設定します。

そのため、`--add-host="host.docker.internal:host-gateway"`は**必ず**つけるようにしてください。

**----- 以下から異なります。-----**

`-v <開発用のディレクトリの絶対パス>:/home/ubuntu/<任意のディレクトリ名>`の指定により、dockerコンテナに開発用のディレクトリをマウントします。
これにより、docker上での変更およびホスト上での変更の両方が適応されるようになります。
最終的には、このディレクトリをdockerにコピーしたイメージの提出をしていただくことになりますが、開発時はマウントすることでより快適な開発が可能になります。

`/bin/bash`を指定するのは、今のdockerfileでは、コンテナ起動時に、サンプル対話システムが呼び出されるのを、`/bin/bash`で上書きすることで、シェル操作を起動するためです。
dockerfileの最後の`CMD [ "python3", "sample.py" ]`を`CMD [ "/bin/bash"]`に変更すれば済みますが、dockerの操作に自信のない方ははじめは、上に示した`docker run ...`で開発を始めることができます。
