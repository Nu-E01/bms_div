import re
import os
import json
import math
import sys
import locale
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from pathlib import Path


LANGUAGES = {
    "zh": {
        "title": "BMS_div",
        "select_file": "选择BMS文件",
        "not_selected": "未选择文件",
        "ready": "就绪",
        "waiting": "加载中...",
        "loading_audio": "预加载音频中...",
        "load_success": "成功加载",
        "initial_bpm": "初始BPM={}",
        "pending_group": "待分组",
        "groups": "分组",
        "group_detail": "组内详情",
        "group_name_col": "组名",
        "count_col": "数量",
        "search_group": "搜索并分组",
        "group_remaining": "剩余分一组",
        "export_bms": "导出BMS",
        "export_rpp": "导出RPP",
        "export_json": "导出分组配置",
        "import_json": "导入分组配置",
        "file_error": "文件错误",
        "rpp_fail": "RPP 导出失败",
        "group_import_fail": "分组导入失败",
        "bms_export_done": "BMS 导出完毕",
        "rpp_export_done": "RPP 导出完毕：{}",
        "group_export_ok": "分组导出成功",
        "group_import_ok": "导入完成：共 {} 个分组",
        "group_import_failed": "导入失败：{}",
        "rename_group": "重命名",
        "new_group": "新建组",
        "merge_group": "合并组",
        "rename_group_prompt": "原名: {}",
        "enter_group_name": "请输入组名：",
        "enter_merge_name": "请输入合并后的组名：",
        "group_config": "导出分组配置",
        "loading_timeline": "正在计算时间线...",
        "move_to_new": "移入新组",
        "move_to_existing": "移入现有组",
        "remove_from_group": "移出本组",
        "move_to_other": "移入其他组",
        "disband_group": "解散组",
        "move_to_new_short": "移入新组",
        "load_failed": "加载失败",
        "copy_group": "移入新组",
        "export_group_title": "导出分组配置",
        "import_group_title": "导入分组配置",
    },
    "ja": {
        "title": "BMS_div",
        "select_file": "BMSファイルを選択",
        "not_selected": "ファイル未選択",
        "ready": "準備完了",
        "waiting": "読み込み中...",
        "loading_audio": "音声を事前読み込み中...",
        "load_success": "読み込み成功",
        "initial_bpm": "初期BPM={}",
        "pending_group": "未分類",
        "groups": "グループ",
        "group_detail": "グループ詳細",
        "group_name_col": "グループ名",
        "count_col": "件数",
        "search_group": "キーワードでグループ化",
        "group_remaining": "残りの音源をまとめてグループ化",
        "export_bms": "BMSを出力",
        "export_rpp": "RPPを出力",
        "export_json": "グループ設定を出力",
        "import_json": "グループ設定を読み込み",
        "file_error": "ファイルエラー",
        "rpp_fail": "RPPの出力に失敗しました",
        "group_import_fail": "グループ設定の読み込みに失敗しました",
        "bms_export_done": "BMSの出力が完了しました",
        "rpp_export_done": "RPPの出力が完了しました：{}",
        "group_export_ok": "グループ設定の出力に成功しました",
        "group_import_ok": "読み込み完了：グループ数 {}",
        "group_import_failed": "読み込み失敗：{}",
        "rename_group": "名前変更",
        "new_group": "新規グループ",
        "merge_group": "グループを統合",
        "rename_group_prompt": "元の名前：{}",
        "enter_group_name": "グループ名を入力：",
        "enter_merge_name": "統合後のグループ名を入力：",
        "group_config": "グループ設定を出力",
        "loading_timeline": "タイムラインを計算中...",
        "move_to_new": "新規グループへ移動",
        "move_to_existing": "既存グループへ移動",
        "remove_from_group": "このグループから除外",
        "move_to_other": "他のグループへ移動",
        "disband_group": "グループを解散",
        "move_to_new_short": "新規グループへ",
        "load_failed": "読み込み失敗",
        "copy_group": "新規グループへ",
        "export_group_title": "グループ設定を出力",
        "import_group_title": "グループ設定を読み込み",
    },
    "en": {
        "title": "BMS_div",
        "select_file": "Select BMS file",
        "not_selected": "No file selected",
        "ready": "Ready",
        "waiting": "Loading...",
        "loading_audio": "Preloading audio...",
        "load_success": "Loaded successfully",
        "initial_bpm": "Initial BPM={}",
        "pending_group": "Unsorted",
        "groups": "Groups",
        "group_detail": "Group details",
        "group_name_col": "Group name",
        "count_col": "Count",
        "search_group": "Group by keyword",
        "group_remaining": "Group remaining sounds together",
        "export_bms": "Export BMS",
        "export_rpp": "Export RPP",
        "export_json": "Export group config",
        "import_json": "Import group config",
        "file_error": "File error",
        "rpp_fail": "RPP export failed",
        "group_import_fail": "Group config import failed",
        "bms_export_done": "BMS export complete",
        "rpp_export_done": "RPP export complete: {}",
        "group_export_ok": "Group config export successful",
        "group_import_ok": "Import complete: {} groups",
        "group_import_failed": "Import failed: {}",
        "rename_group": "Rename",
        "new_group": "New group",
        "merge_group": "Merge groups",
        "rename_group_prompt": "Original name: {}",
        "enter_group_name": "Enter group name:",
        "enter_merge_name": "Enter the merged group name:",
        "group_config": "Export group config",
        "loading_timeline": "Calculating timeline...",
        "move_to_new": "Move to new group",
        "move_to_existing": "Move to existing group",
        "remove_from_group": "Remove from this group",
        "move_to_other": "Move to another group",
        "disband_group": "Disband group",
        "move_to_new_short": "Move to new group",
        "load_failed": "Load failed",
        "copy_group": "Move to new group",
        "export_group_title": "Export group config",
        "import_group_title": "Import group config",
    },
}

def detect_system_language():
    candidate_strings = []

    try:
        current_locale = locale.getlocale()[0]
    except Exception:
        current_locale = None
    if current_locale:
        candidate_strings.append(current_locale)

    try:
        locale_name = locale.setlocale(locale.LC_ALL, "")
        if locale_name:
            candidate_strings.append(locale_name)
    except Exception:
        pass

    for candidate in candidate_strings:
        value = str(candidate).lower().replace("-", "_")
        if "zh" in value or "china" in value or "chinese" in value:
            return "zh"
        if "ja" in value or "japan" in value or "japanese" in value:
            return "ja"

        normalized = value.split("_", 1)[0]
        if normalized.startswith("zh"):
            return "zh"
        if normalized.startswith("ja"):
            return "ja"

    return "en"


CURRENT_LANG = os.getenv("BMS_DIV_LANG", detect_system_language())


def gettext(key, lang=None):
    locale_name = (lang or CURRENT_LANG or "en").lower()
    return LANGUAGES.get(locale_name, LANGUAGES["en"]).get(key, key)


