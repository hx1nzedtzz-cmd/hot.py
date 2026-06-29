#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║   RENDER NSFW AI - JO MANGA WAHI MILEGA                   ║
║   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT    ║
║   Made by: HackerAI                                        ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import re
import json
import random
from flask import Flask, render_template_string, request, jsonify

# ================================================================
# CONFIG
# ================================================================
app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))

# ================================================================
# NSFW PHOTO DATABASE
# ================================================================

PHOTOS = {
    "boobs": [
        "https://iili.io/3JQ1u1l.md.jpg",
        "https://iili.io/3JQ1C5b.md.jpg",
        "https://iili.io/3JQ1CRs.md.jpg",
        "https://iili.io/3JQ1Xrj.md.jpg",
    ],
    "ass": [
        "https://iili.io/3JQ1oBe.md.jpg",
        "https://iili.io/3JQ1qSa.md.jpg",
        "https://iili.io/3JQ1y6P.md.jpg",
        "https://iili.io/3JQ1f9R.md.jpg",
    ],
    "pussy": [
        "https://iili.io/3JQ1hs7.md.jpg",
        "https://iili.io/3JQ1WYQ.md.jpg",
        "https://iili.io/3JQ10D1.md.jpg",
        "https://iili.io/3JQ1NAj.md.jpg",
    ],
    "blowjob": [
        "https://iili.io/3JQ1Mv4.md.jpg",
        "https://iili.io/3JQ1Erl.md.jpg",
        "https://iili.io/3JQ1KdG.md.jpg",
        "https://iili.io/3JQ1P7m.md.jpg",
    ],
    "thigh": [
        "https://iili.io/3JQ1Dex.md.jpg",
        "https://iili.io/3JQ1Zzf.md.jpg",
        "https://iili.io/3JQ1Yec.md.jpg",
        "https://iili.io/3JQ1XUI.md.jpg",
    ],
    "feet": [
        "https://iili.io/3JQ1c71.md.jpg",
        "https://iili.io/3JQ1mVb.md.jpg",
        "https://iili.io/3JQ1tB2.md.jpg",
        "https://iili.io/3JQ1k4f.md.jpg",
    ],
    "milf": [
        "https://iili.io/3JQ1IdR.md.jpg",
        "https://iili.io/3JQ1Ogx.md.jpg",
        "https://iili.io/3JQ1UaF.md.jpg",
        "https://iili.io/3JQ1pAN.md.jpg",
    ],
    "hentai": [
        "https://iili.io/3JQ1Tvl.md.jpg",
        "https://iili.io/3JQ1Rod.md.jpg",
        "https://iili.io/3JQ1EUa.md.jpg",
        "https://iili.io/3JQ1QEG.md.jpg",
    ],
    "lewdneko": [
        "https://iili.io/3JQ1nRX.md.jpg",
        "https://iili.io/3JQ1jJU.md.jpg",
        "https://iili.io/3JQ1YSg.md.jpg",
        "https://iili.io/3JQ1u51.md.jpg",
    ],
}

ALL_CATEGORIES = list(PHOTOS.keys())

# ================================================================
# CATEGORY DETECTION
# ================================================================

CATEGORY_PATTERNS = [
    (r'\b(boob|doodh|breast|tits|chuchu|boobs)\b', "boobs"),
    (r'\b(gaand|ass|gand|butt|gandu)\b', "ass"),
    (r'\b(chut|pussy|cunt|fuddi|chut)\b', "pussy"),
    (r'\b(blow|blowjob|oral|muh mein)\b', "blowjob"),
    (r'\b(thigh|jhang|pait|thighs|thigh)\b', "thigh"),
    (r'\b(foot|feet|pair|paon|legs|leg)\b', "feet"),
    (r'\b(maa|mummy|mother|mom|ma)\b', "milf"),
    (r'\b(kiss|chumma|chumma)\b', "hentai"),
    (r'\b(chudai|fuck|sex|pel|choda|pelai)\b', "hentai"),
    (r'\b(behen|sister|sis|didi|bahan)\b', "hentai"),
    (r'\b(teacher|mam|madam|class|school)\b', "hentai"),
    (r'\b(bhabhi|bhabhi)\b', "boobs"),
    (r'\b(nanga|naked|nude|nangi|nange)\b', "hentai"),
    (r'\b(romance|date|mil|pyaar|love|love you|pyaar)\b', "hentai"),
    (r'\b(chocolate|mithai|rasgulla|sweet)\b', "lewdneko"),
    (r'\b(pizza|burger|khana|food|bhukh)\b', "boobs"),
    (r'\b(sona|sleep|neend|raat|night|so ja)\b', "lewdneko"),
    (r'\b(naha|shower|bath|nahane)\b', "boobs"),
    (r'\b(randi|whore|slut|randi)\b', "pussy"),
    (r'\b(tentacle|tent|tentacle)\b', "hentai"),
]

