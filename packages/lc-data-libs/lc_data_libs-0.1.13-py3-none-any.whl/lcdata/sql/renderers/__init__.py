from jinja2 import meta, Environment, PackageLoader, ChoiceLoader, FileSystemLoader, Undefined, pass_context
from lcdata.utils.python import czip, isiterable, to_list
import datetime, os, itertools
from operator import getitem

class StreamableUndefined(Undefined):
  """
  Unlike StrinctUndefined, it can be iterated and evaluates to false
  """
  __str__ = __eq__ =   __ne__ =  __hash__ = __unicode__ = __iter__ = Undefined._fail_with_undefined_error

  def __getattr__(self, key):
    if key == 'stream':
      return False
    else:
      Undefined._fail_with_undefined_error(self)



class IterCount(object):
  def __init__(self):
    self.iter_count = itertools.count()
    self.current = None

  def reset(self):
    self.iter_count = itertools.count()

  def next(self):
    self.current = next(self.iter_count)
    return self.current

class Renderer(Environment):
  """

  Args:
    module (str): module where templates are stored
    templates_dirs (list of str): directories (relative to the module) where templates are stored
    filters_dict (dict): directory with custom filter functions.
    functions_dict (dict): directory with custom functions
    global_variables_dict (dict): directory with global variables
    streamable: (bool) it true, the filter 'stream' can be used, which allows a filter to be applies to element-wise to a list
      eg. a=['a','b','c']; {{ a | stream | upper }} = ['A','B','C']
  """

  def __init__(self, module, templates_dirs, filters_dict=None, functions_dict=None, global_variables_dict=None, streamable=True):

    filters_dict = filters_dict or FILTERS
    functions_dict = functions_dict or FUNCTIONS
    global_variables_dict = global_variables_dict or {}

    # Init environment
    super(Renderer,self).__init__(
      loader = ChoiceLoader([ PackageLoader(module, d) for d in templates_dirs]),
      undefined=StreamableUndefined,
      trim_blocks=True,
      lstrip_blocks=True
    )

    # Add custom filters and functions
    self.filters.update(filters_dict)
    self.globals.update(functions_dict)
    self.globals.update(global_variables_dict)

    # add iter_count
    self.iter_count = IterCount()
    self.globals['iter_count'] = self.iter_count

    # Make all filters streamable
    if streamable:
      self.filters = {k: streamablefilter(v) for k, v in list(self.filters.items())}

  def add_path(self, new_path):
      loaders = self.loader.loaders
      loaders.insert(0,FileSystemLoader(new_path))
      self.loader = ChoiceLoader(loaders)

  def render_file(self, template_file_name, variables=None, **kwargs):
    template = self.get_template(template_file_name)
    variables = {**(variables or {}), **kwargs}
    return template.render(variables)

  def render_str(self, string, variables=None, **kwargs):
    template = self.from_string(string)
    variables = {**(variables or {}), **kwargs}
    return template.render(variables)

  def get_file_variables(self, template_file_name):
    source = self.loader.get_source(self,template_file_name)[0]
    return self.get_string_variables(source)

  def get_string_variables(self, string):
    return meta.find_undeclared_variables(self.parse(string))

  def get_macros(self):

      def insert_in_edict(cdict_obj, location, obj):
          if len(location) == 1:
              setattr(cdict_obj,location[0], obj)
          else:
              if not hasattr(cdict_obj,location[0]):
                  setattr(cdict_obj, location[0], type('cdict', (), {}))
              insert_in_edict(getattr(cdict_obj,location[0]),location[1:],obj)

      # list all files in <dir>/macros/...
      files = set()
      for loader in self.loader.loaders:
          dir = os.path.join(loader._loader.path.rsplit('/',1)[0],loader.package_path,'macros')
          for r, d, f in os.walk(dir):
              for file in f:
                  path = os.path.join(r,file)
                  path = path.split('/macros/',1)[1]
                  files.add(path)

      # get all macros
      macros = type('cdict',(),{})
      for f in files:
        locations = str(f).rsplit('.',1)[0].split('/')
        insert_in_edict(macros, locations, self.get_template('/macros/' + f).module)
      return macros

# ------------------------------------------------------------------
# ------------------------ STREAMABLE  -----------------------------
# ------------------------------------------------------------------


def streamablefilter(f):
  """
  Decorator to make filter streamable: filter can accept an optional keyword 'stream' that when true,
    assumes 'value' is iterable and tries to apply the filter to each element
  """
  if hasattr(f,'jinja_pass_arg'):
    def wrapper(context, value, *args,**kwargs):
      stream = kwargs.pop('stream',False)
      if stream:
        return [f(context, v, *args,**kwargs) for v in value]
      else:
        return f(context, value, *args,**kwargs)
    wrapper.jinja_pass_arg = f.jinja_pass_arg

  else:
    def wrapper(value,*args,**kwargs):
      stream = kwargs.pop('stream', False)
      if stream:
        return [f(v,*args,**kwargs) for v in value]
      else:
        return f(value,*args,**kwargs)

  return wrapper