def set_language(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang.lower() if lang else detect_system_language()
    if CURRENT_LANG not in LANGUAGES:
        CURRENT_LANG = "en"

try:
    import pygame
except ImportError:  # optional for headless validation or minimal installs
    pygame = None

try:
    import chardet
except ImportError:  # fallback to a common BMS encoding when charset detection is unavailable
    chardet = None


# ------------------------- Model layer -------------------------

class BMSParser:
    """Parse BMS files and validate track length data while excluding numeric channels."""

    RE_WAV_DEFINITION = re.compile(r'#WAV([0-9A-Z]{2})\s+(.+)\r?\n')
    RE_BPM_DEFINITION = re.compile(r'#BPM\s+(.+)\r?\n')
    RE_DATA_LINE_HEADER = re.compile(r'#\d{5}:')
    PROTECTED_CHANNELS = ("02", "03", "04", "06", "07", "08", "09", "97", "98")

    @staticmethod
    def parse_bms_content(lines):
        wav_id_to_path = {}
        wav_id_order = []

        for line_index, line in enumerate(lines):
            wav_match = BMSParser.RE_WAV_DEFINITION.match(line)
            if wav_match:
                wav_id = wav_match.group(1)
                wav_id_to_path[wav_id] = wav_match.group(2).strip()
                wav_id_order.append(wav_id)

            if BMSParser.RE_DATA_LINE_HEADER.match(line):
                header = line.split(":", 1)[0]
                channel_number = header[-2:]
                if channel_number not in BMSParser.PROTECTED_CHANNELS:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        data_content = parts[1].strip()
                        if len(data_content) % 2 != 0:
                            raise ValueError(
                                f"Track data length error (odd length): line {line_index + 1}\n"
                                f"Channel {channel_number} requires every two characters to represent one ID."
                            )

        initial_bpm = ""
        for line in lines:
            bpm_match = BMSParser.RE_BPM_DEFINITION.match(line)
            if bpm_match:
                initial_bpm = bpm_match.group(1)
                break

        return wav_id_to_path, wav_id_order, initial_bpm


class GroupManager:
    """Manage BMS keysound grouping logic and undo/redo history."""

    def __init__(self, wav_id_to_path=None, wav_id_order=None):
        self.label_bpm_info = None
        self.wav_id_order = wav_id_order or []
        self.original_wav_map = {}
        self.remaining_wav_map = {}
        self.groups = {}
        self.history_stack = []
        self.redo_stack = []
        if wav_id_to_path:
            self.reset_data(wav_id_to_path)

    def reset_data(self, wav_id_to_path):
        self.original_wav_map = dict(wav_id_to_path)
        self.remaining_wav_map = dict(wav_id_to_path)
        self.groups = {}
        self.history_stack = []
        self.redo_stack = []

    def save_state_to_history(self):
        snapshot = (
            self.remaining_wav_map.copy(),
            {name: group.copy() for name, group in self.groups.items()},
        )
        self.history_stack.append(snapshot)
        if len(self.history_stack) > 100:
            self.history_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if not self.history_stack:
            return False
        current_state = (
            self.remaining_wav_map.copy(),
            {name: group.copy() for name, group in self.groups.items()},
        )
        self.redo_stack.append(current_state)
        rem, grp = self.history_stack.pop()
        self.remaining_wav_map, self.groups = rem, grp
        return True

    def redo(self):
        if not self.redo_stack:
            return False
        current_state = (
            self.remaining_wav_map.copy(),
            {name: group.copy() for name, group in self.groups.items()},
        )
        self.history_stack.append(current_state)
        rem, grp = self.redo_stack.pop()
        self.remaining_wav_map, self.groups = rem, grp
        return True

    def create_group_by_search(self, query, reference_names_dict):
        group_name = query.strip()
        if not group_name:
            return None
        term_lower = group_name.lower()
        new_group_content = {}
        for wav_id, full_path in list(self.remaining_wav_map.items()):
            file_stem = Path(full_path).stem.lower()
            if term_lower in file_stem:
                new_group_content[wav_id] = self.remaining_wav_map.pop(wav_id)
        if new_group_content:
            if group_name in self.groups:
                self.groups[group_name].update(new_group_content)
            else:
                self.groups[group_name] = new_group_content
            return group_name
        return None

    def move_ids_to_target_group(self, wav_ids, target_group_name):
        if target_group_name not in self.groups:
            self.groups[target_group_name] = {}
        for wav_id in wav_ids:
            if wav_id in self.remaining_wav_map:
                self.groups[target_group_name][wav_id] = self.remaining_wav_map.pop(wav_id)
            else:
                for name in list(self.groups.keys()):
                    if wav_id in self.groups[name]:
                        self.groups[target_group_name][wav_id] = self.groups[name].pop(wav_id)
                        if not self.groups[name]:
                            del self.groups[name]
                        break

    def remove_ids_from_group(self, group_name, wav_ids):
        if group_name not in self.groups:
            return
        for wav_id in wav_ids:
            if wav_id in self.groups[group_name]:
                self.remaining_wav_map[wav_id] = self.groups[group_name].pop(wav_id)
        sorted_remaining = {}
        for wav_id in self.wav_id_order:
            if wav_id in self.remaining_wav_map:
                sorted_remaining[wav_id] = self.remaining_wav_map[wav_id]
        self.remaining_wav_map = sorted_remaining
        if not self.groups[group_name]:
            del self.groups[group_name]

    def disband_group(self, group_name):
        if group_name in self.groups:
            self.remaining_wav_map.update(self.groups.pop(group_name))
            sorted_remaining = {}
            for wav_id in self.wav_id_order:
                if wav_id in self.remaining_wav_map:
                    sorted_remaining[wav_id] = self.remaining_wav_map[wav_id]
            self.remaining_wav_map = sorted_remaining

    def rename_group(self, old_name, new_name, merge_if_exists=True):
        if old_name not in self.groups or not new_name:
            return
        content = self.groups.pop(old_name)
        if merge_if_exists and new_name in self.groups:
            self.groups[new_name].update(content)
        else:
            self.groups[new_name] = content

    def create_group_from_ids(self, group_name, wav_ids):
        target_group = {}
        for wav_id in wav_ids:
            if wav_id in self.remaining_wav_map:
                target_group[wav_id] = self.remaining_wav_map.pop(wav_id)
            else:
                for name in list(self.groups.keys()):
                    if wav_id in self.groups[name]:
                        target_group[wav_id] = self.groups[name].pop(wav_id)
                        if not self.groups[name]:
                            del self.groups[name]
                        break
        if group_name in self.groups:
            self.groups[group_name].update(target_group)
        else:
            self.groups[group_name] = target_group
        return group_name

    def merge_groups(self, group_names, new_name):
        merged_content = {}
        for name in group_names:
            if name in self.groups:
                merged_content.update(self.groups.pop(name))
        if new_name in self.groups:
            self.groups[new_name].update(merged_content)
        else:
            self.groups[new_name] = merged_content
        return new_name

    def group_all_remaining(self, group_name="remaining_group"):
        if not self.remaining_wav_map:
            return None
        while group_name in self.groups:
            group_name += ".1"
        self.groups[group_name] = self.remaining_wav_map.copy()
        self.remaining_wav_map = {}
        return group_name

    def export_to_json(self, export_path, base_directory=None):
        export_data = {}
        base_path = Path(base_directory) if base_directory else None
        for name, group in self.groups.items():
            export_data[name] = {}
            for wav_id, full_path in group.items():
                try:
                    rel_path = str(Path(full_path).relative_to(base_path)) if base_path else full_path
                except ValueError:
                    rel_path = str(full_path)
                export_data[name][wav_id] = rel_path
        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

    def import_from_json(self, import_path, base_directory=None):
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            new_groups = {}
            used_ids = set()
            base_path = Path(base_directory) if base_directory else None
            for group_name, group_content in data.items():
                current_group = {}
                for wav_id, json_path in group_content.items():
                    abs_json_path = (base_path / json_path).resolve() if base_path and not Path(json_path).is_absolute() else Path(json_path).resolve()
                    if wav_id not in self.original_wav_map:
                        return False, f"曲目不匹配：BMS 不含 ID [{wav_id}]"
                    current_wav_path = Path(self.original_wav_map[wav_id]).resolve()
                    if abs_json_path.name.lower() != current_wav_path.name.lower():
                        return False, f"曲目不匹配：ID [{wav_id}] 对应的文件名冲突。"
                    current_group[wav_id] = str(current_wav_path)
                    used_ids.add(wav_id)
                if current_group:
                    new_groups[group_name] = current_group
            self.groups = new_groups
            self.remaining_wav_map = {wid: p for wid, p in self.original_wav_map.items() if wid not in used_ids}
            return True, f"Import complete: {len(new_groups)} groups"
        except Exception as e:
            return False, f"Import failed: {e}"


# ------------------------- Writer logic -------------------------

def sanitize_filename(name):
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def get_adjusted_track_data(original_data, valid_ids):
    result = []
    for i in range(0, len(original_data), 2):
        note_id = original_data[i:i + 2]
        result.append(note_id if note_id in valid_ids else "00")
    return "".join(result)


def build_grouped_bms_content(lines, group_wavs):
    wav_ids_in_group = set(group_wavs.keys())
    output_lines = []
    for line in lines:
        if line.startswith("#WAV"):
            if line[4:6] in wav_ids_in_group:
                output_lines.append(line)
        elif BMSParser.RE_DATA_LINE_HEADER.match(line):
            header = line.split(":", 1)[0]
            channel = header[-2:]
            if channel in BMSParser.PROTECTED_CHANNELS:
                output_lines.append(line)
            else:
                raw_data = line.split(":", 1)[1].strip().strip("\r\n")
                new_data = get_adjusted_track_data(raw_data, wav_ids_in_group)
                output_lines.append(f"{header}:{new_data}\n")
        else:
            output_lines.append(line)
    return "".join(output_lines)


def _data_to_array(data):
    out = []
    note = ""
    for c in data:
        if c.isdigit() or c.isalpha():
            note += c
            if len(note) == 2:
                out.append(note)
                note = ""
    return out


def _update_data(old_data, new_data):
    old_data_len = len(old_data)
    new_data_len = len(new_data)
    data_lcm = int(old_data_len * new_data_len / math.gcd(old_data_len, new_data_len))
    old_data_factor = data_lcm / old_data_len
    new_data_factor = data_lcm / new_data_len
    merged_data = [0] * data_lcm
    for i in range(data_lcm):
        if i % old_data_factor == 0:
            old_data_value = old_data[int(i / old_data_factor)]
        else:
            old_data_value = "00"
        if i % new_data_factor == 0:
            new_data_value = new_data[int(i / new_data_factor)]
        else:
            new_data_value = "00"
        if new_data_value == "00":
            merged_data[i] = old_data_value
        else:
            merged_data[i] = new_data_value
    return merged_data


def compute_bms_timeline(bms_lines, wav_id_to_path):
    MPS_FACTOR = 240.0

    BMS_PLAYABLE_CHANNELS = (
        "01",
        "11", "12", "13", "14", "15", "16", "17", "18", "19",
        "21", "22", "23", "24", "25", "26", "27", "28", "29",
        "51", "52", "53", "54", "55", "56", "57", "58", "59",
        "61", "62", "63", "64", "65", "66", "67", "68", "69",
    )
    LONG_NOTE_CHANNELS = (
        "51", "52", "53", "54", "55", "56", "57", "58", "59",
        "61", "62", "63", "64", "65", "66", "67", "68", "69",
    )
    MEASURE_LEN_CHANNEL = "02"
    BPM_CHANNEL = "03"
    EXTBPM_CHANNEL = "08"
    STOP_CHANNEL = "09"

    chart_bpm = 120.0
    bpm_dict = {0.0: chart_bpm}
    bpm_positions = [0.0]
    bpmtime_dict = {0.0: 0.0}
    measurelen_dict = {}
    measurelentime_dict = {}
    stop_dict = {}
    stop_lengths = {}
    notes_dict = {}
    extbpm_dict = {}
    max_measure = 0
    master_volume = 100.0

    for line in bms_lines:
        line_strip = line.strip()
        if not line_strip.startswith('#'):
            continue

        bpm_tag = re.match(r'#BPM\s+(.+)', line_strip)
        if bpm_tag:
            try:
                chart_bpm = float(bpm_tag.group(1))
                bpm_dict[0.0] = chart_bpm
                bpm_positions = [0.0]
                bpmtime_dict[0.0] = 0.0
            except ValueError:
                pass
            continue

        vol_tag = re.match(r'#VOLWAV\s+(.+)', line_strip)
        if vol_tag:
            try:
                master_volume = float(vol_tag.group(1))
            except ValueError:
                pass
            continue

        extbpm_match = re.match(r'#BPM([0-9A-Za-z]{2})\s+(.+)', line_strip)
        if extbpm_match:
            extbpm_dict[extbpm_match.group(1)] = float(extbpm_match.group(2))
            continue

        stop_match = re.match(r'#STOP([0-9A-Za-z]{2})\s+(.+)', line_strip)
        if stop_match:
            stop_dict[stop_match.group(1)] = float(stop_match.group(2))
            continue

        note_re = re.match(r'#(\d{3})(\w{2}):?\s*(\S+)', line_strip)
        if note_re:
            measure = int(note_re.group(1))
            channel = note_re.group(2)
            data = note_re.group(3)
            if measure > max_measure:
                max_measure = measure

            if channel == MEASURE_LEN_CHANNEL:
                try:
                    measurelen_dict[measure] = float(data)
                except ValueError:
                    pass
                continue

            if channel in BMS_PLAYABLE_CHANNELS + (BPM_CHANNEL, EXTBPM_CHANNEL, STOP_CHANNEL) and data != "00":
                data_array = _data_to_array(data)
                header = f"{measure:03d}{channel}"
                if channel == "01":
                    notes_dict.setdefault(header, []).append(data_array)
                elif header in notes_dict:
                    notes_dict[header] = _update_data(notes_dict[header], data_array)
                else:
                    notes_dict[header] = data_array

    max_measure += 1

    keysound_lengths = {}
    import wave as _wave
    mutagen_available = False
    try:
        import mutagen
        mutagen_available = True
    except ImportError:
        pass
    for wav_id, wav_path in wav_id_to_path.items():
        ext = Path(wav_path).suffix.lower()
        try:
            if ext == '.wav':
                with _wave.open(wav_path, 'r') as wf:
                    keysound_lengths[wav_id] = wf.getnframes() / float(wf.getframerate())
            elif mutagen_available:
                keysound_lengths[wav_id] = mutagen.File(wav_path).info.length
            else:
                keysound_lengths[wav_id] = 1.0
        except Exception:
            keysound_lengths[wav_id] = 1.0

    sample_dict = {}
    channelsample_dict = {}
    current_timepos = 0.0
    current_bpmpos_i = 0
    active_long_notes = {}

    def measure_offset_seconds(start_measure, beatpos, bpmpos_array, stop_positions, measure_len):
        bpmpos = bpmpos_array[0]
        bpm = bpm_dict[bpmpos]
        if bpmpos < start_measure:
            bpmpos = start_measure

        current_time = 0.0
        for i in range(1, len(bpmpos_array)):
            next_bpmpos = bpmpos_array[i]
            if beatpos > next_bpmpos:
                current_time += (next_bpmpos - bpmpos) * MPS_FACTOR * measure_len / bpm
            else:
                break
            bpmpos = next_bpmpos
            bpm = bpm_dict[bpmpos]

        stop_bpmpos_i = 0
        for s in range(len(stop_positions)):
            current_stop_pos = stop_positions[s]
            if beatpos > current_stop_pos:
                stop_bpmpos = bpmpos_array[stop_bpmpos_i]
                stop_bpm = bpm_dict[stop_bpmpos]
                for i in range(stop_bpmpos_i + 1, len(bpmpos_array)):
                    next_bpmpos = bpmpos_array[i]
                    if current_stop_pos < next_bpmpos:
                        stop_bpmpos_i = i - 1
                        break
                    stop_bpmpos = next_bpmpos
                    stop_bpm = bpm_dict[stop_bpmpos]
                current_time += stop_lengths[current_stop_pos] * MPS_FACTOR / stop_bpm
            else:
                break

        current_time += (beatpos - bpmpos) * MPS_FACTOR * measure_len / bpm
        return current_time

    def add_keysounds_to_sample_dict(channel, keysounds, keysound_lengths_arg, current_timepos_arg, current_bpmpos_i_arg, stop_positions_arg, measure_num_arg, measure_len_arg):
        keysounds_len = len(keysounds)
        for k in range(len(keysounds)):
            keysound = keysounds[k]
            if keysound in keysound_lengths_arg:
                if keysound not in sample_dict:
                    sample_dict[keysound] = []
                if channel not in channelsample_dict:
                    channelsample_dict[channel] = []
                sample = {}
                sample["length"] = keysound_lengths_arg[keysound]
                sample["pos"] = current_timepos_arg + measure_offset_seconds(measure_num_arg, measure_num_arg + k / keysounds_len, bpm_positions[current_bpmpos_i_arg:], stop_positions_arg, measure_len_arg)
                sample["index"] = keysound
                sample_dict[keysound].append(sample)
                channelsample_dict[channel].append(sample)

    for measure_num in range(max_measure):
        measure_len = measurelen_dict.get(measure_num, 1.0)
        if measure_num == 0:
            measurelentime_dict[0] = 0.0

        bpms_in_measure = 1
        num_bpms_added = 0

        stop_positions = []
        stop_header = f"{measure_num:03d}{STOP_CHANNEL}"
        if stop_header in notes_dict:
            stop_indices = notes_dict[stop_header]
            stop_arraylen = len(stop_indices)
            for s in range(stop_arraylen):
                if stop_indices[s] != "00" and stop_indices[s] in stop_dict:
                    stop_position = measure_num + s / stop_arraylen
                    stop_positions.append(stop_position)
                    stop_lengths[stop_position] = stop_dict[stop_indices[s]] / 192.0

        bpm_header = f"{measure_num:03d}{BPM_CHANNEL}"
        if bpm_header in notes_dict:
            bpm_hex = notes_dict[bpm_header]
            bpm_arraylen = len(bpm_hex)
            for b in range(bpm_arraylen):
                if bpm_hex[b] != "00":
                    bpm_pos = measure_num + b / bpm_arraylen
                    num_bpms_added += 1
                    if b != 0:
                        bpms_in_measure += 1
                    else:
                        current_bpmpos_i += 1
                    bpm_positions.append(bpm_pos)
                    bpm_dict[bpm_pos] = int("0x" + bpm_hex[b], 16)

        extbpm_header = f"{measure_num:03d}{EXTBPM_CHANNEL}"
        if extbpm_header in notes_dict:
            extbpm_indices = notes_dict[extbpm_header]
            extbpm_arraylen = len(extbpm_indices)
            for b in range(extbpm_arraylen):
                if extbpm_indices[b] in extbpm_dict:
                    bpm_pos = measure_num + b / extbpm_arraylen
                    num_bpms_added += 1
                    if b != 0:
                        bpms_in_measure += 1
                    else:
                        current_bpmpos_i += 1
                    bpm_positions.append(bpm_pos)
                    bpm_dict[bpm_pos] = abs(extbpm_dict[extbpm_indices[b]])

        bpm_positions.sort()

        for bpmpos_i in range(len(bpm_positions) - num_bpms_added, len(bpm_positions)):
            bpm_pos = bpm_positions[bpmpos_i]
            bpmtime_dict[bpm_pos] = current_timepos + measure_offset_seconds(
                measure_num, bpm_pos, bpm_positions[current_bpmpos_i:], stop_positions, measure_len
            )

        for channel in BMS_PLAYABLE_CHANNELS:
            header = f"{measure_num:03d}{channel}"
            if header in notes_dict:
                if channel == "01":
                    for keysounds in notes_dict[header]:
                        add_keysounds_to_sample_dict(channel, keysounds, keysound_lengths, current_timepos, current_bpmpos_i, stop_positions, measure_num, measure_len)
                else:
                    keysounds = notes_dict[header]
                    add_keysounds_to_sample_dict(channel, keysounds, keysound_lengths, current_timepos, current_bpmpos_i, stop_positions, measure_num, measure_len)

        current_timepos += measure_offset_seconds(
            measure_num, measure_num + 1, bpm_positions[current_bpmpos_i:], stop_positions, measure_len
        )

        if measure_num + 1 in measurelen_dict:
            measurelentime_dict[measure_num + 1] = current_timepos
        elif measure_len != 1:
            measurelen_dict[measure_num + 1] = 1.0
            measurelentime_dict[measure_num + 1] = current_timepos

        current_bpmpos_i += (bpms_in_measure - 1)

    for channel in channelsample_dict:
        sample_array = channelsample_dict[channel]
        sample_array.sort(key=lambda s: s["pos"])
        for s in range(len(sample_array)):
            sample = sample_array[s]
            if channel in LONG_NOTE_CHANNELS:
                if channel not in active_long_notes:
                    active_long_notes[channel] = sample["index"]
                    if s + 1 < len(sample_array):
                        next_sample = sample_array[s + 1]
                        if sample["pos"] + sample["length"] > next_sample["pos"]:
                            sample["length"] = next_sample["pos"] - sample["pos"]
                else:
                    if sample["index"] == active_long_notes[channel]:
                        sample["length"] = 0
                    del active_long_notes[channel]

    tempoenv_lines = []
    if bpm_positions or len(measurelentime_dict) > 1:
        for bpm_pos in bpm_positions:
            if bpm_pos in bpmtime_dict:
                tempoenv_lines.append(f'    PT {bpmtime_dict[bpm_pos]} {bpm_dict[bpm_pos]} 1\n')
        for measurelen_pos in sorted(measurelentime_dict.keys()):
            measurelentime = measurelentime_dict[measurelen_pos]
            measurelen = measurelen_dict.get(measurelen_pos, 1.0)
            ts_num, ts_den = float(measurelen).as_integer_ratio()
            den4_factor = 4 / ts_den
            if den4_factor > 1:
                ts_num = int(ts_num * den4_factor)
                ts_den = int(ts_den * den4_factor)
            if ts_num <= 256 and ts_den <= 256:
                tempoenv_lines.append(f'    PT {measurelentime} 0 1 {ts_den * 65536 + ts_num} 0 3\n')

    return sample_dict, chart_bpm, tempoenv_lines, master_volume


def write_sub_bms(lines, group_wavs, group_name, target_dir, encoding):
    out_dir = Path(target_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{sanitize_filename(group_name)}.bms"
    output_path = out_dir / file_name
    output_path.write_text(build_grouped_bms_content(lines, group_wavs), encoding=encoding, errors='ignore')
    return str(output_path)


class BMSController:
    def __init__(self):
        self.file_path = None
        self.directory = None
        self.bms_lines = []
        self.wav_id_to_path = {}
        self.wav_id_order = []
        self.initial_bpm = ""
        self.group_manager = None
        self.encoding = 'utf-8'

    def load_bms_file(self, file_path_str):
        self.file_path = Path(file_path_str)
        self.directory = self.file_path.parent
        raw_bytes = self.file_path.read_bytes()
        if chardet is not None:
            detection = chardet.detect(raw_bytes)
            self.encoding = detection['encoding'] if detection and detection.get('confidence', 0) > 0.5 else 'shift_jis'
        else:
            self.encoding = 'shift_jis'
        content = raw_bytes.decode(self.encoding, errors='ignore')
        self.bms_lines = content.splitlines(keepends=True)
        self.wav_id_to_path, self.wav_id_order, self.initial_bpm = BMSParser.parse_bms_content(self.bms_lines)

        audio_extensions = ['.wav', '.ogg', '.mp3', '.m4a', '.flac']
        resolved_map = {}
        for wav_id, relative_path in self.wav_id_to_path.items():
            base_p = self.directory / relative_path
            final_p = base_p
            if not base_p.exists():
                for ext in audio_extensions:
                    alt_p = base_p.with_suffix(ext)
                    if alt_p.exists():
                        final_p = alt_p
                        break
            resolved_map[wav_id] = str(final_p.resolve())

        self.group_manager = GroupManager(resolved_map, self.wav_id_order)

        if self.wav_id_to_path and all(re.fullmatch(r'[0-9A-Z]{2}', Path(resolved_map[wid]).stem, flags=re.IGNORECASE) for wid in self.wav_id_order):
            return

        try:
            prefix_map = {}

            def candidate_key_from_stem(stem):
                left = re.split(r'(_v\d+|_l\d+|_o\d+|_#\d+|_\d+$)', stem, flags=re.IGNORECASE)[0]
                if not left:
                    return None
                left = left.strip()
                if not left:
                    return None
                while True:
                    m = re.search(r'[-_]\s*\d+\s*$', left)
                    if m:
                        left = left[:m.start()].strip()
                    else:
                        break
                if left and any(ch.isalpha() for ch in left):
                    return left
                return None

            for wid in self.wav_id_order:
                if wid not in resolved_map:
                    continue
                stem = Path(resolved_map[wid]).stem
                key = candidate_key_from_stem(stem)
                if key:
                    prefix_map.setdefault(key, []).append(wid)

            created_any = False
            for prefix, ids in prefix_map.items():
                if len(ids) >= 2:
                    self.group_manager.save_state_to_history()
                    self.group_manager.move_ids_to_target_group(ids, prefix)
                    created_any = True
            if created_any:
                self.group_manager.redo_stack = []
        except Exception:
            pass

    def generate_group_bms_files(self):
        if not self.group_manager:
            return []
        return [write_sub_bms(self.bms_lines, group_data, name, self.directory, self.encoding) for name, group_data in self.group_manager.groups.items()]

    def export_sub_bms_files(self):
        return self.generate_group_bms_files()

    def generate_rpp_file(self):
        if not self.file_path:
            raise ValueError("No BMS file loaded; cannot export RPP")

        sample_dict, chart_bpm, tempoenv_lines, master_volume = compute_bms_timeline(self.bms_lines, self.group_manager.original_wav_map)

        out_rpp_path = self.file_path.with_suffix('.rpp')
        with open(out_rpp_path, 'w', encoding='utf-8') as rpp_out:
            rpp_out.write("<REAPER_PROJECT\n")
            rpp_out.write("TEMPO {} 4 4\n".format(chart_bpm))
            rpp_out.write("MASTERTRACKVIEW 1 0.6667 0.5 0.5 0 0 0 0 0 0\n")
            rpp_out.write("MASTER_VOLUME {} 0 -1 -1 1\n".format(master_volume / 300.0))
            rpp_out.write("VIDEO_CONFIG 0 0 256\n")
            rpp_out.write("PANMODE 3\n")
            if tempoenv_lines:
                rpp_out.write("<TEMPOENVEX\n")
                for line in tempoenv_lines:
                    rpp_out.write(line)
                rpp_out.write(">\n")

            def write_samples_for_index(ki, wav_path):
                wav_fullname = Path(wav_path).name
                wav_ext = Path(wav_path).suffix.lower()
                sample_array = sample_dict[ki]
                sample_array.sort(key=lambda s: s["pos"])
                for s in range(len(sample_array)):
                    sample = sample_array[s]
                    if s + 1 < len(sample_array):
                        next_sample = sample_array[s + 1]
                        if sample["pos"] + sample["length"] > next_sample["pos"]:
                            sample["length"] = next_sample["pos"] - sample["pos"]
                    if sample["length"] > 0:
                        rpp_out.write("<ITEM\n")
                        rpp_out.write("POSITION {}\n".format(sample["pos"]))
                        rpp_out.write("LENGTH {}\n".format(sample["length"]))
                        rpp_out.write("LOOP 0\n")
                        rpp_out.write("NAME {}\n".format(wav_fullname))
                        if wav_ext == '.wav':
                            rpp_out.write("<SOURCE WAVE\n")
                        elif wav_ext == '.ogg':
                            rpp_out.write("<SOURCE VORBIS\n")
                        elif wav_ext == '.mp3':
                            rpp_out.write("<SOURCE MP3\n")
                        else:
                            rpp_out.write("<SOURCE\n")
                        rpp_out.write('FILE "{}"\n'.format(wav_path))
                        rpp_out.write(">\n")
                        rpp_out.write(">\n")

            if self.group_manager and self.group_manager.groups:
                for group_name, group_data in self.group_manager.groups.items():
                    rpp_out.write('<TRACK\n')
                    rpp_out.write('NAME "{}"\n'.format(group_name))
                    rpp_out.write("VOLPAN 1 0 -1 -1 1\n")
                    rpp_out.write("ISBUS 1 1\n")
                    rpp_out.write(">\n")

                    wav_ids_in_group = list(group_data.keys())
                    for child_idx, wav_id in enumerate(wav_ids_in_group):
                        wav_path = group_data[wav_id]
                        wav_name = Path(wav_path).stem
                        is_last_child = (child_idx == len(wav_ids_in_group) - 1)

                        rpp_out.write('<TRACK\n')
                        rpp_out.write('NAME "{}"\n'.format(wav_name))
                        rpp_out.write("VOLPAN 1 0 -1 -1 1\n")
                        if is_last_child:
                            rpp_out.write("ISBUS 2 -1\n")
                        else:
                            rpp_out.write("ISBUS 0 0\n")

                        if wav_id in sample_dict:
                            write_samples_for_index(wav_id, wav_path)

                        rpp_out.write(">\n")

            if self.group_manager:
                for wav_id in self.wav_id_order:
                    if wav_id in self.group_manager.remaining_wav_map and wav_id in sample_dict:
                        wav_path = self.group_manager.remaining_wav_map[wav_id]
                        wav_name = Path(wav_path).stem
                        rpp_out.write('<TRACK\n')
                        rpp_out.write('NAME "{}"\n'.format(wav_name))
                        rpp_out.write("VOLPAN 1 0 -1 -1 1\n")
                        rpp_out.write("ISBUS 0 0\n")
                        write_samples_for_index(wav_id, wav_path)
                        rpp_out.write(">\n")

            rpp_out.write(">\n")

        return str(out_rpp_path)

    def export_rpp_file(self):
        return self.generate_rpp_file()


# ------------------------- View (GUI) layer -------------------------

class BMSDivGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(gettext("title"))
        self.controller = BMSController()
        if pygame is not None:
            try:
                pygame.mixer.init()
            except Exception:
                pass
        self.sound_cache = {}
        self.active_channel = None
        self.visible_remaining_ids = []
        self.visible_detail_ids = []
        self._smart_selection_active = False
        self._expected_smart_selection = (None, None)
        self._prev_remaining_sel = set()
        self._prev_detail_sel = set()
        self._setup_ui()
        self._setup_event_bindings()

    def _setup_ui(self):
        file_frame = tk.Frame(self.root)
        file_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        tk.Button(file_frame, text=gettext("select_file"), command=self._on_select_file_clicked).pack(side="left")
        self.label_file_info = tk.Label(file_frame, text=gettext("not_selected"))
        self.label_file_info.pack(side="left", padx=10)
        self.label_bpm_info = tk.Label(file_frame, text="")
        self.label_bpm_info.pack(side="right", padx=10)

        main_container = tk.Frame(self.root)
        main_container.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        wav_frame = tk.LabelFrame(main_container, text=gettext("pending_group"))
        wav_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        search_box_frame = tk.Frame(wav_frame)
        search_box_frame.pack(fill="x", padx=2, pady=2)

        self.var_search_query = tk.StringVar()
        self.var_search_query.trace_add("write", lambda *args: self._refresh_remaining_listbox())
        self.entry_search = tk.Entry(search_box_frame, textvariable=self.var_search_query)
        self.entry_search.pack(side="left", fill="x", expand=True, ipady=2)
        self.entry_search.bind("<Return>", lambda e: self._handle_grouping_action())

        tk.Button(search_box_frame, text=gettext("search_group"), command=self._handle_grouping_action, bg="#e1e1e1").pack(side="left", padx=(2, 0))
        tk.Button(search_box_frame, text=gettext("group_remaining"), command=self._handle_group_remaining_action, bg="#e1e1e1").pack(side="left", padx=(2, 0))

        self.listbox_remaining = tk.Listbox(wav_frame, width=50, height=20, selectmode="extended", exportselection=False)
        self.listbox_remaining.pack(side="left", fill="both", expand=True)
        scroll_remaining = tk.Scrollbar(wav_frame, command=self.listbox_remaining.yview)
        scroll_remaining.pack(side="left", fill="y")
        self.listbox_remaining.config(yscrollcommand=scroll_remaining.set)

        tree_frame = tk.LabelFrame(main_container, text=gettext("groups"))
        tree_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.tree_groups = ttk.Treeview(tree_frame, columns=("group_name", "count"), show="headings", height=20)
        self.tree_groups.heading("group_name", text=gettext("group_name_col"))
        self.tree_groups.heading("count", text=gettext("count_col"))
        self.tree_groups.column("group_name", width=120)
        self.tree_groups.column("count", width=50)
        self.tree_groups.pack(side="left", fill="both", expand=True)

        detail_frame = tk.LabelFrame(main_container, text=gettext("group_detail"))
        detail_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.listbox_group_detail = tk.Listbox(detail_frame, width=50, height=22, selectmode=tk.EXTENDED, exportselection=False)
        self.listbox_group_detail.pack(side="left", fill="both", expand=True)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.label_status = tk.Label(bottom_frame, text=gettext("ready"))
        self.label_status.pack(side="right", padx=5)

        tk.Button(bottom_frame, text=gettext("export_bms"), command=self._on_export_bms_clicked).pack(side="left", padx=5)
        tk.Button(bottom_frame, text=gettext("export_rpp"), command=self._on_export_rpp_clicked).pack(side="left", padx=5)
        tk.Button(bottom_frame, text=gettext("export_json"), command=self._on_export_json_clicked).pack(side="left", padx=5)
        tk.Button(bottom_frame, text=gettext("import_json"), command=self._on_import_json_clicked).pack(side="left", padx=5)

    def _setup_event_bindings(self):
        self.root.bind("<Control-z>", lambda e: self._perform_undo())
        self.root.bind("<Control-y>", lambda e: self._perform_redo())
        self.listbox_remaining.bind("<<ListboxSelect>>", self._on_remaining_selection_changed)
        self.listbox_remaining.bind("<ButtonPress-1>", self._on_listbox_press)
        self.listbox_remaining.bind("<ButtonRelease-3>", self._on_remaining_right_release)
        self.listbox_remaining.bind("<ButtonPress-2>", self._handle_auto_fill_search)

        self.tree_groups.bind("<Delete>", self._handle_disband_group_action)
        self.tree_groups.bind("<<TreeviewSelect>>", self._on_group_tree_selection_changed)
        self.tree_groups.bind('<F2>', lambda e: self._handle_rename_group_action())
        self.tree_groups.bind('<ButtonRelease-3>', self._on_group_tree_right_release)

        self.listbox_group_detail.bind("<<ListboxSelect>>", self._on_detail_selection_changed)
        self.listbox_group_detail.bind("<ButtonPress-1>", self._on_listbox_press)
        self.listbox_group_detail.bind("<ButtonRelease-3>", self._on_detail_right_release)
        self.listbox_group_detail.bind("<ButtonPress-2>", self._handle_auto_fill_search)

        self.entry_search.bind('<KeyPress>', self._on_entry_key_press)

    def _on_select_file_clicked(self):
        file_path = filedialog.askopenfilename(filetypes=[('BMS Files', '*.bms;*.bme;*.bml;*.pms'), ('All', '*.*')])
        if not file_path:
            return

        try:
            pygame.mixer.stop()
        except Exception:
            pass
        self.sound_cache.clear()
        self.active_channel = None

        self.label_file_info.config(text=gettext("waiting"), fg="blue")
        self.label_status.config(text=gettext("loading_audio"))
        self.root.update()

        try:
            self.controller.load_bms_file(file_path)
            if pygame is not None:
                for wav_id, path in self.controller.group_manager.original_wav_map.items():
                    p_obj = Path(path)
                    if p_obj.exists():
                        try:
                            self.sound_cache[path] = pygame.mixer.Sound(path)
                        except Exception:
                            pass

            self.label_file_info.config(text=str(self.controller.file_path), fg="black")
            if self.controller.initial_bpm and self.controller.initial_bpm.strip():
                self.label_bpm_info.config(text=gettext("initial_bpm").format(self.controller.initial_bpm.strip()))
            else:
                self.label_bpm_info.config(text="")
            self._ui_refresh_all()
            self.label_status.config(text=f"{gettext('load_success')} (编码: {self.controller.encoding})")
        except Exception as e:
            self.label_file_info.config(text=gettext("load_failed"), fg="red")
            self.label_bpm_info.config(text="")
            messagebox.showerror(gettext("file_error"), str(e))

    def _play_sound(self, path):
        if not path or pygame is None:
            return
        if path in self.sound_cache:
            if self.active_channel:
                self.active_channel.stop()
            try:
                self.active_channel = self.sound_cache[path].play()
            except Exception:
                pass

    def _ui_refresh_all(self):
        self._refresh_remaining_listbox()
        self._refresh_group_tree()
        self._refresh_detail_listbox()

    def _refresh_remaining_listbox(self):
        self.listbox_remaining.delete(0, tk.END)
        self.visible_remaining_ids = []
        self._prev_remaining_sel.clear()
        if not self.controller.group_manager:
            return
        search_keyword = self.var_search_query.get().lower()
        for wav_id in self.controller.wav_id_order:
            if wav_id in self.controller.group_manager.remaining_wav_map:
                full_path = self.controller.wav_id_to_path.get(wav_id, "")
                file_stem = Path(full_path).stem.lower()
                if not search_keyword or search_keyword in file_stem:
                    self.listbox_remaining.insert(tk.END, f"{wav_id}: {self.controller.wav_id_to_path.get(wav_id, '')}")
                    self.visible_remaining_ids.append(wav_id)

    def _refresh_group_tree(self, select_group_name=None):
        for item in self.tree_groups.get_children():
            self.tree_groups.delete(item)
        if not self.controller.group_manager:
            return
        for name, content in self.controller.group_manager.groups.items():
            node = self.tree_groups.insert("", "end", values=(name, len(content)))
            if select_group_name == name:
                self.tree_groups.selection_set(node)
                self.tree_groups.see(node)

    def _refresh_detail_listbox(self):
        self.listbox_group_detail.delete(0, tk.END)
        self.visible_detail_ids = []
        self._prev_detail_sel.clear()
        selected_nodes = self.tree_groups.selection()
        if not selected_nodes:
            return
        group_name = self.tree_groups.item(selected_nodes[0], "values")[0]
        group_dict = self.controller.group_manager.groups.get(group_name, {})
        for wav_id in self.controller.wav_id_order:
            if wav_id in group_dict:
                self.listbox_group_detail.insert(tk.END, f"{wav_id}: {self.controller.wav_id_to_path.get(wav_id, '')}")
                self.visible_detail_ids.append(wav_id)

    def _handle_auto_fill_search(self, event):
        listbox = event.widget
        index = listbox.nearest(event.y)
        if index < 0:
            return
        listbox.focus_set()
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index)
        listbox.activate(index)

        if listbox is self.listbox_remaining and index < len(self.visible_remaining_ids):
            wav_id = self.visible_remaining_ids[index]
            path = self.controller.group_manager.remaining_wav_map.get(wav_id)
            self._play_sound(path)
        elif listbox is self.listbox_group_detail and index < len(self.visible_detail_ids):
            selected = self.tree_groups.selection()
            if selected:
                group = self.tree_groups.item(selected[0], "values")[0]
                wav_id = self.visible_detail_ids[index]
                path = self.controller.group_manager.groups.get(group, {}).get(wav_id)
                self._play_sound(path)

        self.entry_search.focus_set()
        text = listbox.get(index)
        wav_id = text.split(":", 1)[0].strip()
        path = self.controller.group_manager.original_wav_map.get(wav_id)
        if path:
            stem = Path(path).stem
            self.var_search_query.set(stem)
            self._select_last_segment()
            try:
                start = self.entry_search.index('sel.first')
                end = self.entry_search.index('sel.last')
                self._expected_smart_selection = (int(start), int(end))
                self._smart_selection_active = True
            except tk.TclError:
                self._smart_selection_active = False
            self.entry_search.icursor(tk.END)

    def _select_last_segment(self):
        stem = self.var_search_query.get()
        if not stem:
            return
        last_sep_pos = -1
        for sep in ['_', '-', ' ']:
            pos = stem.rfind(sep)
            if pos > last_sep_pos:
                last_sep_pos = pos
        start_pos = last_sep_pos if last_sep_pos != -1 else 0
        self.entry_search.selection_range(start_pos, tk.END)

    def _on_entry_key_press(self, event):
        if event.keysym != 'BackSpace':
            self._smart_selection_active = False
            return
        if not self._smart_selection_active:
            return
        try:
            sel_start = self.entry_search.index('sel.first')
            sel_end = self.entry_search.index('sel.last')
        except tk.TclError:
            self._smart_selection_active = False
            return
        if (int(sel_start), int(sel_end)) == self._expected_smart_selection:
            current_text = self.var_search_query.get()
            new_text = current_text[:int(sel_start)] + current_text[int(sel_end):]
            self.var_search_query.set(new_text)
            self._select_last_segment()
            try:
                new_start = self.entry_search.index('sel.first')
                new_end = self.entry_search.index('sel.last')
                self._expected_smart_selection = (int(new_start), int(new_end))
            except tk.TclError:
                self._smart_selection_active = False
            return 'break'
        self._smart_selection_active = False
        return

    def _handle_grouping_action(self):
        query = self.var_search_query.get()
        if not query:
            return
        self.controller.group_manager.save_state_to_history()
        created_name = self.controller.group_manager.create_group_by_search(query.strip(), self.controller.wav_id_to_path)
        if created_name:
            self._ui_refresh_all()
            self._refresh_group_tree(select_group_name=created_name)
            self.var_search_query.set("")
        else:
            self.controller.group_manager.history_stack.pop()

    def _handle_group_remaining_action(self):
        self.controller.group_manager.save_state_to_history()
        name = self.controller.group_manager.group_all_remaining()
        if name:
            self._ui_refresh_all()
            self._refresh_group_tree(select_group_name=name)

    def _handle_disband_group_action(self, event=None):
        selection = self.tree_groups.selection()
        if not selection:
            return
        self.controller.group_manager.save_state_to_history()
        for item in selection:
            name = self.tree_groups.item(item, "values")[0]
            self.controller.group_manager.disband_group(name)
        self._ui_refresh_all()

    def _handle_rename_group_action(self):
        selection = self.tree_groups.selection()
        if not selection:
            return
        old_name = self.tree_groups.item(selection[0], "values")[0]
        new_name = simpledialog.askstring(gettext("rename_group"), gettext("rename_group_prompt").format(old_name), initialvalue=old_name)
        if new_name and new_name.strip() != old_name:
            safe_new_name = sanitize_filename(new_name.strip())
            self.controller.group_manager.save_state_to_history()
            self.controller.group_manager.rename_group(old_name, safe_new_name, merge_if_exists=True)
            self._ui_refresh_all()
            self._refresh_group_tree(select_group_name=safe_new_name)

    def _on_listbox_press(self, event):
        listbox = event.widget
        idx = listbox.nearest(event.y)
        if idx < 0:
            return
        listbox.activate(idx)
        if idx in listbox.curselection() and len(listbox.curselection()) == 1:
            if listbox is self.listbox_remaining and idx < len(self.visible_remaining_ids):
                wav_id = self.visible_remaining_ids[idx]
                path = self.controller.group_manager.remaining_wav_map.get(wav_id)
                self._play_sound(path)
            elif listbox is self.listbox_group_detail and idx < len(self.visible_detail_ids):
                selected = self.tree_groups.selection()
                if selected:
                    group = self.tree_groups.item(selected[0], "values")[0]
                    wav_id = self.visible_detail_ids[idx]
                    path = self.controller.group_manager.groups.get(group, {}).get(wav_id)
                    self._play_sound(path)

    def _on_remaining_selection_changed(self, event):
        current_sel = set(self.listbox_remaining.curselection())
        added = current_sel - self._prev_remaining_sel
        removed = self._prev_remaining_sel - current_sel
        self._prev_remaining_sel = current_sel
        target_idx = None

        if added:
            target_idx = max(added) if max(added) == max(current_sel) else min(added)
        elif removed:
            if current_sel:
                if max(removed) > max(current_sel):
                    target_idx = min(removed)
                elif min(removed) < min(current_sel):
                    target_idx = max(removed)
                else:
                    target_idx = list(removed)[0]
            else:
                target_idx = list(removed)[0]

        if target_idx is not None and target_idx < len(self.visible_remaining_ids):
            wav_id = self.visible_remaining_ids[target_idx]
            path = self.controller.group_manager.remaining_wav_map.get(wav_id)
            self._play_sound(path)

    def _on_detail_selection_changed(self, event):
        current_sel = set(self.listbox_group_detail.curselection())
        added = current_sel - self._prev_detail_sel
        removed = self._prev_detail_sel - current_sel
        self._prev_detail_sel = current_sel
        target_idx = None

        if added:
            target_idx = max(added) if max(added) == max(current_sel) else min(added)
        elif removed:
            if current_sel:
                if max(removed) > max(current_sel):
                    target_idx = min(removed)
                elif min(removed) < min(current_sel):
                    target_idx = max(removed)
                else:
                    target_idx = list(removed)[0]
            else:
                target_idx = list(removed)[0]

        if target_idx is not None and target_idx < len(self.visible_detail_ids):
            selected_groups = self.tree_groups.selection()
            if selected_groups:
                group_name = self.tree_groups.item(selected_groups[0], "values")[0]
                wav_id = self.visible_detail_ids[target_idx]
                path = self.controller.group_manager.groups.get(group_name, {}).get(wav_id)
                self._play_sound(path)

    def _on_group_tree_selection_changed(self, event):
        self._refresh_detail_listbox()
        if self.listbox_group_detail.size() > 0:
            self.listbox_group_detail.selection_clear(0, tk.END)
            self.listbox_group_detail.selection_set(0)
            self.listbox_group_detail.activate(0)
            self.listbox_group_detail.focus_set()
            self._prev_detail_sel = {0}
            selected_groups = self.tree_groups.selection()
            if selected_groups and len(self.visible_detail_ids) > 0:
                group_name = self.tree_groups.item(selected_groups[0], "values")[0]
                wav_id = self.visible_detail_ids[0]
                path = self.controller.group_manager.groups[group_name].get(wav_id)
                self._play_sound(path)

    def _perform_undo(self):
        if self.controller.group_manager and self.controller.group_manager.undo():
            self._ui_refresh_all()

    def _perform_redo(self):
        if self.controller.group_manager and self.controller.group_manager.redo():
            self._ui_refresh_all()

    def _on_remaining_right_release(self, event):
        index = self.listbox_remaining.nearest(event.y)
        if index >= 0:
            if index not in self.listbox_remaining.curselection():
                self.listbox_remaining.selection_clear(0, tk.END)
                self.listbox_remaining.selection_set(index)
                self.listbox_remaining.activate(index)
        if not self.listbox_remaining.curselection():
            return
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=gettext("move_to_new"), command=self._action_move_remaining_to_new)
        if self.controller.group_manager.groups:
            sub = tk.Menu(menu, tearoff=0)
            for name in self.controller.group_manager.groups:
                sub.add_command(label=name, command=lambda n=name: self._action_move_selected_to_existing(n, from_remaining=True))
            menu.add_cascade(label=gettext("move_to_existing"), menu=sub)
        menu.tk_popup(event.x_root, event.y_root)

    def _on_group_tree_right_release(self, event):
        if not self.tree_groups.selection():
            return
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=gettext("rename_group"), command=self._handle_rename_group_action)
        menu.add_command(label=gettext("disband_group"), command=self._handle_disband_group_action)
        menu.add_command(label=gettext("merge_group"), command=self._handle_merge_groups_action)
        menu.tk_popup(event.x_root, event.y_root)

    def _on_detail_right_release(self, event):
        index = self.listbox_group_detail.nearest(event.y)
        if index >= 0:
            if index not in self.listbox_group_detail.curselection():
                self.listbox_group_detail.selection_clear(0, tk.END)
                self.listbox_group_detail.selection_set(index)
                self.listbox_group_detail.activate(index)
        if not self.listbox_group_detail.curselection():
            return
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=gettext("remove_from_group"), command=self._handle_remove_from_group_action)
        menu.add_command(label=gettext("move_to_new"), command=lambda: self._action_move_selected_to_new(False))
        if self.controller.group_manager.groups:
            sub = tk.Menu(menu, tearoff=0)
            for name in self.controller.group_manager.groups:
                sub.add_command(label=name, command=lambda n=name: self._action_move_selected_to_existing(n, from_remaining=False))
            menu.add_cascade(label=gettext("move_to_other"), menu=sub)
        menu.tk_popup(event.x_root, event.y_root)

    def _action_move_remaining_to_new(self):
        indices = self.listbox_remaining.curselection()
        wav_ids = [self.visible_remaining_ids[i] for i in indices]
        new_name = simpledialog.askstring(gettext("new_group"), gettext("enter_group_name"))
        if new_name:
            safe_name = sanitize_filename(new_name.strip())
            self.controller.group_manager.save_state_to_history()
            res_name = self.controller.group_manager.create_group_from_ids(safe_name, wav_ids)
            self._ui_refresh_all()
            self._refresh_group_tree(select_group_name=res_name)

    def _action_move_selected_to_new(self, from_remaining):
        if from_remaining:
            indices = self.listbox_remaining.curselection()
            wav_ids = [self.visible_remaining_ids[i] for i in indices]
        else:
            indices = self.listbox_group_detail.curselection()
            wav_ids = [self.visible_detail_ids[i] for i in indices]
        if not wav_ids:
            return
        new_name = simpledialog.askstring(gettext("new_group"), gettext("enter_group_name"))
        if new_name:
            safe_name = sanitize_filename(new_name.strip())
            self.controller.group_manager.save_state_to_history()
            res_name = self.controller.group_manager.create_group_from_ids(safe_name, wav_ids)
            self._ui_refresh_all()
            self._refresh_group_tree(select_group_name=res_name)

    def _action_move_selected_to_existing(self, target_name, from_remaining):
        self.controller.group_manager.save_state_to_history()
        indices = self.listbox_remaining.curselection() if from_remaining else self.listbox_group_detail.curselection()
        wav_ids = [(self.visible_remaining_ids[i] if from_remaining else self.visible_detail_ids[i]) for i in indices]
        self.controller.group_manager.move_ids_to_target_group(wav_ids, target_name)
        self._ui_refresh_all()
        self._refresh_group_tree(select_group_name=target_name)

    def _handle_remove_from_group_action(self):
        selection = self.tree_groups.selection()
        if not selection:
            return
        group_name = self.tree_groups.item(selection[0], "values")[0]
        indices = self.listbox_group_detail.curselection()
        ids_to_remove = [self.visible_detail_ids[i] for i in indices]
        self.controller.group_manager.save_state_to_history()
        self.controller.group_manager.remove_ids_from_group(group_name, ids_to_remove)
        self._ui_refresh_all()

    def _handle_merge_groups_action(self):
        selection = self.tree_groups.selection()
        names = [self.tree_groups.item(item, "values")[0] for item in selection]
        new_name = simpledialog.askstring(gettext("merge_group"), gettext("enter_merge_name"), initialvalue=names[0])
        if new_name:
            self.controller.group_manager.save_state_to_history()
            res_name = self.controller.group_manager.merge_groups(names, sanitize_filename(new_name))
            self._ui_refresh_all()
            self._refresh_group_tree(select_group_name=res_name)

    def _on_export_bms_clicked(self):
        if not self.controller.group_manager or not self.controller.group_manager.groups:
            return
        self.controller.generate_group_bms_files()
        self.label_status.config(text=gettext("bms_export_done"))
        try:
            os.startfile(self.controller.directory)
        except Exception:
            pass

    def _on_export_rpp_clicked(self):
        if not self.controller.group_manager or not self.controller.group_manager.groups:
            return
        try:
            self.label_status.config(text=gettext("loading_timeline"))
            self.root.update()
            rpp_path = self.controller.generate_rpp_file()
            self.label_status.config(text=gettext("rpp_export_done").format(Path(rpp_path).name))
            try:
                os.startfile(self.controller.directory)
            except Exception:
                pass
        except Exception as exc:
            messagebox.showerror(gettext("rpp_fail"), str(exc))
            self.label_status.config(text=gettext("rpp_fail"))

    def _on_export_json_clicked(self):
        if not self.controller.group_manager or not self.controller.file_path:
            return
        default_name = self.controller.file_path.stem + "_set.json"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            initialdir=str(self.controller.directory),
            initialfile=default_name,
            filetypes=[("JSON Files", "*.json")],
            title=gettext("export_group_title"),
        )
        if save_path:
            self.controller.group_manager.export_to_json(save_path, base_directory=self.controller.directory)
            self.label_status.config(text=gettext("group_export_ok"))

    def _on_import_json_clicked(self):
        if not self.controller.group_manager:
            return
        load_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            initialdir=str(self.controller.directory),
            title=gettext("import_group_title"),
        )
        if load_path:
            self.controller.group_manager.save_state_to_history()
            success, msg = self.controller.group_manager.import_from_json(load_path, base_directory=self.controller.directory)
            self._ui_refresh_all()
            self.label_status.config(text=msg)
            if not success:
                messagebox.showerror(gettext("group_import_fail"), msg)


