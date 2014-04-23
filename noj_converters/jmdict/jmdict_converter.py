# -*- coding: utf-8 -*-
from collections import defaultdict
import codecs
import os
import re
from pyparsing import *
import progressbar as pb
from lxml import etree
from textwrap import dedent
from noj_converters.misc.uni_printer import UniPrinter

__version__ = '1.0.0a'
__schema_version__ = '1.0.0a'

pp = UniPrinter(indent=4)

NAMESPACE_URI = "http://www.naturalorderjapanese.com"
NAMESPACE_PREFIX = "{" + NAMESPACE_URI + "}"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
XSI_PREFIX = "{" + XSI + "}"
SCHEMA_LOCATION = "http://www.naturalorderjapanese.com dictionary_schema-{}.xsd".format(__schema_version__)
NSMAP = {None:  NAMESPACE_URI,
         'xsi': XSI}

comment_re = re.compile(ur'#ID=\d.*')
component_re = re.compile(ur"(?P<base>.+?)(\((?P<reading>.*?)\))?(\[(?P<defnum>\d*?)\])?({(?P<conj>.*?)})?(?P<validated>~)?$")

def load_examples(example_path):
    example_dict = defaultdict(list)
    expression = None
    meaning = None
    with codecs.open(example_path, 'r', 'euc-jp') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(u'A: '):
                without_comments = re.sub(comment_re, u"", line[3:])
                expression, meaning = without_comments.split(u'\t')
            else:
                components = line[3:].split(u" ")
                for c in components:
                    m = component_re.match(c)
                    if m:
                        key = m.group("base")
                        comp = dict()
                        comp["expression"] = expression
                        comp["meaning"] = meaning
                        if m.group("reading") is not None:
                            comp['reading'] = m.group("reading")
                        if m.group("defnum") is not None:
                            comp['defnum'] = int(m.group("defnum"))
                        if m.group("conj") is not None:
                            comp['conj'] = m.group("conj")
                        if m.group("validated") is not None:
                            comp['validated'] = True
                        # print c, m
                        # print str(m.groups()).decode("unicode-escape")
                        example_dict[key].append(comp)
    return example_dict

def unescape_entities(entity_line):
    translation_table = dict.fromkeys(map(ord, '&;'), None)
    return entity_line.translate(translation_table)

def create_meta(jmdict_path):
    xml_meta = etree.Element("dictionary_meta")

    # name
    xml_name = etree.Element('name')
    xml_name.text = "JMDict/EDICT + Examples"
    xml_meta.append(xml_name)

    # dump_version
    pass # no dump_version

    # convert_version
    xml_convert_version = etree.Element('convert_version')
    xml_convert_version.text = __version__
    xml_meta.append(xml_convert_version)

    # date
    date = None
    with codecs.open(jmdict_path, 'r', 'utf-8') as f:
        for line in f:
            m = re.match(r'<!-- JMdict created: (.*?) -->', line)
            if m:
                date = m.group(1)
                break
        else:
            raise Exception("Created date not found.")
    xml_date = etree.Element('date')
    xml_date.text = date
    xml_meta.append(xml_date)

    # extra
    pass # no extra

    return xml_meta
    

