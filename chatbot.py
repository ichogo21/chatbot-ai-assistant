"""
Chatbot Sederhana - Asisten Ide Konten AI/Teknologi
=====================================================
Ini project belajar coding pertama kamu! Chatbot ini bakal jadi
"partner curhat" buat brainstorm ide konten AI & Teknologi.

Cara kerja singkatnya:
1. Kamu ngetik pesan di terminal
2. Pesan itu dikirim ke Claude API
3. Claude balas, dan balasannya muncul di terminal
4. Diulang terus sampai kamu ketik 'exit'
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# STEP 1: Load API key dari file .env
# (Kita nggak pernah nulis API key langsung di kode, biar aman
# kalau nanti di-push ke GitHub)
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ API key belum ketemu! Cek lagi file .env kamu.")
    exit()

# STEP 2: Bikin koneksi ke Claude API
client = Anthropic(api_key=api_key)

# STEP 3: Kasih "kepribadian" ke chatbot ini lewat system prompt
SYSTEM_PROMPT = """Kamu adalah asisten brainstorming ide konten untuk
kreator konten AI & Teknologi di Indonesia, target audiens usia 18-34 tahun.
Gaya bicara kamu santai, kayak temen ngobrol, pakai bahasa Indonesia
yang natural (boleh 'kamu', 'nggak', 'banget', 'cuan').
Fokus bahas 3 hal: Uang (side hustle/AI buat cari cuan), Karir (AI di
tempat kerja), dan Kehidupan sehari-hari (AI buat produktivitas).
Jawaban singkat, praktis, dan to the point. Hindari kata klise kayak
'merevolusi' atau 'mencengangkan'."""

# STEP 4: Nyimpen riwayat chat, biar chatbot inget percakapan sebelumnya
conversation_history = []

print("=" * 50)
print("🤖 Asisten Ide Konten AI/Teknologi")
print("Ketik pesan kamu, atau ketik 'exit' buat keluar.")
print("=" * 50)

# STEP 5: Loop percakapan - ini jantungnya chatbot
while True:
    user_input = input("\n👤 Kamu: ")

    if user_input.lower() in ["exit", "quit", "keluar"]:
        print("\n👋 Sampai ketemu lagi! Semangat bikin konten ya!")
        break

    # Tambahin pesan user ke riwayat
    conversation_history.append({"role": "user", "content": user_input})

    # Kirim ke Claude API
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )

        # Ambil teks balasan dari Claude
        reply = response.content[0].text
        print(f"\n🤖 Asisten: {reply}")

        # Tambahin balasan Claude ke riwayat juga
        conversation_history.append({"role": "assistant", "content": reply})

    except Exception as e:
        print(f"\n❌ Ada error nih: {e}")
