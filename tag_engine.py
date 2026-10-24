# ==============================================================================
# 🏷️ TAG ENGINE: GẮN 10 NHÃN ĐỊNH DANH ĐỘC QUYỀN CHO BẢN KHUÔN BẤT BIẾN
# ==============================================================================
TAG_DICTIONARY = {
    "workflow": "#TRỤC_CI_CD_TỰ_HÀNH",
    "docker": "#MÔI_TRƯỜNG_CONTAINER_3_14",
    "dependabot": "#BẢO_TRÌ_TỰ_ĐỘNG",
    "contract": "#HIẾN_ƯỚC_GỐC_PHÁP_LÝ",
    "engine": "#HẠT_NHÂN_ĐỘNG_CƠ_XOR",
    "forward": "#SÓNG_GIAO_CẢM_NGOẠI_VI",
    "passport": "#HỘ_CHIẾU_DÒNG_HỌ_TAM_ĐOẠN",
    "state": "#SỔ_CÁI_KỶ_NGUYÊN_CID",
    "gitignore": "#LÁ_CHẮN_POKA_YOKE_BYTECODE",
    "readme": "#TUYÊN_NGÔN_SỨ_MỆNH_BẢO_TÀNG"
}

def identify_tag(fname):
    fn = fname.lower()
    if "lifecycle" in fn or "node.yml" in fn: return TAG_DICTIONARY["workflow"]
    if "dockerfile" in fn: return TAG_DICTIONARY["docker"]
    if "dependabot" in fn: return TAG_DICTIONARY["dependabot"]
    if "contract.json" in fn: return TAG_DICTIONARY["contract"]
    if "engine" in fn or "kernel" in fn: return TAG_DICTIONARY["engine"]
    if "forward" in fn: return TAG_DICTIONARY["forward"]
    if "passport" in fn: return TAG_DICTIONARY["passport"]
    if "state.json" in fn: return TAG_DICTIONARY["state"]
    if "gitignore" in fn: return TAG_DICTIONARY["gitignore"]
    if "readme" in fn: return TAG_DICTIONARY["readme"]
    return "#THÀNH_PHẦN_MÃ_NGUỒN"

print("🏷️ [TAG ENGINE] Đã cập nhật 10 nhãn định danh chuẩn mực.")
