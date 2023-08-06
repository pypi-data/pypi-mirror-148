class Enviador:
    def enviar(self, remetente, destinatario, assunto, corpo):
        if '@' not in remetente:
            raise EmailInvalido(f'E-mail de remetende inválido: {remetente}')
        return remetente


class EmailInvalido(Exception):
    pass