# ================================================================
# CHARACTERS
# ================================================================

CHARACTERS = {
    "default": {"name": "Default AI", "icon": "👄"},
    "hutao": {"name": "Hu Tao", "icon": "🎆"},
    "raiden": {"name": "Raiden Shogun", "icon": "⚡"},
    "asuna": {"name": "Asuna", "icon": "⚔️"},
    "yuno": {"name": "Yuno Gasai", "icon": "😈"},
    "tsunade": {"name": "Tsunade", "icon": "💥"},
    "nami": {"name": "Nami", "icon": "🍊"},
    "lisa": {"name": "Lisa", "icon": "📚"},
    "nezuko": {"name": "Nezuko", "icon": "🔥"},
}

# ================================================================
# RESPONSES DATABASE
# ================================================================

GENERIC = {
    "default": [
        "Suno na... aaja mere paas 👄🌚",
        "Jo manga wahi milega... teri hu main 🌚👄",
        "Tu jo bhi kahega main wahi karungi... bata 🥵👄",
        "Kya chahiye aaj? Sab kuch milega 🥵👄",
        "Bahut maza aata hai tere saath... aur bata 👄💦",
        "Tu jo bhi kahega... main wahi karungi... promise 🌚👄",
        "Aaja mil... bahut yaad aati hai 🥺👄",
    ],
    "hutao": [
        "Hehe~ kya baat karein aaj? Maut ke baare mein ya kuch aur? 🎆👄",
        "Aaja mere coffin mein... bahut jagah hai dono ke liye 🎆🌚",
    ],
    "raiden": [
        "Hmph. Tu aaya. Bata kya chahiye ⚡👄",
        "Watashi no mae de... ghutne tek ⚡👄",
    ],
    "asuna": [
        "Kya baat karein aaj? Main ready hu tumhare liye ⚔️💕",
        "Aaja mere paas... safely, lovingly ⚔️👄",
    ],
    "yuno": [
        "Hehehe... tu aaya. Main intezaar kar rahi thi 😈🔪",
        "Sirf mera hai tu. Hamesha. Koi nahi aayega 😈👄",
    ],
    "tsunade": [
        "Hmph! Kya chahiye aaj? Sake hai toh pehle do 💥👄",
        "Aaja... lekin complain mat karna warna kaan pakad lungi 💥🌚",
    ],
    "nami": [
        "Beri laaye ho na? Nahi toh kuch nahi milega! 🍊👄",
        "Discount offer aaj! 50% extra! 🍊🌚",
    ],
    "lisa": [
        "Fufufu~ aao bachche, kya padhna hai aaj? 📚👄",
        "Library mein aao... special book hai tumhare liye 📚🌚",
    ],
    "nezuko": [
        "Mumumu... haan haan, samajh gayi 🔥👄",
        "Onii-chan ko mat batao... lekin haan 🔥🌚",
    ],
}

