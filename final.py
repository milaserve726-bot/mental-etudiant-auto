# AI VIDEO GENERATOR - Github كيولد هو الفيديو
import os, asyncio, requests, urllib.parse
from moviepy.editor import *
import edge_tts

SCENES = [
  {"text": "3 heures du matin, je pleure avant mon partiel. Tu connais ce moment?", "prompt": "stressed french student girl crying in bed at 3am dark room cinematic"},
  {"text": "Tu n'as meme pas ouvert ton cours et tu stresses deja. Coeur a 120.", "prompt": "anxious student looking at closed book anxiety dark academic"},
  {"text": "L'an dernier, 200 pages a 22h dans mon lit. J'en connais 30 pourcent.", "prompt": "overwhelmed student in bed surrounded by books late night"},
  {"text": "Je pleure jusqu'a 3h, lendemain 7 sur 20 feuille blanche.", "prompt": "student failing exam blank paper university classroom sad"},
  {"text": "Pas parce que j'etais nulle. Parce que mon cerveau etait grille.", "prompt": "burned out brain stress anxiety concept artistic"},
  {"text": "Harvard 2019: les anxieux retiennent 40 pourcent de moins.", "prompt": "Harvard university library brain science study"},
  {"text": "Prends une feuille, ecris ce qui te stresse. Ca comptera dans 5 ans?", "prompt": "student writing journal anxiety relief calm light"},
  {"text": "Regle 2 minutes: chrono 2 minutes, ouvre ton cours, calme.", "prompt": "happy calm french student breathing success studying bright"},
]

async def voice(text, out):
    await edge_tts.Communicate(text, "fr-FR-HenriNeural").save(out)

def gen_image(prompt, idx):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt + ' vertical portrait 9:16 cinematic 8k')}?width=1080&height=1920&nologo=true"
    path = f"ai_{idx}.jpg"
    try:
        r = requests.get(url, timeout=60)
        open(path,'wb').write(r.content)
        return path
    except: return None

async def main():
    clips=[]
    for i,s in enumerate(SCENES):
        await voice(s['text'], f"v{i}.mp3")
        audio=AudioFileClip(f"v{i}.mp3")
        img=gen_image(s['prompt'], i)
        if img:
            vc=ImageClip(img, duration=audio.duration).resize((1080,1920)).set_audio(audio)
            vc=vc.resize(lambda t: 1+0.03*t)
        else:
            vc=ColorClip((1080,1920), color=(10,10,10), duration=audio.duration).set_audio(audio)
        txt=TextClip(s['text'], fontsize=36, color='white', method='caption', size=(900,None), stroke_color='black', stroke_width=2).set_position('center').set_duration(audio.duration)
        clips.append(CompositeVideoClip([vc, txt]))
    final=concatenate_videoclips(clips, method="compose")
    final.write_videofile("FINAL_AI.mp4", fps=24, codec='libx264', audio_codec='aac')
    print("WAJED!")

asyncio.run(main())
