import csv
from CwnGraph import CwnImage
from CwnGraph.cwn_types import CwnSense

cwn = CwnImage.latest()
lemma_groups = cwn.get_all_lemmas()  # Dict[str, List[CwnLemma]]

rows = []

for lemmas in lemma_groups.values():  # 🔁 List[CwnLemma]
    for lemma in lemmas:
        for sense in lemma.senses:
            for rel_type, target, _ in sense.relations:
                if rel_type == "antonym" and isinstance(target, CwnSense):
                    antonyms = set(ant.lemma for ant in target.lemmas)
                    for ant_word in antonyms:
                        rows.append([
                            lemma.lemma,
                            sense.definition,
                            ant_word
                        ])

# 寫入 CSV
with open("all_antonyms.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["詞條", "定義", "反義詞"])
    writer.writerows(rows)


print("All antonyms are done!")