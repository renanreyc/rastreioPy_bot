from pyrastreio import correios  # pip install pyrastreio
import telebot  # pip install pyTelegramBotAPI
import time
from datetime import datetime
from valores_internos import TOKEN

TOKEN1 = TOKEN  # Gera o token no @BotFather no telegram
bot = telebot.TeleBot(TOKEN)

text_messages = {
    'welcome':
        "Para rastrear só é necessario\n"
        "enviar o codigo de rastreio\n"
        "com padrão dos correios\n"
        "Ex : AB123456789CD ou /AB123456789CD",

    'example':
        "_Calma jovem, Esse codigo é apenas um exemplo! _",

    'developers':
        " 👨🏻‍💻  Desenvolvedores:  \n\n"
        " *Bruno Silva*\n"
        " *Gabriel Silva*\n"
        " *Renan Rodrigues*\n"
        " *Wilton Lima*\n"
}


# resposta automática caso o usuario digite /start
@bot.message_handler(commands=['start'])
def send_welcome(session):
    bot.send_message(session.chat.id, text_messages['welcome'])


# resposta automática caso ele digite o exemplo
@bot.message_handler(commands=['/AB123456789CD', 'AB123456789CD'])
def send_welcome(session):
    print(session)
    bot.reply_to(session, text_messages['example'], parse_mode='Markdown')


# resposta automática caso ele digite o exemplo
@bot.message_handler(commands=['dog'])
def dog_entrega(session):
    gif = "https://media3.giphy.com/media/hpEfWyx4W2dGU4kPbz/giphy.gif?cid=ecf05e477fo9715l7z4h88c6b83b9cd0v6kdxnkqrfami026&rid=giphy.gif"
    bot.send_document(session.chat.id, gif)


# resposta automática para a parte dos créditos dos devs envolvidos no projeto
@bot.message_handler(commands=['credits'])
def send_credits(session):
    print(session)
    bot.reply_to(session, text_messages['developers'], parse_mode='Markdown')


# lambda gera uma função anônima para o possível código enviado no chat, def <lambda>(argumento)
@bot.message_handler(func=lambda m: True)
def all_messages(session):
    # rastreio que o usuario enviou
    respostaRastreio = (session.text.replace('/', ''))
    rastreio = respostaRastreio
    # pega o nome do usuário na sessão e coloca dentro da variavel
    nome = session.from_user.first_name

    print(respostaRastreio)  # printa no terminal o codigo enviado
    busca_Correios(respostaRastreio, session)  # Busca todo historico do codigo
    buscaAtt(session, rastreio, nome)  # Fica procurando att no rastreio!


def busca_Correios(respostaRastreio, session):
    # coloca o rastreio em maiusculo
    lista = correios(respostaRastreio.upper())
    print(correios(respostaRastreio))  # print resposta do Rastreio no terminal
    trajetoRastreio = ""

    if len(respostaRastreio) == 13:
        try:
            dic = lista[0]
            dic2 = lista[-1]
            dias = int(contDias(dic, dic2))

            # Insere o codigo de rastreio no comeco da msg
            trajetoRastreio += f'📦 *{respostaRastreio}* ({dias} dias) \n\n'

            nome = session.from_user.first_name  # Nome do usuario
            bot.reply_to(
                session, f"Olá {nome}, Estou checando a situação do pacote, por favor aguarde...")
            time.sleep(4)
            for attRastreio in lista:
                tracinhos = 75 * '_'
                dic = attRastreio

                data = dic['data']
                hora = dic['hora']
                local = dic['local']
                mensagem = dic["mensagem"]

                status = separaMensagem(mensagem)

                infoRastreio = f"{data} - {hora} \nlocalização = {local} \n{status} \n{tracinhos}\n"
                trajetoRastreio += infoRastreio

            bot.reply_to(session, trajetoRastreio, parse_mode='Markdown')

        except:  # gerou um erro com o rastreio
            bot.reply_to(
                session, "Código não foi encontrado no sistema dos Correios. Talvez seja necessário aguardar algumas horas para que esteja disponível para consultas.")
    else:
        bot.send_message(
            session.chat.id, "Você digitou o codigo de forma incorreta!")
        time.sleep(2)


def buscaAtt(session, rastreio, nome):
    if len(rastreio) == 13:

        listaRastreio = correios(rastreio.upper())
        print(listaRastreio)
        print('\n')
        tamRastreio1 = len(listaRastreio)

        while True:
            try:

                novoRastreio = correios(rastreio.upper())
                tamRastreio2 = len(novoRastreio)
                dic = novoRastreio[0]
                dic2 = novoRastreio[-1]
                print(dic)

                dias = int(contDias(dic, dic2))
                data = dic['data']
                hora = dic['hora']
                local = dic['local']
                mensagem = dic["mensagem"]
                status = separaMensagem(mensagem)

                try:
                    if tamRastreio2 != tamRastreio1:
                        # print(novoRastreio[0])
                        if dic["mensagem"] == 'Objeto entregue ao destinatário ✅ ':
                            attRastreio = f"Boa noticia {nome}, tem atualização no seu pacote: \n {data} - {hora} \nlocalização = {local} \nStatus = {status} \n"
                            bot.send_message(session.chat.id, attRastreio)
                            print(attRastreio)
                            break
                        else:
                            attRastreio = f"Boa noticia {nome}, tem atualização no seu pacote: \n {data} - {hora} \nlocalização = {local} \nStatus = {status} \n"
                            bot.send_message(session.chat.id, attRastreio)
                            listaRastreio == novoRastreio
                            # time.sleep(3600)

                    else:
                        if dic["mensagem"] == 'Objeto entregue ao destinatário':
                            attRastreio = (
                                f'Objeto: {rastreio} \nEntregue em {dias} dias!!!')
                            bot.send_message(
                                session.chat.id, attRastreio, parse_mode='Markdown')
                            print(attRastreio)
                            break

                        else:
                            time.sleep(60)
                            pass

                        # time.sleep(3600)

                except:
                    print('Erro1')
                    pass

                time.sleep(60)
            except:
                print('Erro2')
                break


def separaMensagem(mensagem):
    mensagemDevolvida = []
    msgFormatada = ''
    """
        É criado duas variaveis para dividir e tratar o texto que nos é devolvido pela biblioteca pyrastreio
    """
    try:
        splitText1 = mensagem.split("Para retirá-lo,")

        if len(splitText1) == 1:
            splitText2 = splitText1[0].split("- por favor aguarde de ")
            mensagemDevolvida.append(splitText2)
            print(splitText2)
        else:
            mensagemDevolvida.append(splitText1)
            print(splitText1)

        if len(mensagemDevolvida[0]) == 1:
            print(mensagemDevolvida)
            msgFormatada = (f"Situação: *{mensagemDevolvida[0][0]}*")
        if len(mensagemDevolvida[0]) == 2:
            print(mensagemDevolvida)

            msgFormatada = (
                f"Situação: *{mensagemDevolvida[0][0]}*\nObservação: {mensagemDevolvida[0][1]}")

        return (msgFormatada)

    except:
        pass


def contDias(dic, dic2):
    data2 = dic['data']  # data da ultima atualização
    data1 = dic2['data']  # data da primeira atualização

    # Data final
    d2 = datetime.strptime(data2, '%d/%m/%Y')

    # Data inicial
    d1 = datetime.strptime(data1, '%d/%m/%Y')

    # Realizamos o calculo da quantidade de dias
    quantidade_dias = abs((d2 - d1).days)
    return quantidade_dias


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

        # reply_to     ===      responde a msg
        # send_message ===      envia msg sem responder ela
