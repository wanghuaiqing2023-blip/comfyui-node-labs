#!/usr/bin/env python3
"""Create deterministic measurement fixtures; no GPU or image generation model."""
import argparse
import hashlib
import json
import wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.out.exists():ap.error('output directory already exists; choose a new directory')
    a.out.mkdir(parents=True);w,h=512,384
    yy,xx=np.mgrid[:h,:w]
    checker=(((xx//16+yy//16)%2)*160+48).astype('uint8')
    p1=Image.fromarray(np.repeat(checker[...,None],3,axis=2));d=ImageDraw.Draw(p1)
    for box,col in [((0,0,63,63),(255,0,0)),((448,0,511,63),(0,255,0)),((0,320,63,383),(0,0,255)),((448,320,511,383),(255,255,0))]:d.rectangle(box,fill=col)
    d.rectangle((180,0,330,40),fill='white');d.text((230,15),'TOP',fill='black')
    for y in range(64,320,64):
        for x in range(64,448,64):d.text((x,y),f'{x},{y}',fill='white')
    p1.save(a.out/'P1.png')
    for name,col in [('red',(255,0,0)),('blue',(0,0,255)),('black',(0,0,0)),('white',(255,255,255))]:Image.new('RGB',(w,h),col).save(a.out/(name+'.png'))
    ramp=np.tile(np.linspace(0,255,w).round().astype('uint8'),(h,1))
    Image.fromarray(ramp).save(a.out/'gray-ramp.png')
    m=np.zeros((h,w),dtype='uint8');m[96:288,128:384]=255;Image.fromarray(m).save(a.out/'M1.png')
    p2=np.zeros((h,w,4),dtype='uint8');p2[...,:3]=(255,64,0);p2[:,:171,3]=0;p2[:,171:342,3]=128;p2[:,342:,3]=255
    Image.fromarray(p2).save(a.out/'P2.png')
    frames=a.out/'V1';frames.mkdir()
    for i in range(24):
        im=Image.new('RGB',(w,h),(16,16,16));di=ImageDraw.Draw(im);x=32+16*i
        di.ellipse((x,160,x+24,184),fill='red');di.text((240,40),f'{i:02d}',fill='white');im.save(frames/f'{i:02d}.png')
    sr=48000
    def tone(freq,seconds):return .1*np.sin(2*np.pi*freq*np.arange(int(seconds*sr))/sr)
    def wav(name,s):
        with wave.open(str(a.out/name),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes(np.rint(s*32767).astype('<i2').tobytes())
    wav('A1.wav',tone(440,1));wav('A2.wav',tone(880,2));wav('A2-one-second.wav',tone(880,1));wav('A3-segments.wav',np.concatenate([tone(f,1) for f in [440,880,1320]]))
    manifest={'P1_size':[512,384],'M1_white_xyxy_exclusive':[128,96,384,288],'P2_alpha_bands':[0,128,255],'V1_frames':24,'V1_nominal_fps':24,'audio_sample_rate':sr,'audio_peak_target':.1,'sha256':{str(p.relative_to(a.out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(a.out.rglob('*')) if p.is_file()}}
    (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(a.out)

if __name__=='__main__':main()
