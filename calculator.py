"""
亲戚称呼计算器 - 核心逻辑
"""
from relations import ALL_RELATIONS, RELATION_OPTIONS


def get_title(relation_path: str, target_gender: str, my_gender: str) -> dict:
    """
    根据关系路径和性别，计算应该如何称呼这个亲戚
    以及这个亲戚应该如何称呼自己（我）

    Args:
        relation_path: 关系路径，如 "father.elder_brother"
        target_gender: 亲戚的性别，"male" 或 "female"
        my_gender: 自己的性别，"male" 或 "female"

    Returns:
        dict 包含:
            - title: 我叫对方什么
            - reverse_title: 对方叫我什么
            - relation_desc: 关系描述
            - generation_diff: 辈分差（正数=对方辈分高）
    """

    # 1. 查找正向称呼（我叫对方什么）
    title = _lookup_title(relation_path, target_gender)

    # 2. 计算反向路径（对方和我的关系）
    reverse_path = _compute_reverse_path(relation_path, my_gender)
    reverse_title = _lookup_title(reverse_path, my_gender) if reverse_path else "未知"

    # 3. 计算辈分差
    generation_diff = _compute_generation(relation_path)

    # 4. 关系分析
    relation_desc = _describe_relation(relation_path, target_gender)

    return {
        "title": title,
        "reverse_title": reverse_title,
        "generation_diff": generation_diff,
        "relation_desc": relation_desc,
        "relation_path": relation_path,
    }


def _lookup_title(path: str, gender: str) -> str:
    """在关系表中查找称呼"""
    if path in ALL_RELATIONS:
        entry = ALL_RELATIONS[path]
        if gender in entry:
            return entry[gender]
        elif "male" in entry:
            return entry["male"]
    return "未知称呼"


def _compute_generation(path: str) -> int:
    """
    计算辈分差
    正数: 对方辈分比我高（长辈）
    负数: 对方辈分比我低（晚辈）
    0: 同辈
    """
    UP_WORDS = {"father", "mother", "spouse"}  # spouse算平辈
    DOWN_WORDS = {"son", "daughter"}
    SAME_GEN_WORDS = {"elder_brother", "younger_brother", "elder_sister", "younger_sister",
                      "spouse", "elder_brother", "younger_brother"}

    parts = path.split(".")
    gen = 0

    for p in parts:
        if p in ("father", "mother"):
            gen += 1
        elif p in ("son", "daughter"):
            gen -= 1
        elif p == "spouse":
            gen += 0  # 配偶同辈
        # elder_brother / younger_brother / sister / elder_sister 等同辈，不计

    return gen


def _compute_reverse_path(path: str, my_gender: str) -> str:
    """
    根据关系路径，推算对方眼中我是什么关系
    简化版：只处理常见路径
    """
    REVERSE_MAP = {
        # 直系
        "father": "son" if my_gender == "male" else "daughter",
        "mother": "son" if my_gender == "male" else "daughter",
        "father.father": "son.son" if my_gender == "male" else "son.daughter",
        "father.mother": "son.son" if my_gender == "male" else "son.daughter",
        "mother.father": "daughter.son" if my_gender == "male" else "daughter.daughter",
        "mother.mother": "daughter.son" if my_gender == "male" else "daughter.daughter",
        "son": "father",
        "daughter": "mother",
        "son.son": "father.father",
        "son.daughter": "father.mother",
        "daughter.son": "mother.father",
        "daughter.daughter": "mother.mother",

        # 同辈
        "elder_brother": "younger_brother" if my_gender == "male" else "younger_sister",
        "younger_brother": "elder_brother" if my_gender == "male" else "elder_sister",
        "elder_sister": "younger_brother" if my_gender == "male" else "younger_sister",
        "younger_sister": "elder_brother" if my_gender == "male" else "elder_sister",

        # 父系
        "father.elder_brother": "son" if my_gender == "male" else "daughter",
        "father.younger_brother": "son" if my_gender == "male" else "daughter",
        "father.elder_sister": "son" if my_gender == "male" else "daughter",
        "father.younger_sister": "son" if my_gender == "male" else "daughter",

        # 母系
        "mother.elder_brother": "son" if my_gender == "male" else "daughter",
        "mother.younger_brother": "son" if my_gender == "male" else "daughter",
        "mother.elder_sister": "son" if my_gender == "male" else "daughter",
        "mother.younger_sister": "son" if my_gender == "male" else "daughter",

        # 堂表亲 - 对方叫我堂/表兄弟姐妹
        "father.elder_brother.son": "elder_brother" if my_gender == "male" else "elder_sister",
        "father.elder_brother.daughter": "elder_brother" if my_gender == "male" else "elder_sister",
        "father.younger_brother.son": "younger_brother" if my_gender == "male" else "younger_sister",
        "father.younger_brother.daughter": "younger_brother" if my_gender == "male" else "younger_sister",
        "mother.elder_brother.son": "elder_brother" if my_gender == "male" else "elder_sister",
        "mother.younger_brother.son": "younger_brother" if my_gender == "male" else "younger_sister",
        "mother.elder_sister.son": "elder_brother" if my_gender == "male" else "elder_sister",
        "mother.younger_sister.son": "younger_brother" if my_gender == "male" else "younger_sister",

        # 配偶
        "spouse": "spouse",
        "spouse.father": "son" if my_gender == "male" else "daughter",
        "spouse.mother": "son" if my_gender == "male" else "daughter",
    }

    return REVERSE_MAP.get(path, "")


