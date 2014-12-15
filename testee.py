def fib(n):
    if n < 0:
        raise ValueError, "n < 0"
    if n > 1:
        return fib(n-1) + fib(n-2)
    return 1

def fib2(n):
    "fib() that guarantees it is dealing with ints."
    if n < 0:
        raise ValueError, "n < 0"
    n = int(n)
    if n > 1:
        return fib2(n-1) + fib2(n-2)
    return 1
  
def main():
  print "fib(5) ==", fib(5)
  print "fib(4.0) ==", fib(4.0)
  print "fib2(5) ==", fib2(5)
  print "fib2(4.0) ==", fib2(4.0)
