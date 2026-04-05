"""
中国亲戚称呼关系数据库
路径格式：(性别，父系/母系，辈分偏移，关系链)
"""

# ==================== 基础关系定义 ====================
DIRECT_RELATIONS = {
    # 自己
    "self": {"male": "自己 (男)", "female": "自己 (女)"},
    # 上一辈
    "father": {"male": "父亲", "female": "父亲"},
    "mother": {"male": "母亲", "female": "母亲"},
    # 上两辈
    "father.father": {"male": "爷爷", "female": "爷爷"},
    "father.mother": {"male": "奶奶", "female": "奶奶"},
    "mother.father": {"male": "外公/姥爷", "female": "外公/姥爷"},
    "mother.mother": {"male": "外婆/姥姥", "female": "外婆/姥姥"},
    # 上三辈
    "father.father.father": {"male": "曾祖父", "female": "曾祖父"},
    "father.father.mother": {"male": "曾祖母", "female": "曾祖母"},
    "father.mother.father": {"male": "曾祖父 (外)", "female": "曾祖父 (外)"},
    "father.mother.mother": {"male": "曾祖母 (外)", "female": "曾祖母 (外)"},
    "mother.father.father": {"male": "外曾祖父", "female": "外曾祖父"},
    "mother.father.mother": {"male": "外曾祖母", "female": "外曾祖母"},
    "mother.mother.father": {"male": "外曾祖父", "female": "外曾祖父"},
    "mother.mother.mother": {"male": "外曾祖母", "female": "外曾祖母"},
    # 下一辈
    "son": {"male": "儿子", "female": "儿子"},
    "daughter": {"male": "女儿", "female": "女儿"},
    # 下两辈
    "son.son": {"male": "孙子", "female": "孙子"},
    "son.daughter": {"male": "孙女", "female": "孙女"},
    "daughter.son": {"male": "外孙", "female": "外孙"},
    "daughter.daughter": {"male": "外孙女", "female": "外孙女"},
    # 同辈
    "elder_brother": {"male": "哥哥", "female": "哥哥"},
    "younger_brother": {"male": "弟弟", "female": "弟弟"},
    "elder_sister": {"male": "姐姐", "female": "姐姐"},
    "younger_sister": {"male": "妹妹", "female": "妹妹"},
}

PATERNAL_RELATIONS = {
    # 父亲的兄弟姐妹
    "father.elder_brother": {"male": "大伯/伯父", "female": "大伯/伯父"},
    "father.younger_brother": {"male": "叔叔/叔父", "female": "叔叔/叔父"},
    "father.elder_sister": {"male": "姑姑/姑妈", "female": "姑姑/姑妈"},
    "father.younger_sister": {"male": "姑姑/小姑", "female": "姑姑/小姑"},
    # 父亲兄弟的配偶
    "father.elder_brother.spouse": {"male": "伯母", "female": "伯母"},
    "father.younger_brother.spouse": {"male": "婶婶/婶母", "female": "婶婶/婶母"},
    # 父亲姐妹的配偶
    "father.elder_sister.spouse": {"male": "姑父", "female": "姑父"},
    "father.younger_sister.spouse": {"male": "姑父", "female": "姑父"},
    # 父亲兄弟的孩子（堂亲）
    "father.elder_brother.son": {"male": "堂哥", "female": "堂哥"},
    "father.elder_brother.daughter": {"male": "堂姐", "female": "堂姐"},
    "father.younger_brother.son": {"male": "堂弟", "female": "堂弟"},
    "father.younger_brother.daughter": {"male": "堂妹", "female": "堂妹"},
    # 父亲姐妹的孩子（表亲）
    "father.elder_sister.son": {"male": "表哥", "female": "表哥"},
    "father.elder_sister.daughter": {"male": "表姐", "female": "表姐"},
    "father.younger_sister.son": {"male": "表弟", "female": "表弟"},
    "father.younger_sister.daughter": {"male": "表妹", "female": "表妹"},
}

