import unittest
from ukling.tokenizer import UkrainianWordTokenizer

class UkrainianWordTokenizerTest(unittest.TestCase):
        def testTokenizeUrl(self):
                w = UkrainianWordTokenizer()
                url = "http://youtube.com:80/herewego?start=11&quality=high%3F"
                testList = w.tokenize(url)
                self.assertEqual([url], testList)

        def testNumbers(self):
                w = UkrainianWordTokenizer()

                testList = w.tokenize("300 грн на балансі")
                self.assertEqual(["300", " ", "грн", " ", "на", " ", "балансі"], testList)

                testList = w.tokenize("надійшло 2,2 мільйона")
                self.assertEqual(["надійшло", " ", "2,2", " ", "мільйона"], testList)

                testList = w.tokenize("надійшло 84,46 мільйона")
                self.assertEqual(["надійшло", " ", "84,46", " ", "мільйона"], testList)

                #TODO
                #testList = w.tokenize("в 1996,1997,1998")
                #self.assertEqual(["в", " ", "1996,1997,1998"], testList)

                testList = w.tokenize("2 000 тон з 12 000 відер")
                self.assertEqual(["2 000", " ", "тон", " ", "з", " ", "12 000", " ", "відер"], testList)

                testList = w.tokenize("надійшло 12 000 000 тон")
                self.assertEqual(["надійшло", " ", "12 000 000", " ", "тон"], testList)

                testList = w.tokenize("до 01.01.42 400 000 шт.")
                self.assertEqual(["до", " ", "01.01.42", " ", "400 000", " ", "шт."], testList)

                #should not merge these numbers
                testList = w.tokenize("2 15 мільярдів")
                self.assertEqual(["2", " ", "15", " ", "мільярдів"], testList)

                testList = w.tokenize("у 2004 200 мільярдів")
                self.assertEqual(["у", " ", "2004", " ", "200", " ", "мільярдів"], testList)

                testList = w.tokenize("в бюджеті-2004 200 мільярдів")
                self.assertEqual(["в", " ", "бюджеті-2004", " ", "200", " ", "мільярдів"], testList)

                testList = w.tokenize("з 12 0001 відер")
                self.assertEqual(["з", " ", "12", " ", "0001", " ", "відер"], testList)

                testList = w.tokenize("сталося 14.07.2001 вночі")
                self.assertEqual(["сталося", " ", "14.07.2001", " ", "вночі"], testList)

                testList = w.tokenize("вчора о 7.30 ранку")
                self.assertEqual(["вчора", " ", "о", " ", "7.30", " ", "ранку"], testList)

                testList = w.tokenize("вчора о 7:30 ранку")
                self.assertEqual(["вчора", " ", "о", " ", "7:30", " ", "ранку"], testList)
        
        def testTokenize(self):
                w = UkrainianWordTokenizer()

                testList = w.tokenize("Вони прийшли додому.")
                self.assertEqual(["Вони", " ", "прийшли", " ", "додому", "."], testList)

                testList = w.tokenize("Вони прийшли пʼятими зів’ялими.")
                self.assertEqual(["Вони", " ", "прийшли", " ", "п'ятими", " ", "зів'ялими", "."], testList)

                #testList = w.tokenize("Вони\u0301 при\u00ADйшли пʼя\u0301тими зів’я\u00ADлими.")
                #self.assertEqual(["Вони", " ", "прийшли", " ", "п'ятими", " ", "зів'ялими", "."], testList)

                testList = w.tokenize("я українець(сміється")
                self.assertEqual(["я", " ", "українець", "(", "сміється"], testList)
                        
                testList = w.tokenize("ОУН(б) та КП(б)У")
                self.assertEqual(["ОУН(б)", " ", "та", " ", "КП(б)У"], testList)

                testList = w.tokenize("Негода є... заступником")
                self.assertEqual(["Негода", " ", "є", "...", " ", "заступником"], testList)

                testList = w.tokenize("Запагубили!.. також")
                self.assertEqual(["Запагубили", "!..", " ", "також"], testList)

                testList = w.tokenize("Цей графин.")
                self.assertEqual(["Цей", " ", "графин", "."], testList)

                testList = w.tokenize("— Гм.")
                self.assertEqual(["—", " ", "Гм", "."], testList)

                testList = w.tokenize("стін\u00ADку")
                self.assertEqual(["стін\u00ADку"], testList)

                testList = w.tokenize("стін\u00AD\nку")
                self.assertEqual(["стін\u00AD\nку"], testList)

                testList = w.tokenize("п\"яний")
                self.assertEqual(["п'яний"], testList)
                
        def testAbbreviations(self):
                w = UkrainianWordTokenizer()

                testList = w.tokenize("Засідав І.Єрмолюк.")
                #self.assertEqual(["Засідав", " ", "І.", "Єрмолюк", "."], testList)

                testList = w.tokenize("Засідав І. П. Єрмолюк.")
                self.assertEqual(["Засідав", " ", "І.", " ", "П.", " ", "Єрмолюк", "."], testList)

                testList = w.tokenize("Засідав І.П.Єрмолюк.")
                self.assertEqual(["Засідав", " ", "І.", "П.", "Єрмолюк", "."], testList)

                testList = w.tokenize("І.\u00A0Єрмолюк.")
                self.assertEqual(["І.", "\u00A0", "Єрмолюк", "."], testList)

                #скорочення
                
                testList = w.tokenize("140 тис. працівників")
                self.assertEqual(["140", " ", "тис.", " ", "працівників"], testList)

                testList = w.tokenize("450 тис. 297 грн")
                self.assertEqual(["450", " ", "тис.", " ", "297", " ", "грн"], testList)

                testList = w.tokenize("450 тис.")
                self.assertEqual(["450", " ", "тис."], testList)

                testList = w.tokenize("354\u202Fтис.")
                self.assertEqual(["354", "\u202F", "тис."], testList)

                testList = w.tokenize("911 тис.грн. з бюджету")
                self.assertEqual(["911", " ", "тис.", "грн", ".", " ", "з", " ", "бюджету"], testList)

                testList = w.tokenize("за $400\n  тис., здавалося б")
                self.assertEqual(["за", " ", "$400", "\n", " ", " ", "тис.", ",", " ", "здавалося", " ", "б"], testList)


                testList = w.tokenize("проф. Артюхов")
                self.assertEqual(["проф.", " ", "Артюхов"], testList)

                testList = w.tokenize("проф.\u00A0Артюхов")
                self.assertEqual(["проф.", "\u00A0", "Артюхов"], testList)

                testList = w.tokenize("також зав. відділом")
                self.assertEqual(["також", " ", "зав.", " ", "відділом"], testList)

                testList = w.tokenize("до н. е.")
                self.assertEqual(["до", " ", "н.", " ", "е."], testList)
                
                testList = w.tokenize("до н.е.")
                self.assertEqual(["до", " ", "н.", "е."], testList)

                testList = w.tokenize("1998 р.н.")
                self.assertEqual(["1998", " ", "р.", "н."], testList)

                testList = w.tokenize("22 коп.")
                self.assertEqual(["22", " ", "коп."], testList)

                testList = w.tokenize("18-19 ст.ст. були")
                self.assertEqual(["18-19", " ", "ст.", "ст.", " ", "були"], testList)
                
                testList = w.tokenize("І ст. 11")
                self.assertEqual(["І", " ", "ст.", " ", "11"], testList)

                testList = w.tokenize("куб. м")
                self.assertEqual(["куб.", " ", "м"], testList)

                testList = w.tokenize("куб.м")
                self.assertEqual(["куб.", "м"], testList)

                testList = w.tokenize("У с. Вижва")
                self.assertEqual(["У", " ", "с.", " ", "Вижва"], testList)

                testList = w.tokenize("Довжиною 30 см. з гаком.")
                self.assertEqual(["Довжиною", " ", "30", " ", "см", ".", " ", "з", " ", "гаком", "."], testList)

                testList = w.tokenize("Довжиною 30 см. Поїхали.")
                self.assertEqual(["Довжиною", " ", "30", " ", "см", ".", " ", "Поїхали", "."], testList)

                testList = w.tokenize("100 м. дороги.")
                self.assertEqual(["100", " ", "м", ".", " ", "дороги", "."], testList)

                testList = w.tokenize("На висоті 4000 м...")
                self.assertEqual(["На", " ", "висоті", " ", "4000", " ", "м", "..."], testList)

                testList = w.tokenize("№47 (м. Слов'янськ)")
                self.assertEqual(["№47", " ", "(", "м.", " ", "Слов'янськ", ")"], testList)

                testList = w.tokenize("с.-г.")
                self.assertEqual(["с.-г."], testList)

                testList = w.tokenize("100 грн. в банк")
                self.assertEqual(["100", " ", "грн", ".", " ", "в", " ", "банк"], testList)
                
                testList = w.tokenize("таке та ін.")
                self.assertEqual(["таке", " ", "та", " ", "ін."], testList)

                testList = w.tokenize("і т. ін.")
                self.assertEqual(["і", " ", "т.", " ", "ін."], testList)

                testList = w.tokenize("Інститут ім. акад. Вернадського.")
                self.assertEqual(["Інститут", " ", "ім.", " ", "акад.", " ", "Вернадського", "."], testList)

                testList = w.tokenize("Палац ім. гетьмана Скоропадського.")
                self.assertEqual(["Палац", " ", "ім.", " ", "гетьмана", " ", "Скоропадського", "."], testList)

                testList = w.tokenize("від лат. momento")
                self.assertEqual(["від", " ", "лат.", " ", "momento"], testList)

                testList = w.tokenize("на 1-кімн. кв. в центрі")
                self.assertEqual(["на", " " , "1-кімн.", " ", "кв.", " ", "в", " ", "центрі"], testList)
                
                testList = w.tokenize("Валерій (міліціонер-пародист.\n–  Авт.) стане пародистом.")
                self.assertEqual(["Валерій", " ", "(", "міліціонер-пародист", ".", "\n", "–", " ", " ", "Авт.", ")", " ", "стане", " ", "пародистом", "."], testList)

                testList = w.tokenize("Сьогодні (у четвер.  — Ред.), вранці.")
                self.assertEqual(["Сьогодні", " ", "(", "у", " ", "четвер", ".", " ", " ", "—", " ", "Ред.", ")", ",", " ", "вранці", "."], testList)
                
                testList = w.tokenize("Fair trade [«Справедлива торгівля». –    Авт.], який стежить за тим, щоб у країнах")
                self.assertTrue("Авт." in testList)
                
                testList = w.tokenize("диво з див.")
                self.assertEqual(["диво", " ", "з", " ", "див", "."], testList)
                
                testList = w.tokenize("диво з див...")
                self.assertEqual(["диво", " ", "з", " ", "див", "..."], testList)

                testList = w.tokenize("тел.: 044-425-20-63")
                self.assertEqual(["тел.", ":", " ", "044-425-20-63"], testList)

if __name__ == '__main__':
        unittest.main()
