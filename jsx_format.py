import sublime, sublime_plugin
import subprocess,os,sys

directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(directory)

import merge_util


PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))

# debug with view.run_command('jsx_format')
class JsxFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):

		formatScript = os.path.join(PLUGIN_FOLDER, 'cmd.js')

		region = sublime.Region(0, self.view.size())
		code = self.view.substr(region)

		try:
			child = subprocess.Popen(['node',formatScript],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE ,shell=True)
			formatedCode,err = child.communicate(input=code.encode('utf-8'))
			if err:
				sublime.status_message('esformat filed');
				return
			_, err = merge_util.merge_code(self.view, edit, code, formatedCode.decode('utf-8'))
			if err:
				sublime.error_message("JsFormat: Merge failure: '%s'" % err)
		except Exception as e :
			print('JSX Format Error:',e)
			sublime.error_message("JsFormat: Merge failure" )
			pass
		else:
			pass
		finally:
			pass

def is_jsx(view):
	fName = view.file_name()
	vSettings = view.settings()
	syntaxPath = vSettings.get('syntax')
	syntax = ""
	ext = ""

	if (fName != None):
		ext = os.path.splitext(fName)[1][1:]
	if(syntaxPath != None):
		syntax = os.path.splitext(syntaxPath)[0].split('/')[-1].lower()
	return ext in ['jsx', 'JSX'] or "jsx" in syntax

class JsxFormatEventListeners(sublime_plugin.EventListener):
	@staticmethod
	def on_pre_save_async(view):
		if is_jsx(view):
			view.run_command("jsx_format");
		else:
			print('JSXFormat','byebye');