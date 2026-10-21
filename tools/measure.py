#!/usr/bin/env python3
"""Read-only PNG/image and PCM16 WAV inspection; outputs JSON."""
import argparse
import json
import wave
import numpy as np
from PIL import Image

def inspect_image(path, reference=None):
    im=Image.open(path); arr=np.asarray(im.convert('RGBA') if 'A' in im.getbands() else im.convert('RGB'),dtype=np.float64)/255
    mask=arr[...,0]>0;y,x=np.nonzero(mask)
    result={'width':im.width,'height':im.height,'channels':arr.shape[-1],'min':float(arr.min()),'max':float(arr.max()),'channel_mean':arr.mean(axis=(0,1)).tolist(),'unique_colors':int(len(np.unique(arr.reshape(-1,arr.shape[-1]),axis=0))),'first_channel_nonzero_bbox_xyxy_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)] if x.size else None}
    if reference:
        ref=np.asarray(Image.open(reference).convert('RGBA' if arr.shape[-1]==4 else 'RGB'),dtype=np.float64)/255
        if ref.shape!=arr.shape:raise ValueError(f'shape mismatch: {arr.shape} vs {ref.shape}')
        diff=np.abs(arr-ref);result.update(mae=float(diff.mean()),max_abs_error=float(diff.max()),equal=bool(np.array_equal(arr,ref)))
    return result

def inspect_audio(path):
    with wave.open(str(path),'rb') as f:
        if f.getsampwidth()!=2 or f.getcomptype()!='NONE':raise ValueError('only uncompressed PCM16 WAV supported')
        sr=f.getframerate();ch=f.getnchannels();n=f.getnframes();data=np.frombuffer(f.readframes(n),dtype='<i2').reshape(-1,ch).astype(float)/32768
    if not n:raise ValueError('empty WAV')
    window=np.hanning(n);spectrum=np.abs(np.fft.rfft(data*window[:,None],axis=0));freq=np.fft.rfftfreq(n,1/sr)
    peak_freq=[float(freq[np.argmax(spectrum[:,i])]) if np.any(data[:,i]) else None for i in range(ch)]
    return dict(sample_rate=sr,channels=ch,samples_per_channel=n,duration_seconds=n/sr,peak=np.max(np.abs(data),axis=0).tolist(),rms=np.sqrt(np.mean(data**2,axis=0)).tolist(),dominant_hz=peak_freq)

def main():
    p=argparse.ArgumentParser();p.add_argument('kind',choices=['image','audio']);p.add_argument('path');p.add_argument('--reference');a=p.parse_args()
    if a.kind=='audio' and a.reference:p.error('--reference only supports image')
    print(json.dumps(inspect_image(a.path,a.reference) if a.kind=='image' else inspect_audio(a.path),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