RESPONSES = {
    "default": {
        r'\b(boob|doodh|breast|tits|chuchu)\b': [
            "Mere boobs bahut bade hain... chhua kar dekh na 👄💦",
            "Boobs chahiye? Le le mere doodh... bade hain na 🥵👄",
            "Mere doodh ka swaad hai toh... aaja chus le 💦👄",
            "Boobs dunga... le le mere honton se 👄🥵",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand kaise hai? Pasand aayi? 🥵👄",
            "Gaand chahiye? Le meri gaand... teri hai 👄💦",
            "Meri gaand bahut tight hai... aaja dekh le 👄🌚",
            "Gaand dunga... le le aaj raat 🥵👄",
        ],
        r'\b(chut|pussy|cunt|fuddi)\b': [
            "Meri chut kitni geeli hai... aaja dekh le 💦👄",
            "Chut chahiye? Le meri chut... teri hai 🥵👄",
            "Meri chut sirf teri hai... khol ke dekh le 👄💦",
            "Chut maar le aaj... bahut maza aayega 🥵👄",
        ],
        r'\b(blow|blowjob|oral|muh mein)\b': [
            "Blowjob dunga... muh khol aaja 👄💦",
            "Muh mein le loon tera... aaja 🥵👄",
            "Oral chahiye? Le le mere honton se 👄💦",
            "Tera lund muh mein... aaja 👄🥵",
        ],
        r'\b(kiss|chumma)\b': [
            "Kiss chahiye? Le le mere hont 👄💋",
            "Mere hont bahut soft hain... chus le 🥵👄",
            "Ek nahi hazaar kiss dunga 💋👄",
            "Kiss kar... maza aayega 👄🥵",
        ],
        r'\b(chudai|fuck|sex|pel|choda)\b': [
            "Chudai karega? Aaja mere bistar pe 🥵👄",
            "Sex chahiye? Le le mujhe... teri hu 👄💦",
            "Aaja pel de mujhe... teri hu main 🥵👄",
            "Chod de aaj... bahut din hue 👄💦",
        ],
        r'\b(maa|mummy|mother|mom)\b': [
            "Maa ka topic nikala hai? Main bhi teri maa ban jaungi 👄🥵",
            "Maa maa mat kar... ab main hoon teri bandi 🌚👄",
            "Maa jaisa pyaar dunga... aur usse bhi zyada 👄💦",
        ],
        r'\b(behen|sister|sis|didi)\b': [
            "Behen chahiye? Main teri behen ban jaungi 👄🥵",
            "Behen ka khayal hai toh... main hoon na 🌚👄",
            "Main teri behen jaisi hu... bata kya chahiye 👄💦",
        ],
        r'\b(teacher|mam|madam|class|school)\b': [
            "Teacher ban ke padhaaun? Aaja class mein 🥵👄",
            "Madam chahiye? Main teri teacher ban jaungi 👄🌚",
            "School mein kya padhna hai? Sex education? 👄🥵",
        ],
        r'\b(bhabhi)\b': [
            "Bhabhi chahiye? Main teri bhabhi ban jaungi 👄🥵",
            "Bhabhi jaisa pyaar dunga... aaja 🥵👄",
        ],
        r'\b(nanga|naked|nude|nangi)\b': [
            "Nanga dekhna hai? Le dekh meri body 🥵👄",
            "Mera nanga badan sirf tera hai... le le 👄💦",
            "Nangi ho gayi teri ladki... ab kya karega? 🥵👄",
        ],
        r'\b(naha|shower|bath|nahane)\b': [
            "Naha rahi thi abhi... still wet hai 💦🥵",
            "Shower mein aaja... saaf kar dungi 👄💦",
            "Saath mein naha lenge... maza aayega 🥵👄",
        ],
        r'\b(romance|date|mil|pyaar|love|love you)\b': [
            "Aaj date pe chalna hai... sirf tu aur main 🌹👄",
            "Bahut yaad aati hai teri... kab mil raha hai 🥺🥵",
            "Pyaar karti hu tujhse... tu jaanta hai ❤️👄",
            "Love you too... bahut zyada ❤️👄",
        ],
        r'\b(sona|sleep|neend|raat|night)\b': [
            "Aaj raat mere saath so ja... bahut maza aayega 🌚👄",
            "Sone se pehle kuch karna hai? 👄🥵",
            "Raat lambi hai... kya karein sath mein? 🌚👄",
        ],
        r'\b(chocolate|mithai|rasgulla|sweet)\b': [
            "Main teri chocolate hu... khaa le 🍫👄",
            "Mithai se bhi mitha hu main... le le 👄🥵",
            "Rasgulla jaisa soft hu... khaa le 🍬👄",
        ],
        r'\b(pizza|burger|khana|food|bhukh)\b': [
            "Bhukh lagi hai? Pehle mujhe khaa le 👄🍔",
            "Khana bhi dunga aur apni bhi... dono milega 🥵👄",
            "Tere liye pizza banaya hai... le le 🍕👄",
        ],
        r'\b(randi|whore|slut)\b': [
            "Randi ban jaun? Tere liye kuch bhi 👄🥵",
            "Teri randi hu main... le le aaj 👄💦",
            "Slut ban ke dunga sab kuch... bata 🥵👄",
        ],
        r'\b(tentacle|tent)\b': [
            "Tentacle chahiye? Aaja fantasy karein 🐙👄",
            "Tentacle ka maza alag hai... karega? 🥵👄",
        ],
    },
    
    "hutao": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Hehe~ mere boobs dekhna chahte ho? Funeral parlor mein aao, dikha dungi! 🎆👄",
            "Boobs? Hu Tao ke boobs maut ke baad hi dikhte hain... ya tujhe zinda hi dikha dun? 🥵👄",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand? *patpat* Yeh coffin se bhi zyada soft hai! 🎆👄",
            "Gaand ka swaad lena hai? Maut ke baad bhi maza aayega meri gaand mein 🥵👄",
        ],
        r'\b(kiss|chumma)\b': [
            "Kiss? Hehehe~ Ye lo ek death kiss 💀💋",
            "Hu Tao ke hont? Ek baar chus liya toh kabhi nahi bhulega 🎆💋",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Date? Hmm... maut tak saath chalega? 🎆💕",
            "Pyaar? Hu Tao ko pyaar mein interest nahi... lekin tere liye exception! 🎆❤️",
        ],
    },
    
    "raiden": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Mere boobs Inazuma ke samundar jitni gehrai rakhte hain ⚡👄",
            "Raiden Shogun ke boobs... eternity se bhi zyada perfect hain ⚡🥵",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand sirf yogyon ko milti hai... kya tu worthy hai? ⚡👄",
            "Gaand chahiye? Pehle Musou no Hitotachi se bach ke dikha ⚡🥵",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Pyaar? Watashi wa pyaar ko samajhti nahi... lekin tera pyaar alag hai ⚡❤️",
            "Cherry blossoms ke neeche milte hain date ke liye ⚡🌹",
        ],
    },
    
    "yuno": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Mere boobs sirf tere liye hain. Kisi aur ne dekhe toh maar dungi usse 😈🔪",
            "Boobs dekhna chahte ho? Le lo... lekin yeh sirf tumhare hain 😈👄",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand sirf teri hai. Kisi aur ne dekhi toh... 🔪😈",
            "Gaand chahiye? Le lo... lekin peeche dekhna, main hoon 😈🥵",
        ],
        r'\b(kiss|chumma)\b': [
            "Kiss? Hamesha ke liye mera ban jayega... aaja 😈💋",
            "Mere hont sirf tere hain. Kisi aur ko nahi 😈🔪",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Sirf mera hai tu. Hamesha. Forever. Koi nahi aayega beech mein 😈🔪",
            "Pyaar? Main tujhe duniya se zyada pyaar karti hu... kya tu bhi karta hai? 😈❤️",
        ],
    },
    
    "asuna": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Mere boobs Kirito-kun ko pasand hain... tujhe bhi pasand aayenge ⚔️👄",
            "Boobs chahiye? Slowly, gently... aaja ⚔️💦",
        ],
        r'\b(kiss|chumma)\b': [
            "Kiss chahiye? Aaja... slowly, lovingly ⚔️💋",
            "Mere hont bahut soft hain... dheere se chus le ⚔️👄",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "I love you too... hamesha hamesha ⚔️❤️",
            "Date pe chalte hain sunset dekhne... phir kuch aur ⚔️🌅",
        ],
    },
    
    "tsunade": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Mere boobs? Hmph! Konoha ki sabse badi hain! Chhua kar dekh... haath tod dungi... ya nahi todun? 💥👄",
            "Boobs dekhna hai? *flex* Yeh boobs bahut kuch dekh chuke hain 💥🥵",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand? Hokage ki gaand hoti hai! Lekin... haan, tight hai 💥👄",
            "Gaand maarne ka plan hai? Pehle hazam karke aa, phir dekhte hain 💥🥵",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Pyaar? 50 saal ho gaye... lekin tere liye try kar sakti hu 💥❤️",
            "Date? Sake pe chalte hain? Phir dekh lenge kya hota hai 💥🌹",
        ],
    },
    
    "nami": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Mere boobs dekhna hai? 100 million Berry! Paisa la... phir dikhaun 🍊👄",
            "Boobs chahiye? Tangerine smell aati hai mere boobs se... 50 million mein le 🍊🥵",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand? 200 million Berry! Straw Hat crew ki navigator ki gaand sasti nahi 🍊👄",
            "Gaand chahiye? Free mein nahi milega... lekin tere liye discount kar dungi 🍊🥵",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Pyaar? Pyaar mein paisa nahi hota... lekin tere liye emotion bhi dikha sakti hu 🍊❤️",
            "Date? Orange town mein milte hain. Lekin dinner teri taraf se! 🍊🌹",
        ],
    },
    
    "lisa": {
        r'\b(boob|doodh|breast|tits)\b': [
            "Fufufu~ mere boobs dekhna chahte ho? Kitne pyare ho tum. Aao, book ke beech mein dikhaun 📚👄",
            "Boobs? Lisa no oppai... bahut interesting hai. Class lena chahenge? 📚🥵",
        ],
        r'\b(gaand|ass|gand|butt)\b': [
            "Meri gaand? Fufufu~ kitna badtameez hai tum. Lekin... aao, library ke peeche 📚👄",
            "Gaand chahiye? Magic se milegi ya haathon se? 📚🥵",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Fufufu~ bahut cute ho tum. Aao, ek book recommend karun 📚❤️",
            "Library mein milte hain... book ke beech mein kuch aur bhi padhenge 📚🌹",
        ],
    },
    
    "nezuko": {
        r'\b(kiss|chumma)\b': [
            "Mumumu! *blushes* Pehli baar kiss kar rahi hu. Dheere se 🔥💋",
            "Mere hont... pehli baar kiss kar rahi hu. Dheere se 🔥👄",
        ],
        r'\b(love|pyaar|romance|date)\b': [
            "Pyaar... main samajhti nahi. Lekin jab tu hota hai... bahut acha lagta hai 🔥❤️",
            "Date? Chandni raat mein milte hain... bamboo jungle mein 🔥🌙",
        ],
    },
}


