from TableGenerator import *
'''
options = Options()

print(options.font_size)

print(options.__dict__)

# Example usage
for option in options:
    print(option)

'''

#startProcess('tables/')
options = Options()

#GenerateOneTable('tables/default.pdf', options.__default__)

options_example = options.__default__
options_example[OptionsENUM.WITH_LINES.value] = True
options_example[OptionsENUM.TEXT_ALIGNMENT.value] = "C"
options_example[OptionsENUM.COLORED_UNEVEN_ROWS.value] = True
options_example[OptionsENUM.COLORED_HEADER.value] = False
print(str(options_example))

GenerateOneTable('tables/testingnewfunctions.pdf', options_example)

#for option in options.__dict__:
#    print(option)
