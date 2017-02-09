import time
import unittest

from ppm.Commands.init import InitCommand


class InitTests(unittest.TestCase):
	def setUp(self):
		pass

	def testParseInfo(self):
		self.assertEqual(InitCommand.parse_info({
			'version'   : '1.3.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'https://github.com/luisholanda/ppm.git'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		}), {
			'version'   : '1.3.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'https://github.com/luisholanda/ppm.git'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		})
		self.assertEqual(InitCommand.parse_info({
			'version'   : '',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'https://github.com/luisholanda/ppm.git'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		}), {
			'version'   : '1.0.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'https://github.com/luisholanda/ppm.git'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		})
		self.assertEqual(InitCommand.parse_info({
			'version'   : '1.3.0',
			'main'      : '',
			'repository': {
				'type': 'git',
				'url' : 'https://github.com/luisholanda/ppm.git'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		}), {
			'version'   : '1.3.0',
			'main'      : 'app.py',
			'repository': {
				'type': 'git',
				'url' : 'https://github.com/luisholanda/ppm.git'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		})
		self.assertEqual(InitCommand.parse_info({
			'version'   : '1.3.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : ''
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		}), {
			'version' : '1.3.0',
			'main'    : 'main.py',
			'keywords': [
				'a',
				'b',
				'c'
			]
		})
		self.assertEqual(InitCommand.parse_info({
			'version'   : '1.3.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'abc'
			},
			'keywords'  : 'a, b, c'
		}), {
			'version'   : '1.3.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'abc'
			},
			'keywords'  : [
				'a',
				'b',
				'c'
			]
		})
		self.assertRaises(TypeError, InitCommand.parse_info, {
			'version'   : '1.3.0',
			'main'      : 'main.py',
			'repository': {
				'type': 'git',
				'url' : 'abc'
			},
			'keywords'  : 4
		})

	def testInitTemplate(self):
		self.assertEqual(
				InitCommand.init_template('test1'),
				f'# test1 created in {time.strftime(r"%d/%m/%Y", time.localtime())}'
		)
		self.assertEqual(
				InitCommand.init_template('test2'),
				f'# test2 created in {time.strftime(r"%d/%m/%Y", time.localtime())}'
		)

	def testMainTemplate(self):
		self.assertEqual(InitCommand.main_template({
			'author': 'me',
			'name'  : 'test1'
		}),
				f"# Created by me in {time.strftime(r'%d/%m/%Y', time.localtime())}\n"
				"import test1\n"
				"\n\n"
				"def main():\n"
				"    pass\n"
				"\n\n"
				"if __name__ == '__main__':\n"
				"    main()\n"
		)


if __name__ == '__main__':
	unittest.main()