def build_cli_parser():
    parser = argparse.ArgumentParser(
        description="BMS_div: export grouped BMS files or RPP projects from a BMS chart directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("bms", nargs="?", help="Input .bms file")
    parser.add_argument("json", nargs="?", help="Optional group configuration .json file generated by the GUI")
    parser.add_argument(
        "-o",
        "--output",
        choices=("bms", "rpp"),
        help="Export format. Results are written next to the source BMS file in the same directory.",
    )
    parser.add_argument("--lang", choices=("zh", "ja", "en"), default=os.getenv("BMS_DIV_LANG", detect_system_language()), help="Language for CLI/help text")
    parser.add_argument("--version", action="version", version="BMS_div")
    return parser


def run_cli(argv=None):
    parser = build_cli_parser()
    args = parser.parse_args(argv)
    set_language(args.lang)

    if not args.bms:
        if args.json or args.output:
            raise SystemExit("BMS file is required when using --output or JSON import.")
        print(f"Language set to: {args.lang}")
        return 0

    bms_path = Path(args.bms).resolve()
    if not bms_path.exists():
        raise SystemExit(f"BMS file not found: {bms_path}")

    controller = BMSController()
    controller.load_bms_file(str(bms_path))

    if args.json:
        json_path = Path(args.json)
        if not json_path.is_absolute():
            json_path = (bms_path.parent / json_path).resolve()
        ok, message = controller.group_manager.import_from_json(str(json_path), base_directory=controller.directory)
        if not ok:
            raise SystemExit(f"JSON import failed: {message}")
        print(message)

    if args.output == "bms":
        if not controller.group_manager or not controller.group_manager.groups:
            raise SystemExit("No groups were available for BMS export.")
        outputs = controller.generate_group_bms_files()
        print(f"Generated {len(outputs)} BMS files in {controller.directory}")
        return 0

    if args.output == "rpp":
        if not controller.group_manager or not controller.group_manager.groups:
            raise SystemExit("No groups were available for RPP export.")
        rpp_path = controller.generate_rpp_file()
        print(f"Generated RPP: {rpp_path}")
        return 0

    print(f"Loaded BMS: {controller.file_path}")
    print(f"Encoding: {controller.encoding}")
    if controller.group_manager:
        print(f"WAV count: {len(controller.wav_id_order)}")
        print(f"Groups: {len(controller.group_manager.groups)}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit(run_cli())

    root_window = tk.Tk()
    app_instance = BMSDivGUI(root_window)
    root_window.mainloop()