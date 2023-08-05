import os
import sys
import sqlparse
import logging
from collections import namedtuple
from sqlparse.sql import Comparison, Identifier, Where
from sqlparse.compat import text_type

from athenacli.packages.parseutils import last_word, extract_tables, find_prev_keyword
from athenacli.packages.special import parse_special_command

_logger = logging.getLogger(__name__)

Column = namedtuple('Column', ['tables', 'drop_unique'])
Column.__new__.__defaults__ = (None, None)

Function = namedtuple('Function', ['schema', 'filter'])
# For convenience, don't require the `filter` argument in Function constructor
Function.__new__.__defaults__ = (None, None)

Keyword = namedtuple('Keyword', ['last_token'])
Keyword.__new__.__defaults__ = (None,)

Table = namedtuple('Table', ['schema'])
View = namedtuple('View', ['schema'])
Alias = namedtuple('Alias', ['aliases'])
Database = namedtuple('Database', [])
Schema = namedtuple('Schema', [])
Keyword.__new__.__defaults__ = (None,)
Show = namedtuple('Show', [])
Special = namedtuple('Special', [])
TableFormat = namedtuple('TableFormat', [])
FileName = namedtuple('FileName', [])
FavoriteQuery = namedtuple('FavoriteQuery', [])


def suggest_type(full_text, text_before_cursor):
    """Takes the full_text that is typed so far and also the text before the
    cursor to suggest completion type and scope.
    Returns a tuple with a type of entity ('table', 'column' etc) and a scope.
    A scope for a column category will be a list of tables.
    """

    word_before_cursor = last_word(text_before_cursor,
            include='many_punctuations')

    identifier = None

    # here should be removed once sqlparse has been fixed
    try:
        # If we've partially typed a word then word_before_cursor won't be an empty
        # string. In that case we want to remove the partially typed string before
        # sending it to the sqlparser. Otherwise the last token will always be the
        # partially typed string which renders the smart completion useless because
        # it will always return the list of keywords as completion.
        if word_before_cursor:
            if word_before_cursor.endswith(
                    '(') or word_before_cursor.startswith('\\'):
                parsed = sqlparse.parse(text_before_cursor)
            else:
                parsed = sqlparse.parse(
                    text_before_cursor[:-len(word_before_cursor)])

                # word_before_cursor may include a schema qualification, like
                # "schema_name.partial_name" or "schema_name.", so parse it
                # separately
                p = sqlparse.parse(word_before_cursor)[0]

                if p.tokens and isinstance(p.tokens[0], Identifier):
                    identifier = p.tokens[0]
        else:
            parsed = sqlparse.parse(text_before_cursor)
    except (TypeError, AttributeError):
        return (Keyword(),)

    if len(parsed) > 1:
        # Multiple statements being edited -- isolate the current one by
        # cumulatively summing statement lengths to find the one that bounds the
        # current position
        current_pos = len(text_before_cursor)
        stmt_start, stmt_end = 0, 0

        for statement in parsed:
            stmt_len = len(text_type(statement))
            stmt_start, stmt_end = stmt_end, stmt_end + stmt_len

            if stmt_end >= current_pos:
                text_before_cursor = full_text[stmt_start:current_pos]
                full_text = full_text[stmt_start:]
                break

    elif parsed:
        # A single statement
        statement = parsed[0]
    else:
        # The empty string
        statement = None

    # Check for special commands and handle those separately
    if statement:
        # Be careful here because trivial whitespace is parsed as a statement,
        # but the statement won't have a first token
        tok1 = statement.token_first()
        if tok1 and tok1.value.startswith("\\"):
            return suggest_special(text_before_cursor)

    last_token = statement and statement.token_prev(len(statement.tokens))[1] or ''

    return suggest_based_on_last_token(last_token, text_before_cursor,
                                       full_text, identifier)


def suggest_special(text):
    text = text.lstrip()
    cmd, _, arg = parse_special_command(text)

    if cmd == text:
        # Trying to complete the special command itself
        return (Special(),)

    if cmd in ('\\u', '\\r'):
        return (Database(),)

    if cmd in ('\\T'):
        return (TableFormat(),)

    if cmd in ['\\f', '\\fs', '\\fd']:
        return (FavoriteQuery(),)

    if cmd in ['\\dt', '\\dt+']:
        return (
            Table(schema=None),
            View(schema=None),
            Schema(),
        )
    elif cmd in ['\\.', 'source']:
        return (FileName(),)

    return (Keyword(), Special())


