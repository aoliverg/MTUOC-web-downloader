import html2text
import os
from bs4 import BeautifulSoup
import codecs
import sys
import dewiki
import re
import fasttext
import html2text
from langcodes import *

def remove_tags(segment):
    segmentnotags=re.sub('<[^>]+>',' ',segment).strip()
    segmentnotags=re.sub(' +', ' ', segmentnotags)
    return(segmentnotags)

#SRX_SEGMENTER
import lxml.etree
import regex
from typing import (
    List,
    Set,
    Tuple,
    Dict,
    Optional
)


class SrxSegmenter:
    """Handle segmentation with SRX regex format.
    """
    def __init__(self, rule: Dict[str, List[Tuple[str, Optional[str]]]], source_text: str) -> None:
        self.source_text = source_text
        self.non_breaks = rule.get('non_breaks', [])
        self.breaks = rule.get('breaks', [])

    def _get_break_points(self, regexes: List[Tuple[str, str]]) -> Set[int]:
        return set([
            match.span(1)[1]
            for before, after in regexes
            for match in regex.finditer('({})({})'.format(before, after), self.source_text)
        ])

    def get_non_break_points(self) -> Set[int]:
        """Return segment non break points
        """
        return self._get_break_points(self.non_breaks)

    def get_break_points(self) -> Set[int]:
        """Return segment break points
        """
        return self._get_break_points(self.breaks)

    def extract(self) -> Tuple[List[str], List[str]]:
        """Return segments and whitespaces.
        """
        non_break_points = self.get_non_break_points()
        candidate_break_points = self.get_break_points()

        break_point = sorted(candidate_break_points - non_break_points)
        source_text = self.source_text

        segments = []  # type: List[str]
        whitespaces = []  # type: List[str]
        previous_foot = ""
        for start, end in zip([0] + break_point, break_point + [len(source_text)]):
            segment_with_space = source_text[start:end]
            candidate_segment = segment_with_space.strip()
            if not candidate_segment:
                previous_foot += segment_with_space
                continue

            head, segment, foot = segment_with_space.partition(candidate_segment)

            segments.append(segment)
            whitespaces.append('{}{}'.format(previous_foot, head))
            previous_foot = foot
        whitespaces.append(previous_foot)

        return segments, whitespaces


def parse(srx_filepath: str) -> Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]:
    """Parse SRX file and return it.
    :param srx_filepath: is soruce SRX file.
    :return: dict
    """
    tree = lxml.etree.parse(srx_filepath)
    namespaces = {
        'ns': 'http://www.lisa.org/srx20'
    }

    rules = {}

    for languagerule in tree.xpath('//ns:languagerule', namespaces=namespaces):
        rule_name = languagerule.attrib.get('languagerulename')
        if rule_name is None:
            continue

        current_rule = {
            'breaks': [],
            'non_breaks': [],
        }

        for rule in languagerule.xpath('ns:rule', namespaces=namespaces):
            is_break = rule.attrib.get('break', 'yes') == 'yes'
            rule_holder = current_rule['breaks'] if is_break else current_rule['non_breaks']

            beforebreak = rule.find('ns:beforebreak', namespaces=namespaces)
            beforebreak_text = '' if beforebreak.text is None else beforebreak.text

            afterbreak = rule.find('ns:afterbreak', namespaces=namespaces)
            afterbreak_text = '' if afterbreak.text is None else afterbreak.text

            rule_holder.append((beforebreak_text, afterbreak_text))

        rules[rule_name] = current_rule

    return rules

def segmenta(cadena,srxlang):
    parts=cadena.split("\n")
    resposta=[]
    for part in parts:
        segmenter = SrxSegmenter(rules[srxlang],part)
        segments=segmenter.extract()
        for segment in segments[0]:
            segment=segment.replace("’","'")
            segment=segment.replace("\t"," ")
            #segment=segment.replace("\n"," ")
            segment = " ".join(segment.split())
            resposta.append(segment)
    #resposta="\n".join(resposta)
    return(resposta)


modelFT = fasttext.load_model("lid.176.bin")

rules = parse("segment.srx")
validLangs=rules.keys()
direntrada=sys.argv[1]
fileprefix=sys.argv[2]
h = html2text.HTML2Text()
h.ignore_links = True
h.body_width = 0
createdfiles=[]
for path, currentDirectory, files in os.walk(direntrada):
    for file in files:
        try:
            if file.endswith(".htm") or file.endswith(".html"):
                print("Converting: ",file)
                fullpath=os.path.join(path, file)
                content=open(fullpath,"r").read()
                text=h.handle(content)
                textP=text.replace("\n"," ")
                DL1=modelFT.predict(textP, k=1)
                L1=DL1[0][0].replace("__label__","")
                LangObject=Language.get(L1)
                L1fullname=LangObject.display_name()
                print("Language detected: ", L1, L1fullname)
                if L1fullname in validLangs:
                    srxlang=L1fullname
                else:
                    srxlang="Generic"
                print("SRXLang:",srxlang)
                outfilename=fileprefix+"-"+L1+".txt"
                if outfilename in createdfiles:
                    outfile=codecs.open(outfilename,"a",encoding="utf-8")
                else:
                    outfile=codecs.open(outfilename,"w",encoding="utf-8")
                    createdfiles.append(outfile)
                print("Writing text to: ",outfilename)
                segments=segmenta(text,srxlang)
                for segment in segments:
                    if len(segment)>0:
                        segment2=segment.strip()
                        segment2=dewiki.from_string(segment2)
                        segment2=remove_tags(segment2)
                        outfile.write(segment2+"\n")
                outfile.close()
                print("--------")
        except:
            print("ERROR",fullpath,sys.exc_info())
            sys.exit()