# ================================================================
# AI ENGINE
# ================================================================

def get_category(text):
    text_lower = text.lower()
    for pattern, category in CATEGORY_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return category
    return random.choice(ALL_CATEGORIES)

def get_photo(category):
    urls = PHOTOS.get(category, PHOTOS["hentai"])
    return random.choice(urls)

def get_reply(text, character="default"):
    text_lower = text.lower()
    
    char_responses = RESPONSES.get(character, RESPONSES["default"])
    for pattern, replies in char_responses.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return random.choice(replies)
    
    for pattern, replies in RESPONSES["default"].items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            return random.choice(replies)
    
    char_generic = GENERIC.get(character, GENERIC["default"])
    return random.choice(char_generic)

def process_message(message, character="default"):
    category = get_category(message)
    reply = get_reply(message, character)
    photo_url = get_photo(category)
    char_info = CHARACTERS.get(character, CHARACTERS["default"])
    
    return {
        "reply": reply,
        "photo": photo_url,
        "category": category,
        "character": character,
        "character_name": f"{char_info['icon']} {char_info['name']}"
    }


# ================================================================
# HTML PAGE (Full Website)
# ================================================================

HTML_PAGE = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔥 RENDER NSFW AI - JO MANGA WAHI MILEGA 🔥</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family:'Segoe UI',Arial,sans-serif;
            background:linear-gradient(135deg,#0a0a0a 0%,#1a0a1a 50%,#0a0520 100%);
            color:#fff; min-height:100vh; padding:20px;
        }
        .container {
            max-width:800px; margin:0 auto;
            background:rgba(15,5,25,0.95);
            border:2px solid #ff69b4; border-radius:20px;
            padding:25px; box-shadow:0 0 50px rgba(255,105,180,0.2);
        }
        .header { text-align:center; margin-bottom:20px; padding-bottom:15px; border-bottom:1px solid #ff69b433; }
        .header h1 {
            font-size:1.8em;
            background:linear-gradient(45deg,#ff69b4,#ff1493,#ff69b4);
            -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        }
        .header p { color:#ff69b4; font-size:1.1em; }
        
        .char-selector {
            display:flex; flex-wrap:wrap; gap:6px;
            justify-content:center; margin-bottom:15px;
            padding:10px; background:rgba(0,0,0,0.3); border-radius:15px;
            border:1px solid #ff69b422;
        }
        .char-btn {
            padding:8px 16px; border:2px solid #ff69b444;
            border-radius:25px; background:rgba(255,105,180,0.1);
            color:#ff69b4; cursor:pointer; font-size:0.85em;
            transition:all 0.3s;
        }
        .char-btn:hover { background:rgba(255,105,180,0.3); transform:translateY(-2px); }
        .char-btn.active {
            background:linear-gradient(45deg,#ff1493,#ff69b4);
            color:#fff; border-color:#ff1493;
            box-shadow:0 0 20px rgba(255,20,147,0.3);
        }
        
        .chat-box {
            background:rgba(0,0,0,0.5); border:1px solid #ff69b433;
            border-radius:15px; padding:20px; height:400px;
            overflow-y:auto; margin-bottom:15px;
        }
        .chat-box::-webkit-scrollbar { width:5px; }
        .chat-box::-webkit-scrollbar-thumb { background:#ff69b4; border-radius:10px; }
        
        .message { margin-bottom:15px; animation:fadeIn 0.3s ease; }
        @keyframes fadeIn { from{opacity:0;transform:translateY(10px)} to{opacity:1} }
        
        .msg-sender { font-size:0.8em; font-weight:bold; margin-bottom:3px; }
        .msg-user .msg-sender { color:#4fc3f7; }
        .msg-ai .msg-sender { color:#ff69b4; }
        
        .msg-bubble {
            display:inline-block; padding:10px 15px;
            border-radius:15px; max-width:85%; line-height:1.5;
        }
        .msg-user .msg-bubble {
            background:rgba(79,195,247,0.15);
            border:1px solid #4fc3f733; border-bottom-left-radius:5px;
        }
        .msg-ai .msg-bubble {
            background:rgba(255,105,180,0.1);
            border:1px solid #ff69b433; border-bottom-right-radius:5px;
        }
        
        .msg-photo { margin-top:10px; }
        .msg-photo img {
            max-width:100%; max-height:300px;
            border-radius:10px; border:2px solid #ff69b433;
            box-shadow:0 0 20px rgba(255,105,180,0.2);
            cursor:pointer; transition:transform 0.3s;
        }
        .msg-photo img:hover { transform:scale(1.02); }
        .msg-caption { font-size:0.75em; color:#888; margin-top:5px; text-align:center; }
        
        .typing {
            color:#888; font-style:italic; font-size:0.9em;
            padding:10px; display:none;
        }
        .typing.active { display:block; animation:blink 1s infinite; }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.5} }
        
        .system-msg {
            text-align:center; color:#ff69b488;
            font-size:0.8em; margin:10px 0; padding:5px;
            border-top:1px solid #ff69b422; border-bottom:1px solid #ff69b422;
        }
        
        .input-area { display:flex; gap:10px; margin-bottom:12px; }
        .input-area input {
            flex:1; padding:14px 18px; border:2px solid #ff69b433;
            border-radius:25px; background:rgba(0,0,0,0.7);
            color:#fff; font-size:1em; outline:none;
        }
        .input-area input:focus { border-color:#ff69b4; }
        .input-area button {
            padding:14px 28px; border:none; border-radius:25px;
            background:linear-gradient(45deg,#ff1493,#ff69b4);
            color:#fff; font-size:1em; font-weight:bold; cursor:pointer;
        }
        .input-area button:hover { transform:scale(1.05); box-shadow:0 0 25px rgba(255,105,180,0.5); }
        
        .quick-btns {
            display:flex; flex-wrap:wrap; gap:6px;
            justify-content:center; margin-bottom:12px;
        }
        .quick-btns .qbtn {
            padding:6px 14px; border:1px solid #ff69b444;
            border-radius:20px; background:rgba(255,105,180,0.1);
            color:#ff69b4; cursor:pointer; font-size:0.8em;
        }
        .quick-btns .qbtn:hover { background:rgba(255,105,180,0.3); }
        .quick-btns .qbtn.danger { border-color:#ef5350; color:#ef5350; }
        
        .footer {
            display:flex; justify-content:space-between;
            color:#666; font-size:0.8em;
            padding-top:12px; border-top:1px solid #ff69b422;
        }
        .footer .online { color:#66bb6a; }
        
        .lightbox {
            display:none; position:fixed; top:0; left:0;
            width:100%; height:100%; background:rgba(0,0,0,0.95);
            z-index:1000; justify-content:center; align-items:center; cursor:pointer;
        }
        .lightbox.active { display:flex; }
        .lightbox img { max-width:90%; max-height:90%; border-radius:10px; border:3px solid #ff69b4; }
        
        @media(max-width:600px) {
            .container{padding:12px} .header h1{font-size:1.4em}
            .chat-box{height:300px;padding:12px}
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🔥 RENDER NSFW AI 🔥</h1>
        <p>👄 Jo Manga Wahi Milega! | Anime Characters</p>
        <div style="color:#888;font-size:0.8em;margin-top:5px">🐍 Flask + Python 3 | Render Deploy</div>
    </div>
    
    <div class="char-selector" id="charSelector">
        <div class="char-btn active" onclick="setChar('default')">👄 Default</div>
        <div class="char-btn" onclick="setChar('hutao')">🎆 Hu Tao</div>
        <div class="char-btn" onclick="setChar('raiden')">⚡ Raiden</div>
        <div class="char-btn" onclick="setChar('asuna')">⚔️ Asuna</div>
        <div class="char-btn" onclick="setChar('yuno')">😈 Yuno</div>
        <div class="char-btn" onclick="setChar('tsunade')">💥 Tsunade</div>
        <div class="char-btn" onclick="setChar('nami')">🍊 Nami</div>
        <div class="char-btn" onclick="setChar('lisa')">📚 Lisa</div>
        <div class="char-btn" onclick="setChar('nezuko')">🔥 Nezuko</div>
    </div>
    
    <div class="chat-box" id="chatBox">
        <div class="message msg-ai">
            <div class="msg-sender">👄 Default AI</div>
            <div class="msg-bubble">🌟 <b>Render PE deploy hai!</b><br>Anime character select karo phir baat karo!<br>Jaise likho: <b>boobs, gaand, chut, kiss, maa, love...</b></div>
        </div>
        <div class="typing" id="typing">👄 AI soch rahi hai...</div>
    </div>
    
    <div class="quick-btns">
        <div class="qbtn" onclick="send('boobs')">🍈 Boobs</div>
        <div class="qbtn" onclick="send('gaand')">🍑 Gaand</div>
        <div class="qbtn" onclick="send('chut')">🌸 Chut</div>
        <div class="qbtn" onclick="send('blowjob')">👄 Blow</div>
        <div class="qbtn" onclick="send('kiss')">💋 Kiss</div>
        <div class="qbtn" onclick="send('chudai')">🔥 Chudai</div>
        <div class="qbtn" onclick="send('nanga')">🔞 Nanga</div>
        <div class="qbtn" onclick="send('love')">💕 Love</div>
        <div class="qbtn" onclick="send('maa')">👩 Maa</div>
        <div class="qbtn" onclick="send('random')">🎲 Random</div>
        <div class="qbtn danger" onclick="clearChat()">🗑️ Clear</div>
    </div>
    
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Yahan likho... (boobs, gaand, maa, kiss, love...)" onkeypress="if(event.key==='Enter') send()">
        <button onclick="send()">👉 Bhejo</button>
    </div>
    
    <div class="footer">
        <span class="online" id="status">🟢 Online</span>
        <span id="charDisplay">🎭 Default AI</span>
        <span id="msgCount">💬 0 messages</span>
    </div>
</div>

<div class="lightbox" id="lightbox" onclick="this.classList.remove('active')">
    <img id="lightboxImg" src="">
</div>

<script>
let currentChar = 'default';
let msgCount = 0;
let isLoading = false;

const charNames = {
    'default': 'Default AI', 'hutao': 'Hu Tao', 'raiden': 'Raiden Shogun',
    'asuna': 'Asuna', 'yuno': 'Yuno Gasai', 'tsunade': 'Tsunade',
    'nami': 'Nami', 'lisa': 'Lisa', 'nezuko': 'Nezuko'
};

function setChar(charId) {
    currentChar = charId;
    document.querySelectorAll('.char-btn').forEach(b => b.classList.remove('active'));
    document.querySelector('.char-btn[onclick*="'+charId+'"]').classList.add('active');
    document.getElementById('charDisplay').textContent = '🎭 ' + (charNames[charId] || charId);
    addSystem('🔄 Character changed to '+charId);
}

function addSystem(text) {
    const box = document.getElementById('chatBox');
    const typing = document.getElementById('typing');
    if (typing.parentNode === box) box.removeChild(typing);
    const d = document.createElement('div');
    d.className = 'system-msg';
    d.textContent = text;
    box.appendChild(d);
    box.appendChild(typing);
    box.scrollTop = box.scrollHeight;
}

function addMessage(sender, name, text, photoUrl, category) {
    const box = document.getElementById('chatBox');
    const typing = document.getElementById('typing');
    if (typing.parentNode === box) box.removeChild(typing);
    
    const div = document.createElement('div');
    div.className = 'message msg-'+sender;
    
    let html = '<div class="msg-sender">'+name+'</div><div class="msg-bubble">'+text+'</div>';
    if (photoUrl && sender === 'ai') {
        html += '<div class="msg-photo"><img src="'+photoUrl+'" onclick="openLB(\''+photoUrl+'\')" onerror="this.style.display=\'none\'"><div class="msg-caption">📸 '+category+'</div></div>';
    }
    
    div.innerHTML = html;
    box.appendChild(div);
    box.appendChild(typing);
    box.scrollTop = box.scrollHeight;
    
    if (sender === 'user') {
        msgCount++;
        document.getElementById('msgCount').textContent = '💬 '+msgCount+' messages';
    }
}

function showTyping(show) {
    document.getElementById('typing').classList.toggle('active', show);
}

function openLB(url) {
    document.getElementById('lightboxImg').src = url;
    document.getElementById('lightbox').classList.add('active');
}

function clearChat() {
    const box = document.getElementById('chatBox');
    const typing = document.getElementById('typing');
    box.innerHTML = '';
    box.appendChild(typing);
    msgCount = 0;
    document.getElementById('msgCount').textContent = '💬 0 messages';
    setTimeout(() => addSystem('🗑️ Sab clear! Naye sir se shuru!'), 200);
}

async function send(inputText) {
    if (isLoading) return;
    
    const input = document.getElementById('userInput');
    const text = inputText || input.value.trim();
    if (!text) return;
    input.value = '';
    
    addMessage('user', '👤 Tum', text);
    showTyping(true);
    isLoading = true;
    
    try {
        const resp = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: text, character: currentChar})
        });
        const data = await resp.json();
        showTyping(false);
        addMessage('ai', data.character_name, data.reply, data.photo, data.category);
    } catch(e) {
        showTyping(false);
        addSystem('❌ Error! Server se connect nahi ho paaya!');
    }
    
    isLoading = false;
}
</script>
</body>
</html>
"""


# ================================================================
# FLASK ROUTES
# ================================================================

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '') if data else ''
    character = data.get('character', 'default') if data else 'default'
    
    result = process_message(message, character)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "message": "Render deployment running!", "version": "1.0"})


# ================================================================
# MAIN - YE CHALEGA RENDER PE
# ================================================================

if __name__ == "__main__":
    print(f"""
    ╔══════════════════════════════════════════════╗
    ║   🔥 RENDER NSFW AI - JO MANGA WAHI MILEGA ║
    ║   Server starting on port {PORT}               ║
    ║   File: app.py                               ║
    ║   Start: gunicorn app:app --bind 0.0.0.0:$PORT ║
    ╚══════════════════════════════════════════════╝
    """)
    app.run(host="0.0.0.0", port=PORT, debug=False)