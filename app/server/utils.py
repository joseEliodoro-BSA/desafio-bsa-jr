def fibonacci(n: int) -> int:
  """Calcula o n-ésimo número da sequência de Fibonacci.

  A sequência de Fibonacci é definida como:\n
  F(0) = 0\n
  F(1) = 1\n
  F(n) = F(n-1) + F(n-2), para n > 1

  :param n: int - A posição desejada na sequência de Fibonacci (n >= 0)
  :return: int - O valor do n-ésimo número de Fibonacci
  """
  if(not(isinstance(n, int))):
    raise TypeError("n só aceita valores inteiros positivos")
  
  if(n < 0):
    raise ValueError("n não aceita valor negativo")

  if n == 0: return 0

  a, b = 0, 1
  for _ in range(1, n):
    a, b = b, a+b
    
  return b