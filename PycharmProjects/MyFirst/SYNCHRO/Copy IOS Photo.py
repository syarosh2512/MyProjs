"""
Копіювання папки Photo:
  C:\\Temp\\Photo  --->  [T5 EVO]\\Photo

Односторонньо: копіюються ТІЛЬКИ нові або змінені файли (за розміром і
часом модифікації). Файли, які вже є на SSD і не змінились, пропускаються.
Ніщо не видаляється і не перезаписується без потреби.

SSD шукається за МІТКОЮ ТОМУ ("T5 EVO"), а не за літерою диска (D:, E:, F:),
бо літера може змінюватись залежно від того, скільки USB пристроїв підключено.

Використання:
    python copy_photo_to_ssd.py              # прев'ю + питання підтвердження
    python copy_photo_to_ssd.py --yes        # без питання, одразу копіює
    python copy_photo_to_ssd.py --dry-run    # тільки прев'ю, нічого не копіює
"""

import ctypes
import os
import shutil
import sys
import string

SOURCE_DIR = r"C:\Temp\Photo"
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


def plan_copy(source: str, dest: str):
    """Повертає список (rel_path, reason) файлів, які треба скопіювати:
    нові (яких немає в dest) або змінені (розмір/дата відрізняються)."""
    source_files = scan_folder(source)
    dest_files = scan_folder(dest)
    actions = []

    for rel in sorted(source_files):
        size_s, mtime_s = source_files[rel]

        if rel not in dest_files:
            actions.append((rel, "новий файл"))
            continue

        size_d, mtime_d = dest_files[rel]
        if size_s != size_d or abs(mtime_s - mtime_d) > TIME_TOLERANCE_SEC:
            actions.append((rel, "змінений файл"))
        # інакше - ідентичний, пропускаємо

    return actions


def print_plan(actions, dest):
    if not actions:
        print("Немає нових або змінених файлів. Копіювати нічого.")
        return
    print(f"\nЗнайдено {len(actions)} файл(ів) для копіювання в {dest}:\n")
    for rel, reason in actions:
        print(f"  {rel}   ({reason})")
    print()


def apply_plan(actions, source, dest):
    for rel, _ in actions:
        src_path = os.path.join(source, rel)
        dst_path = os.path.join(dest, rel)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)  # copy2 зберігає час модифікації
        print(f"  Скопійовано: {rel}")


def main():
    dry_run = "--dry-run" in sys.argv
    auto_yes = "--yes" in sys.argv

    ssd_drive = find_drive_by_label(VOLUME_LABEL)
    if not ssd_drive:
        print(f"Помилка: диск з міткою '{VOLUME_LABEL}' не знайдено.")
        print("Перевір, чи підключений SSD, і чи правильно вказана мітка тому.")
        sys.exit(1)

    dest_dir = os.path.join(ssd_drive, SUBFOLDER_ON_SSD)
    print(f"SSD знайдено: {ssd_drive}  (мітка: {VOLUME_LABEL})")
    print(f"Джерело:      {SOURCE_DIR}")
    print(f"Призначення:  {dest_dir}")

    if not os.path.isdir(SOURCE_DIR):
        print(f"Помилка: папка-джерело не знайдена: {SOURCE_DIR}")
        sys.exit(1)
    if not os.path.isdir(dest_dir):
        print(f"Увага: папка на SSD не існує, буде створена: {dest_dir}")
        os.makedirs(dest_dir, exist_ok=True)

    actions = plan_copy(SOURCE_DIR, dest_dir)
    print_plan(actions, dest_dir)

    if not actions:
        return
    if dry_run:
        print("Режим --dry-run: нічого не скопійовано.")
        return

    if not auto_yes:
        answer = input("Виконати копіювання? (y/n): ").strip().lower()
        if answer != "y":
            print("Скасовано.")
            return

    apply_plan(actions, SOURCE_DIR, dest_dir)
    print("\nКопіювання завершено.")


if __name__ == "__main__":
    main()