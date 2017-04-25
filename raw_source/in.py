""" Crosswalks INEGI murder data into year-month-city row form. """

import csv
import unidecode
import unicodedata

def transcode(fix_text):
	""" Runs transcode. """
	results = [["Year", "Month", "ID", "State", "City", "Murders"]]
	for y in xrange(1990, 2016):
		filename = str(y)+".csv"
		with open(filename, "rb") as f:
			read = csv.reader(f, delimiter=",", quotechar='"')
			for r in read:
				if len(r) < 10:
					continue

				if not len(r[0].strip()):
					continue

				if r[0].strip().startswith("=CONCAT"):
					if fix_text:
						state = unidecode.unidecode(r[1].strip().decode("iso-8859-1"))
					else:
						state = r[1].strip()
					continue

				for m in xrange(3, 15):
					murders = str(0)
					if r[m]:
						murders = str(int(r[m].replace(",","")))

					if fix_text:
						city = unidecode.unidecode(r[1].strip().decode("iso-8859-1"))
					else:
						city = r[1].strip()

					new_line = [y, m-2, r[0].strip(), state, city, murders]
					results.append(new_line)

	if fix_text:
		out_file_name = "out-fixed.csv"
	else:
		out_file_name = "out.csv"

	with open(out_file_name, "wb") as f:
		out = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
		for result in results:
			try:
				out.writerow(result)
			except:
				print result

	print len(results)

if __name__ == "__main__":
	transcode(0)
	transcode(1)
