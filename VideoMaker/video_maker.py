import sys
import os

def convert(mp4Path, wavPath, outMp4Path):
    os.system('ffmpeg -i {0} -i {1} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {2}'.format(mp4Path, wavPath, outMp4Path))

def main():
    if len(sys.argv) < 4:
        sys.exit()
    mp4Path = sys.argv[1]
    wavPath = sys.argv[2]
    outMp4Path = sys.argv[3]
    convert(mp4Path, wavPath, outMp4Path)

if __name__ == '__main__':
    main()
