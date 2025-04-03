import re
import time
from pyrogram import Client, filters

# Configuração da conta
API_ID = ""
API_HASH = ""

# IDs dos grupos para monitorar
SOURCE_CHAT_IDS = []  # Adicione mais IDs aqui
DESTINATION_CHAT_ID = [] # Para onde enviar os endereços capturados

# Inicia o cliente como usuário (não é um bot)
app = Client("my_account", api_id=API_ID, api_hash=API_HASH)

# Cache para evitar spam de mensagens repetidas
sent_cache = {}

@app.on_message(filters.chat(SOURCE_CHAT_IDS))
def forward_message(client, message):
    print(f"[🔹] Mensagem recebida de {message.chat.id}: {message.text or '[Mídia]'}")

    if message.text:
        # Expressão regular para capturar endereços válidos da Solana (Base58, 30+ caracteres)
        match = re.search(r'\b[123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{30,}\b', message.text)

        if match:
            extracted_address = match.group()

            # Evita duplicatas (espera 5 minutos antes de reenviar o mesmo endereço)
            if extracted_address in sent_cache and time.time() - sent_cache[extracted_address] < 300:
                print(f"[⚠️] Endereço duplicado, ignorando... ({extracted_address})")
                return
            
            # Salva no cache com timestamp atual
            sent_cache[extracted_address] = time.time()

            # Envia o endereço para o chat de destino
            client.send_message(DESTINATION_CHAT_ID, f"🔹 Endereço capturado: {extracted_address}")
            print(f"[✅] Endereço identificado e enviado: {extracted_address}")
        else:
            print("[⚠️] Nenhum endereço Solana encontrado.")

    elif message.media:
        message.copy(DESTINATION_CHAT_ID)
        print(f"[✅] Mídia encaminhada.")

print("[🚀] Bot iniciado e monitorando múltiplos grupos...")
app.run()
