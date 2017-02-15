import argparse
import json
import os
import re
import time

from typing import Dict, List


class InitCommand:
    prog = 'ppm init'
    description = 'Command to simply create a pyckage.json file'
    initial_text = """This utility will walk you through creating a pyckage.json file.
It only covers the most common items, and tries to guess sensible defaults.

Use `ppm add <pkg> --save` afterwards to install a package and
save it as a dependency in the pyckage.json file."""

    def __init__(self):
        print(self.initial_text)

        self._parser = argparse.ArgumentParser(
                prog=self.prog,
                description=self.description
        )

    def main(self, args: List[str]):
        self._parser.parse_args(args)
        pyckage = self.get_info()
        pyckage_parsed = self.parse_info(pyckage)
        self.write_on_disk(pyckage_parsed)

    @staticmethod
    def parse_info(pyckage: Dict[str, str or dict]) -> Dict[str, str or dict]:
        if pyckage['version'] == '':
            pyckage['version'] = '1.0.0'

        if pyckage['main'] == '':
            pyckage['main'] = 'app.py'

        if pyckage['repository'].get('url') == '':
            del pyckage['repository']

        if pyckage['keywords'] != '' and type(pyckage['keywords']) == str:
            pyckage['keywords'] = re.findall(r'\w+', pyckage['keywords'])
        elif pyckage['keywords'] == '':
            del pyckage['keywords']
        elif type(pyckage['keywords']) != list:
            # This shouldn't happen, ever
            raise TypeError('keywords field must be a list')

        return pyckage

    @staticmethod
    def get_info() -> Dict[str, str or dict]:
        name = input('name: ')

        version = input('version: (1.0.0) ')

        description = input('description: ')

        entry_point = input('entry point: (app.py) ')

        test_command = input('test command: ')
        git_repo = input('git repository: ')
        key_words = input('keywords: ')
        author = input('author: ')
        license = input('license: (MIT) ')

        return {
            'name'       : name,
            'version'    : version,
            'description': description,
            'main'       : entry_point,
            'scripts'    : {
                'test': test_command
            },
            'author'     : author,
            'license'    : license,
            'repository' : {
                'type': 'git',
                'url' : git_repo
            },
            'keywords'   : key_words
        }

    def write_on_disk(self, pyckage: Dict[str, str or dict]):
        with open('pyckage.json', 'w') as file:
            json.dump(pyckage, file, indent=2)

        with open(pyckage["main"], 'w') as file:
            main_file_text = self.main_template(pyckage)
            file.write(main_file_text)

        os.mkdir(pyckage["name"])
        with open(os.path.join(pyckage["name"], '__init__.py'), 'w') as file:
            init_text = self.init_template(pyckage['name'])
            file.write(init_text)
        with open(os.path.join(pyckage["name"], '__main__.py'), 'w') as file:
            init_text = self.init_template(pyckage['name'])
            file.write(init_text)

    @staticmethod
    def init_template(name: str) -> str:
        date = time.strftime(r'%d/%m/%Y', time.localtime())
        return f"# {name} created in {date}"

    @staticmethod
    def main_template(options: Dict[str, str or dict]) -> str:
        date = time.strftime(r'%d/%m/%Y', time.localtime())
        return \
            f"# Created by {options['author']} in {date}\n" \
            f"import {options['name']}\n" \
            f"\n\n" \
            f"def main():\n" \
            f"    pass\n" \
            f"\n\n" \
            f"if __name__ == '__main__':\n" \
            f"    main()\n"
