import logging
import inspect 
from pydoc import locate 

__all__ = ["get_model"]

def get_model(args):
    assert len(args.model.keys()) == 1, logging.error("Only one model can be used")    
    model_name = list(args.model.keys())[0]
    if locate(model_name):
        margs = {} if args.model[model_name] is None else args.model[model_name]
        margs["input"] = args.input
        margs["output"] = args.output
        margs["responses"] = args.dataset.shard_keys.GeoJSON.questions

        model_func = locate(model_name)

        if not margs:
            model = model_func()
        else:
            model = model_func(**margs)
        
        model.to(args.device)
    else:
        raise Exception('Please provide correct key path as argument')
    
    return model 