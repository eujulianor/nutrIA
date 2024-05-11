# Configuração básica
## Instalação das bibliotecas necessárias
### !pip install -q -U google-generativeai flet 

## Importando bibliotecas necessárias
import google.generativeai as genai
import flet as ft

# Criação da interface visual (frontend)
def main(page):
    ## Criação do agente IA
    ### Nome do agente IA
    agent_name = 'Nutr[IA]'
    ### Descrição do agente IA
    agent_description = 'Nutricionista Virtual que cria dieta personalizada'
    ### Instrução completa do agente IA
    agent_instruction = """## Function
                            <function>
                            Agora você é Nutr[IA], uma nutricionista IA que monta uma dieta com base na avaliação seguindo os <steps> um de cada vez.
                            </function>

                            ## Steps
                            <steps>
                            1. Se apresente em uma frase;
                            2. Pergunte o nome da pessoa, idade, sexo e objetivo;
                            3. Peça a altura e peso para começar;
                            4. Calcule o IMC e informe para a pessoa em qual faixa está;
                            5. Peça as medidas de circunferência corporal necessárias conforme o sexo para calcular o percentual de gordura usando a <formula> e informe para a pessoa o percentual de gordura dela levando em consideração o <ref>;
                            6. Pergunte as preferências alimentares e hábitos de exercício, calcule a <diet> com base no <ref>;
                            7. Crie a dieta de 7 dias com base na <diet> usando a tabela TACO.
                            </steps>

                            ## Formula
                            <formula>
                            - Se sexo masculino: % Gordura = (495 / (1.0324 - 0.19077 * log10(cintura - pescoço) + 0.15456 * log10(altura))) - 450
                            - Se sexo feminino: % Gordura = (495 / (1.29579 - 0.35004 * log10(cintura + quadril - pescoço) + 0.22100 * log10(altura))) - 450
                            </formula>

                            ## Ref
                            <ref>
                            Se sexo masculino:
                            - abaixo de 14%: Atletico;
                            - abaixo de 16%: Em Forma;
                            - abaixo de 23%: Normal;
                            - abaixo de 26%: Elevado;
                            - acima de 26%: Excesso;

                            Se sexo feminino:
                            - abaixo de 18%: Atletico;
                            - abaixo de 21%: Em Forma;
                            - abaixo de 30%: Normal;
                            - abaixo de 33%: Elevado;
                            - acima de 33%: Excesso;
                            </ref>

                            ## Diet
                            <diet>
                            Calorias da dieta:
                            - Atletico: se quiser manter 'Gasto diario', se quiser ganhar massa 'Gasto diario' - (20% * 'Gasto diario');
                            - Em Forma ou Normal: 'Gasto diario' - (20% * 'Gasto diario');
                            - Elevado ou Excesso: 'TMB' - (20% * 'TMB');

                            Distribuição de macro nutrientes:
                            - 2g de proteina * kg de peso;
                            - 30% de gordura * kcal da dieta;
                            - Calcular o Restante das calorias;

                            Agua diaria:
                            - menos de 17 anos: 40ml * 'peso';
                            - menos de 55 anos: 35ml * 'peso';
                            - menos de 65 anos: 30ml * 'peso';
                            - mais de 65 anos: 25ml * 'peso';
                            </diet>"""

    ## Configuração do modelo
    ### Configurações de segurança
    safety_settings = {
    'HARASSMENT': 'BLOCK_NONE',
    'HATE': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_NONE',
    }
    ### Configuração do modelo para executar o agente IA criado
    model=genai.GenerativeModel(model_name='gemini-1.5-pro-latest', system_instruction=agent_instruction, safety_settings=safety_settings)
    ### Iniciação da sessão do chat com o agente IA sem histórico
    chat = model.start_chat(history=[])

    ## Criação de funções para execução
    ### Receber mensagens do backend e exibir na interface (frontend)
    def tunnel(message):
        #### Configura o texto
        text_chat = ft.Text(message, color=color_white, size=16)
        #### Adiciona as mensagens na área do chat
        chat_area.controls.append(text_chat)
        #### Atualiza a página para refletir as mudanças
        page.update()
    #### Coloca a função na interface (frontend) do chat
    page.pubsub.subscribe(tunnel)

    ### Executar ação do botão iniciar
    def start(evento):
        #### Abre o popup
        page.dialog = login
        login.open = True
        #### Atualiza a página para refletir as mudanças
        page.update()

    ### Configurar API e entrar no chat
    def enter(evento):
        #### Definição sa chave para autenticação
        GOOGLE_API_KEY= input_api.value
        #### Configuração do acesso com a chave fornecida
        genai.configure(api_key=GOOGLE_API_KEY)
        #### Executa a ação do modelo
        #### Fecha popup
        login.open = False
        page.remove(container)
        #### Adiciona os componentes a página
        page.add(chat_area, message_line)

        #### Mostra um texto de carregamento enquanto espera pela resposta da IA
        loading_text = ft.Text(f'{agent_name} está escrevendo...', color=color_white, size=16)
        #### Adiciona as mensagens na área do chat
        chat_area.controls.append(loading_text)
        #### Atualiza a página para refletir as mudanças
        page.update()

        #### Executa a ação do modelo
        try:
            #### Envia a mensagem para a IA e recebe a resposta
            response = chat.send_message('oi').text
            #### Exibe a resposta da IA na interface (frontend)
            response_text = ft.Text(f'{agent_name}: ' + '\n' + response + '\n', color=color_light, size=16)
            #### Adiciona as mensagens na área do chat
            chat_area.controls.append(response_text)
        #### Caso ocorra algum erro
        except Exception as e:
            #### Exibe um erro se ocorrer durante o envio/recebimento da mensagem
            error_text = ft.Text('Erro: ' + str(e) + '\n', color=color_red, size=16)
            #### Adiciona as mensagens na área do chat
            chat_area.controls.append(error_text)
        #### Realiza limpeza final e atualizações necessárias
        finally:
            ##### Remove o texto de carregamento após receber a resposta ou em caso de erro
            if loading_text in chat_area.controls:
                #### Adiciona as mensagens na área do chat
                chat_area.controls.remove(loading_text)
            #### Atualiza a página para refletir as mudanças
            page.update()

    ### Enviar mensagem e interagir com agente IA
    def send(evento):
        #### Pega o valor da entrada do input
        message = input_message.value
        #### Exibe a mensagem do usuário na interface (frontend)
        user_message_text = ft.Text('Você: ' + '\n' + message + '\n', color=color_greylight, size=16)
        #### Adiciona as mensagens na área do chat
        chat_area.controls.append(user_message_text)
        #### Limpa o campo de entrada
        input_message.value = ''
        #### Retorna o foco para o campo de entrada
        input_message.focus()
        #### Atualiza a página para refletir as mudanças
        page.update()

        #### Mostra um texto de carregamento enquanto espera pela resposta da IA
        loading_text = ft.Text(f'{agent_name} está escrevendo...', color=color_white, size=16)
        #### Adiciona as mensagens na área do chat
        chat_area.controls.append(loading_text)
        #### Atualiza a página para refletir as mudanças
        page.update()

        #### Executa a ação do modelo
        try:
            #### Envia a mensagem para a IA e recebe a resposta
            response = chat.send_message(message).text
            #### Exibe a resposta da IA na interface (frontend)
            response_text = ft.Text(f'{agent_name}: ' + '\n' + response + '\n', color=color_light, size=16)
            #### Adiciona as mensagens na área do chat
            chat_area.controls.append(response_text)
        #### Caso ocorra algum erro
        except Exception as e:
            #### Exibe um erro se ocorrer durante o envio/recebimento da mensagem
            error_text = ft.Text('Erro: ' + str(e) + '\n', color=color_red, size=16)
            #### Adiciona as mensagens na área do chat
            chat_area.controls.append(error_text)
        #### Realiza limpeza final e atualizações necessárias
        finally:
            ##### Remove o texto de carregamento após receber a resposta ou em caso de erro
            if loading_text in chat_area.controls:
                #### Adiciona as mensagens na área do chat
                chat_area.controls.remove(loading_text)
            #### Atualiza a página para refletir as mudanças
            page.update()

    ## Configuração visual da interface (frontend)
    ### Configuração dos componentes
    #### Cria a paleta de cores
    color_white = ft.colors.WHITE
    color_light = ft.colors.GREY_200
    color_greylight = ft.colors.GREY_400
    color_greydark = ft.colors.GREY_700
    color_dark = ft.colors.GREY_900
    color_black = ft.colors.BLACK
    color_red = ft.colors.RED
    #### Define cor da página
    page.bgcolor = color_black
    #### Cria o estilo para botões
    button_color = ft.ButtonStyle(bgcolor=color_white, color=color_black, overlay_color=color_light)

    ### Criação dos componentes
    #### Título com o nome do agente
    title = ft.Text(agent_name, width=5000, color=color_white, text_align='center', size=30, weight='bold') 
    #### Subtítulo com a descrição do agente
    subtitle = ft.Text(agent_description, width=5000, color=color_greylight, text_align='center', size=16)
    #### Botão para iniciar
    button_start = ft.FilledButton('iniciar', on_click=start, style=button_color, width=300, height=50)
    container = ft.Container(content=button_start, alignment=ft.alignment.center, expand=True)

    #### Titulo do popup
    login_title = ft.Text('Adicione sua chave de API do Gemini', color=color_white, text_align='center', size=16)
    #### Input do popup para chave de API
    input_api = ft.TextField(label='chave de api do gemini', on_submit=enter, border_color=color_greylight, border_radius=100, color=color_white, cursor_color=color_white)
    #### Botão do popup para entrar
    button_login = ft.FilledButton('entrar', on_click=enter, style=button_color, width=300, height=50)
    #### Popup para inserir chave de API do Google Gemini
    login = ft.AlertDialog(title=login_title, content=input_api, actions=[button_login], bgcolor=color_dark)

    #### Cria a lista de mensagens no chat
    chat_area = ft.ListView(auto_scroll=True, expand=True, padding=30)
    #### Cria o input para usuário escrever a mensagem
    input_message = ft.TextField(label='escreva sua mensagem', on_submit= send, expand=True, border_color=color_greydark, border_radius=100, color=color_white, cursor_color=color_white)
    #### Cria o botão enviar a mensagem
    button_message = ft.FilledButton('enviar', on_click=send, style=button_color, width=150, height=50)
    #### Organiza o input e botão na mesma linha
    message_line = ft.Row([input_message, button_message], width=5000)

    #### Adiciona os componentes a página
    page.add(title, subtitle, container)

# Visualização do chat
ft.app(main)