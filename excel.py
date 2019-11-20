# -*- coding: utf-8 -*-
class pdf:
    entity = ""
    note_type = ""
    date = ""
    subject = ""
    source = ""
    attachment = ""

    def __init__(self, entity, note_type, date, subject, source, attachment):
        self.entity = entity
        self.note_type = note_type
        self.date = date
        self.subject = subject
        self.source = source
        self.attachment = attachment

    def __str__(self):
        return "" + self.entity + self.note_type + self.date + self.subject + self.source + self.attachment
