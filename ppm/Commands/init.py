import json
import os
import re
import time


class InitCommand:
	def __init__(self):
		print("""This utility will walk you through creating a pyckage.json file.
It only covers the most common items, and tries to guess sensible defaults.

Use `ppm add <pkg> --save` afterwards to install a package and
save it as a dependency in the pyckage.json file.""")
		name = input('name: ')

		version = input('version: (1.0.0) ')
		if version == '':
			version = '1.0.0'

		description = input('description: ')

		entry_point = input('entry point: (app.py) ')
		if entry_point == '':
			entry_point = 'app.py'

		test_command = input('test command: ')
		git_repo = input('git reposirtory: ')
		key_words = input('keywords: ')
		author = input('author: ')
		license = input('license: (MIT) ')

		pyckage = {
			'name'       : name,
			'version'    : version,
			'description': description,
			'main'       : entry_point,
			'scripts'    : {
				'test': test_command
			},
			'author'     : author,
			'license'    : license
		}

		if git_repo != '':
			pyckage['repository'] = {
				'type': 'git',
				'url' : git_repo
			}

		if key_words != '':
			pyckage['keywords'] = re.findall(r'\w+', key_words)

		with open('pyckage.json', 'w') as file:
			json.dump(pyckage, file, indent=2)

		date = time.strftime(r'%d/%m/%Y', time.localtime())
		with open(entry_point, 'w') as file:
			file.write(
					f'# Created by {author} in {date}.\n'
					f'import {name}\n'
					'\n\n'
					'def main():\n'
					'    pass\n'
					'\n\n'
					"if __name__ == '__main__':\n"
					"    main()\n"
			)

		os.mkdir(name)
		with open(os.path.join(name, '__init__.py'), 'w') as file:
			file.write(
					f'# {name} created in {date}.\n'
			)