def _describe_relation(path: str, gender: str) -> str:
    """生成关系的自然语言描述"""
    PART_NAMES = {
        "father": "父亲",
        "mother": "母亲",
        "son": "儿子",
        "daughter": "女儿",
        "elder_brother": "哥哥",
        "younger_brother": "弟弟",
        "elder_sister": "姐姐",
        "younger_sister": "妹妹",
        "spouse": "配偶",
    }
    parts = path.split(".")
    if len(parts) == 1:
        return f"直系亲属"
    chain = " → ".join(PART_NAMES.get(p, p) for p in parts[:-1])
    last = PART_NAMES.get(parts[-1], parts[-1])
    return f"通过 {chain} 找到的{last}"


def search_relations(keyword: str) -> list:
    """
    通过关键词搜索亲戚关系
    返回匹配的关系列表
    """
    results = []
    for display_name, path, gender in RELATION_OPTIONS:
        if keyword.lower() in display_name.lower():
            male_title = ALL_RELATIONS.get(path, {}).get("male", "")
            female_title = ALL_RELATIONS.get(path, {}).get("female", "")
            results.append({
                "display": display_name,
                "path": path,
                "male_title": male_title,
                "female_title": female_title,
            })
    return results


def get_all_relations_by_generation() -> dict:
    """
    按辈分分组返回所有关系
    """
    groups = {
        "祖辈及以上 (+2代及以上)": [],
        "父辈 (+1代)": [],
        "同辈 (0代)": [],
        "子辈 (-1代)": [],
        "孙辈及以下 (-2代及以下)": [],
        "配偶及姻亲": [],
    }

    for display_name, path, gender in RELATION_OPTIONS:
        gen = _compute_generation(path)
        entry = {
            "display": display_name,
            "path": path,
            "gender": gender,
            "male_title": ALL_RELATIONS.get(path, {}).get("male", ""),
            "female_title": ALL_RELATIONS.get(path, {}).get("female", ""),
        }

        if "spouse" in path:
            groups["配偶及姻亲"].append(entry)
        elif gen >= 2:
            groups["祖辈及以上 (+2代及以上)"].append(entry)
        elif gen == 1:
            groups["父辈 (+1代)"].append(entry)
        elif gen == 0:
            groups["同辈 (0代)"].append(entry)
        elif gen == -1:
            groups["子辈 (-1代)"].append(entry)
        else:
            groups["孙辈及以下 (-2代及以下)"].append(entry)

    return groups


# ==================== 自定义关系路径计算 ====================

STEP_OPTIONS = {
    "root": {
        "label": "选择起始关系",
        "choices": [
            {"key": "father", "label": "父亲", "gender": "male"},
            {"key": "mother", "label": "母亲", "female": "female"},
            {"key": "elder_brother", "label": "哥哥", "gender": "male"},
            {"key": "younger_brother", "label": "弟弟", "gender": "male"},
            {"key": "elder_sister", "label": "姐姐", "gender": "female"},
            {"key": "younger_sister", "label": "妹妹", "gender": "female"},
            {"key": "son", "label": "儿子", "gender": "male"},
            {"key": "daughter", "label": "女儿", "gender": "female"},
            {"key": "spouse", "label": "配偶", "gender": "both"},
        ]
    }
}


def calculate_custom_path(steps: list, target_gender: str, my_gender: str) -> dict:
    """
    通过步骤列表计算自定义路径的称呼
    steps: ["father", "elder_brother", "son"] 表示 "父亲的哥哥的儿子"
    """
    path = ".".join(steps)
    return get_title(path, target_gender, my_gender)
