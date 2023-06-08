from app.models import Keyword, KeywordGroup, ParentKeyword
from file_tools import load_csv_data

def cleanse(keyword, check=['X', 'x', '[']):
    l = keyword.split(' ')
    for c in check:
        if c in l:
            return False
    return True


def update_keywords(fn='Fin keywords.csv', fp='app/data/keywords', cleanse_keyword=True):
    rows = load_csv_data(fn, fp)
    for i,row in enumerate(rows):
        if i != 0:
            k = row[0]
            print(k)
            if not cleanse_keyword or (cleanse_keyword and cleanse(k)):
                d = {}
                d['is_primary'] = bool(row[1])
                d['is_category'] = bool(row[2])
                d['is_bank'] = bool(row[3])
                d['is_investment'] = bool(row[4])
                d['is_general'] = bool(row[5])
                d['is_location'] = bool(row[6])
                d['is_rate'] = bool(row[11])
                d['is_biz'] = bool(row[9])
                d['audience'] = row[10]
                d['is_core_product'] = bool(row[12])
                keyword, created = Keyword.objects.update_or_create(keyword=k, defaults=d)

                if row[8]:
                    print('kg', row[8])
                    kg, created = KeywordGroup.objects.update_or_create(keyword=row[8], defaults={'is_core_product':bool(row[12])})
                    kg.related_keyword.add(keyword)

                if row[7]:
                    print('pk', row[7])
                    pk, created = ParentKeyword.objects.update_or_create(keyword=row[7], defaults={'is_core_product':bool(row[12])})
                    pk.related_keyword.add(keyword)



