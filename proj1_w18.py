
class Media:

	def __init__(self, title="No Title", author="No Author", year = "No Year"):
		self.title = title
		self.author = author
		self.release_year = year

	def __str__(self):
		return "{} by {} ({})".format(self.title, self.author, self.release_year)

	def __len__(self):
		return 0

## Other classes, functions, etc. should go here

if __name__ == "__main__":
	# your control code for Part 4 (interactive search) should go here
	pass
