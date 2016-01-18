
class Param(object):
    def __init__(self, name, default, value, description, value_type, value_lower_bound=None, value_upper_bound=None):
        self.name=name
        self.default=default
        self.value=value
        self.description=description
        self.value_type=value_type
        self.value_lower_bound=value_lower_bound
        self.value_upper_bound=value_upper_bound

    def __repr__(self):
        return self.name

    def setValue(self, val):

        if self.value_type=="file" or self.value_type=="File":
            if type(val)==str:
                self.value=val
        elif self.value_type=="float" or self.value_type=="integer":

            if self.value_type=="float":
                val=float(val)
            elif self.value_type=="integer":
                val=int(val)


            if self.value_lower_bound is not None:
                if val>=self.value_lower_bound:
                    if self.value_upper_bound is not None:
                        if val<=self.value_upper_bound:
                            self.value=val
                    else:
                        self.value=val
            else:
                if self.value_upper_bound is not None:
                    if val<self.value_upper_bound:
                        self.value=val
        elif self.value_type=="boolean":
            if val=="true" or val=="True" or val==True or val=="false" or val=="False" or val==False:
                self.value=val
        elif self.value_type=="list":
            if type(val)==list or type(val)==tuple:
                if self.value_lower_bound is not None:
                    if len(val)>=self.value_lower_bound:
                        if self.value_upper_bound is not None:
                            if len(val)<=self.value_upper_bound:
                                self.val=val
        else:
            print("Type of value for parameter: ", self.name, "Unclear! type() returns ", type(val), ". The parameter was set but please update the corresponding conf file")
            self.val=val

def paramsFromJson(path):
    import json
    with open(path, 'r') as f:
        param_json=json.loads(f.read())
    parameters=[]
    for name, p in param_json.items():
        parameters.append(Param(
            name,
            p["default"],
            p["value"],
            p["description"],
            p["value_type"],
            p["value_lower_bound"],
            p["value_upper_bound"]
            ))
    return parameters


def jsonFromParams(path, params_list):
    import json
    param_dict={}

    for p in params_list:

        param_dict[p.name]={
            "default": p.default,
            "value": p.value,
            "description": p.description,
            "value_type": p.value_type,
            "value_lower_bound": p.value_lower_bound,
            "value_upper_bound": p.value_upper_bound
        }
    j=json.dumps(param_dict, indent=2)

    with open(path, 'w') as f:
        f.write(j)
    return 0
