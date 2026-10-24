import os, json, subprocess, re, sys

SHARED_DIR = "/tmp/bodhi_workspace"
TARGET_REPO = os.environ.get("TARGET_REPO", "retina")
GH_TOKEN = os.environ.get("GH_PAT")

print(f"🏷️ [TAG ENGINE] Bắt đầu dán nhãn kết hợp KHUÔN MẪU và KINH NGHIỆM cho {TARGET_REPO}...")

storage_dir = f"{SHARED_DIR}/storage"
if not os.path.exists(storage_dir):
    res = subprocess.run(["git", "clone", "--depth", "1", f"https://x-access-token:{GH_TOKEN}@github.com/100048777766367/storage.git", storage_dir], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"🔴 Lỗi không thể kéo Storage: {res.stderr}")
        sys.exit(1)

try:
    with open(f"{storage_dir}/file_registry.json", "r") as f: file_reg = json.load(f)
    with open(f"{storage_dir}/dir_registry.json", "r") as f: dir_reg = json.load(f)

    with open(f"{SHARED_DIR}/dir_data.json", "r") as f: d_data = json.load(f)["directories"]
    with open(f"{SHARED_DIR}/file_data.json", "r") as f: f_data = json.load(f)["files"]
    with open(f"{SHARED_DIR}/code_data.json", "r") as f: c_data = json.load(f)
except Exception as e:
    print(f"🔴 Lỗi đọc dữ liệu thô: {e}")
    sys.exit(1)

normalized = re.sub(r'[_\.\s]+', '-', re.sub(r'([a-z])([A-Z])', r'\1-\2', TARGET_REPO)).lower().split('-')
r_root = normalized[0]
r_branch = normalized[1] if len(normalized) > 1 and not normalized[1].startswith(("g","v")) else "core"
r_gen = 0
for tok in normalized:
    m = re.match(r'^(?:g|gen|v)(\d+)$', tok)
    if m: r_gen = int(m.group(1))

canonical_repo_id = f"{r_root}-{r_branch}-g{r_gen}-00"

micro_passports = {
    "provenance_header": {
        "tags": ["#CHỨNG_CHỈ_XUẤT_XỨ", "#PROVENANCE_IDENTITY"],
        "repo_name": TARGET_REPO,
        "canonical_id": canonical_repo_id,
        "root_ancestor": r_root,
        "branch": r_branch,
        "generation": f"g{r_gen}"
    },
    "tier_2_directories": [], "tier_3_files": [], "tier_4_classes": [], "tier_5_functions": []
}

for d in d_data:
    base_dir = os.path.basename(d["path"]).lower()
    role = dir_reg.get(base_dir, "📂 THƯ MỤC TÙY BIẾN / KINH NGHIỆM ĐỘNG")
    d_clean = d["path"].replace("/", "_").replace("\\", "_")
    micro_passports["tier_2_directories"].append({
        "canonical_id": f"dir-{TARGET_REPO}-{d_clean}-g{r_gen}",
        "path": d["path"], "depth": d["depth"], "file_count": d["file_count"], "role_label": role
    })

blueprint_tags = file_reg.get("blueprint_tags", {})
for f in f_data:
    fp = f["path"]
    ext = os.path.splitext(fp)[1].lower()
    if not ext and "dockerfile" in fp.lower(): ext = "dockerfile"

    lang_label = file_reg.get("extensions", {}).get(ext, "📄 File Không Đuôi")
    is_core_template = False
    file_tags = []
    role_desc = "Thành phần mã nguồn động"

    for core_file, c_tags in blueprint_tags.items():
        if fp == core_file or fp.endswith("/" + core_file):
            file_tags = c_tags
            role_desc = "Trụ cột khuôn mẫu (Khóa cứng)"
            is_core_template = True
            break

    if not is_core_template:
        for kw, role_str in file_reg.get("role_rules", {}).items():
            if kw in fp.lower():
                role_desc = role_str
                break
        file_tags.append("#TỆP_SÁNG_TẠO_TÙY_BIẾN")
        if ext in [".json", ".yaml"]: file_tags.append("#DỮ_LIỆU_TRỌNG_SỐ")
        if ext in [".py", ".c", ".cpp", ".java", ".go", ".rs"]: file_tags.append("#MÃ_THỰC_THI_ĐỘNG")

    f_clean = fp.replace("/", "_").replace("\\", "_").replace(".", "_")
    micro_passports["tier_3_files"].append({
        "canonical_id": f"file-{TARGET_REPO}-{f_clean}-g{r_gen}",
        "path": fp, "hash": f["hash"], "size_bytes": f["size"],
        "language_tag": lang_label, "role_tag": role_desc, "biological_tags": file_tags
    })

for cls in c_data.get("classes", []):
    f_clean = os.path.splitext(os.path.basename(cls["file"]))[0]
    micro_passports["tier_4_classes"].append({
        "canonical_id": f"class-{TARGET_REPO}-{f_clean}-{cls['name']}",
        "class_name": cls["name"], "file": cls["file"], "line_start": cls["line"]
    })

for fn in c_data.get("functions", []):
    f_clean = os.path.splitext(os.path.basename(fn["file"]))[0]
    snip = fn.get("snippet", "").lower()

    tags = []
    if "assert" in snip or "try" in snip or "require" in snip: tags.append("#GUARDED_LÁ_CHẮN")
    if "^" in snip or "xor" in snip: tags.append("#XOR_MẦM_ĐỘT_BIẾN")
    if "request" in snip or "socket" in snip or "fetch" in snip: tags.append("#THỤ_CẢM_RECEPTOR")
    if "print" in snip or "write" in snip or "emit" in snip: tags.append("#TÁC_TỬ_ACTUATOR")
    if not tags: tags.append("#NORMAL_THỰC_THI")

    micro_passports["tier_5_functions"].append({
        "canonical_id": f"fn-{TARGET_REPO}-{f_clean}-{fn['name']}",
        "func_name": fn["name"], "file": fn["file"], "line_start": fn["line"],
        "biological_tags": tags
    })

os.makedirs(f"{storage_dir}/micro_passports", exist_ok=True)
output_path = f"{storage_dir}/micro_passports/{TARGET_REPO}_passports.json"

with open(output_path, "w", encoding="utf-8") as fw:
    json.dump(micro_passports, fw, indent=4, ensure_ascii=False)

os.chdir(storage_dir)
subprocess.run(["git", "config", "--global", "user.name", "Bodhi-Tag-Bot"])
subprocess.run(["git", "config", "--global", "user.email", "tag@bodhi.node"])
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", f"🏷️ [Dynamic Tagging] Lưu căn cước vi mô (Mẫu + Kinh nghiệm) cho {TARGET_REPO} [skip ci]"])
push_res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)

if push_res.returncode == 0:
    print(f"👑 [TAG ENGINE] Đã dán nhãn kết hợp KHUÔN MẪU và KINH NGHIỆM thành công!")
else:
    print(f"⚠️ Lỗi đẩy Git từ Trạm Tag: {push_res.stderr.strip()}")