def convert_entry(entry_xml, example_dict):
    xml_entry = etree.Element("entry", format="J-E1")
    # print etree.tostring(entry_xml, pretty_print=True, encoding='utf-8')

    # convert "ent_seq"
    # MAYBE incorporate later
    # ent_seq_xml = entry_xml.find('ent_seq')
    # xml_entry.set('orig_id', ent_seq_xml.text)

    # convert "r_ele+"
    kana_set = set()
    r_ele_list = entry_xml.findall('r_ele')
    for r_ele_xml in r_ele_list:
        # convert reb
        reb_xml = r_ele_xml.find('reb')
        xml_kana = etree.Element("kana")
        xml_kana.text = reb_xml.text

        # convert re_nokanji
        re_nokanji = r_ele_xml.find('re_nokanji')
        if re_nokanji is not None:
            continue

        # TODO: handle this properly

        # convert re_restr*
        pass
        # convert re_inf*
        pass
        # convert re_pri*
        pass

        kana_set.add(reb_xml.text)
        xml_entry.append(xml_kana)

    # convert "k_ele*"
    kanji_set = set()
    k_ele_list = entry_xml.findall('k_ele')
    for k_ele_xml in k_ele_list:
        # convert keb
        keb_xml = k_ele_xml.find('keb')
        xml_kanji = etree.Element("kanji")
        xml_kanji.text = keb_xml.text

        # TODO: handle this properly

        # convert ke_inf*
        pass
        # convert ke_pri*
        pass

        kanji_set.add(keb_xml.text)
        xml_entry.append(xml_kanji)

    # Find candidate example sentences
    defnum_to_examples = defaultdict(list)
    key_set = kana_set if len(kanji_set) == 0 else kanji_set
    for key in key_set:
        if key in example_dict:
            for comp in example_dict[key]:
                if 'reading' in comp and comp['reading'] not in kana_set:
                    continue
                if 'defnum' in comp:
                    defnum_to_examples[comp['defnum']].append(comp)
                else:
                    defnum_to_examples[None].append(comp)


    # convert "info?"
    pass # not using

    # convert "sense+"
    sense_list = entry_xml.findall('sense')
    append_to = xml_entry
    if len(sense_list) > 1:
        append_to = etree.Element('definition', group="multidefinition")
        if None in defnum_to_examples:
            for comp in defnum_to_examples[None]:
                xml_ue = convert_example(comp)
                append_to.append(xml_ue)
        xml_entry.append(append_to)

    for sense_num, sense_xml in enumerate(sense_list):
        examples_for_defnum = list()
        if len(sense_list) == 1 and None in defnum_to_examples:
            examples_for_defnum.extend(defnum_to_examples[None])
        if (sense_num + 1) in defnum_to_examples:
            examples_for_defnum.extend(defnum_to_examples[sense_num + 1])
        xml_definition = convert_sense(sense_xml, examples_for_defnum)
        append_to.append(xml_definition)

    return xml_entry

def convert_example(comp):
    xml_ue = etree.Element('usage_example', type="SENTENCE")

    xml_expression = etree.Element('expression')
    xml_expression.text = comp['expression']
    xml_ue.append(xml_expression)

    xml_meaning = etree.Element('meaning')
    xml_meaning.text = comp['meaning']
    xml_ue.append(xml_meaning)

    if 'validated' not in comp:
        xml_ue.set('validated', 'false')
    return xml_ue

