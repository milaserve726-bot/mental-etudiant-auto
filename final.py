# Mental Etudiant - AUTO AI FACTORY - كلشي على الطالب
import os, asyncio, requests, urllib.parse, random
from moviepy.editor import *
import edge_tts

# 10 قصص كلهم على الطالب - ستريس، نعاس، امتحان، عقل
SCENES = [
  {"text": "3 heures du matin, tu es en larmes devant tes cours. Ton coeur bat a 130. C'est l'anxiete etudiante.", "prompt": "stressed moroccan french student girl crying studying at 3am in small bedroom, books everywhere, cinematic emotional"},
  {"text": "Tu n'as meme pas ouvert ton cahier et tu paniques deja. C'est ton cerveau en mode survie, pas toi.", "prompt": "anxious student looking at closed notebook panic attack university dorm"},
  {"text": "L'an dernier, j'ai essaye 200 pages en une nuit. Resultat? 7 sur 20. Mon cerveau avait abandonne.", "prompt": "exhausted student falling asleep on desk with many books open night studying failure"},
  {"text": "Ton cerveau sous stress retient 40 pour cent de moins. C'est la science, pas un manque d'intelligence.", "prompt": "brain scan stress neuroscience anxiety student study concept artistic"},
  {"text": "Tu compares ta journee a la story Instagram des autres. Eux ils reussissent, toi tu coules. Faux.", "prompt": "student scrolling instagram comparison anxiety depression dark room phone light"},
  {"text": "Ecris sur une feuille: qu'est ce qui me stresse vraiment? Est ce que ca comptera dans 5 ans?", "prompt": "student journaling writing anxiety on paper therapy calm desk light"},
  {"text": "La regle des 2 minutes: mets un chrono de 2 minutes. Ouvre juste ton cours. C'est tout.", "prompt": "student opening book with timer 2 minutes study motivation calm"},
  {"text": "Technique 4-2-6: Inspire 4 secondes, bloque 2 secondes, expire 6 secondes. Ton coeur va se calmer.", "prompt": "student doing breathing exercise meditation calm in bedroom university"},
  {"text": "Tu n'es pas en retard. Tu es epuise. Dors 7 heures, bois de l'eau, marche 10 minutes.", "prompt": "student sleeping peacefully healthy lifestyle water walking university wellness"},
  {"text": "Demain, ouvre ton cours 10 minutes seulement. Pas 5 heures. 10 minutes. Tu vas gagner.", "prompt": "happy successful student studying small victory smiling bright future hope"},
]

async def voice(text, out):
    await edge_tts.Communicate(text, "fr-FR-HenriNeural", rate="-5%").save(out)

def gen_ai_image(prompt, idx):
    # AI كيولد صورة جديدة - ماشي من مكتبة - كلها على الطالب
    full_prompt = f"{prompt}, french moroccan student, realistic, cinematic, emotional, 8k, vertical portrait 9:16"
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(full_prompt)}?width=1080&height=1920&nologo=true&seed={random.randint(1,999999)}"
    path = f"ai_student_{idx}.jpg"
    try:
        print(f"🎨 Generation AI Etudiant {idx+1}: {prompt[:40]}")
        r = requests.get(url, timeout=90)
        open(path,'wb').write(r.content)
        return path
    except: return None

async def main():
    clips=[]
    for i,s in enumerate(SCENES):
        print(f"\n--- SCENE ETUDIANT {i+1}/10 ---")
        await voice(s['text'], f"v{i}.mp3")
        audio=AudioFileClip(f"v{i}.mp3")
        img=gen_ai_image(s['prompt'], i)
        if img and os.path.exists(img):
            vc=ImageClip(img, duration=audio.duration).resize((1080,1920)).set_audio(audio)
            # zoom lent باش يولي بحال فيديو
            vc=vc.resize(lambda t: 1 + 0.04*t/audio.duration if audio.duration>0 else 1)
        else:
            vc=ColorClip((1080,1920), color=(15,15,15), duration=audio.duration).set_audio(audio)
        txt=TextClip(s['text'], fontsize=38, color='white', font='Arial-Bold', method='caption', size=(920,None), stroke_color='black', stroke_width=3, align='center').set_position(('center',0.75), relative=True).set_duration(audio.duration)
        clips.append(CompositeVideoClip([vc, txt]))
    
    final=concatenate_videoclips(clips, method="compose")
    # موسيقى هادئة 12%
    try:
        open("m.mp3",'wb').write(requests.get("https://cdn.pixabay.com/download/audio/2021/11/25/audio_3c1d2b5a2e.mp3?filename=lofi-study-112191.mp3", timeout=20).content)
        music=AudioFileClip("m.mp3").volumex(0.11).set_duration(final.duration).audio_fadeout(3)
        final=final.set_audio(CompositeAudioClip([final.audio, music]))
    except: pass
    final.write_videofile("FINAL_ETUDIANT.mp4", fps=24, codec='libx264', audio_codec='aac', threads=2)
    print("✅ VIDEO ETUDIANT AI WAJED!")

asyncio.run(main())
