# -*- coding: utf-8 -*-

def consoleconvert(message, emojiEnable):
  translation_table = str.maketrans({"." : " ", "n" : "#"})
  translation_table = str.maketrans({})
  if emojiEnable:
    translation_table = str.maketrans({'~': '🟦', 'c': '🟨', 'b': '🔘', '_': '⬜', 'p' : '🟪' , 'w': '🟡', '.': ' ', 'g' : '🟩', 'r' : '🟥', 'n' : '🟫' , 'o' : '🟠'})
    return message.translate(translation_table)
  return message[:16].translate(translation_table)
