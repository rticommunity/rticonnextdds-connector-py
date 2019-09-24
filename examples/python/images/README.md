# Example: Images

## Example description
In this example `image_writer.py` publishes images at a set rate.
`image_reader.py` polls every certain amount of time to retrieve the last
received image and display it.

This example shows how to manipulate a more complex type.

## Running the example
This examples requires the Python packages **matplotlib** and **numpy**:

    $ pip install matplotlib numpy

To run the example, in different shells, run any number of instances of the writer and the reader in any order:

    $ python image_writer.py
    $ python image_reader.py

`image_reader.py` requires a graphical backend for *matplotlib*. If your python
installation doesn't have one, you can run `image_reader_file.py` instead, which
will save the last image into a file called *image.png*.

