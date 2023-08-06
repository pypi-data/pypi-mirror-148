# This file is part of Indico.
# Copyright (C) 2002 - 2022 CERN
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see the
# LICENSE file for more details.

from indico.modules.events.fields import PersonLinkListFieldBase
from indico.modules.events.sessions.models.persons import SessionBlockPersonLink
from indico.modules.events.util import serialize_person_link
from indico.web.forms.widgets import JinjaWidget


class SessionBlockPersonLinkListField(PersonLinkListFieldBase):
    person_link_cls = SessionBlockPersonLink
    linked_object_attr = 'session_block'
    widget = JinjaWidget('events/sessions/forms/session_person_link_widget.html')

    def _serialize_person_link(self, principal, extra_data=None):
        return (extra_data or {}) | serialize_person_link(principal)

    def _convert_data(self, data):
        return list({self._get_person_link(x) for x in data})
