from pyrastreio import correios
import telebot
import time

TOKEN = ""  # token gerado no @BotFather no telegram
bot = telebot.TeleBot(TOKEN)

text_messages = {
    'welcome':
        " ** Em Desenvolvimento **\n"
        " Para rastrear só é necessario\n"
        " enviar o codigo de rastreio\n"
        " com padrão dos correios\n"
        " Ex : AB123456789CD ou /AB123456789CD \n",

    'example':
        "Calma jovem, Esse codigo é apenas um exemplo! ",

    'developers':
        " Desenvolvedores:  \n"
        " Bruno\n"
        " Gabriel\n"
        " Renan\n"
        " Wilton\n"
}


@bot.message_handler(commands=['start', 'help'])  ## resposta automática caso o usuario digite /start ou /help.
def send_welcome(session):
    bot.reply_to(session, text_messages['welcome'])


@bot.message_handler(
    commands=['/AB123456789CD', 'AB123456789CD'])  ## resposta automática caso ele digite o exemplo dado.
def send_welcome(session):
    print(session)
    bot.reply_to(session, text_messages['example'])


@bot.message_handler(
    commands=['credits'])  ## resposta automática caso ele digite o exemplo dado.
def send_welcome(session):
    print(session)
    bot.reply_to(session, text_messages['developers'])



@bot.message_handler(func=lambda m: True)  ## resposta para possivel rastreio inserido no chat do telegram
def all_messages(session):
    respostaRastreio = (session.text.replace('/', ''))  ## rastreio que o usuario enviou
    print(respostaRastreio)  ## printa no terminal o codigo enviado
    busca_Correios(respostaRastreio, session)


def busca_Correios(respostaRastreio, session):
    lista = correios(respostaRastreio.upper())  ## coloca o rastreio em maiusculo
    print(correios(respostaRastreio))
    trajetoRastreio = ""
    if len(respostaRastreio) == 13:
        try:

            nome = session.from_user.first_name
            bot.reply_to(session, f"Olá {nome}, Estou checando a situação do pacote, por favor aguarde...")
            time.sleep(4)
            cont = 0
            for attRastreio in lista:
                tracinhos = 75 * '-'
                dic = attRastreio

                data = dic['data']
                hora = dic['hora']
                local = dic['local']
                mensagem = dic["mensagem"]

                status = separaMensagem(mensagem)

                rastreio = f"{data} - {hora} \nlocalização = {local} \n{status} \n{tracinhos}\n"
                trajetoRastreio += rastreio

            bot.reply_to(session, trajetoRastreio)
        except:  ## gerou um erro com o rastreio
            bot.reply_to(session, "O codigo Digitado nao consta no sistema dos correios!!!")
    else:
        bot.send_message(session.chat.id, "Você digitou o codigo de forma incorreta 😂!!!")
        time.sleep(2)
        bot.reply_to(session, resposta)


def separaMensagem(mensagem):
    mensagemDevolvida = []
    msgFormatada = ''
    """
        É criado duas variaveis para dividir e tratar o texto que nos é devolvido pela biblioteca pyrastreio
    """
    try:
        splitText1 = mensagem.split("Para")

        if len(splitText1) == 1:
            splitText2 = splitText1[0].split("- por favor aguarde de ")
            mensagemDevolvida.append(splitText2)
            print(splitText2)
        else:
            mensagemDevolvida.append(splitText1)
            print(splitText1)

        if len(mensagemDevolvida[0]) == 1:
            print(mensagemDevolvida)
            msgFormatada = (f"Situação: {mensagemDevolvida[0][0]}")
        if len(mensagemDevolvida[0]) == 2:
            print(mensagemDevolvida)

            msgFormatada = (f"Situação: {mensagemDevolvida[0][0]}\nObservação: {mensagemDevolvida[0][1]}")

        return (msgFormatada)

    except:
        pass


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)

        # reply_to     ===      responde a msg
        # send_message ===      envia msg sem responder ela