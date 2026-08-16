<p align="center">
  <a href="#zh">简体中文</a> ·
  <a href="#ja">日本語</a> ·
  <a href="#en">English</a>
</p>

<a id="zh"></a>

# BMS_div

BMS_div is a lightweight tool for organizing BMS charts. Users can group notes by keysound name, either automatically or manually, and export the grouped BMS files or REAPER projects.

## 简体中文

### 项目简介

BMS_div 是一款用于整理 BMS 谱面的轻量工具，可根据按键音名称对 note 进行自动分组，并导出已分组的 BMS 文件或 REAPER 工程。

### 主要功能

- 对 BMS 按键音进行自动分组
- 在 GUI 中手动管理分组
- 导出分组后的 BMS 文件
- 导出 REAPER `.rpp` 工程
- 导出 / 导入分组配置为 JSON
- 通过语言切换支持简体中文、日文和英文

### 系统要求

- Python 3.9+
- tkinter
- 可选依赖：pygame, chardet

### 安装

```bash
pip install -r requirements.txt
```

### 启动

```bash
python bms_div.py
```

### GUI 快捷功能

- Enter：在搜索框中按回车后执行“按关键词分组”
- Ctrl + Z：撤销上一条分组操作
- Ctrl + Y：重做刚撤销的分组操作
- F2：重命名当前选中的分组
- Delete：解散当前选中的分组
- 左键点击：预览该音源的声音，方便快速判定分组归属
- 右键菜单：快捷管理分组，包括重命名、合并、解散等操作
- 中键点击：将当前选中的文件名复制到输入框，可使用智能退格功能快速删去批处理编号

### 命令行使用

#### 仅加载 BMS 文件

```bash
python bms_div.py path/to/chart.bms
```

#### 使用 JSON 配置导出分组 BMS

```bash
python bms_div.py path/to/chart.bms path/to/groups.json -o bms
```

#### 使用 JSON 配置导出 RPP

```bash
python bms_div.py path/to/chart.bms path/to/groups.json -o rpp
```

#### 指定语言

```bash
python bms_div.py --lang zh
python bms_div.py --lang ja
python bms_div.py --lang en
```

#### 查看版本

```bash
python bms_div.py --version
```

---

<a id="ja"></a>

## 日本語

### プロジェクト概要

BMS_div は、BMS 譜面を整理するための軽量ツールです。ユーザーはキー音名に基づいて note を自動または手動で分組し、分組済みの BMS ファイルや REAPER プロジェクトを出力できます。

### 主な機能

- BMS 譜面の WAV マッピングと BPM 情報を読み込み
- GUI でグループの作成、名前変更、統合、解散を実行
- キーワード検索や自動ロジックで残りの音源をまとめて分組
- 分組済み BMS を出力
- REAPER の `.rpp` を出力
- 分組設定を JSON でインポート / エクスポート
- 中文 / 日本語 / English の三言語切り替えに対応

### 必要環境

- Python 3.9+
- tkinter
- 任意依存: pygame
- 任意依存: chardet

### インストール

```bash
pip install -r requirements.txt
```

### 起動

```bash
python bms_div.py
```

### GUI のショートカット機能

- Enter：検索欄で Enter を押すと「キーワードでグループ化」を実行
- Ctrl + Z：直前の分組操作を取り消し
- Ctrl + Y：取り消しをやり直し
- F2：現在選択中のグループ名を変更
- Delete：現在選択中のグループを解散
- 左クリック：リスト項目の音声をプレビューして、所属グループを判断しやすくする
- 右クリック：未分類リストから新規グループまたは既存グループへ即移動
- 中クリック：選択中のファイル名を入力欄にコピーし、バッチ番号を簡単に削除

### CLI の使用例

#### BMS ファイルのみ読み込み

```bash
python bms_div.py path/to/chart.bms
```

#### JSON を使って分組済み BMS を出力

```bash
python bms_div.py path/to/chart.bms path/to/groups.json -o bms
```

#### JSON を使って RPP を出力

```bash
python bms_div.py path/to/chart.bms path/to/groups.json -o rpp
```

#### 言語指定

```bash
python bms_div.py --lang zh
python bms_div.py --lang ja
python bms_div.py --lang en
```

#### バージョン確認

```bash
python bms_div.py --version
```

---

<a id="en"></a>

## English

### Project overview

BMS_div is a lightweight tool for organizing BMS charts. Users can group notes by keysound name, either automatically or manually, and export the grouped BMS files or REAPER projects.

### Features

- Parse BMS files and extract WAV mappings and BPM metadata
- Create, rename, merge, and disband groups from the GUI
- Use keyword search or built-in automatic logic to group remaining sounds
- Export grouped BMS files
- Export REAPER `.rpp` project files
- Import and export group configuration as JSON
- Support Chinese, Japanese, and English via built-in language switching

### Requirements

- Python 3.9+
- tkinter
- optional: pygame
- optional: chardet

### Installation

```bash
pip install -r requirements.txt
```

### Running the application

```bash
python bms_div.py
```

### Shortcut features

- Enter: run the keyword grouping action from the search box
- Ctrl + Z: undo the previous grouping action
- Ctrl + Y: redo the last undone grouping action
- F2: rename the currently selected group
- Delete: disband the currently selected group
- Left-click: preview the sound to help decide group membership faster
- Right-click: move a selection into a new or existing group immediately
- Middle-click: copy the selected filename into the input box for quick cleanup of batch numbering

### CLI examples

#### Load a BMS file only

```bash
python bms_div.py path/to/chart.bms
```

#### Export grouped BMS using an existing JSON config

```bash
python bms_div.py path/to/chart.bms path/to/groups.json -o bms
```

#### Export RPP using an existing JSON config

```bash
python bms_div.py path/to/chart.bms path/to/groups.json -o rpp
```

#### Set locale explicitly

```bash
python bms_div.py --lang zh
python bms_div.py --lang ja
python bms_div.py --lang en
```

#### Show version

```bash
python bms_div.py --version
```
