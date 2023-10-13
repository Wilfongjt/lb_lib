from source.stack import Stack

class DDict(dict):

    def get(self, stack):
        rc = None
        if stack.size() == 0:
            rc=None
        elif stack.size() == 1:
            rc = self[stack[0]]
        elif stack.size() == 2:
            rc = self[stack[0]][stack[1]]

        #print('get dict ', dt)
        #print('get stack', stack)
        #print('get rc', rc)
        return

    def set(self, stack_key, value):
        # values are {}, [], number, alfa
        # stack_key is all keys no values eg
        # replace when stack_key exists
        # add all elements of stack key when stack_key does not exist
        #print('in ',self)
        p = self.sett(self, stack_key, value)
        #print('out', self)

        return self

    def sett(self, data, keys, value):
        #print('    sett data ', data)
        #print('     keys ', keys)
        #print('     value', value)
        if isinstance(data, dict):
            if len(keys) == 0:
                #print('          dict A ', self)
                return None  # No keys left to search; return None
            key = keys[0]
            if key in data:
                if len(keys) == 1:
                    if isinstance(data[key],list):
                        #print('          dict 1B', self)
                        data[key].append(value)
                    else:
                        #print('          dict B2', self)
                        data[key]=value  # Found the final key; set its value
                    return self
                else:
                    #print('          dict C', self)
                    return self.sett(data[key], keys[1:], value)  # Recurse with the remaining keys
            else:
                if len(keys) == 1:
                    data[key] = value
                    #print('         dict D1', self)
                else:
                    data[key]={}
                    #print('         dict D2', self)
                    return self.sett(data[key], keys[1:], value)  # Recurse with the remaining keys

                return self
        elif isinstance(data, list):
            #print('         list A', self)
            data.append(value) # untested
        else:
            print('unknown', data)
        #print('         out', data)
        return None  # Key not found in the dictionary



def main():
    '''
    actual = LbConfigMd()
    assert (actual)
    #assert (actual.toJSON() == {})
    assert (actual.set_md_text(md).toJSON()=={'project': {'name': ' example', 'tp': ' paper'}})
    '''
    stack_key=Stack()
    ddt=DDict()
    assert(ddt=={})
    assert(ddt.set(Stack().push('project'), []) == {'project': []})
    assert(ddt.set(Stack().push('project'), 'A') == {'project': ['A']})
    assert(ddt.set(Stack().push('project'), 1) == {'project': ['A', 1]})
    assert(ddt.set(Stack().push('project'), {}) == {'project': ['A', 1, {}]})
    ddt.clear()
    assert(ddt.set(Stack().push('project').push('a'), 'A') == {'project': {'a': 'A'}} )
    assert(ddt.set(Stack().push('project').push('a'), 'B') == {'project': {'a': 'B'}} )
    assert(ddt.set(Stack().push('project').push('a'), 1) == {'project': {'a': 1}} )
    assert(ddt.set(Stack().push('project').push('a'), 2) == {'project': {'a': 2}} )

    assert(ddt.set(Stack().push('project').push('a'), {}) == {'project': {'a': {}}} )
    assert(ddt.set(Stack().push('project').push('a'), []) == {'project': {'a': []}} )
    assert(ddt.set(Stack().push('project').push('a'), 'A') == {'project': {'a': ['A']}} )
    assert(ddt.set(Stack().push('project').push('a'), 'B') == {'project': {'a': ['A', 'B']}} )


if __name__ == "__main__":
    # execute as script
    main()