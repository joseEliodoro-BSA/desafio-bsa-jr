class Message:
  SERVER_DISCONNECTED = "Servidor encerrou a conexão"
  CLIENT_DISCONNECTED = "Cliente encerrou a conexão"
  UNEXPECTED_ERROR_SERVER = "Ocorreu um erro inesperado"
  
  @staticmethod
  def CONNECT_ERROR(e: str):
    return "Erro ao conectar: %s" % e