def convert_sense(sense_xml, example_list):
    definition_text_parts = list()
    xml_definition = etree.Element('definition')

    stag_str_list = list()

    # convert stagk*
    stagk_list = sense_xml.findall('stagk')
    if stagk_list:
        stagk_str_list = list()
        for stagk_xml in stagk_list:
            stag_str_list.append(stagk_xml.text)

    # convert stagr*
    stagr_list = sense_xml.findall('stagr')
    if stagr_list:
        stagr_str_list = list()
        for stagr_xml in stagr_list:
            stag_str_list.append(stagr_xml.text)

    if stag_str_list:
        stag_line = '(' + ', '.join(stag_str_list) + ' only)'
        definition_text_parts.append(stag_line)

    # convert pos*
    pos_list = sense_xml.findall('pos')
    if pos_list:
        pos_str_list = list()
        for pos_xml in pos_list:
            pos_str = str(pos_xml[0])
            pos_str = pos_str.translate(None, '&;')
            pos_str_list.append(pos_str)
        pos_line = '(' + ','.join(pos_str_list) + ')'
        definition_text_parts.append(pos_line)

    # convert xref*
    xref_list = sense_xml.findall('xref')
    if xref_list:
        xref_str_list = list()
        for xref_xml in xref_list:
            xref_str_list.append(xref_xml.text)
        xref_line = '(See ' + ','.join(xref_str_list) + ')'
        definition_text_parts.append(xref_line)

    # convert ant*
    ant_list = sense_xml.findall('ant')
    if ant_list:
        ant_str_list = list()
        for ant_xml in ant_list:
            ant_str_list.append(ant_xml.text)
        ant_line = '(ant: ' + ','.join(ant_str_list) + ')'
        definition_text_parts.append(ant_line)

    # convert field*
    field_list = sense_xml.findall('field')
    if field_list:
        field_str_list = list()
        for field_xml in field_list:
            field_str = str(field_xml[0])
            field_str = field_str.translate(None, '&;')
            field_str_list.append(field_str)
        field_line = '{' + ','.join(field_str_list) + '}'
        definition_text_parts.append(field_line)

    # convert misc*
    misc_list = sense_xml.findall('misc')
    if misc_list:
        misc_str_list = list()
        for misc_xml in misc_list:
            misc_str = str(misc_xml[0])
            misc_str = misc_str.translate(None, '&;')
            misc_str_list.append('(' + misc_str + ')')
        misc_line = ' '.join(misc_str_list)
        definition_text_parts.append(misc_line)

    # convert s_inf*
    s_inf_list = sense_xml.findall('s_inf')
    if s_inf_list:
        s_inf_str_list = list()
        for s_inf_xml in s_inf_list:
            s_inf_str_list.append('(' + s_inf_xml.text + ')')
        s_inf_line = ' '.join(s_inf_str_list)
        definition_text_parts.append(s_inf_line)

    # convert lsource*
    lsource_list = sense_xml.findall('lsource')
    if lsource_list:
        lsource_str_list = list()
        for lsource_xml in lsource_list:
            XML_NAMESPACE_PREFIX = '{http://www.w3.org/XML/1998/namespace}'
            ls_wasei = lsource_xml.get('ls_wasei')
            lang = lsource_xml.get(XML_NAMESPACE_PREFIX + 'lang')
            text = lsource_xml.text
            tmp = ''
            if ls_wasei is not None:
                tmp = 'wasei:'
            elif lang is not None:
                tmp = lang + ':'
            else:
                continue
            if text is not None:
                tmp = tmp + ' ' + text
            lsource_str_list.append(tmp)
        lsource_line = '(' + ', '.join(lsource_str_list) + ')'
        definition_text_parts.append(lsource_line)

    # convert dial*
    dial_list = sense_xml.findall('dial')
    if dial_list:
        dial_str_list = list()
        for dial_xml in dial_list:
            dial_str = str(dial_xml[0])
            dial_str = dial_str.translate(None, '&;')
            dial_str_list.append('(' + dial_str + ')')
        dial_line = ' '.join(dial_str_list)
        definition_text_parts.append(dial_line)

    # convert gloss*
    gloss_list = sense_xml.findall('gloss')
    definition_text_list = [xml.text for xml in gloss_list]
    xml_definition_text = etree.Element('definition_text')
    if definition_text_list:
        definition_text_parts.append(u'; '.join(definition_text_list))

    # convert example*
    pass # not using

    xml_definition_text.text = u' '.join(definition_text_parts)
    xml_definition.append(xml_definition_text)

    # convert example_list
    for comp in example_list:
        xml_ue = convert_example(comp)
        xml_definition.append(xml_ue)
    return xml_definition

def test_real(jmdict_path, examples_path):
    i = 0
    errs = 0

    ef = open('errors.txt', 'wb')
    out = open('jmdict-importable.xml', 'wb')

    jmdict_total_size = os.path.getsize(jmdict_path)
    examples_total_size = os.path.getsize(examples_path)
    widgets = ['Converting: ', pb.Percentage(), ' ', pb.Bar(),
               ' ', pb.Timer(), ' ']
    pbar = pb.ProgressBar(widgets=widgets, maxval=jmdict_total_size).start()

    example_dict = load_examples(examples_path)

    with open(jmdict_path, 'rb') as f:
        with etree.xmlfile(out, encoding='utf-8') as xf:
            xf.write_declaration()
            context = etree.iterparse(f, tag=('entry'), resolve_entities=False)

            with xf.element(NAMESPACE_PREFIX+'dictionary', nsmap=NSMAP,
                            attrib={XSI_PREFIX+'schemaLocation': SCHEMA_LOCATION,
                                    'schema_version': __schema_version__}): 
                xf.write("\n")
                xml_meta = create_meta(jmdict_path)
                xf.write(xml_meta, pretty_print=True)

                for action, elem in context:
                    xml_entry = convert_entry(elem, example_dict)
                    xf.write(xml_entry, pretty_print=True)
                    pbar.update(f.tell())
                    elem.clear()

    pbar.finish()

def main():
    jmdict_path = 'JMdict_e'
    examples_path = 'examples'
    test_real(jmdict_path, examples_path)

if __name__ == '__main__':
    main()

