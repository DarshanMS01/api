from django.utils.html import escape
from django.utils.safestring import mark_safe
from rest_framework.renderers import BrowsableAPIRenderer


class TableBrowsableAPIRenderer(BrowsableAPIRenderer):
    """Browsable API page that shows list responses as an HTML table.

    Everything else (navbar, status line, POST form) is unchanged. Responses
    that are not a list of objects, such as validation errors or a single
    student, fall back to the normal JSON block.
    """

    def get_context(self, data, media_type, renderer_context):
        context = super().get_context(data, media_type, renderer_context)
        context['response_table'] = self._table(data)
        return context

    def _table(self, data):
        rows = data
        # Support paginated responses: {"count": .., "results": [..]}
        if isinstance(rows, dict) and isinstance(rows.get('results'), list):
            rows = rows['results']

        if not isinstance(rows, list) or not rows:
            return ''
        if not all(isinstance(row, dict) for row in rows):
            return ''

        columns = list(rows[0].keys())
        for row in rows[1:]:
            for key in row:
                if key not in columns:
                    columns.append(key)

        head = ''.join(f'<th>{escape(column)}</th>' for column in columns)
        body = ''.join(
            '<tr>' + ''.join(
                f'<td>{escape(str(row.get(column, "")))}</td>' for column in columns
            ) + '</tr>'
            for row in rows
        )

        return mark_safe(
            '<table class="table table-striped table-bordered">'
            f'<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'
        )
