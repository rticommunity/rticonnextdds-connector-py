from docutils.core import publish_doctree

s = '''

My title
========

Use this to square a number.

.. code:: python

   def square(x):
       return x**2

and here is some javascript too.

.. code:: javascript

    foo = function() {
        console.log('foo');
    }

This is also code::

    foo = alex()
    x = 3

'''

def is_code_block(node):
    print ("Alex - ")
    print(type(node))
    print (node)
    return (node.tagname == 'literal_block')

with open('input.rst', 'r') as content_file:
    content = content_file.read()

doctree = publish_doctree(content)
code_blocks = doctree.traverse(condition=is_code_block)
source_code = [block.astext() for block in code_blocks]

print(len(source_code))
for c in source_code:
    print("*****")
    print(c)
