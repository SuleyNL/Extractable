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

GenerateOneTable('tables/default.pdf', **options.__default__)

for option in options.__dict__:
    print(option)