MATERNAL_RELATIONS = {
    # 母亲的兄弟姐妹
    "mother.elder_brother": {"male": "舅舅/大舅", "female": "舅舅/大舅"},
    "mother.younger_brother": {"male": "舅舅/小舅", "female": "舅舅/小舅"},
    "mother.elder_sister": {"male": "姨妈/大姨", "female": "姨妈/大姨"},
    "mother.younger_sister": {"male": "小姨/姨妈", "female": "小姨/姨妈"},
    # 母亲兄弟的配偶
    "mother.elder_brother.spouse": {"male": "舅妈/大舅妈", "female": "舅妈/大舅妈"},
    "mother.younger_brother.spouse": {"male": "舅妈/小舅妈", "female": "舅妈/小舅妈"},
    # 母亲姐妹的配偶
    "mother.elder_sister.spouse": {"male": "姨父/大姨父", "female": "姨父/大姨父"},
    "mother.younger_sister.spouse": {"male": "姨父/小姨父", "female": "姨父/小姨父"},
    # 母亲兄弟的孩子（表亲）
    "mother.elder_brother.son": {"male": "表哥", "female": "表哥"},
    "mother.elder_brother.daughter": {"male": "表姐", "female": "表姐"},
    "mother.younger_brother.son": {"male": "表弟", "female": "表弟"},
    "mother.younger_brother.daughter": {"male": "表妹", "female": "表妹"},
    # 母亲姐妹的孩子（表亲）
    "mother.elder_sister.son": {"male": "表哥", "female": "表哥"},
    "mother.elder_sister.daughter": {"male": "表姐", "female": "表姐"},
    "mother.younger_sister.son": {"male": "表弟", "female": "表弟"},
    "mother.younger_sister.daughter": {"male": "表妹", "female": "表妹"},
}

SPOUSE_RELATIONS = {
    # 配偶
    "spouse": {"male": "丈夫/老公", "female": "妻子/老婆"},
    # 配偶父母
    "spouse.father": {"male": "岳父/泰山", "female": "公公/爸爸"},
    "spouse.mother": {"male": "岳母/泰水", "female": "婆婆/妈妈"},
    # 配偶兄弟姐妹
    "spouse.elder_brother": {"male": "大舅子/内兄", "female": "大伯子"},
    "spouse.younger_brother": {"male": "小舅子/内弟", "female": "小叔子"},
    "spouse.elder_sister": {"male": "大姨子/内姐", "female": "大姑子"},
    "spouse.younger_sister": {"male": "小姨子/内妹", "female": "小姑子"},
}

# 合并所有关系
ALL_RELATIONS = {
    **DIRECT_RELATIONS,
    **PATERNAL_RELATIONS,
    **MATERNAL_RELATIONS,
    **SPOUSE_RELATIONS,
}

# 关系步骤定义
RELATION_STEPS = {
    "父方祖辈": {
        "father.father": "爷爷",
        "father.mother": "奶奶",
    },
    "母方祖辈": {
        "mother.father": "外公/姥爷",
        "mother.mother": "外婆/姥姥",
    },
    "父辈": {
        "father": "父亲",
        "mother": "母亲",
        "father.elder_brother": "伯父（父亲的哥哥）",
        "father.younger_brother": "叔父（父亲的弟弟）",
        "father.elder_sister": "姑母（父亲的姐姐）",
        "father.younger_sister": "小姑（父亲的妹妹）",
        "mother.elder_brother": "舅父（母亲的哥哥）",
        "mother.younger_brother": "小舅（母亲的弟弟）",
        "mother.elder_sister": "姨母（母亲的姐姐）",
        "mother.younger_sister": "小姨（母亲的妹妹）",
    }
}

