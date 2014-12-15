import sys
import trace
import testee
import inspect
import os.path

class Accumulator(object):
  def __init__(self):
    self.values = []
    self.types = {}  #: maps type to number of occurences

  def __repr__(self):
    return repr(self.types)

  def accumulate(self, value):
    #self.values.append(value)
    t = type(value)
    try:
      self.types[t] += 1
    except KeyError:
      self.types[t] = 1

# maps code objects to (map that maps variable name to Accumulator object)
locations = {}

def trace_function(frame, why, arg):
  #print "trace: frame=%s, why=%s, arg=%s" % (frame, why, arg)
  #print "Name: ", frame.f_code.co_name
  #print "Names: ", frame.f_code.co_names
  #print "Number of args: ", frame.f_code.co_argcount
  #print "Cellvars: ", frame.f_code.co_cellvars
  #print "Freevars: ", frame.f_code.co_freevars
  #print "varnames: ", frame.f_code.co_varnames
  arg_names, vararg_name, kwarg_name, variables = inspect.getargvalues(frame)
  try:
    location = locations[frame.f_code]
  except KeyError:
    location = {}
    locations[frame.f_code] = location
  for arg in arg_names:
    #print arg, "=", variables[arg], type(variables[arg])
    value = variables[arg]
    try:
      location[arg].accumulate(value)
    except KeyError:
      location[arg] = Accumulator()
      location[arg].accumulate(value)

  #print "getargvalues", inspect.getargvalues(frame)
  #print "inspect", inspect.formatargvalues(*inspect.getargvalues(frame))

sys.settrace(trace_function)
try:
  import testee
  testee.main()
finally:
  sys.settrace(None)

for code, location in locations.iteritems():
  sys.stdout.write("%s (%s:%s)\n" % (code.co_name, os.path.basename(code.co_filename), code.co_firstlineno))
  sys.stdout.write("%d arguments\n" % code.co_argcount)
  for i in xrange(code.co_argcount):
    arg_name = code.co_varnames[i]
    #print "  " + arg_name
    sys.stdout.write('  ')
    sys.stdout.write(arg_name)
    sys.stdout.write(':')
    for typ, count in location[arg_name].types.iteritems():
      sys.stdout.write(" %s (%d)" % (typ, count))
    sys.stdout.write("\n")
  sys.stdout.write("\n")
#import pprint
#pprint.pprint(locations)

sys.exit()

# create a Trace object, telling it what to ignore, and whether to
# do tracing or line-counting or both.
tracer = trace.Trace(
    ignoredirs=[sys.prefix, sys.exec_prefix],
    trace=1,
    count=1, countfuncs=1, countcallers=1
    )

# run the new command using the given tracer
tracer.run('testee.main()')

# make a report, placing output in /tmp
r = tracer.results()
r.write_results(show_missing=True, coverdir="/tmp")
