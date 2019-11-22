# Example: Data Transformation

## Example description
In this example `transform.py` subscribes to the *Square* topic, applies
a simple transformation to the data it receives, and publishes it into a topic of
the same type, *Circle*.

## Running the example
To run the example:

* Run any *DDS* application that publishes the *Square* topic. For example, run
  `python ../simple/writer.py`; or run
  [RTI Shapes Demo](https://www.rti.com/free-trial/shapes-demo) and create
  a *Square* publisher.
* Run any *DDS* application that subscribes to the *Circle* topic. For example,
  run `python reader.py`; or run
  [RTI Shapes Demo](https://www.rti.com/free-trial/shapes-demo) and create a
  *Circle* subscriber.
* Run the transformation application: `python transform.py`