from pynestor import *

abloc = NestorInstance("abloc")
desc = NestorDescSet()
for opt in abloc.show("spec").split(","):
    key, value = opt.split("=")
    desc.add(NestorOpt(key, value))
print(desc.to_str(True))
