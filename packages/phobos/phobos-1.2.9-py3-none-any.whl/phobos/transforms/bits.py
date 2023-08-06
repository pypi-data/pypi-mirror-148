import logging 
import numpy as np 

from albumentations import ImageOnlyTransform

__all__ = ["ToFloatChannelWise", "FromFloatChannelWise"]


class ToFloatChannelWise(ImageOnlyTransform):
    r""""Divide pixel values by `max_values` to get a float32 output array where all values lie in the range [0, 1.0].
   
    Parameters
    ----------
    max_values : channel-wise  max values
    
    Examples
    --------
    Create a ToFloatChannelWise instance

    >>> to_float = ToFloatChannelWise(max_values=[2000, 3000, 4000])

    Apply normalize transform on a mock image

    >>> image = np.ones([64, 64, 3]) * 3000 
    >>> image = to_float.apply(image)
    >>> norm[0, 0, :]
    array([0.67, 1.0, 1.34], dtype=float32)

    """    

    def __init__(self, max_values=(1, 1, 1), always_apply=False, p=1.0):
        super(ToFloatChannelWise, self).__init__(always_apply, p)
        self.max_values = np.array(max_values, dtype=np.float32)
        
    def apply(self, image, **params):
        logging.debug("Enter ToFLoatChannelWise apply routine")
        denominator = np.reciprocal(self.max_values, dtype=np.float32)

        img = np.array(image, dtype=np.float32)
        img *= denominator

        return img

    def get_transform_init_args_names(self):
        return ("max_values")


class FromFloatChannelWise(ImageOnlyTransform):
    r""""Take an input array where all values should lie in the range [0, 1.0], multiply them by `max_value` and then
    cast the resulted value to a type specified by `dtype`.
   
    Parameters
    ----------
    max_values : channel-wise  max values
    dtype :  data type of the output. See the `'Data types' page from the NumPy docs`_.
            Default: 'uint16'.
    
    Examples
    --------
    Create a FromFloatChannelWise instance

    >>> from_float = FromFloatChannelWise(dtype="uint16", max_values=[2000, 3000, 4000])

    Apply normalize transform on a mock image

    >>> image = np.ones([64, 64, 3])  
    >>> image = from_float.apply(image)
    >>> norm[0, 0, :]
    array([2000, 3000, 4000], dtype=float32)

    """    

    def __init__(self, dtype="uint16", max_values=(1, 1, 1), always_apply=False, p=1.0):
        super(FromFloatChannelWise, self).__init__(always_apply, p)
        self.dtype = np.dtype(dtype)
        self.max_values = np.array(max_values, dtype=np.float32)
        
    def apply(self, image, **params):
        logging.debug("Enter ToFLoatChannelWise apply routine")

        img *= self.max_values

        return img.astype(self.dtype)

    def get_transform_init_args_names(self):
        return ("dtype", "max_values")