# ==============================================================================
# 🏷️ TAG ENGINE: GẮN NHÃN TỰ THÂN ĐA CHIỀU (KHÔNG PHỤ THUỘC README)
# ==============================================================================
import os, json

MASTER_TAGS = {
    "engine": ["#HẠT_NHÂN_ĐỘNG_CƠ", "#TRÁI_TIM_TỰ_TRỊ"],
    "workflow": ["#TRỤC_CI_CD_TỰ_HÀNH", "#GIT_BỌC_THÉP_CHỐNG_128"],
    "docker": ["#MÔI_TRƯỜNG_CONTAINER", "#MẪU_SỐ_CHUNG_3_14"],
    "dependabot": ["#BẢO_TRÌ_TỰ_ĐỘNG", "#VÁ_LỖ_HỔNG_HÀNG_TUẦN"],
    "contract": ["#HIẾN_ƯỚC_GỐC", "#PHÁP_LÝ_NÚT_MẠNG"]
}

def tag_file(fname):
    fn = fname.lower()
    if "engine" in fn or "kernel" in fn: return MASTER_TAGS["engine"]
    if "lifecycle" in fn or "node.yml" in fn: return MASTER_TAGS["workflow"]
    if "dockerfile" in fn: return MASTER_TAGS["docker"]
    if "dependabot" in fn: return MASTER_TAGS["dependabot"]
    if "contract" in fn: return MASTER_TAGS["contract"]
    return ["#THÀNH_PHẦN_MÃ_NGUỒN"]

print("🏷️ [TAG ENGINE] Đã nạp bộ quy chuẩn 5 nhãn định danh cốt lõi.")
