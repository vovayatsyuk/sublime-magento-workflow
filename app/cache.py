import re


class Cache:
    def __init__(self, app):
        self.app = app

    def bin_magento(self):
        return self.app.settings.get('bin_magento_command')

    def flush(self):
        return self.app.terminal.run('{} cache:flush')

    def clean(self, type=None):
        if type is None:
            type = self.get_types_to_clean()
            if len(type) == 0:
                return

        cmd = '{} cache:clean '.format(self.bin_magento())
        if isinstance(type, (set, list)):
            cmd += ' '.join(type)
        elif type is not 'All':
            cmd += type

        return self.app.terminal.run(cmd)

    def get_types_to_clean(self):
        rules = {
            r'/etc/.*\.xml': ['config'],
            r'/Block/.*\.php': ['block_html'],
            r'/templates/.*\.phtml': ['block_html'],
            r'/layout/.*\.xml': ['layout', 'block_html'],
            r'/ui_component/.*\.xml': ['config'],
            r'/i18n/.*\.csv': ['translate', 'block_html'],
            r'\.(php|xml|json)': ['full_page'],
            r'/web/css/': ['full_page'],
            r'/requirejs-config\.js': ['full_page'],
        }

        types = set()
        for pattern in rules:
            if re.findall(pattern, self.app.filepath):
                for cache_type in rules[pattern]:
                    types.add(cache_type)

        if len(types) > 0:
            types.add('full_page')

        return types

    def type(self, index=False):
        types = [
            'block_html',
            'config',
            'db_ddl',
            'full_page',
            'layout',
            'translate',
        ]

        if index is not False:
            return types[index]

        return list(types)
