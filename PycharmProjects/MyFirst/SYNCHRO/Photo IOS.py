"""
Двостороння синхронізація папки Photo:
  C:\\Temp\\Photo  <-->  [T5 EVO]\\Photo

Особливість: SSD шукається за МІТКОЮ ТОМУ ("T5 EVO"), а не за літерою диска
(D:, E:, F:...), бо літера може змінюватись залежно від того, скільки USB
пристроїв підключено в даний момент.

Режим: ручний запуск. Скрипт спочатку показує ПОПЕРЕДНІЙ ПЕРЕГЛЯД (dry-run)
усіх дій і запитує підтвердження, перш ніж щось реально копіювати.
"""

import ctypes
import os
import shutil
import sys
import string

LOCAL_PHOTO_DIR = r"C:\Temp\Photo"
VOLUME_LABEL = "T5 EVO"
SUBFOLDER_ON_SSD = "Photo"

TIME_TOLERANCE_SEC = 2  # похибка порівняння часу модифікації (FAT/exFAT округлює до 2с)


def find_drive_by_label(label: str) -> str | None:
    """Знаходить літеру диска за міткою тому (Windows-only, без сторонніх бібліотек)."""
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    volume_name_buf = ctypes.create_unicode_buffer(261)

    for i, letter in enumerate(string.ascii_uppercase):
        if not (bitmask >> i) & 1:
            continue
        drive = f"{letter}:\\"
        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive)
        if drive_type not in (2, 3):  # removable або fixed
            continue
        ok = ctypes.windll.kernel32.GetVolumeInformationW(
            drive, volume_name_buf, ctypes.sizeof(volume_name_buf),
            None, None, None, None, 0
        )
        if ok and volume_name_buf.value.strip().lower() == label.strip().lower():
            return drive
    return None


def scan_folder(root: str) -> dict:
    """Повертає {relative_path: (size, mtime)} для всіх файлів у папці."""
    result = {}
    if not os.path.isdir(root):
        return result
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                st = os.stat(full)
                result[rel] = (st.st_size, st.st_mtime)
            except OSError:
                continue
    return result


def plan_sync(left: str, right: str):
    """Порівнює дві папки і повертає список дій."""
    left_files = scan_folder(left)
    right_files = scan_folder(right)
    actions = []

    all_rel_paths = set(left_files) | set(right_files)

    for rel in sorted(all_rel_paths):
        in_left = rel in left_files
        in_right = rel in right_files

        if in_left and not in_right:
            actions.append(("copy", left, right, rel, "новий файл (тільки на ПК)"))
        elif in_right and not in_left:
            actions.append(("copy", right, left, rel, "новий файл (тільки на SSD)"))
        else:
            size_l, mtime_l = left_files[rel]
            size_r, mtime_r = right_files[rel]
            if size_l == size_r and abs(mtime_l - mtime_r) <= TIME_TOLERANCE_SEC:
                continue
            if mtime_l > mtime_r:
                actions.append(("copy", left, right, rel, "новіший на ПК"))
            else:
                actions.append(("copy", right, left, rel, "новіший на SSD"))

    return actions


def print_plan(actions):
    if not actions:
        print("Немає розбіжностей. Папки вже синхронізовані.")
        return
    print(f"\nЗнайдено {len(actions)} дій для синхронізації:\n")
    for _, src_root, dst_root, rel, reason in actions:
        arrow = "ПК -> SSD" if src_root == LOCAL_PHOTO_DIR else "SSD -> ПК"
        print(f"  [{arrow}] {rel}   ({reason})")
    print()


def apply_plan(actions):
    for _, src_root, dst_root, rel, _ in actions:
        src = os.path.join(src_root, rel)
        dst = os.path.join(dst_root, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  Скопійовано: {rel}")


def main():
    dry_run = "--dry-run" in sys.argv
    auto_yes = "--yes" in sys.argv

    ssd_drive = find_drive_by_label(VOLUME_LABEL)
    if not ssd_drive:
        print(f"Помилка: диск з міткою '{VOLUME_LABEL}' не знайдено.")
        print("Перевір, чи підключений SSD, і чи правильно вказана мітка тому.")
        sys.exit(1)

    ssd_photo_dir = os.path.join(ssd_drive, SUBFOLDER_ON_SSD)
    print(f"SSD знайдено: {ssd_drive}  (мітка: {VOLUME_LABEL})")
    print(f"Локальна папка: {LOCAL_PHOTO_DIR}")
    print(f"Папка на SSD:   {ssd_photo_dir}")

    if not os.path.isdir(LOCAL_PHOTO_DIR):
        print(f"Помилка: локальна папка не знайдена: {LOCAL_PHOTO_DIR}")
        sys.exit(1)
    if not os.path.isdir(ssd_photo_dir):
        print(f"Увага: папка на SSD не існує, буде створена: {ssd_photo_dir}")
        os.makedirs(ssd_photo_dir, exist_ok=True)

    actions = plan_sync(LOCAL_PHOTO_DIR, ssd_photo_dir)
    print_plan(actions)

    if not actions:
        return
    if dry_run:
        print("Режим --dry-run: нічого не змінено.")
        return

    if not auto_yes:
        answer = input("Виконати синхронізацію? (y/n): ").strip().lower()
        if answer != "y":
            print("Скасовано.")
            return

    apply_plan(actions)
    print("\nСинхронізацію завершено.")


if __name__ == "__main__":
    main()