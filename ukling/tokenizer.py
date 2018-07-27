"""
Thanks to Andriy Rysin and the LanguageTool Java library team
"""

import regex
from typing import List

class UkrainianWordTokenizer:
        SPLIT_CHARS = ("\u0020\u00A0"
                       "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007" 
                       "\u2008\u2009\u200A\u200B\u200c\u200d\u200e\u200f"
                       "\u201A\u2028\u2029\u202a\u202b\u202c\u202d\u202e\u202f"
                       "\u205F\u2060\u2061\u2062\u2063\u206A\u206b\u206c\u206d"
                       "\u206E\u206F\u3000\u3164\ufeff\uffa0\ufff9\ufffa\ufffb" 
                       ",.;()[]{}<>!?:/|\\\"«»„”“…¿¡=\t\n\r\uE100\uE101\uE102\uE110")

        SPLIT_REGEX_STR = "([{0}])".format(regex.escape(SPLIT_CHARS))
        SPLIT_REGEX = regex.compile(SPLIT_REGEX_STR)
        
        #for handling exceptions
        DECIMAL_COMMA_SUBST = '\uE001' #some unused character to hide comma in decimal number temporary for tokenizer run
        NON_BREAKING_SPACE_SUBST = '\uE002'
        NON_BREAKING_DOT_SUBST = '\uE003' #some unused character to hide dot in date temporary for tokenizer run
        NON_BREAKING_COLON_SUBST = '\uE004'

        WEIRD_APOSTROPH_PATTERN = regex.compile("([бвджзклмнпрстфхш])[\"\u201D\u201F]([єїюя])", regex.IGNORECASE|regex.UNICODE)

        #decimal comma between digits
        DECIMAL_COMMA_PATTERN = regex.compile("([\\d]),([\\d])", regex.IGNORECASE|regex.UNICODE)
        DECIMAL_COMMA_REPL = r"\1" + DECIMAL_COMMA_SUBST + r"\2"

        #space between digits
        DECIMAL_SPACE_PATTERN = regex.compile("(?<=^|[\\s(])\\d{1,3}( [\\d]{3})+(?=[\\s(]|$)", regex.IGNORECASE|regex.UNICODE)


        #dots in numbers
        DOTTED_NUMBERS_PATTERN = regex.compile("([\\d])\\.([\\d])", regex.IGNORECASE|regex.UNICODE)
        DOTTED_NUMBERS_REPL = r"\1" + NON_BREAKING_DOT_SUBST + r"\2"
  
        #colon in numbers
        COLON_NUMBERS_PATTERN = regex.compile("([\\d]):([\\d])", regex.IGNORECASE|regex.UNICODE)
        COLON_NUMBERS_REPL = r"\1" + NON_BREAKING_COLON_SUBST + r"\2"

        #dates
        DATE_PATTERN = regex.compile("([\\d]{2})\\.([\\d]{2})\\.([\\d]{4})|([\\d]{4})\\.([\\d]{2})\\.([\\d]{2})|([\\d]{4})-([\\d]{2})-([\\d]{2})", regex.IGNORECASE|regex.UNICODE)
        DATE_PATTERN_REPL = r"\1" + NON_BREAKING_DOT_SUBST + r"\2" + NON_BREAKING_DOT_SUBST + r"\3"

        # braces in words
        BRACE_IN_WORD_PATTERN = regex.compile("([а-яіїєґ'])\\(([а-яіїєґ']+)\\)", regex.IGNORECASE|regex.UNICODE)
        LEFT_BRACE_SUBST = '\uE005'
        RIGHT_BRACE_SUBST = '\uE006'
        BREAKING_PLACEHOLDER = "\uE110"

        # abbreviation dot
        # TODO: л.с., ч.л./ч. л., ст. л., р. х.
        ABBR_DOT_TYS_PATTERN1 = regex.compile("([0-9IІ][\\s\u00A0\u202F]+)(тис)\\.")
        ABBR_DOT_TYS_PATTERN2 = regex.compile("(тис)\\.([\\s\u00A0\u202F]+[а-яіїєґ0-9])")
        ABBR_DOT_LAT_PATTERN = regex.compile("([^а-яіїєґА-ЯІЇЄҐ'-]лат)\\.([\\s\u00A0\u202F]+[a-zA-Z])")
        ABBR_DOT_PROF_PATTERN = regex.compile("([Аа]кад|[Пп]роф|[Дд]оц|[Аа]сист|вул|о|р|ім)\\.([\\s\u00A0\u202F]+[А-ЯІЇЄҐ])")

        #tokenize initials with dot, e.g. "А.", "Ковальчук"
        INITIALS_DOT_PATTERN_SP_2 = regex.compile("([А-ЯІЇЄҐ])\\.([\\s\u00A0\u202F][А-ЯІЇЄҐ])\\.([\\s\u00A0\u202F][А-ЯІЇЄҐ][а-яіїєґ']+)")
        INITIALS_DOT_REPL_SP_2 = r"\1" + NON_BREAKING_DOT_SUBST + r"\2" + NON_BREAKING_DOT_SUBST + r"\3"
        INITIALS_DOT_PATTERN_SP_1 = regex.compile("([А-ЯІЇЄҐ])\\.([\\s\u00A0\u202F][А-ЯІЇЄҐ][а-яіїєґ']+)")
        INITIALS_DOT_REPL_SP_1 = r"\1" + regex.escape(NON_BREAKING_DOT_SUBST) + r"\2"
        INITIALS_DOT_PATTERN_NSP_2 = regex.compile("([А-ЯІЇЄҐ])\\.([А-ЯІЇЄҐ])\\.([А-ЯІЇЄҐ][а-яіїєґ']+)")
        INITIALS_DOT_REPL_NSP_2 = r"\1" + regex.escape(NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER) + r"\2" + NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER + r"\3"
        INITIALS_DOT_PATTERN_NSP_1 = regex.compile("([А-ЯІЇЄҐ])\\.([А-ЯІЇЄҐ][а-яіїєґ']+)")
        INITIALS_DOT_REPL_NSP_1 = r"\1" + regex.escape(NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER) + r"\2"

        # село, місто, річка (якщо з цифрою: секунди, метри, роки) - з роками складно
        # ABBR_DOT_INVALID_DOT_PATTERN = regex.compile("((?:[0-9]|кв\\.|куб\\.)[\\s\u00A0\u202F]+(?:[смкд]|мк)?м)\\.(.)")
        ABBR_DOT_KUB_SM_PATTERN = regex.compile("(кв|куб)\\.([\\s\u00A0\u202F]*(?:[смкд]|мк)?м)")
        ABBR_DOT_S_G_PATTERN = regex.compile("(с)\\.(-г)\\.")
        ABBR_DOT_2_SMALL_LETTERS_PATTERN = regex.compile("([^а-яіїєґ'-][векнпрстцч]{1,2})\\.([екмнпрстч]{1,2})\\.")
        ABBR_DOT_2_SMALL_LETTERS_REPL = r"\1" + NON_BREAKING_DOT_SUBST + BREAKING_PLACEHOLDER + r"\2" + NON_BREAKING_DOT_SUBST

        # скорочення що не можуть бути в кінці речення
        ABBR_DOT_NON_ENDING_PATTERN = regex.compile("(?<![а-яіїєґА-ЯІЇЄҐ'-])(абз|амер|англ|акад(ем)?|арк|бл(?:изьк)?|буд|вип|вірм|грец(?:ьк)|див|дод|дол|досл|доц|доп|ел|жін|зав|заст|зб|зв|ім|івр|ісп|італ"
        + "|к|каф|канд|кв|[1-9]-кімн|кімн|кл|н|напр|п|пен|перекл|пл|пор|поч|прибл|пров|просп|[Рр]ед|[Рр]еж|рт|с|[Сс]в|соц|співавт|стор|табл|[тТ]ел|укр|філол|фр|франц|ч|чайн|ц)\\.(?!$)")
        ABBR_DOT_NON_ENDING_PATTERN_2 = regex.compile("([^а-яіїєґА-ЯІЇЄҐ'-]м)\\.([\\s\u00A0\u202F]*[А-ЯІЇЄҐ])")
        # скорочення що можуть бути в кінці речення
        ABBR_DOT_ENDING_PATTERN = regex.compile("([^а-яіїєґА-ЯІЇЄҐ'-]((та|й) ін|е|коп|обл|р|рр|руб|ст|стол|стор|чол|шт))\\.")
        ABBR_DOT_I_T_P_PATTERN = regex.compile("([ій][\\s\u00A0\u202F]+т)\\.([\\s\u00A0\u202F]*(д|п|ін))\\.")

        # Сьогодні (у четвер. - Ред.), вранці.
        #ABBR_DOT_PATTERN8 = regex.compile("([\\s\u00A0\u202F]+[–—-][\\s\u00A0\u202F]+(?:[Рр]ед|[Аа]вт))\\.([\\)\\]])")
        ABBR_DOT_RED_AVT_PATTERN = regex.compile("([\\s\u00A0\u202F]+(?:[Рр]ед|[Аа]вт))\\.([\\)\\]])")
        
        # ellipsis
        ELLIPSIS = "..."
        ELLIPSIS_SUBST = "\uE100"
        ELLIPSIS2 = "!.."
        ELLIPSIS2_SUBST = "\uE101"
        ELLIPSIS3 = "?.."
        ELLIPSIS3_SUBST = "\uE102"
        SOFT_HYPHEN_WRAP = "\u00AD\n"
        SOFT_HYPHEN_WRAP_SUBST = "\uE103"
        # url
        URL_PATTERN = regex.compile("^(https?|ftp)://[^\\s/$.?#].[^\\s]*$", regex.IGNORECASE)
        URL_START_REPLACE_CHAR = 0xE300

        def tokenize(self, text: str) -> List[str]:
                urls = {}
                text = self.cleanup(text)
                if ',' in text:
                        text = self.DECIMAL_COMMA_PATTERN.sub(self.DECIMAL_COMMA_REPL, text)

                # check for urls
                if 'tp' in text: #https?|ftp
                        matcher = self.URL_PATTERN.finditer(text)
                        urlReplaceChar = self.URL_START_REPLACE_CHAR
                        for m in matcher:
                                urlGroup = m.group(0)
                                replaceChar = chr(urlReplaceChar)
                                urls[replaceChar] = urlGroup
                                text = text[:m.start()] + replaceChar + text[m.end() + 1:]
                                #text = matcher.replaceAll(replaceChar) #rework this
                                urlReplaceChar += 1
                
                #if period is not the last character in the sentence
                dotIndex = text.find(".")
                dotInsideSentence = dotIndex >= 0 and dotIndex < len(text)-1
                if dotInsideSentence or (dotIndex == len(text)-1 and text.endswith("тис.")):
                        if self.ELLIPSIS in text:
                                text = text.replace(self.ELLIPSIS, self.ELLIPSIS_SUBST)
                        if self.ELLIPSIS2 in text:
                                text = text.replace(self.ELLIPSIS2, self.ELLIPSIS2_SUBST)
                        if self.ELLIPSIS3 in text:
                                text = text.replace(self.ELLIPSIS3, self.ELLIPSIS3_SUBST)
                
                        text = self.DATE_PATTERN.sub(self.DATE_PATTERN_REPL, text)
                        text = self.DOTTED_NUMBERS_PATTERN.sub(self.DOTTED_NUMBERS_REPL, text)
                        
                        text = self.ABBR_DOT_2_SMALL_LETTERS_PATTERN.sub(self.ABBR_DOT_2_SMALL_LETTERS_REPL, text)
                        text = self.ABBR_DOT_TYS_PATTERN1.sub(r"\1\2" + self.NON_BREAKING_DOT_SUBST + self.BREAKING_PLACEHOLDER, text)
                        text = self.ABBR_DOT_TYS_PATTERN2.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2", text)
                        text = self.ABBR_DOT_LAT_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2", text)
                        text = self.ABBR_DOT_PROF_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2", text)
                        
                        text = self.INITIALS_DOT_PATTERN_SP_2.sub(self.INITIALS_DOT_REPL_SP_2, text)
                        text = self.INITIALS_DOT_PATTERN_SP_1.sub(self.INITIALS_DOT_REPL_SP_1, text)
                        text = self.INITIALS_DOT_PATTERN_NSP_2.sub(self.INITIALS_DOT_REPL_NSP_2, text)
                        text = self.INITIALS_DOT_PATTERN_NSP_1.sub(self.INITIALS_DOT_REPL_NSP_1, text)
                        
                        #text = self.ABBR_DOT_INVALID_DOT_PATTERN.sub("\1" + self.NON_BREAKING_DOT_SUBST + r"\2", text)
                        text = self.ABBR_DOT_KUB_SM_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + self.BREAKING_PLACEHOLDER + r"\2", text)
                        text = self.ABBR_DOT_S_G_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2" + self.NON_BREAKING_DOT_SUBST, text)
                        text = self.ABBR_DOT_I_T_P_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2" + self.NON_BREAKING_DOT_SUBST, text)
                        text = self.ABBR_DOT_RED_AVT_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2", text)
                        text = self.ABBR_DOT_NON_ENDING_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST, text)
                        text = self.ABBR_DOT_NON_ENDING_PATTERN_2.sub(r"\1" + self.NON_BREAKING_DOT_SUBST + r"\2", text)

                text = self.ABBR_DOT_ENDING_PATTERN.sub(r"\1" + self.NON_BREAKING_DOT_SUBST, text)

                # 2 000 000
                matcher = self.DECIMAL_SPACE_PATTERN.finditer(text)
                for m in matcher:
                        split_number = m.group(0)
                        split_number = split_number.replace(' ', self.NON_BREAKING_SPACE_SUBST)
                        split_number = split_number.replace('\u00A0', self.NON_BREAKING_SPACE_SUBST)
                        split_number = split_number.replace('\u202F', self.NON_BREAKING_SPACE_SUBST)
                        text = text[:m.start()] + split_number + text[m.end():]

                #12:25
                if ":" in text:
                        text = self.COLON_NUMBERS_PATTERN.sub(self.COLON_NUMBERS_REPL, text)
                if "(" in text:
                        text = self.BRACE_IN_WORD_PATTERN.sub(r"\1" + self.LEFT_BRACE_SUBST + r"\2" + self.RIGHT_BRACE_SUBST, text)
                if self.SOFT_HYPHEN_WRAP in text:
                        text = text.replace(self.SOFT_HYPHEN_WRAP, self.SOFT_HYPHEN_WRAP_SUBST)
    
                tokens = []
                split_text = self.SPLIT_REGEX.split(text)
                for token in split_text:
                        if token == self.BREAKING_PLACEHOLDER:
                                continue
                        
                        token = token.replace(self.DECIMAL_COMMA_SUBST, ',')
                        token = token.replace(self.NON_BREAKING_COLON_SUBST, ':')
                        token = token.replace(self.NON_BREAKING_SPACE_SUBST, ' ')
                        token = token.replace(self.LEFT_BRACE_SUBST, '(')
                        token = token.replace(self.RIGHT_BRACE_SUBST, ')')

                        #outside of if as we also replace back sentence-ending abbreviations
                        token = token.replace(self.NON_BREAKING_DOT_SUBST, '.')

                        if dotInsideSentence:
                                token = token.replace(self.ELLIPSIS_SUBST, self.ELLIPSIS)
                                token = token.replace(self.ELLIPSIS2_SUBST, self.ELLIPSIS2)
                                token = token.replace(self.ELLIPSIS3_SUBST, self.ELLIPSIS3)

                        token = token.replace(self.SOFT_HYPHEN_WRAP_SUBST, self.SOFT_HYPHEN_WRAP)

                        if len(urls) != 0:
                                for code, url in urls.items():
                                        token = token.replace(code, url)
                        if len(token) > 0:
                                tokens.append(token)
                return tokens

        def cleanup(self, text: str) -> str:
                text = text.replace('\u2019', '\'') \
                           .replace('\u02BC', '\'') \
                           .replace('\u2018', '\'') \
                           .replace('`', '\'') \
                           .replace('´',  '\'') \
                           .replace('\u201A', ',') \
                           .replace('\u2011', '-')

                text = self.WEIRD_APOSTROPH_PATTERN.sub(r"\1'\2", text)
                return text