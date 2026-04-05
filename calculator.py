"""
亲戚称呼计算器 - 核心逻辑
"""
from relations import ALL_RELATIONS, RELATION_OPTIONS

# 预编译常量，避免重复计算
_UP_WORDS = {"father", "mother"}
_DOWN_WORDS = {"son", "daughter"}
_SAME_GEN_WORDS = {"elder_brother", "younger_brother", "elder_sister", "younger_sister", "spouse"}


def get_title(relation_path: str, target_gender: str, my_gender: str) -> dict:
    """
    根据关系路径和性别，计算应该如何称呼这个亲戚

    Args:
        relation_path: 关系路径，如 "father.elder_brother"
        target_gender: 亲戚的性别，"male" 或 "female"
        my_gender: 自己的性别，"male" 或 "female"

    Returns:
        dict 包含称呼、反向称呼、辈分差和关系描述
    """
    title = _lookup_title(relation_path, target_gender)
    reverse_path = _compute_reverse_path(relation_path, my_gender)
    reverse_title = _lookup_title(reverse_path, my_gender) if reverse_path else "未知"
    generation_diff = _compute_generation(relation_path)
    relation_desc = _describe_relation(relation_path)

    return {
        "title": title,
        "reverse_title": reverse_title,
        "generation_diff": generation_diff,
        "relation_desc": relation_desc,
        "relation_path": relation_path,
    }


def _lookup_title(path: str, gender: str) -> str:
    """在关系表中查找称呼"""
    if path not in ALL_RELATIONS:
        return "未知称呼"
    entry = ALL_RELATIONS[path]
    return entry.get(gender) or entry.get("male", "未知称呼")


def _compute_generation(path: str) -> int:
    """
    计算辈分差：正数=长辈，负数=晚辈，0=同辈
    """
    gen = 0
    for p in path.split("."):
        if p in _UP_WORDS:
            gen += 1
        elif p in _DOWN_WORDS:
            gen -= 1
    return gen


def _compute_reverse_path(path: str, my_gender: str) -> str:
    """根据关系路径，推算对方眼中我是什么关系"""
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

        # 堂表亲
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


def _describe_relation(path: str) -> str:
    """生成关系的自然语言描述"""
    PART_NAMES = {
        "father": "父亲", "mother": "母亲",
        "son": "儿子", "daughter": "女儿",
        "elder_brother": "哥哥", "younger_brother": "弟弟",
        "elder_sister": "姐姐", "younger_sister": "妹妹",
        "spouse": "配偶",
    }
    parts = path.split(".")
    if len(parts) == 1:
        return "直系亲属"
    chain = " → ".join(PART_NAMES.get(p, p) for p in parts[:-1])
    last = PART_NAMES.get(parts[-1], parts[-1])
    return f"通过 {chain} 找到的{last}"


def search_relations(keyword: str) -> list:
    """通过关键词搜索亲戚关系"""
    keyword_lower = keyword.lower()
    results = []
    for display_name, path, gender in RELATION_OPTIONS:
        if keyword_lower in display_name.lower():
            rel = ALL_RELATIONS.get(path, {})
            results.append({
                "display": display_name,
                "path": path,
                "male_title": rel.get("male", ""),
                "female_title": rel.get("female", ""),
            })
    return results


def get_all_relations_by_generation() -> dict:
    """按辈分分组返回所有关系"""
    groups = {
        "祖辈及以上 (+2 代及以上)": [],
        "父辈 (+1 代)": [],
        "同辈 (0 代)": [],
        "子辈 (-1 代)": [],
        "孙辈及以下 (-2 代及以下)": [],
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
            groups["祖辈及以上 (+2 代及以上)"].append(entry)
        elif gen == 1:
            groups["父辈 (+1 代)"].append(entry)
        elif gen == 0:
            groups["同辈 (0 代)"].append(entry)
        elif gen == -1:
            groups["子辈 (-1 代)"].append(entry)
        else:
            groups["孙辈及以下 (-2 代及以下)"].append(entry)

    return groups


def calculate_custom_path(steps: list, target_gender: str, my_gender: str) -> dict:
    """通过步骤列表计算自定义路径的称呼"""
    path = ".".join(steps)
    return get_title(path, target_gender, my_gender)
