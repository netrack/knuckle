import numpy
import tensorflow as tf


class InputShapeError(Exception):
    """Exception raised for invalid model input shape

    Attributes:
        expected_dims -- model's dimensions
        actual_dims -- input dimensions
    """

    def __init__(self, expected_dims, actual_dims):
        self.expected_dims = tuple(expected_dims)
        self.actual_dims = tuple(actual_dims)

    def __str__(self):
        return ("Input shape is '{expected_dims}', while "
                "'{actual_dims}' is given.").format(
                    expected_dims=self.expected_dims,
                    actual_dims=self.actual_dims)


class Model:

    def __init__(self, name: str, tag: str, model=None):
        self.model = model
        self.name = name
        self.tag = tag

    def predict(self, x):
        self.model.summary()

        x = numpy.array(x)

        # Calculate the shape of the input data and validate it with the
        # model parameters. This exception is handled by the server in
        # order to return an appropriate error to the client.
        _, *expected_dims = self.model.input_shape
        _, *actual_dims = x.shape

        if expected_dims != actual_dims:
            raise InputShapeError(expected_dims, actual_dims)

        return self.model.predict(x).tolist()

    def todict(self):
        return dict(name=self.name, tag=self.tag)

    def __str__(self):
        return "Model(name={0}, tag={1})".format(self.name, self.tag)