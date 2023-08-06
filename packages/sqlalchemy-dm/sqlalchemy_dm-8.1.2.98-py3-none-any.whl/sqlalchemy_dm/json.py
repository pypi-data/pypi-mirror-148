# mysql/json.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import absolute_import

from sqlalchemy_dm import types as sqltypes
from sqlalchemy.types import VARCHAR
from sqlalchemy import types as sqltypes

# __all__ = ("JSON")

from sqlalchemy.sql import operators

idx_precedence = operators._PRECEDENCE[operators.json_getitem_op]

ASTEXT = operators.custom_op(
    "$.",
    precedence=idx_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
)

JSONPATH_ASTEXT = operators.custom_op(
    "#>>",
    precedence=idx_precedence,
    natural_self_precedent=True,
    eager_grouping=True,
)

class JSON(VARCHAR):
    __visit_name__ = 'JSON'

    def get_dbapi_type(self, dbapi):
        return dbapi.VARCHAR

    def bind_processor(self, dialect):
        def process(value):
            import json
            return json.dumps(value) if value is not None and isinstance(value,dict) else value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                import json
                return json.loads(value) if isinstance(value,str) else value
            else:
                return value

        return process

    class Comparator(sqltypes.JSON.Comparator):
        """Define comparison operations for :class:`.JSON`."""

        @property
        def astext(self):
            """On an indexed expression, use the "astext" (e.g. "->>")
            conversion when rendered in SQL.

            E.g.::

                select([data_table.c.data['some key'].astext])

            .. seealso::

                :meth:`.ColumnElement.cast`

            """
            if isinstance(self.expr.right.type, sqltypes.JSON.JSONPathType):
                return self.expr.left.operate(
                    JSONPATH_ASTEXT,
                    self.expr.right,
                    result_type=self.type.astext_type,
                )
            else:
                return self.expr.left.operate(
                    ASTEXT, self.expr.right, result_type=self.type.astext_type
                )

    comparator_factory = Comparator


class _FormatTypeMixin(object):
    def _format_value(self, value):
        raise NotImplementedError()

    def bind_processor(self, dialect):
        super_proc = self.string_bind_processor(dialect)

        def process(value):
            value = self._format_value(value)
            if super_proc:
                value = super_proc(value)
            return value

        return process

    def literal_processor(self, dialect):
        super_proc = self.string_literal_processor(dialect)

        def process(value):
            value = self._format_value(value)
            if super_proc:
                value = super_proc(value)
            return value

        return process


class JSONIndexType(_FormatTypeMixin, sqltypes.JSON.JSONIndexType):
    def _format_value(self, value):
        # if isinstance(value, int):
        #     value = "$[%s]" % value
        # else:
        value = '$.%s' % value
        return value


class JSONPathType(_FormatTypeMixin, sqltypes.JSON.JSONPathType):
    def _format_value(self, value):
        return '$%s' % (
            "".join(
                [
                     '.%s' % elem
                    for elem in value
                ]
            )
        )
