#!/usr/bin/env python3
"""Render a steady, subpixel camera move from existing shell to renovation concept.
Requires FFmpeg. No new still imagery is synthesized by this renderer.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
FPS = 60
DURATION = 24
TRANSITION = 4
OFFSET = 10
SHOT = 14

def camera(offset):
    # Continuous fractional source coordinates avoid integer crop rounding in zoompan.
    # Both inputs share one global trajectory, including through the dissolve.
    ease = f'(1-cos(PI*(on+{offset})/{FPS*DURATION-1}))/2'
    dx, dy = f'W*0.025*{ease}', f'H*0.025*{ease}'
    return (f"perspective=x0='{dx}':y0='{dy}':x1='W-{dx}':y1='{dy}':"
            f"x2='{dx}':y2='H-{dy}':x3='W-{dx}':y3='H-{dy}':"
            'eval=frame:interpolation=cubic')

inputs = []
for name in ['asset-existing.jpg', 'asset-reimagined.jpg']:
    inputs += ['-loop', '1', '-framerate', str(FPS), '-t', str(SHOT), '-i', str(ROOT/'assets'/name)]
filters = []
for index, offset in enumerate([0, OFFSET*FPS]):
    filters.append(f'[{index}:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,'
                   f'format=yuv444p,{camera(offset)},settb=AVTB,setpts=PTS-STARTPTS,fps={FPS}[v{index}]')
filters.append(f'[v0][v1]xfade=transition=fade:duration={TRANSITION}:offset={OFFSET},format=yuv420p[out]')
subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'warning', '-filter_complex_threads', '2',
                *inputs, '-filter_complex', ';'.join(filters), '-map', '[out]', '-an', '-t', str(DURATION),
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-r', str(FPS), '-movflags', '+faststart',
                str(ROOT/'assets/asset-repurposing-smooth.mp4')], check=True)
