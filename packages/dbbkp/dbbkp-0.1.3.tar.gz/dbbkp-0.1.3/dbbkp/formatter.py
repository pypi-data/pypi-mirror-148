import utilum
from sql_formatter.core import format_sql


# fileReadPath = "input.sql"
# fileWritePath = "output.sql"
fw1 = "output1.sql"
fw2 = "output2.sql"

class Config:
    language= "spark", # Defaults to "sql" (see the above list of supported dialects)
    indent= " ", # Defaults to two spaces
    uppercase= True, # Defaults to false
    linesBetweenQueries= 2, # Defaults to 1

config = Config()
DEV_MODE = False


def process(fileReadPath, fileWritePath):
  # print("<formatter.process>")
  originalOutput = utilum.file.readFile(fileReadPath)
  formattedOutput = originalOutput;
  formattedFinalOutput = formattedOutput.replace("),(", "),\n(").replace(");",")\n;").replace("),\n(",")\n,(")
  # .replace(",\n  ", ",").replace("\n;", ";").replace(";\n", ";").replace("(\n", "(").replace("\n )", ")")

  o1 = format_sql(originalOutput)
  o2 = format_sql(formattedOutput)

  if (o1 == o2):
      utilum.file.clearFile(fileWritePath)
      utilum.file.writeFile(fileWritePath, formattedFinalOutput)
  else:
    if (DEV_MODE):
      utilum.file.clearFile(fw1)
      utilum.file.writeFile(fw1, o1)
      utilum.file.clearFile(fw2)
      utilum.file.writeFile(fw2, o2)
    # pass
    # No Re-write since original file is not same formatted file
  # print("</formatter.process>")