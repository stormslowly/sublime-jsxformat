import sublime, sublime_plugin


# debug with view.run_command('jsx_format')
class JsxFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# self.view.insert(edit, 0, "Hello, World!")
		region = sublime.Region(0, self.view.size())
		code = self.view.substr(region)
		print(code)