def suggest_based_on_last_token(token, text_before_cursor, full_text, identifier):
    if isinstance(token, str):
        token_v = token.lower()
    elif isinstance(token, Comparison):
        # If 'token' is a Comparison type such as
        # 'select * FROM abc a JOIN def d ON a.id = d.'. Then calling
        # token.value on the comparison type will only return the lhs of the
        # comparison. In this case a.id. So we need to do token.tokens to get
        # both sides of the comparison and pick the last token out of that
        # list.
        token_v = token.tokens[-1].value.lower()
    elif isinstance(token, Where):
        # sqlparse groups all tokens from the where clause into a single token
        # list. This means that token.value may be something like
        # 'where foo > 5 and '. We need to look "inside" token.tokens to handle
        # suggestions in complicated where clauses correctly
        prev_keyword, text_before_cursor = find_prev_keyword(text_before_cursor)
        return suggest_based_on_last_token(prev_keyword, text_before_cursor,
                                           full_text, identifier)
    else:
        token_v = token.value.lower()

    is_operand = lambda x: x and any([x.endswith(op) for op in ['+', '-', '*', '/']])

    if not token:
        return (Keyword(), Special())
    elif token_v.endswith('('):
        p = sqlparse.parse(text_before_cursor)[0]

        if p.tokens and isinstance(p.tokens[-1], Where):
            # Four possibilities:
            #  1 - Parenthesized clause like "WHERE foo AND ("
            #        Suggest columns/functions
            #  2 - Function call like "WHERE foo("
            #        Suggest columns/functions
            #  3 - Subquery expression like "WHERE EXISTS ("
            #        Suggest keywords, in order to do a subquery
            #  4 - Subquery OR array comparison like "WHERE foo = ANY("
            #        Suggest columns/functions AND keywords. (If we wanted to be
            #        really fancy, we could suggest only array-typed columns)

            column_suggestions = suggest_based_on_last_token('where',
                                    text_before_cursor, full_text, identifier)

            # Check for a subquery expression (cases 3 & 4)
            where = p.tokens[-1]
            idx, prev_tok = where.token_prev(len(where.tokens) - 1)

            if isinstance(prev_tok, Comparison):
                # e.g. "SELECT foo FROM bar WHERE foo = ANY("
                prev_tok = prev_tok.tokens[-1]

            prev_tok = prev_tok.value.lower()
            if prev_tok == 'exists':
                return (Keyword(),)
            else:
                return column_suggestions

        # Get the token before the parens
        idx, prev_tok = p.token_prev(len(p.tokens) - 1)
        if prev_tok and prev_tok.value and prev_tok.value.lower() == 'using':
            # tbl1 INNER JOIN tbl2 USING (col1, col2)
            tables = extract_tables(full_text)

            # suggest columns that are present in more than one table
            return (Column(tables=tables, drop_unique=True))
        elif p.token_first().value.lower() == 'select':
            # If the lparen is preceeded by a space chances are we're about to
            # do a sub-select.
            if last_word(text_before_cursor, 'all_punctuations').startswith('('):
                return (Keyword(),)

        # We're probably in a function argument list
        return (Column(tables=extract_tables(full_text)),)
    elif token_v in ('set', 'by', 'distinct'):
        return (Column(tables=extract_tables(full_text)),)
    elif token_v == 'as':
        # Don't suggest anything for an alias
        return tuple()
    elif token_v in ('select', 'where', 'having'):
        # Check for a table alias or schema qualification
        parent = (identifier and identifier.get_parent_name()) or []

        tables = extract_tables(full_text)
        if parent:
            tables = [t for t in tables if identifies(parent, *t)]
            return (
                Column(tables=tables),
                Table(schema=parent),
                View(schema=parent),
                Function(schema=parent),
            )
        else:
            aliases = [alias or table for (schema, table, alias) in tables]
            return (
                Column(tables=tables),
                Function(schema=None),
                Alias(aliases=aliases),
                Keyword(token_v.upper()),
            )
    elif (token_v.endswith('join') and token.is_keyword) or (token_v in
            ('copy', 'from', 'update', 'into', 'describe', 'truncate',
                'desc', 'explain', 'partitions')):
        schema = (identifier and identifier.get_parent_name()) or None

        # Suggest tables from either the currently-selected schema or the
        # public schema if no schema has been specified
        suggest = [Table(schema=schema)]

        if not schema:
            # Suggest schemas
            suggest.insert(0, Schema())

        # Only tables can be TRUNCATED, otherwise suggest views
        if token_v != 'truncate':
            suggest.append(View(schema=schema))

        return suggest

    elif token_v in ('table', 'view', 'function', 'tblproperties'):
        # E.g. 'DROP FUNCTION <funcname>', 'ALTER TABLE <tablname>'
        rel_type = {
            'table': Table,
            'view': View,
            'function': Function,
            'tblproperties': Table,
        }[token_v]

        schema = (identifier and identifier.get_parent_name()) or None
        if schema:
            return (rel_type(schema=schema))
        else:
            return (Schema(), rel_type(schema=schema))

    elif token_v == 'on':
        tables = extract_tables(full_text)  # [(schema, table, alias), ...]
        parent = (identifier and identifier.get_parent_name()) or None
        if parent:
            # "ON parent.<suggestion>"
            # parent can be either a schema name or table alias
            tables = tuple(t for t in tables if identifies(parent, *t))
            return (
                Column(tables=tables),
                Table(schema=parent),
                View(schema=parent),
                Function(schema=parent)
            )
        else:
            # ON <suggestion>
            # Use table alias if there is one, otherwise the table name
            aliases = tuple(alias or table for (schema, table, alias) in tables)
            suggest = [Alias(aliases=aliases)]

            # The lists of 'aliases' could be empty if we're trying to complete
            # a GRANT query. eg: GRANT SELECT, INSERT ON <tab>
            # In that case we just suggest all tables.
            if not aliases:
                suggest.append(Table(schema=parent))
            return suggest

    elif token_v in ('use', 'database', 'template', 'connect'):
        # "\c <db", "use <db>", "DROP DATABASE <db>",
        # "CREATE DATABASE <newdb> WITH TEMPLATE <db>"
        return (Database(),)
    elif token_v == 'tableformat':
        return (TableFormat(),)
    elif token_v.endswith(',') or is_operand(token_v) or token_v in ['=', 'and', 'or']:
        prev_keyword, text_before_cursor = find_prev_keyword(text_before_cursor)
        if prev_keyword:
            return suggest_based_on_last_token(
                prev_keyword, text_before_cursor, full_text, identifier)
        else:
            return tuple()
    elif token_v in {'alter', 'create', 'drop', 'show'}:
        return (Keyword(token_v.upper()),)
    else:
        return (Keyword(token_v.upper()),)


def identifies(id, schema, table, alias):
    return id == alias or id == table or (
        schema and (id == schema + '.' + table))