import json

class Media:
    """ base class for CD or DVD """
    def __init__(self,**kwargs):
        self.title = kwargs.get('title')
        self.length = kwargs.get('length',0)
        self.language = kwargs.get('language')
        self.subject = kwargs.get('subject')
        self.artists = kwargs.get('artists',[])
        self.quality = kwargs.get('quality')

    # do data validation for length in a property setter
    # to make sure it is a number > 0
    @property
    def length(self):
        return self._length
    @length.setter
    def length(self,value):
        try:
            self._length = float(value)
        except ValueError:
            raise ValueError('length must be a number')
        if self._length < 0:
            raise ValueError('length must be a positive number')

    def display(self):
        return '{}: {}'.format(self.title,self.length)

class Track:
    """ track class. there can be multiple tracks on a CD """
    def __init__(self,**kwargs):
        self.title = kwargs.get('title')
        self.artists = kwargs.get('artists',[])
        self.length = kwargs.get('length')
    def __repr__(self):
        print('Track.__repr__()')
        return str(vars(self))

class CD(Media):
    def __init__(self,**kwargs):
        Media.__init__(self,**kwargs)
        self.tracks = kwargs.get('tracks',[])
    def __repr__(self):
        print('CD.__repr__()')
        return str(vars(self))

class DVD(Media):
    def __init__(self,**kwargs):
        Media.__init__(self,**kwargs)
        self.director = kwargs.get('director')
        self.dolby = kwargs.get('dolby')
        self.mpaa = kwargs.get('mpaa')

def enter_cls(cls,prefix=None):
    field_types = {
        'tracks' : Track
    }
    prefix = '' if prefix is None else prefix + '.'
    obj = cls()
    fields = []
    for k in vars(obj).keys():
        if k.startswith('_'):
            fields.append(k[1:])
        else:
            fields.append(k)
    fields = sorted(fields)
    field_width = max([len(f) for f in fields])

    for f in fields:
        while True:
            try:
                fld_cls = field_types.get(f)
                if fld_cls is not None:
                    if isinstance(getattr(obj,f),list):
                        entries = []
                        while True:
                            x = enter_cls(fld_cls,f)
                            entries.append(x)
                            if input('more {} (y/n)?'.format(f)).lower() != 'y':
                                break
                        x = entries
                else:
                    x = input('{0}{1:{2}}: '.format(prefix,f,field_width))
                    if isinstance(getattr(obj,f),list):
                        x = [v.strip() for v in x.split(',')]
                setattr(obj,f,x)
                break
            except ValueError as e:
                print('{}: {}'.format(f,e))

    return obj

def enter_media():
    lookup = {
        'dvd': DVD,
        'cd': CD
    }
    what = input('Enter type of media (CD or DVD): ')
    cls = lookup.get(what.lower())
    if cls is None: return what.upper(), None
    obj = enter_cls(cls)
    return what.upper(),obj

def enter():
    library = []    
    while True:
        what, obj = enter()
        if obj is None:
            break
        print('{}: {}'.format(what,vars(obj)))
        library.append({what.lower():vars(obj)})

    with open('media.json','w') as fp:
        json.dump(library,fp)


