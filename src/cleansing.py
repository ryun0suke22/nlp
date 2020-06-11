import re
import unicodedata

# 半角カタカナなどは全角に変換したほうが安全
# タブや空白記号などにも要注意
text = '	ＣＬＥＡＮＳ ing  によりﾃｷｽﾄﾃﾞｰﾀを変換すると　トラブルが少なくなります。'
print("Before:", text)

translation_table = str.maketrans(dict(zip('()!', '（）！')))
text = unicodedata.normalize('NFKC', text).translate(translation_table)
text = re.sub(r'\s+', '', text)
print("After:", text)
