class Error:
  def __init__(self):
    self.total = 0
    self.errores = []

  def reportar_error(self, num_linea, tipo_error, mensaje):
    self.total += 1
    self.errores.append("ln# {}: Error {}: {}".format(num_linea, tipo_error, mensaje))
