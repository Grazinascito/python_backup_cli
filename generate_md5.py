import hashlib


""" Limitamos o valor do chunk em 8MB """
CHUNK_SIZE = 8 * 1024 * 1024

def generate_md5(path, chunk_size = CHUNK_SIZE):
   """Computa o digest MD5 (128 bits, hex) do conteúdo de um arquivo.

    Lê o arquivo em blocos de `chunk_size` bytes e alimenta o estado do
    hash incrementalmente, mantendo uso de memória constante (O(1))
    independente do tamanho do arquivo.
    """
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()
