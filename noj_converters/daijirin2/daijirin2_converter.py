#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import sys
from pyparsing import *
from lxml import etree
from textwrap import dedent
from noj_converters.misc.uni_printer import UniPrinter
import daijirin2_grammar as g

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

class Daijrin2Converter(object):
    def __init__(self, dump_path, out_path, error_path):
        super(Daijrin2Converter, self).__init__()
        self.dump_path = dump_path
        self.out_path = out_path
        self.error_path = error_path

    def convert_generator(self):
        errs = 0
        ef = open(self.error_path, 'wb')
        out = open(self.out_path, 'wb')

        with codecs.open(self.dump_path, 'r', 'utf-8') as f:
            with etree.xmlfile(out, encoding='utf-8') as xf:
                xf.write_declaration()
                with xf.element(NAMESPACE_PREFIX+'dictionary', nsmap=NSMAP,
                                attrib={XSI_PREFIX+'schemaLocation': SCHEMA_LOCATION,
                                        'schema_version': __schema_version__}): 
                    xf.write("\n")
                    entry_buffer = list()
                    in_metadata = True
                    for line in f:

                        is_entry_header = g.ENTRY_HEADER_MATCHER.match(line)
                        if is_entry_header:
                            if in_metadata:
                                in_metadata = False
                                xml_meta = self.meta_to_xml(entry_buffer[:-1])
                                xf.write(xml_meta, pretty_print=True)
                            else:
                                entry_lines = ''.join(entry_buffer)
                                
                                try:
                                    res = (g.ENTRY_BLOCK + stringEnd).parseString(entry_lines)
                                    xml_entry = self.entry_to_xml(res)
                                    xf.write(xml_entry, pretty_print=True)
                                except ParseException as e:
                                    errs += 1
                                    print "errs = {}".format(errs)
                                    ef.write((u"{}\n".format(e)).encode('utf-8', errors='ignore'))
                                    ef.write((entry_lines + u"\n").encode('utf-8', errors='ignore'))

                            entry_buffer = list()
                            yield f.tell()
                        entry_buffer.append(line)

    def entry_to_xml(self, pr):
        xml_entry = etree.Element("entry", format="J-J1")

        remove_punct_map = dict([(ord(p), None) for p in u"-・"])

        xml_kana = etree.Element("kana")
        xml_kana.text = pr.kana[0]
        xml_entry.append(xml_kana)

        if pr.g1:
            for k in pr.surf:
                kanji = etree.Element("kanji")
                kanji.text = k
                xml_entry.append(kanji)
        else:
            if pr.hist_surf_list:
                for hist, surf in pr.hist_surf_list:
                    for k in surf:
                        kanji = etree.Element("kanji")
                        kanji.text = k
                        xml_entry.append(kanji)


        if pr.acc:
            accent = etree.Element("accent")
            accent.text = ''.join(pr.acc)
            xml_entry.append(accent)

        # print
        if pr.gsg:
            xml_entry.append(self.grammar_subentry_group_to_xml(pr.gsg))
        elif pr.msg:
            xml_entry.append(self.meaning_subentry_group_to_xml(pr.msg))
        elif pr.nsg:
            xml_entry.append(self.no_subentry_group_to_xml(pr.nsg))
        return xml_entry

    def grammar_subentry_group_to_xml(self, pr):
        # print "gsg"
        # pp.pprint(pr.dump())
        root_def = etree.Element("definition", group="grammar")
        if pr.pre_def:
            def_text = etree.Element("definition_text")
            def_text.text = pr.pre_def[0]
            root_def.append(def_text)
        for se in pr.subentries:
            # pp.pprint(se.dump())
            sub_def = etree.Element("definition", group="subgrammar")
            subdef_text = etree.Element("definition_text")
            terms = list()
            for t in se.terms:
                terms.append(u"〔" + t + u"〕")
            subdef_text.text = se.def_text + u"".join(terms)
            sub_def.append(subdef_text)

            # Go deeper
            if se.msg:
                sub_def.append(self.meaning_subentry_group_to_xml(se.msg))
            elif se.nsg:
                sub_def.append(self.no_subentry_group_to_xml(se.nsg))

            root_def.append(sub_def)
        return root_def

    def meaning_subentry_group_to_xml(self, pr):
        # print "msg"
        # pp.pprint(pr.dump())
        root_def = etree.Element("definition", group="meaning")
        if pr.pre_def:
            def_text = etree.Element("definition_text")
            def_text.text = pr.pre_def[0]
            root_def.append(def_text)
        for se in pr.subentries:
            # pp.pprint(se.dump())
            sub_def = etree.Element("definition", group="submeaning")
            # TODO might need to split the examples off
            subdef_text = etree.Element("definition_text")
            text, examples = se.def_text
            subdef_text.text = text
            sub_def.append(subdef_text)
            self.examples_to_xml(examples, sub_def)

            # Go deeper
            if se.nsg:
                sub_def.append(self.no_subentry_group_to_xml(se.nsg))

            root_def.append(sub_def)
        return root_def

    def no_subentry_group_to_xml(self, pr):
        # print "nsg"
        if pr.multi_def:
            return self.multi_def_to_xml(pr.multi_def)
        else:
            return self.single_def_to_xml(pr.sgl_def)

    def multi_def_to_xml(self, pr):
        # print "multidef"
        # pp.pprint(pr.dump())
        root_def = etree.Element("definition", group="multidefinition")
        if pr.pre_def:
            def_text = etree.Element("definition_text")
            def_text.text = pr.pre_def[0]
            root_def.append(def_text)
        for d in pr.defs:
            # TODO handle this properly
            sub_def = etree.Element("definition")
            self.definition_text_to_xml(d.def_text, sub_def)
            root_def.append(sub_def)
        return root_def

    def single_def_to_xml(self, pr):
        # print "sgl_def"
        # pp.pprint(pr.dump())
        root_def = etree.Element("definition")
        # sub_def = etree.Element("definition")
        # self.definition_text_to_xml(pr.def_text, sub_def)
        # root_def.append(sub_def)
        self.definition_text_to_xml(pr.def_text, root_def)
        return root_def

    def definition_text_to_xml(self, pr, subdef):
        # print "def_text"
        # print "--- here"
        # pp.pprint(pr)
        # print "--- fin"
        # head
        text, examples = pr['head']
        subdef_text = etree.Element("definition_text")
        subdef_text.text = text
        subdef.append(subdef_text)
        self.examples_to_xml(examples, subdef)
        # body
        if 'body' in pr:
            subdef.set('group', 'subdefinition')
            # print "body~~~~~"
            for b in pr['body']:
                # print b
                subsub_def = etree.Element("definition", group="subsubdefinition")
                text, examples = b['extract']
                subsubdef_text = etree.Element("definition_text")
                subsubdef_text.text = text
                subsub_def.append(subsubdef_text)
                self.examples_to_xml(examples, subsub_def)
                subdef.append(subsub_def)

    def examples_to_xml(self, examples, root_def):
        for ex in examples:
            usage_example = etree.Element('usage_example', type='UNKNOWN')
            expression = etree.Element('expression')
            expression.text = ex
            usage_example.append(expression)
            root_def.append(usage_example)

    def meta_to_xml(self, meta_lines):
        xml_meta = etree.Element("dictionary_meta")
        has_title = False
        for line in meta_lines:
            line = line.rstrip()
            s = line.split(u': ', 1)
            if len(s) == 2:
                key, value = s
                if key == u'FORMAT':
                    pass
                elif key == u'TITLE':
                    xml_name = etree.Element("name")
                    xml_name.text = value
                    xml_meta.append(xml_name)
                    has_title = True
                elif key == u'VERSION':
                    xml_dump_version = etree.Element("dump_version")
                    xml_dump_version.text = value
                    xml_meta.append(xml_dump_version)
        xml_convert_version = etree.Element("convert_version")
        xml_convert_version.text = __version__
        xml_meta.append(xml_convert_version)
        if has_title == False:
            raise Exception("No TITLE metadata.")

        return xml_meta


    # what does this do???
    def entry_test(self):
        print testentry
        res = (g.ENTRY_BLOCK + stringEnd).parseString(testentry)
        # pp.pprint(res.dump())
        xml_entry = self.entry_to_xml(res)

        print etree.tostring(xml_entry, pretty_print=True, encoding="UTF-8")
        print

    def __len__(self):
        return os.path.getsize(self.dump_path)

def main():
    # self.entry_test()
    dump_path = sys.argv[1] # TODO validate or change to FP
    out_path = 'daijirin2_importable.xml'
    error_path = 'errors.txt'
    converter = Daijrin2Converter(dump_path, out_path, error_path)

    import progressbar as pb
    widgets = ['Converting: ', pb.Percentage(), ' ', pb.Bar(),
               ' ', pb.Timer(), ' ']
    pbar = pb.ProgressBar(widgets=widgets, maxval=len(converter)).start()

    for i in converter.convert_generator():
        pbar.update(i)
    pbar.finish()


if __name__ == '__main__':
    main()

