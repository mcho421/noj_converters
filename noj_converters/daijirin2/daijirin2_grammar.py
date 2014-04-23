#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from StringIO import StringIO
import re
from textwrap import dedent
from pyparsing import *
from noj_converters.misc.uni_printer import UniPrinter

pp = UniPrinter(indent=4)

# Notes from Super Daijirin legend #####################################
# 《1. Headword》
# 1. Headwords are in accordance to the modern kana usage. 
# 2. Native/Sino Japanese words and foreign words are shown in hiragana
#    and katakana respectively.
# 3. The ｢-｣ inside the headword shows the delimitation in terms of word
#    composition.
# 4. The ｢･｣ inside the headword delimits the stem of the general use 
#    word from the word ending.
# ｢∘｣ shows a conjugated word that cannot be separated into a stem and
# a word ending.
#
# 《2. Historical kana usage》
# In the case where the historical kana usage differs from the headword,
# after the headword the parts that differ are written in katakana small
# text. Parts that remain the same are abbreviated by the - symbol.
#
# 《3. Accent》
# For the contemporary language headword, inside the [ ] shows the 
# accent in standard language. See "Accent" for more information.
#
# 《4. Surface form》
# 1. Inside【 】shows the standard written form method.
# 2. Okurigana is shown based on the official government rules for 
#    affixing okurigana. Archaic words were by the historical kana 
#    usage.
# 3. Concerning foreign words, the spelling is shown inside the 〖  〗. 
#    Greek, Sanskrit etc. are re-spelled romaji.
#
# 《5. Part of speech / Conjugations》
# 1. The variety of part of speech / conjugations is abbreviated in the 
#    ( ). However, the part of speech indicator for nouns is omitted. 
#    -> See "Abbreviation list"
# 2. For verbs the conjugation line is shown.
# 3. For main auxiliary verbs the conjugations are shown.
# 4. スル indicates the word can be conjugated as a nominal verb
#
# 《6. Literary form》
# Differences between the usage of a word in spoken and written forms is
# handled as follows: The literary form and type of use is indicated by 
# [文] after the spoken form of the headword.
#
# 《7. Commentary》
# 1. First the modern language meaning and usage, and then the archaic 
#    meaning and direction for use is described.
# 2. Regarding terminology, the appropriate field is shown in the 
#    〔 〕. See "Abbreviation list".
# 3. If the case when the complete commentary appears under another 
#    heading, the referenced item is shown by a ⇒.
#
# 《8. Examples》
# 1. Examples are enclosed in ｢ ｣ after the word interpretation.
# 2. In side the example, portions that correspond with the headword are
#    abbreviated with a ―. In conjugated words, the stem is abbreviated 
#    as ―・. Words that cannot be separated into a stem and word ending 
#    are not abbreviated.
# 3. Source name, author name are shown using the appropriate 
#    abbreviations. See "Source abbreviation list".


# Entry header grammar #################################################

# Parse actions
def kanji_split(t):
    return ParseResults(t[0].split(u'・'))

# Helpers
KATAKANA_WORD = Regex(ur'[ァ-ン―・]+')
ACCENT_BOX = Suppress(u"[") + Word(nums) + Suppress(u"]")
KANJI_FORM = Suppress(u"【") + SkipTo(u"】") + Suppress(u"】")
KANJI_FORM.setParseAction(kanji_split)
ROMAJI_FORM = Suppress(u"〖") + SkipTo(u"〗") + Suppress(u"〗")
# TODO: split romaji
PART_OF_SPEECH = nestedExpr(u"（", u"）")
CONJUGATION = nestedExpr(u"(", u")")

# Entry header components
HEADWORD = Suppress(u"<HEAD>") + SkipTo(u"</HEAD>") + Suppress(u"</HEAD>")
HISTORICAL_KANA_USAGE = KATAKANA_WORD
ACCENT = Group(ACCENT_BOX + ZeroOrMore(Optional('-') + ACCENT_BOX))
SURFACE_FORM = Group(KANJI_FORM('kanji') | ROMAJI_FORM('romaji'))
PART_OF_SPEECH_AND_CONJUGATION = PART_OF_SPEECH('pos') + Optional(CONJUGATION('conj')) | CONJUGATION('conj')
SURU = Literal(u'スル') + Optional(Suppress(" "))
LITERARY_FORM = Suppress(u"[文]") + SkipTo(lineEnd)

# Entry header subgrammar alternate forms
ENTRY_HEADER_SUBGRAMMAR_1 = Optional(Suppress(u" ") + HISTORICAL_KANA_USAGE('hist')) + \
                            Optional(Suppress(u" ") + ACCENT('acc')) + \
                            Optional(Suppress(u" ") + SURFACE_FORM('surf'))