# ---------------------------------------------------------------------------------------
# ------------------------ CUSTOM FUNCTIONS AND FILTERS ---------------------------------
# ---------------------------------------------------------------------------------------

#-- FUNCTIONS

def do_zip(*values):
  return list(zip(*values))

def do_czip(*values):
  return czip(*values)

def do_now(format="%Y-%m-%d %H:%M:%S"):
  return datetime.datetime.utcnow().strftime(format)

def do_neg(values):
  return [not v for v in values]

#-- FILTERS

def do_apply(value, function, *args):
  return function(value,*args)

def do_fequals(value, t1, t2):
  return '%s.%s = %s.%s' % (t1,value,t2,value)

def do_invformat(value, format):
  try:
    return format % value
  except TypeError:
    if isiterable(value):
      return format.format(*value)
    else :
      return format.format(value)

def do_fix(value, interpret_str=False):

  # STRING
  if isinstance(value,str):
    if not interpret_str:
      return "'%s'" % value
    # INTERPRETED STRING
    else:
      if value[0]+value[-1] in ('""',"''"):
        return value
      elif value.lower()=='null':
          return 'NULL'
      elif value.lower()=='true':
        return 'TRUE'
      elif value.lower()=='false':
        return 'FALSE'
      elif value[0]+value[-1] == '[]':
        return '[' + ', '.join([do_fix(v,interpret_str) for v in to_list(value[1:-1])]) + ']'
      try:
        date_format = '%Y-%m-%d %H:%M:%S' if ' ' in value else '%Y-%m-%d'
        datetime.datetime.strptime(value, date_format)
        return "CAST('%s' AS TIMESTAMP)" % value
      except ValueError:
        pass
      try:
        float(value)
        return value
      except ValueError:
        pass
      return "'%s'"%value
  # NULL
  elif value is None or str(value).lower() in ('null','nan'):
    return 'NULL'
  # TRUE et FALSE
  elif value is True:
    return 'TRUE'
  elif value is False:
    return 'FALSE'
  # LIST
  elif isiterable(value):
    return '[' + ', '.join([do_fix(v,interpret_str) for v in value]) + ']'
  # DATE
  elif isinstance(value, datetime.datetime):
    date_str = datetime.datetime.strftime(value,'%Y-%m-%d %H:%M:%S')
    return "CAST('%s' AS TIMESTAMP)" % date_str
  # NUMERIC, etc..
  else:
    return value

def do_intersection(set1,set2):
  return set(set1) & set(set2)

def do_union(set1,set2):
  return set(set1) | set(set2)

def do_difference(set1,set2):
  return set(set1) - set(set2)

def do_getitem(lst,index):
  return getitem(lst,index)

def do_getslice(lst,start,end):
  return getitem(lst,slice(start,end))

def do_flatten(lst):
  return [e for l in lst for e in l]

try:
    from lcdata.utils.sql import ensure_dataset
    @pass_context
    def do_ensure_dataset(context,table_name):
      return ensure_dataset(table_name,context.parent['constants'])
except Exception as e:
    def do_ensure_dataset(context,table_name):
      raise e


FILTERS = {
  'fix' : do_fix,
  'invformat' : do_invformat,
  'fequals' : do_fequals,
  'intersection' : do_intersection,
  'union' : do_union,
  'difference' : do_difference,
  'getitem' : do_getitem,
  'getslice' : do_getslice,
  'flatten' : do_flatten,
  'apply': do_apply,
  'ensure_dataset' : do_ensure_dataset,

}

FUNCTIONS = {
  'zip' : do_zip,
  'czip' : do_czip,
  'now' : do_now,
  'neg' : do_neg
}



_RENDERERS = {}

def get_renderer(name=None):

    if name in _RENDERERS.keys():
      return _RENDERERS[name]

    else:
        if name is None:
            name = 'general'
            templates_dirs = []
            global_variables_dict = None
        else:
            from lcdata.sql.constants import get_constants, BIGQUERY
            if name == BIGQUERY:
               templates_dirs = ['templates/bigquery/']
               global_variables_dict = {'constants': get_constants(name)}

        renderer = Renderer(
            module='lcdata.sql',
            templates_dirs=templates_dirs,
            filters_dict=FILTERS,
            functions_dict=FUNCTIONS,
            global_variables_dict=global_variables_dict
        )
        renderer.name = name
        _RENDERERS[name] = renderer
        return renderer