# 界面展示的关系树
RELATION_OPTIONS = [
    # 直系
    ("父亲", "father", "male"),
    ("母亲", "mother", "female"),
    ("爷爷（父亲的父亲）", "father.father", "male"),
    ("奶奶（父亲的母亲）", "father.mother", "female"),
    ("外公/姥爷（母亲的父亲）", "mother.father", "male"),
    ("外婆/姥姥（母亲的母亲）", "mother.mother", "female"),
    # 父系旁亲
    ("伯父（父亲的哥哥）", "father.elder_brother", "male"),
    ("叔叔（父亲的弟弟）", "father.younger_brother", "male"),
    ("姑妈/大姑（父亲的姐姐）", "father.elder_sister", "female"),
    ("小姑（父亲的妹妹）", "father.younger_sister", "female"),
    ("伯母（伯父的妻子）", "father.elder_brother.spouse", "female"),
    ("婶婶（叔叔的妻子）", "father.younger_brother.spouse", "female"),
    ("姑父（姑妈的丈夫）", "father.elder_sister.spouse", "male"),
    # 母系旁亲
    ("大舅（母亲的哥哥）", "mother.elder_brother", "male"),
    ("小舅（母亲的弟弟）", "mother.younger_brother", "male"),
    ("大姨（母亲的姐姐）", "mother.elder_sister", "female"),
    ("小姨（母亲的妹妹）", "mother.younger_sister", "female"),
    ("大舅妈（大舅的妻子）", "mother.elder_brother.spouse", "female"),
    ("小舅妈（小舅的妻子）", "mother.younger_brother.spouse", "female"),
    ("大姨父（大姨的丈夫）", "mother.elder_sister.spouse", "male"),
    ("小姨父（小姨的丈夫）", "mother.younger_sister.spouse", "male"),
    # 同辈
    ("哥哥（父母的大儿子）", "elder_brother", "male"),
    ("弟弟（父母的小儿子）", "younger_brother", "male"),
    ("姐姐（父母的大女儿）", "elder_sister", "female"),
    ("妹妹（父母的小女儿）", "younger_sister", "female"),
    # 堂亲（父系）
    ("堂哥（伯父/叔叔的大儿子）", "father.elder_brother.son", "male"),
    ("堂弟（伯父/叔叔的小儿子）", "father.younger_brother.son", "male"),
    ("堂姐（伯父/叔叔的大女儿）", "father.elder_brother.daughter", "female"),
    ("堂妹（伯父/叔叔的小女儿）", "father.younger_brother.daughter", "female"),
    # 表亲（母系）
    ("表哥（舅舅/姨妈的大儿子）", "mother.elder_brother.son", "male"),
    ("表弟（舅舅/姨妈的小儿子）", "mother.younger_brother.son", "male"),
    ("表姐（舅舅/姨妈的大女儿）", "mother.elder_brother.daughter", "female"),
    ("表妹（舅舅/姨妈的小女儿）", "mother.younger_brother.daughter", "female"),
    # 晚辈
    ("儿子", "son", "male"),
    ("女儿", "daughter", "female"),
    ("孙子（儿子的儿子）", "son.son", "male"),
    ("孙女（儿子的女儿）", "son.daughter", "female"),
    ("外孙（女儿的儿子）", "daughter.son", "male"),
    ("外孙女（女儿的女儿）", "daughter.daughter", "female"),
    # 配偶
    ("配偶（丈夫/妻子）", "spouse", "both"),
    ("岳父/公公（配偶的父亲）", "spouse.father", "male"),
    ("岳母/婆婆（配偶的母亲）", "spouse.mother", "female"),
    ("大舅子/大伯子（配偶的哥哥）", "spouse.elder_brother", "male"),
    ("小舅子/小叔子（配偶的弟弟）", "spouse.younger_brother", "male"),
    ("大姨子/大姑子（配偶的姐姐）", "spouse.elder_sister", "female"),
    ("小姨子/小姑子（配偶的妹妹）", "spouse.younger_sister", "female"),
]