ENTRY_HEADER_SUBGRAMMAR_2 = Optional(Suppress(u" ") + ACCENT('acc')) + \
                            Suppress(u" ") + Group(delimitedList(
                                Group(HISTORICAL_KANA_USAGE + \
                                Suppress(u" ") +  SURFACE_FORM), u" ・ "
                            ))('hist_surf_list')

ENTRY_HEADER_SUFFIX = HEADWORD('kana') + \
               (ENTRY_HEADER_SUBGRAMMAR_1('g1') ^ ENTRY_HEADER_SUBGRAMMAR_2('g2')) + \
               Optional(Suppress(u" ") + PART_OF_SPEECH_AND_CONJUGATION) + \
               Optional(SURU('suru')) + \
               Optional(LITERARY_FORM('lit'))

# Entry header
ENTRY_HEADER = Suppress(u"<INDENT=1><PAGE>") + ENTRY_HEADER_SUFFIX
ENTRY_HEADER.leaveWhitespace()

ENTRY_HEADER_FIRST = Suppress(u"<INDENT=1>") + ENTRY_HEADER_SUFFIX
ENTRY_HEADER_FIRST.leaveWhitespace()

# Entry body grammar ###################################################
# First parsed by higher order grammar, then the definition blocks are
# escaped, then split into subdefinitions.

def example_remove_source(t):
    tsplit = t[0].split(u'/')
    return tsplit[0]

def subdefinition_to_number(t):
    return (ord(t[0]) - ord(u"ア"))//2 + 1

def escape_subdefinition(t):
    return ESCAPE_SUBDEFINITION.transformString(t[0])

def unescape_subdefinition(t):
    return ParseResults(t[0].replace(u"<REF>", u""))

def definition_block_split_subdefinition(t):
    e = ESCAPE_EMBEDDED_SUBDEFINITIONS.transformString(t[0])
    d = (SUBDEFINITION_BLOCK + stringEnd).parseString(e)
    return d

def subdefinition_block_parse(t):
    result_dict = dict()
    result_dict['head'] =  extract_examples(t.head)
    if t.body:
        body_list = list()
        for num, text in t.body:
            body_element = dict()
            body_element['def_num'] = num
            body_element['extract'] = extract_examples(text)
            body_list.append(body_element)

        result_dict['body'] = body_list
    return ParseResults(result_dict)

def extract_examples(text):
    text = text.rstrip()
    text = text.replace(u"<REF>", u"")
    parts = list()
    ex_list = list()
    lo = 0
    for exs in EXAMPLES.scanString(text):
        hi = exs[1]
        parts.append(text[lo:hi])
        parts.append(u"<EXS>")
        lo = exs[2]
        for e in exs[0][0]:
            ex_list.append(e)
    parts.append(text[lo:len(text)])
    text_edited = u''.join(parts)
    return (text_edited, ex_list)

def def_multi_grouping_header_def_text_split_examples(t):
    return ParseResults(extract_examples(t[0]))

# Escape embedded subdefinition references
ESCAPE_QUOTE = Suppress(u"「") + SkipTo(u"」") + Suppress(u"」")
ESCAPE_QUOTE.setParseAction(lambda t : u"「" + escape_subdefinition(t) + u"」")
ESCAPE_LINK = Suppress(u"<LINK>") + SkipTo(lineEnd)
ESCAPE_LINK.setParseAction(lambda t : u"<LINK>" + escape_subdefinition(t))
ESCAPE_TERMINOLOGY = Suppress(u"〔") + SkipTo(u"〕") + Suppress(u"〕")
ESCAPE_TERMINOLOGY.setParseAction(lambda t : u"〔" + escape_subdefinition(t) + u"〕")
ESCAPE_FIG = Suppress(u"<FIG>") + SkipTo(lineEnd)
ESCAPE_FIG.setParseAction(lambda t : u"<FIG>" + escape_subdefinition(t))
ESCAPE_SUBDEFINITION = Suppress(u"（") + Regex(ur'[ア-シ]') + Suppress(u"）")
ESCAPE_SUBDEFINITION.setParseAction(lambda t : u"（<REF>" + t[0] + u"）")
ESCAPE_EMBEDDED_SUBDEFINITIONS = ESCAPE_LINK | ESCAPE_QUOTE | ESCAPE_TERMINOLOGY | ESCAPE_FIG

