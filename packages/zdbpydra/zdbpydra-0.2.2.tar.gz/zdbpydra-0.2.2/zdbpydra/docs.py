# -*- coding: utf-8 -*-
"""
Parser classes for JSON-LD data (with PICA+ data embedded) retrieved
from the German Union Catalogue of Serials (ZDB)

For more information on the PICA-based cataloguing format of ZDB, see
https://zeitschriftendatenbank.github.io/pica3plus/ or
https://zeitschriftendatenbank.de/erschliessung/zdb-format (both in german).
"""

import datetime
from . import utils
from typing import Generator


class BaseParser:

    def __init__(self, data):
        self.raw = data

    def _names(self):
        if self.raw:
            names = list(self.raw.keys())
            names.sort()
            return names
        return []

    def _field(self, name):
        if self.raw and name in self.raw:
            return self.raw[name]

    def get(self, name):
        return self._field(name)


class ObjectParser(BaseParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def id(self):
        return self._field("id")

    @property
    def type(self):
        return self._field("type")


class ResponseParser(ObjectParser):

    def __init__(self, data):
        super().__init__(data)

    @property
    def context(self):
        return self._field("@context")


class SearchResponseParser(ResponseParser):
    """
    Die Metadaten zur Suchanfrage bestehen aus folgenden Schlüsseln:

        `id` - URL der ursprünglich gestellten Suchanfrage
        `freetextQuery` - die Suchterme
        `totalItems` - Absolute Anzahl der Ergebnisse
        `type` - Der Typ einer Ergebnismenge ist immer Collection

    Die eigentlichen Titeldaten werden unter dem Schlüssel `member` in
    einem JSON-Array zusammengefasst. ... die ... Navigation ist unter
    dem Schlüssel `view` als JSON-Objekt zusammengefasst.

    Quelle: https://zeitschriftendatenbank.de/services/schnittstellen/json-api
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def query(self):
        return self._field("freetextQuery")

    @property
    def total_items(self):
        count = self._field("totalItems")
        if count:
            return int(count)
        return 0

    @property
    def member(self):
        return self._field("member")

    @property
    def view(self):
        return self._field("view")

    @property
    def view__parser(self):
        view = self.view
        if view is not None:
            return ViewResponseParser(view)

    def _field_view(self, field):
        view = self.view
        if type(view) == dict and field in view:
            return view[field]

    def get(self, name, view=False):
        if view:
            return self._field_view(name)
        return self._field(name)

    @property
    def view_first(self):
        return self._field_view("first")

    @property
    def view_next(self):
        return self._field_view("next")

    @property
    def view_last(self):
        return self._field_view("last")


class ViewResponseParser(ObjectParser):
    """
    Die Navigation enthält die Schlüssel:

        `id` - Link zur aktuellen Seite
        `type` - ist immer PartialCollectionView
        `first` - Link zur ersten Seite
        `last` - Link zur letzten Seite
        `totalItems` - Anzahl der Datensätze, die auf der aktuellen Seite angezeigt werden
        `pageIndex` - Nummer der aktuellen Seite
        `numberOfPages` - Anzahl der Ergebnisseiten
        `offset` - Nummer des ersten Datensatzes auf der aktuellen Seite
        `limit` - Maximale Anzahl von Ergebnissen auf einer Seite

    und möglicherweise:

        `previous` - Link zur vorherigen Seite, falls vorhanden
        `next` - Link zur nächsten Seite, falls vorhanden

    Quelle: https://zeitschriftendatenbank.de/services/schnittstellen/json-api
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def total_items(self):
        return self._field("totalItems")

    @property
    def page_index(self):
        return self._field("pageIndex")

    @property
    def number_of_pages(self):
        return self._field("numberOfPages")

    @property
    def offset(self):
        return self._field("offset")

    @property
    def limit(self):
        return self._field("limit")

    @property
    def first(self):
        return self._field("first")

    @property
    def last(self):
        return self._field("last")

    @property
    def previous(self):
        return self._field("previous")

    @property
    def next(self):
        return self._field("next")


class TitleResponseParser(ResponseParser):
    """
    Jeder Titeldatensatz hat folgende Schlüssel:

        `id` - URL, der den Datensatz identifiziert
        `type` - Liste der Publikationstypen
        `seeAlso` - URL einer RDF-Repräsentation der Daten
        `sameAs` - wie seeAlso
        `identifier` - die ZDB-ID
        `medium`- Medientyp (print, audiovisual, braille, microform, online, electronic)
        `issn` - Liste der gültigen ISSNs
        `title` - Titel der Publikation
        `temporal` - Erscheinungsverlauf
        `publisher`- Publikationsvermerk
        `data` - der PICA-Plus-Datensatz in Form eines JSON-Objekts

    Quelle: https://zeitschriftendatenbank.de/services/schnittstellen/json-api
    """

    def __init__(self, data):
        super().__init__(data)

    @property
    def _id(self):
        return self._field("_id")

    @property
    def data(self):
        return self._field("data")

    @property
    def issn(self):
        return self._field("issn")

    @property
    def medium(self):
        return self._field("medium")

    @property
    def identifier(self):
        return self._field("identifier")

    @property
    def publisher(self):
        return self._field("publisher")

    @property
    def same_as(self):
        return self._field("sameAs")

    @property
    def see_also(self):
        return self._field("seeAlso")

    @property
    def temporal(self):
        return self._field("temporal")

    @property
    def title(self):
        return self._field("title")

    @property
    def _parser_data(self):
        data = self._field("data")
        if data is not None:
            return PicaParser(data)

    @property
    def pica(self):
        return self._parser_data

    def _field_pica(self, field):
        data = self.data
        if type(data) == dict and field in data:
            return data[field]

    def get(self, name, pica=True):
        if pica:
            return self._field_pica(name)
        return self._field(name)

    @property
    def _csv(self):
        raw = self.raw
        if raw is not None:
            return CsvBuilder(raw)

    @property
    def csv(self):
        return self._csv


class PicaParser(BaseParser):
    """
    For the PICA+ / PICA3 field definitions used by ZDB, see
    https://zeitschriftendatenbank.github.io/pica3plus/
    """

    def __init__(self, data):
        self._delim = "|"
        self._sub_delim = "~"
        super().__init__(data)

    @staticmethod
    def clean(value):
        return utils.clean_blanks(value)

    @staticmethod
    def clean_title(value):
        if type(value) == str:
            value = value.replace("¬", "")
            value = value.replace("@", "")
            return PicaParser.clean(value)

    def _field_value(self, name, clean=False):
        value = self._field(name)
        if isinstance(value, list) and len(value) > 0:
            if isinstance(value[0], list) and len(value[0]) > 0:
                if isinstance(value[0][0], list) and len(value[0][0]) > 0:
                    if clean:
                        return PicaParser.clean(value[0][0][0])
                    return value[0][0][0]

    def _subfields(self, name):
        fields = self._field(name)
        if isinstance(fields, list):
            for field in fields:
                yield field

    def _subfield_value(self, name, subname, unique=False, clean=False, joined=False):
        subfields = self._subfields(name)
        if isinstance(subfields, Generator):
            if not unique:
                values = []
            for subfield in subfields:
                if not unique:
                    subvalues = []
                for field in subfield:
                    if subname in field:
                        if unique:
                            if clean:
                                return PicaParser.clean(field[subname])
                            return field[subname]
                        else:
                            subvalues.append(field[subname] if not clean
                                             else PicaParser.clean(field[subname]))
                if joined:
                    values.append(self._sub_delim.join(subvalues))
                elif not unique:
                    values.extend(subvalues)
        if not unique and len(values) > 0:
            if joined:
                return self._delim.join(values)
            return values

    @property
    def first_entry(self):
        """
        001A/0200 – Erfassungskennung und Datum der Ersterfassung
        """
        return self._field_value("001A")

    @property
    def first_entry_code(self):
        """
        001A/0200 – Erfassungskennung
        """
        return self.first_entry.split(":")[0]

    @property
    def first_entry_date(self):
        """
        001A/0200 – Datum der Ersterfassung
        """
        return self.first_entry.split(":")[1]

    @property
    def first_entry_date_date(self):
        """
        001A/0200 – Datum der Ersterfassung (as date object)
        """
        first_entry_date = self.first_entry_date
        return datetime.datetime.strptime(first_entry_date, "%d-%m-%y").date()

    @property
    def first_entry_date_iso(self):
        """
        001A/0200 – Datum der Ersterfassung (in ISO format)
        """
        first_entry_date = self.first_entry_date_date
        return first_entry_date.isoformat()

    @property
    def latest_change(self):
        """
        001B/0210 – Änderungskennung, Datum und Uhrzeit der letzten Änderung

            $0  Pos. 1-4: Änderungskennung
                Pos. 5: Doppelpunkt
                Pos. 6-13: Datum der Änderung in der Form: TT-MM-JJ
        """
        return self._field_value("001B")

    @property
    def latest_change_code(self):
        """
        001B/0210 – Änderungskennung
        """
        return self.latest_change.split(":")[0]

    @property
    def latest_change_date(self):
        """
        001B/0210 – Datum der letzten Änderung
        """
        return self.latest_change.split(":")[1]

    @property
    def latest_change_date_date(self):
        """
        001B/0210 – Datum der letzten Änderung (as date object)
        """
        latest_change_date = self.latest_change_date
        return datetime.datetime.strptime(latest_change_date, "%d-%m-%y").date()

    @property
    def latest_change_date_iso(self):
        """
        001B/0210 – Datum der letzten Änderung (in ISO format)
        """
        latest_change_date = self.latest_change_date_date
        return latest_change_date.isoformat()

    @property
    def latest_change_time(self):
        """
        001B/0210 – Uhrzeit der letzten Änderung

            $t  Uhrzeit (HH:MM:SS)
        """
        return self._subfield_value("001B", "t", unique=True)

    @property
    def latest_change_str(self):
        """
        001B/0210 – Zeitstempel der letzten Änderung
        """
        d = self.latest_change_date
        t = self.latest_change_time
        return "{0} {1}".format(d, t)

    @property
    def latest_change_datetime(self):
        """
        001B/0210 – Zeitstempel der letzten Änderung (as datetime object)
        """
        change_datetime = self.latest_change_str
        return datetime.datetime.strptime(change_datetime, "%d-%m-%y %H:%M:%S.%f")

    @property
    def latest_change_datetime_iso(self):
        """
        001B/0210 – Zeitstempel der letzten Änderung (in ISO format)
        """
        change_datetime = self.latest_change_datetime
        return change_datetime.isoformat()

    @property
    def bbg(self):
        """
        002@/0500 – Bibliographische Gattung/Status
        """
        return self._field_value("002@")

    @property
    def idn(self):
        """
        003@/0100 – Identifikationsnummer des Datensatzes (IDN)
        """
        return self._field_value("003@")

    @property
    def issn(self):
        """
        005A/2010 – International Standard Serial Number (ISSN)

            $0  ISSN (mit Bindestrich)
        """
        return self._field_value("005A")

    @property
    def issn_l(self):
        """
        005A/2010 – International Standard Serial Number (ISSN)

            $l  ISSN-L
        """
        return self._subfield_value("005A", "l", unique=True)

    @property
    def zdb_code(self):
        """
        017A/0600 – Code-Angaben der ZDB

            $a  Code-Angabe {ad,ag,al,...,wk,wl,zt}
        """
        return self._subfield_value("017A", "a", joined=True)

    @property
    def product_code(self):
        """
        017B/0601 – Kennzeichnungsfeld für Nationallizenzen und digitale Sammlungen

            $a  Produktsigel
        """
        return self._subfield_value("017B", "a", joined=True)

    @property
    def title(self):
        """
        021A/4000 – Haupttitel, Titelzusätze, Paralleltitel, Verantwortlichkeitsangabe

            $a  Haupttitel
        """
        value = self._subfield_value("021A", "a", unique=True)
        return self.clean_title(value)

    @property
    def title_supplement(self):
        """
        021A/4000 – Haupttitel, Titelzusätze, Paralleltitel, Verantwortlichkeitsangabe

            $d  Titelzusatz
        """
        value = self._subfield_value("021A", "d", clean=True, joined=True)
        return self.clean_title(value)

    @property
    def title_responsibility(self):
        """
        021A/4000 – Haupttitel, Titelzusätze, Paralleltitel, Verantwortlichkeitsangabe

            $h  Verantwortlichkeitsangabe
        """
        return self._subfield_value("021A", "h", unique=True, clean=True)

    @property
    def publisher(self):
        """
        033A/4030 – Veröffentlichungsangabe

            $n  Angabe des Verlages
        """
        return self._subfield_value("033A", "n", clean=True, joined=True)

    @property
    def publisher_place(self):
        """
        033A/4030 – Veröffentlichungsangabe

            $p  Erster Erscheinungsort
        """
        return self._subfield_value("033A", "p", clean=True, joined=True)

    @property
    def parallel_type(self):
        """
        039D/4243 – Beziehung auf Manifestationsebene – außer Reproduktionen

            $n  Materialart, zeitliche Gültigkeit der Beziehung
        """
        return self._subfield_value("039D", "n", clean=True, joined=True)

    @property
    def parallel_bbg(self):
        """
        039D/4243 – Beziehung auf Manifestationsebene – außer Reproduktionen

            $g  Bibliographische Gattung/Status (undokumentiert)
        """
        return self._subfield_value("039D", "g", joined=True)

    @property
    def parallel_idn(self):
        """
        039D/4243 – Beziehung auf Manifestationsebene – außer Reproduktionen

            $9  IDN des zu verknüpfenden Bezugswerkes
        """
        return self._subfield_value("039D", "9", joined=True)

    @property
    def parallel_issn(self):
        """
        039D/4243 – Beziehung auf Manifestationsebene – außer Reproduktionen

            $X  ISSN
            $I  ISSN (undokumentiert)
        """
        value = []
        value_x = self._subfield_value("039D", "X")
        if isinstance(value_x, list):
            value.extend(value_x)
        value_i = self._subfield_value("039D", "I")
        if isinstance(value_i, list):
            value.extend(value_i)
        if len(value) > 0:
            return self._delim.join(value)

    @property
    def access_source(self):
        """
        047V/4713 – Angaben zu Open Access, Lizenzen und Rechten

            $b  Herkunft der Angabe
        """
        return self._subfield_value("047V", "b", unique=True)

    @property
    def access_rights(self):
        """
        047V/4713 – Angaben zu Open Access, Lizenzen und Rechten

            $c  Benennung des Rechts (Code)
        """
        return self._subfield_value("047V", "c", unique=True)

    @property
    def access_status(self):
        """
        047V/4713 – Angaben zu Open Access, Lizenzen und Rechten

            $o  Open-Access-Markierung (falls vorhanden wahlweise: "nOA" / "OA")
        """
        return self._subfield_value("047V", "o", unique=True)

    @property
    def dewey(self):
        """
        045U/5080 – DDC-Sachgruppen der ZDB

            $e  DDC-Sachgruppen der ZDB
        """
        return self._subfield_value("045U", "e", joined=True)


CSV_HEADER = [
  "id",
  "idn",
  "title",
  "title_supplement",
  "title_responsibility",
  "medium",
  "issn",
  "issn_l",
  "publisher",
  "publisher_place",
  "psg",
  "code",
  "bbg",
  "ddc",
  "access_status",
  "access_rights",
  "access_source",
  "parallel_idn",
  "parallel_issn",
  "parallel_bbg",
  "parallel_type"
]


class CsvBuilder:

    def __init__(self, data):
        self.header = CSV_HEADER
        self._source = TitleResponseParser(data)

    @property
    def row(self):
        return [
          self._source.identifier or "",
          self._source.pica.idn or "",
          self._source.pica.title or "",
          self._source.pica.title_supplement or "",
          self._source.pica.title_responsibility or "",
          self._source.medium or "",
          self._source.pica.issn or "",
          self._source.pica.issn_l or "",
          self._source.pica.publisher or "",
          self._source.pica.publisher_place or "",
          self._source.pica.product_code or "",
          self._source.pica.zdb_code or "",
          self._source.pica.bbg or "",
          self._source.pica.dewey or "",
          self._source.pica.access_status or "",
          self._source.pica.access_rights or "",
          self._source.pica.access_source or "",
          self._source.pica.parallel_idn or "",
          self._source.pica.parallel_issn or "",
          self._source.pica.parallel_bbg or "",
          self._source.pica.parallel_type or ""
        ]

    def output(self, header=False):
        if not header:
            return [self.row]
        return [self.header, self.row]