# Parse definitions into subdefinitions and lower
EXAMPLE_SD = Suppress(u"「") + SkipTo(u"」") + Suppress(u"」")
EXAMPLE_SD.setParseAction(example_remove_source)
EXAMPLES = Group(ZeroOrMore(EXAMPLE_SD) + FollowedBy(lineEnd))
SUBDEFINITION_SD = Suppress(u"（") + Regex(ur'[ア-シ]') + Suppress(u"）")
SUBDEFINITION_SD.setParseAction(subdefinition_to_number)
DEFINITION_LEAF = SkipTo(EXAMPLES)
DEFINITION_LEAF.setParseAction(unescape_subdefinition)
DEFINITION_N_EXAMPLE = Group(DEFINITION_LEAF('definition') + EXAMPLES('examples'))
EXTRACT_EXAMPLES = OneOrMore(DEFINITION_N_EXAMPLE)

SUBDEFINITION_BLOCK = SkipTo(SUBDEFINITION_SD | stringEnd)('head') + \
                      ZeroOrMore(Group(SUBDEFINITION_SD + SkipTo(SUBDEFINITION_SD | stringEnd)))('body')
SUBDEFINITION_BLOCK.setParseAction(subdefinition_block_parse)

# Entry body higher level grammar
WIDE_TRAD_NUMBER_INT_MAP = {u"一":1, u"二":2, u"三":3, u"四":4, u"五":5, 
                            u"六":6, u"七":7, u"八":8, u"九":9, u"〇":0}
BILLARD_BALL_INT_MAP = {u"❶":1, u"❷":2, u"❸":3, u"❹":4, u"❺":5, u"❻":6, 
                        u"❼":7, u"❽":8, u"❾":9, u"❿":10, u"⓫":11, 
                        u"⓬":12, u"⓭":13, u"⓮":14, u"⓯":15, u"⓰":16, 
                        u"⓱":17, u"⓲":18, u"⓳":19}

WIDE_NUMBER = Word(u'０１２３４５６７８９')
WIDE_TRAD_NUMBER = Word(u'一二三四五六七八九〇')
WIDE_TRAD_NUMBER.setParseAction(lambda t : WIDE_TRAD_NUMBER_INT_MAP[t[0]])
DEFINITION_NUMBER = Suppress(u"（") + WIDE_NUMBER + Suppress(u"）")
DEFINITION_NUMBER.setParseAction(lambda t : int(t[0]))
TERMINOLOGY = Suppress(u"〔") + SkipTo(u"〕") + Suppress(u"〕")
EXAMPLE = Suppress(u"「") + SkipTo(u"」") + Suppress(u"」")
LINK = Suppress(u"<LINK>") + SkipTo(u"</LINK[") + Suppress(u"</LINK[") + Suppress(SkipTo(u"]>")) + Suppress("]>")
DEFINITION_LINE = NotAny(Literal(u"<") | Literal(u"〔") | DEFINITION_NUMBER) + SkipTo(lineEnd)
FIGURE = Suppress(u"<FIG>") + SkipTo(u"</FIG>") + Suppress(u"</FIG>") + Suppress(SkipTo(lineEnd))
WAV = Suppress(u"<WAV>") + SkipTo(u"</WAV>") + Suppress(u"</WAV>")
CONJUGATION = Suppress(u"[") + SkipTo(u"]") + Suppress(u"]") + SkipTo(lineEnd)
BILLARD_BALL = oneOf(u"❶ ❷ ❸ ❹ ❺ ❻ ❼ ❽ ❾ ❿ ⓫ ⓬ ⓭ ⓮ ⓯ ⓰ ⓱ ⓲ ⓳")
BILLARD_BALL.setParseAction(lambda t : BILLARD_BALL_INT_MAP[t[0]])
ROUND_BRACKET_LINE = Suppress(u"（") + SkipTo(u"）") + Suppress(u"）") + Optional(Literal(u"スル"))
DATE = Suppress(u"(") + Word(u'1234567890-?　頃') + Suppress(u")")
EQUIVALENCE = Suppress(u"⇔") + SkipTo(lineEnd)
SOURCE = Suppress(u"［") + SkipTo(u"］") + Suppress(u"］")
ALTERNATIVES = Suppress(u"《") + SkipTo(u"》") + Suppress(u"》")
SUBDEFINITION = Suppress(u"（") + Regex(ur'[ア-シ]') + Suppress(u"）")

SUBENTRY_HEADER_1 = Suppress(u"■") + WIDE_TRAD_NUMBER('def_num') + Suppress(u"■") + SkipTo(lineEnd)('def_text')
SUBENTRY_HEADER_2 = Suppress(u"□") + WIDE_TRAD_NUMBER('def_num') + Suppress(u"□") + SkipTo(lineEnd)('def_text')

DEFINITION_BLOCK = SkipTo((FollowedBy(lineStart) + DEFINITION_NUMBER) | \
                          (FollowedBy(lineStart) + BILLARD_BALL) | \
                          (FollowedBy(lineStart) + (SUBENTRY_HEADER_1 | SUBENTRY_HEADER_2)) | \
                          FIGURE | WAV | \
                          stringEnd)
DEFINITION_BLOCK.setParseAction(definition_block_split_subdefinition)

SINGLE_DEF = Group(DEFINITION_BLOCK('def_text'))
MULTI_DEF = Group(OneOrMore(Group(DEFINITION_NUMBER('def_num') + DEFINITION_BLOCK('def_text')))('defs') | \
                  SkipTo(FollowedBy(lineStart) + DEFINITION_NUMBER)('pre_def') + OneOrMore(Group(DEFINITION_NUMBER('def_num') + DEFINITION_BLOCK('def_text')))('defs'))

NO_SUBENTRY_GROUP = Group(MULTI_DEF('multi_def') | SINGLE_DEF('sgl_def'))
DEF_MULTI_GROUPING_HEADER_DEF_TEXT = SkipTo(lineEnd)('def_text')
DEF_MULTI_GROUPING_HEADER_DEF_TEXT.setParseAction(def_multi_grouping_header_def_text_split_examples)
DEF_MULTI_GROUPING_HEADER = BILLARD_BALL('def_num') + DEF_MULTI_GROUPING_HEADER_DEF_TEXT
DEF_MULTI_GROUPING = OneOrMore(Group(DEF_MULTI_GROUPING_HEADER + Suppress(lineEnd) + (FollowedBy(BILLARD_BALL) | NO_SUBENTRY_GROUP('nsg'))))

MEANING_SUBENTRY_GROUP = Group(DEF_MULTI_GROUPING('subentries') | \
                               SkipTo(FollowedBy(lineStart) + BILLARD_BALL)('pre_def') + \
                               DEF_MULTI_GROUPING('subentries'))

SUBENTRY_BLOCK = Group((SUBENTRY_HEADER_1 | SUBENTRY_HEADER_2) + \
                       ZeroOrMore(TERMINOLOGY + Suppress(lineEnd))('terms') + \
                       (MEANING_SUBENTRY_GROUP('msg') | NO_SUBENTRY_GROUP('nsg')))

GRAMMAR_SUBENTRY_GROUP = Group(OneOrMore(SUBENTRY_BLOCK)('subentries') | \
                               SkipTo(FollowedBy(lineStart) + (SUBENTRY_HEADER_1 | SUBENTRY_HEADER_2))('pre_def') + \
                               OneOrMore(SUBENTRY_BLOCK)('subentries'))

ENTRY_BODY = Suppress(u"<INDENT=4>") + \
             (GRAMMAR_SUBENTRY_GROUP('gsg') | MEANING_SUBENTRY_GROUP('msg') | NO_SUBENTRY_GROUP('nsg')) + \
             ZeroOrMore(FIGURE) + \
             ZeroOrMore(WAV)

# Full entry block grammar #############################################

ENTRY_BLOCK = ENTRY_HEADER + Suppress(lineEnd) + \
              ENTRY_BODY('body')

ENTRY_HEADER_MATCHER = re.compile(ur'<INDENT=1>')

def main():
    i = 0
    errs = 0
    ef = open('errors.txt', 'wb')
    with codecs.open('../dumpers/daijirindump.txt', 'r', 'utf-8') as f:
        entry_buffer = list()
        in_metadata = True
        for line in f:
            i += 1
            if i % 1000 == 0:
                print i
            # print i, line.rstrip()

            is_entry_header = ENTRY_HEADER_MATCHER.match(line)
            if is_entry_header:
                if in_metadata:
                    in_metadata = False
                else:
                    entry_lines = ''.join(entry_buffer)
                    
                    try:
                        d = (ENTRY_BLOCK + stringEnd).parseString(entry_lines).dump()
                    except ParseException as e:
                        errs += 1
                        print "errs = {}".format(errs)
                        ef.write((u"{}\n".format(e)).encode('utf-8', errors='ignore'))
                        ef.write((entry_lines + u"\n").encode('utf-8', errors='ignore'))
                    # pp.pprint(d)
                    # print

                entry_buffer = list()
            entry_buffer.append(line)
        # entry_lines = ''.join(entry_buffer)

        # d = (ENTRY_BLOCK + stringEnd).parseString(entry_lines).dump()
        # pp.pprint(d)
        print

if __name__ == '__main__':
    main()
